#!/bin/env python

f = open('test_01_video.lst', 'r')
lines = f.readlines()
f.close()

f = open('test_01_video.lst', 'w')
for line in lines:
	list_parts = line.split(' ')
	#decrease the middle item by 1
	line = ' '.join([line.split(' ')[0], str(int(line.split(' ')[1]) - 1), line.split(' ')[2]])
	f.write(line)
	

f.close()
