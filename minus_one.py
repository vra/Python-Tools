#!/bin/env python

train_file=open('/home/wangyf/Lab/two-stream-dev/vgg_cnn_m_2048_finetune/train.txt','r')
train_file_new = open('/home/wangyf/Lab/two-stream-dev/vgg_cnn_m_2048_finetune/train_0.txt','w')

new_line=""
for line in train_file:
	type_name = line.split(' ')[0]
	order = line.split(' ')[1]
	order = order.split('\r')[0]
	print(type(order))
	print((order))
	
	order = int(order) - 1
	new_line = '%s %d\n' %(type_name, order)
	train_file_new.write(new_line)
		
