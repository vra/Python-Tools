# generate frame format dataset from ucf101 video dataset

#main_dir="/cygdrive/d/ucf101"
main_dir="/cygdrive/d/dataset/Debug"
frm_dir="/cygdrive/d/dataset/Debug_frm"

if [ ! -d "$frm_dir" ]; then
	mkdir $frm_dir
fi

for sub_dir in $main_dir/*
do
	if [ -d "$sub_dir" ]
	then

		echo "sub_dir: $sub_dir"
		if [ ! -d "$sub_dir" ]; then
			mkdir "$sub_dir"
		fi

		for video in $sub_dir/*
		do
			echo "video: $video"
			sub_dir_clean=`echo $sub_dir | cut -d '/' -f 6`
			echo "sub_dir_clean: $sub_dir_clean"
			#get video's type name, for example, 
			#from "ucf101\ApplyEyeMakeup\v_ApplyEyeMakeup_g01_c01.avi"
			#we get "v_ApplyEyeMakeup_g01_c01.avi"
			video_type=`echo $video | cut -d '/' -f 7` 
			echo "video_type: $video_type" 
			#from "v_ApplyEyeMakeup_g01_c01.avi" get "v_ApplyEyeMakeup_g01_c01"
			video_type_clean=`echo $video_type | cut -d '.' -f 1` 
			echo "video_type_clean:$video_type_clean"

			video_dir="$frm_dir/$sub_dir_clean/$video_type_clean"

			echo "video_dir: $video_dir"
			if [ ! -d "$video_dir" ]; then
				mkdir -p $video_dir 
			fi

			#call ffmpeg.exe to do the transform job
			/cygdrive/d/program_file/ffmpeg/bin/ffmpeg.exe -i "D:\dataset\Debug\\$sub_dir_clean\\$video_type" "D:\dataset\Debug_frm\\$sub_dir_clean\\$video_type_clean\%06d.jpg"
		done
	fi
done







