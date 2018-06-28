#!/bin/bash

# ctfs.sh -s <rpm_path> -l <rpm_list_file>
# ctfs.sh -s ~/mirrors/cdn.download.clearlinux.org/releases/22500/clear/x86_64/os/Packages -l ../fl.txt

rpm_path=''
rpm_list_file=''

help(){
	echo 'usage: -s <rpm_path> -l <rpm_list_file>'
}

# $1: rpm file
checkrpm_script(){
	echo "===check script in rpm" `basename $1` "=====" 
	rpm -qp --scripts $1
}

while getopts "s:l:h" arg
do
	case $arg in
 		s)
 			rpm_path=$OPTARG
 			;;
 		l)
 			rpm_list_file=$OPTARG
 			;;
 		h)
 			help
 			exit 0
 			;;
 		?)
 			help
 			exit 0
 			;;
 	esac
done

if [ -z ${rpm_path}  ] || [ ! -d ${rpm_path} ];then
	echo 'missing rpm_path, please append -s <rpm_path>'
	exit 1
fi

if [ -z ${rpm_list_file}  ] ||[ ! -f ${rpm_list_file} ];then
	echo 'missing rpm_list_file, please append -l <rpm_list_file>'
	exit 1
fi

for fn in `cat ${rpm_list_file}`
do
	if [ ! -f ${rpm_path}/${fn}-[0-9]* ];then
		echo "rpm "\"${fn}\" "is not found"
		exit 1
	else
		checkrpm_script ${rpm_path}/${fn}-[0-9]*
	fi
done 


