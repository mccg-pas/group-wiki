#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 17:33:30 2018

@author: phal11
"""

import glob

#Look for all job files in dataintemp
pbsboys = glob.glob("dataintemp/*.pbs")

cmd = []

#Make the list of commands
for boy in pbsboys:
    cmd.append("qsub " + boy[11:] + " \n")

output = open("output.txt","w")

#Output the lines into a text file
for i in cmd:
    output.write(i)
output.close()
