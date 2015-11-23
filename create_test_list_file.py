#!/bin/env python

import os, os.path

ucf101_frm_root = '/data1/wangyf/dataset/ucf101/ucf101_frm/'
label_file = open('/home/wangyf/Lab/two-stream-dev/vgg_cnn_m_2048_finetune/classInd.txt')

video_types = []
for line in label_file:
	video_type_name = line.split()[1]
#	print(video_type_name)
	video_types.append(video_type_name)

label_file.close()

test_list = open('/home/wangyf/Lab/two-stream-dev/vgg_cnn_m_2048_finetune/testlist01.txt','r')
test_list_apdated = open('/home/wangyf/Lab/two-stream-dev/vgg_cnn_m_2048_finetune/test.txt','w')
new_line = ""
for line in test_list:
	type_name = line.split('/')[0];
#	print('type_name:'+type_name)
	line = line.split('\r')[0] 
	frame_dir = ucf101_frm_root + line
#	print('frame_dir:'+frame_dir)
	frame_sum = len([name for name in os.listdir(frame_dir) if os.path.isfile(os.path.join(frame_dir, name))])
#	print('frame sum: '+str(frame_sum))
	order = video_types.index(type_name) + 1
#	print('order:'+str(order))
	middle_frame = frame_sum / 2
	if middle_frame <= 0:
		print('middle<=0, frame_dir:'+frame_dir) 
	new_line = '%s%06d.jpg %d\n' %(line, middle_frame, order-1) 
	test_list_apdated.write(new_line)
#	for i in range(1,frame_sum+1):
#		new_line = '%s%06d.jpg %d\n' %(frame_dir, i, order) 
#		print(new_line)
#		test_list_apdated.write(new_line)

test_list.close()
test_list_apdated.close()


