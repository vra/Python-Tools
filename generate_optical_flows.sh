#!/bin/bash

## Read the sub directorys in this directory and generate optical flows then write them to image.

curr_dir="/home/wangyf/data/ucf101_frm"
main_dir="."

for sub_dir in $main_dir/*
do
	echo 'sub_dir:$sub_dir'
	if [ -d "$sub_dir" ]
	then
		for sub_sub_dir in $sub_dir/*
		do
			if [ -d "$sub_sub_dir" ]
			then
				## This is the directory contains frames,do job at here.
				for frame in $sub_sub_dir/*
				do
					echo frame: $frame
					curr_image=`echo $frame|cut -d '/' -f 4`
					echo curr_image: $curr_image
					curr_number=`echo $curr_image|cut -d '.' -f 1`
					echo "curr_number: $curr_number"
					next_number=`expr $curr_number + 1`
					echo "next_number: $next_number"
					padded_number='00000'${next_number}
					echo "padded_tnumber: $padded_number"
					next_image=${padded_number: -6}'.jpg'
					echo $next_image

					next_frame_path=$sub_sub_dir'/'$next_image
					echo next_frame_path:$next_frame_path
					if [ -f $next_frame_path ]
					then
						inner_path=$curr_dir${sub_sub_dir:1}
						curr_image_path=$inner_path'/'$curr_image 
						next_image_path=$inner_path'/'$next_image 

						echo inner_path:$inner_path
						echo curr_image_path:$curr_image_path
						echo next_image_path:$next_image_path
						./get_optical_flow $inner_path $curr_image $next_image
					fi
				done
				
	
			fi
		done
	fi
done

