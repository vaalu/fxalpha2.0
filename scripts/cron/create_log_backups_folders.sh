#!/bin/sh
indx=9
d=$(date '+%Y-%m-%d')
logs_folder="/home/ubuntu/backups/logs/"
mkdir $logs_folder
mkdir "$logs_folder/$d"
sub_dir=""
while [ "$indx" -lt 24 ] # 09 AM to 00 AM 15 Hours, 15 folders
do
        sub_dir=`printf %02.0f $indx`
        mkdir "$logs_folder/$d/$sub_dir"
        indx=`expr $indx + 1`
done
