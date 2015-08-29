import os
import glob

curr_path = os.getcwd()

directorys = os.listdir()
for directory in directorys:
	if os.path.isdir(directory):
		files = glob.glob(directory+"/*.svm_s")
		for feat_type in range(int(len(files) / 4)):
			same_part_name = files[feat_type * 4].split('.')[0]
			with open(same_part_name+'.svm_a', 'w') as outfile:
				for feat_file in files[feat_type*4 : feat_type * 4 + 4]:
					with open(feat_file) as infile:
						for line in infile:
							outfile.write(line)
