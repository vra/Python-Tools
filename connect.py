from os import listdir
import glob

#files = glob.glob("*.allsvm")
files =['train.txt', 'validation.txt']

with open("train-validation.txt", 'w') as outfile:
	for file in files:
		with open(file) as infile:
			for line in infile:
				outfile.write(line)

