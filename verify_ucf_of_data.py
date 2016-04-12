import os, os.path
import glob

#target file to contain the number of frames of each video
count_file = open('flow_frame_num.txt', 'w')

data_dir = '/data3/wangyf/dataset/ucf101/ucf101_of_matlab/'
sub_dir_list = os.listdir(data_dir)
for sub_dir in sub_dir_list:
	sub_dir_path = data_dir + sub_dir
	print(sub_dir_path)
	video_dir = os.listdir(sub_dir_path)
	for video in video_dir:
		flow_images = glob.glob(sub_dir_path + '/' + video + '/*.jpg')
#		print(flow_images)
		count_file.write(video + ' ' + str(len(flow_images)) + '\n')
