#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 15:24:20 2018

@author: phal11
"""

import glob

#Searching for templates and data files
#Note the directories specified, change at will
temps = glob.glob("temp/*.in")
datas = glob.glob("Data/*.data")

# for each template file
for temp in temps:
    tempy = open(temp,"r")
    tempy2 = tempy.readlines()
    tempy.close()

    #Find where "read_data" is
    for i in range(len(tempy2)):
        if "read_data" in tempy2[i]:
            start = i
            break

    #Create a new input for each .data file for this template
    #Where each input reads in different data
    for data in datas:
        tempy2[start] = "read_data       " + data[5:] + " \n"
        output = open(data[5:-5] + ".in","w")
        for i in tempy2:
            output.write(i)
        output.close()
