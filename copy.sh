#!/bin/bash

for k  in $(seq 80  222)
do
	inc_k=`expr $k + 1`
	cp  11_12 0000$k.jpg_0000$inc_k.jpg
done

