import os
import glob

curr_path = os.getcwd()
directorys = os.listdir()

train_set =[11, 12, 13, 14, 15, 16, 17, 18]
validation_set = [19, 20, 21, 23, 24, 25, 1, 4]
test_set = [22, 2, 3, 5, 6, 7, 8, 9, 10 ]

for directory in directorys:
	if os.path.isdir(directory):
		
		files = glob.glob(directory+"/*.svm_a")
		with open('train.txt','a') as outfile:
			for n in train_set:
				for m in range(4):
					with open(files[(n-1)*4+m]) as infile:
						for line in infile:
							outfile.write(line)

		with open('validation.txt','a') as outfile:
			for n in validation_set:
				for m in range(4):
					with open(files[(n-1)*4+m]) as infile:
						for line in infile:
							outfile.write(line)

		with open('test.txt','a') as outfile:
			for n in test_set:
				for m in range(4):
					with open(files[(n-1)*4+m]) as infile:
						for line in infile:
							outfile.write(line)
