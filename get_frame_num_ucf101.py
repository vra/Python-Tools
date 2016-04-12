# This script is used to count the number of frames of each video in UCF101 dataset
#NOTE: this script is created in cygwin on Windows platform, some kind of functions invoking maybe different on Linux platform.

import subprocess as sp
import os
import glob

os.system("echo ''> frame_num.txt")
root_dir = '/cygdrive/d/dataset/ucf101/'
sub_dir_list = os.listdir(root_dir)
for sub_dir in sub_dir_list:
	if os.path.isdir(root_dir+sub_dir):
		files = glob.glob(root_dir+sub_dir+'/*.avi')
		for file in files:
			with open(file, 'rb') as infile:
#				print(file)
				file = file.replace('/cygdrive/d', 'D:')

				echo_script = "echo -n '" + file+ " ' >> frame_num.txt"
				print(echo_script)
				os.system(echo_script)		

				ffmpeg_script = "ffmpeg -i " + file + " -f null /dev/null 2>&1 | grep 'frame=' | cut -f 2,3,4 -d ' ' >> frame_num.txt"
				os.system(ffmpeg_script)
