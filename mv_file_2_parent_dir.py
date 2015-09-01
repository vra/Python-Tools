import os
import shutil 

dirs = os.listdir()

for dir in dirs:
	if os.path.isdir(dir):
		subdirs = os.listdir(dir)
		for subdir in subdirs:
			files = os.listdir(dir+'/'+subdir)
			for file in files:
				shutil.move(dir + '/'+ subdir + '/'+ file, dir + '/' + file)

			os.rmdir(dir + '/' + subdir)
