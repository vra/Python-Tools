#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>
#include <unistd.h>
#include <errno.h>

#define MAXSIZE 256

#include <iostream>
#include <fstream>

#include <opencv2/core.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/cudaoptflow.hpp>
#include <opencv2/cudaarithm.hpp>

using namespace std;
using namespace cv;
using namespace cv::cuda;

inline bool isFlowCorrect(Point2f u)
{
    return !cvIsNaN(u.x) && !cvIsNaN(u.y) && fabs(u.x) < 1e9 && fabs(u.y) < 1e9;
}

static Vec3b computeColor(float fx, float fy)
{
    static bool first = true;

    // relative lengths of color transitions:
    // these are chosen based on perceptual similarity
    // (e.g. one can distinguish more shades between red and yellow
    //  than between yellow and green)
    const int RY = 15;
    const int YG = 6;
    const int GC = 4;
    const int CB = 11;
    const int BM = 13;
    const int MR = 6;
    const int NCOLS = RY + YG + GC + CB + BM + MR;
    static Vec3i colorWheel[NCOLS];

    if (first)
    {
        int k = 0;

        for (int i = 0; i < RY; ++i, ++k)
            colorWheel[k] = Vec3i(255, 255 * i / RY, 0);

        for (int i = 0; i < YG; ++i, ++k)
            colorWheel[k] = Vec3i(255 - 255 * i / YG, 255, 0);

        for (int i = 0; i < GC; ++i, ++k)
            colorWheel[k] = Vec3i(0, 255, 255 * i / GC);

        for (int i = 0; i < CB; ++i, ++k)
            colorWheel[k] = Vec3i(0, 255 - 255 * i / CB, 255);

        for (int i = 0; i < BM; ++i, ++k)
            colorWheel[k] = Vec3i(255 * i / BM, 0, 255);

        for (int i = 0; i < MR; ++i, ++k)
            colorWheel[k] = Vec3i(255, 0, 255 - 255 * i / MR);

        first = false;
    }

    const float rad = sqrt(fx * fx + fy * fy);
    const float a = atan2(-fy, -fx) / (float) CV_PI;

    const float fk = (a + 1.0f) / 2.0f * (NCOLS - 1);
    const int k0 = static_cast<int>(fk);
    const int k1 = (k0 + 1) % NCOLS;
    const float f = fk - k0;

    Vec3b pix;

    for (int b = 0; b < 3; b++)
    {
        const float col0 = colorWheel[k0][b] / 255.0f;
        const float col1 = colorWheel[k1][b] / 255.0f;

        float col = (1 - f) * col0 + f * col1;

        if (rad <= 1)
            col = 1 - rad * (1 - col); // increase saturation with radius
        else
            col *= .75; // out of range

        pix[2 - b] = static_cast<uchar>(255.0 * col);
    }

    return pix;
}

static void drawOpticalFlow(const Mat_<float>& flowx, const Mat_<float>& flowy, Mat& dst, float maxmotion = -1)
{
    dst.create(flowx.size(), CV_8UC3);
    dst.setTo(Scalar::all(0));

    // determine motion range:
    float maxrad = maxmotion;

    if (maxmotion <= 0)
    {
        maxrad = 1;
        for (int y = 0; y < flowx.rows; ++y)
        {
            for (int x = 0; x < flowx.cols; ++x)
            {
                Point2f u(flowx(y, x), flowy(y, x));

                if (!isFlowCorrect(u))
                    continue;

                maxrad = max(maxrad, sqrt(u.x * u.x + u.y * u.y));
            }
        }
    }

    for (int y = 0; y < flowx.rows; ++y)
    {
        for (int x = 0; x < flowx.cols; ++x)
        {
            Point2f u(flowx(y, x), flowy(y, x));

            if (isFlowCorrect(u))
                dst.at<Vec3b>(y, x) = computeColor(u.x / maxrad, u.y / maxrad);
        }
    }
}

static void showFlow(string curr_path, string name1, string name2, const GpuMat& d_flow)
{
    GpuMat planes[2];
    cuda::split(d_flow, planes);

    Mat flowx(planes[0]);
    Mat flowy(planes[1]);

    Mat out;
    drawOpticalFlow(flowx, flowy, out, 10);
	string optical_name = curr_path+'/'+name1+'_'+name2;
	imwrite(optical_name, out);

	
//    imshow(name, out);
}

int calculate_optical_flow(const char* path, const char* img1, const char* img2)
{
    string curr_path(path);
	string image1(img1);
	string image2(img2);
	string filename1= curr_path + '/'+image1;
	string filename2= curr_path + '/'+image2;
    Mat frame0 = imread(filename1, IMREAD_GRAYSCALE);
    Mat frame1 = imread(filename2, IMREAD_GRAYSCALE);

    if (frame0.empty())
    {
        cerr << "Can't open image ["  << filename1 << "]" << endl;
        return -1;
    }
    if (frame1.empty())
    {
        cerr << "Can't open image ["  << filename2 << "]" << endl;
        return -1;
    }

    if (frame1.size() != frame0.size())
    {
        cerr << "Images should be of equal sizes" << endl;
        return -1;
    }
	
    GpuMat d_frame0(frame0);
    GpuMat d_frame1(frame1);

    GpuMat d_flow(frame0.size(), CV_32FC2);

    Ptr<cuda::BroxOpticalFlow> brox = cuda::BroxOpticalFlow::create(0.197f, 50.0f, 0.8f, 10, 77, 10);

    {
        GpuMat d_frame0f;
        GpuMat d_frame1f;

        d_frame0.convertTo(d_frame0f, CV_32F, 1.0 / 255.0);
        d_frame1.convertTo(d_frame1f, CV_32F, 1.0 / 255.0);

      //  const int64 start = getTickCount();

        brox->calc(d_frame0f, d_frame1f, d_flow);

        showFlow(curr_path, image1, image2, d_flow);
     //   const double timeSec = (getTickCount() - start) / getTickFrequency();

    //   cout << "Brox : " << timeSec << " sec" << endl;
    }

    return 0;
}

int main(int argc, char** argv)
{
	DIR* FD;
	DIR* FD_SUB;
	DIR* FD_SUB_SUB;
	struct dirent* root_dir;
	struct dirent* action_types_dir;
	struct dirent* action_frames_dir;
	struct dirent* current_file_ent;
	const char* previous_file=NULL;
	const char* current_file;
	
	const char* root_path = "/home/wangyf/data/ucf101_frm/";
	//const char* root_path = "/home/wangyf/Dev/two-stream-dev/test_dir/";
	/*Open Root directory of data*/
	if (NULL==(FD = opendir(root_path)))
	{
		fprintf(stderr, "Error: Failed to open input directory - %s\n", strerror(errno));
		return 1;
	}
	while((action_types_dir= readdir(FD)))
	{
		if (!strcmp(action_types_dir->d_name, ".") || !strcmp(action_types_dir->d_name, ".."))
		{
			continue;
		}	
		
		/*Read sub directory*/
		const char* action_types_dir_name = action_types_dir->d_name;
		char sub_path[MAXSIZE];
		strcpy(sub_path, root_path);
		strcat(sub_path, action_types_dir_name);
		const char* sub_path_const = sub_path;
		//printf("action type directory: %s\n", sub_path_const);
		if (NULL == (FD_SUB=opendir(sub_path_const)))
		{
			fprintf(stderr, "Error: Failed to open input directory - %s\n", strerror(errno));
			return 1;
		}
		
		/*Read the directory contains frames*/
		while((action_frames_dir = readdir(FD_SUB)))
		{
			if (!strcmp(action_frames_dir->d_name, ".") || !strcmp(action_frames_dir->d_name, ".."))
			{
				continue;
			}	
			
			const char* frames_dir_name = action_frames_dir->d_name;
			
			char frames_path[MAXSIZE];
			strcpy(frames_path, sub_path_const);
			strcat(frames_path, "/");
			strcat(frames_path, frames_dir_name);
			printf("Frames' path: %s\n", frames_path);
			const char* frames_path_const = frames_path;
			
			/*Read the name of every two frames*/
			if ((NULL == (FD_SUB_SUB=opendir(frames_path_const))))
			{
				fprintf(stderr, "Error: Failed to open input directory - %s\n", strerror(errno));
				return 1;
			}
			
			while((current_file_ent = readdir(FD_SUB_SUB)))
			{
				if (!strcmp(current_file_ent->d_name, ".") || !strcmp(current_file_ent->d_name, ".."))
				{
					continue;
				}	
				
				current_file = current_file_ent->d_name;
				if (previous_file == NULL)
				{
					previous_file = current_file;
					continue;
				}
				//call the function doing main the job
				//printf("previouse file:%s\n current file:%s\n", previous_file, current_file);
				calculate_optical_flow(frames_path, previous_file, current_file);

				previous_file = current_file;
				
			}
	
		}	
		
	}
	
	return 0;
}
