#!/bin/bash

# find_rpm.sh <PATH> <string>

rpm_path=$1
target_str=$2

if [ ! -d ${rpm_path} ];then
	echo "<PATH> is invalid"
 	exit 1
fi

if [ -z ${target_str} ];then
 	echo "no string"
 	exit 1
fi

for f in ${rpm_path}/*
do
	rpm -qpl $f | grep ${target_str} &>/dev/null
	if [ $? -eq 0 ]
	then
		echo $f
	fi
done


