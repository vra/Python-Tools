# This script is used to minus corresoponseding number at the same line  in two different files 
f1 = open('frame_num.txt', 'r')
lines1 = f1.readlines()
f2 = open('flow_frame_num.txt', 'r')
lines2 = f2.readlines()
f3 = open('file_list.txt', 'r')
lines3 = f3.readlines()

num = 0
for i in range(0, len(lines1)):
	line1 = int(lines1[i])
	line2 = int(lines2[i])
	line3 = (lines3[i])
	error = abs(line1-line2)
	if error > 2:
		print('i:'+ str(i) + line3+' i1:'+ str(line1)+ ' line2:'+str(line2))
		
		num  = num + 1	

print(num)
	
