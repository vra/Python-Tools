import os
import glob

directorys = os.listdir()
for directory in directorys:
	if os.path.isdir(directory):
		files = glob.glob(directory+"/*.svm_s")
		for file in files:
			f = open(file, 'r')
			lines = f.readlines()
			f.close()

			f = open(file, 'w')
			for line in lines:
				if line not in ['1 ', '2 ', '3 ', '4 ', '5 ', '6 ']:
					f.write(line)

			f.close()
