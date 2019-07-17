#!/bin/bash

# Author: Anh LP Nguyen
# Date: 09 Nov 2018
# Purpose: cleaning the scratch space
# in the project sn29 on Massive M3

jobs_squ=$PWD/jobs_on_squ.tmp.file
jobs_scr=$PWD/jobs_in_scr.tmp.file

squeue -u $USER -o %i >> $jobs_squ
sed -i "1d" $jobs_squ

/bin/ls /scratch/sn29/$USER >> $jobs_scr
/bin/ls -l /scratch/sn29/ | grep $USER | awk '{print $9}' >> $jobs_scr

sed -i "s/g16.//g" $jobs_scr
sed -i "/$USER/ d" $jobs_scr

while read k
do
    sed -i "/$k/ d" $jobs_scr
done < $jobs_squ

while read m
do
    rm -rf /scratch/sn29/$m
    rm -rf /scratch/sn29/$USER/$m
done < $jobs_scr

rm -rf $jobs_scr $jobs_squ
