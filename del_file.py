import os
import glob

directorys = os.listdir()
for directory in directorys:
	if os.path.isdir(directory):
		# Delete any file contains 'svm_a'
		files = glob.glob(directory+"/*svm_a")
		# Delete any file whose format is 'svm_a'
		#files = glob.glob(directory+"/*.svm_a")
		for file in files:
			os.remove(file)
