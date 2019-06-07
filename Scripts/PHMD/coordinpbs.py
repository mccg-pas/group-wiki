#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:23:59 2018

@author: phal11
"""

import glob

#Search for data files in data in temp
files = glob.glob("dataintemp/*.in")

#Look for the template job script
pbs = open("temp.pbs","r")
pbs2 = pbs.readlines()
pbs.close()

#Change the line for each input file
for file in files:
    pbs2[11] = "mpirun lmp_openmpi -i " + file[11:] + " > " + file[11:-3]+ ".out \n"
    hype = open(file[11:-3] + ".pbs","w")
    for i in pbs2:
        hype.write(i)
    hype.close()
