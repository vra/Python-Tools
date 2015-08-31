import os
import glob

directorys = os.listdir()
for directory in directorys:
	if os.path.isdir(directory):
		files = glob.glob(directory+"/*.svm_a")
		for file in files:
			f = open(file, 'r')
			lines = f.readlines()
			print(len(lines))
			f.close()

			f = open(file+'.in', 'w')
			add_num = [108,96+108,96*2+108]
			if len(lines) <= 0:
				continue
			for n in range(512):
				new_line = lines[n].rstrip('\n')
				for i in range(3):
					list1 = lines[n + (i+1)*512][2:].rstrip('\n').split(' ')
					line_after_new = ''
					for item in list1:
						if item!= '' and item!=' ':
							list2 = item.split(':')
							list2[0]=str(int(list2[0])+ add_num[i])
							item = list2[0] + ':'+ list2[1]

							line_after_new = line_after_new+item+' '

					new_line = new_line + line_after_new

				new_line +='\n'
				f.write(new_line)

			f.close()
