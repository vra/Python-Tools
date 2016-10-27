#!/bin/sh

find . -type f -name 'v_HandStandPushups_*' | while read FILE; do
	newfile="$(echo ${FILE} | sed -e 's/Stand/stand/')";
	mv "${FILE}" "${newfile}";
done
