#!/bin/bash

# The root directory saving  ucf101 frame data
UCF101_FRM_ROOT=/data1/wangyf/dataset/ucf101/ucf101_frm

#The first list file is download from ucf101 website
#Teh second list file is adapted to fine tune
train_list=./trainlist01.txt
train_list_adapted=./train.txt

# Read every line in train list file to get the directory of frames.
while IFS= read -r line
do
	sub_dir=`echo $line | cut -d ' ' -f 1`
	label=`echo $line | cut -d ' ' -f 2`
#	label=`echo $label | cut -d \' -f 1`
#	echo label:$label
#	label_id=${label:0:1} 
#	$label=`expr $label_id - 1`
	##NOTE: check whether label begin with 0 or 1
#	echo label:$label
#	echo $sub_dir
	frame_dir=$UCF101_FRM_ROOT/$sub_dir
#	echo frame_dir:$frame_dir
	frame_sum=`ls -l  $frame_dir |wc -l`
	#Don't know why: the $frame_sum is bigger than really number of frame by one.so minus one
	frame_sum=`expr $frame_sum - 1`
	middle_frame=`expr $frame_sum / 2`
#	echo $middle_frame
	printf "%s%06d.jpg %s\n" "$sub_dir" "$middle_frame" "$label" >> $train_list_adapted
#	echo frame_sum:$frame_sum	
#	for ((i=1;i<=$frame_sum;i++))
#	do
#		printf "%s%06d.jpg %s\n" "$sub_dir" "$i" "$label" >> $train_list_adapted
#	done

done <"$train_list"


