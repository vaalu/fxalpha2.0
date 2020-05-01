#!/bin/sh
d=$(date '+%Y-%m-%d')
h=$(date '+%H')
sub_dir=`printf %02.0f $h`
logs_folder="/home/ubuntu/backups/logs/"
mkdir $logs_folder
mkdir "$logs_folder/$d"
mkdir "$logs_folder/$d/$sub_dir"
mv $logs_folder/*.* $logs_folder/$d/$sub_dir 
