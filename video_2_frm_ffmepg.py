
FFMPEG_BIN = "D:\\program_file\\ffmpeg\\bin\\ffmpeg.exe"

import subprocess as sp
import os
import glob

directorys = os.listdir('D:\dataset\ucf101')
for directory in directorys:
	if os.path.isdir(directory):
		files = glob.glob(directory+"/*.avi")
		with open(file, 'rb') as infile:
			#pipe = sp.Popen([FFMPEG_BIN, '-i', '-', stdin = infile, stdout  = sp.PIPE])
			# USe os.system to execute shell command
			os.system('ffmpeg -i '+ infile) 

			
