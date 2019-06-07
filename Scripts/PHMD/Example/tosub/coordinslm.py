#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:23:59 2018

@author: phal11
"""

import glob

files = glob.glob("dataintemp/*.in")

pbs = open("temp.slm","r")
pbs2 = pbs.readlines()
pbs.close()

for file in files:
    pbs2[9] = 'srun --export=all -n 32 lmp_dam.openmpi -in ' + file[11:] + ' > ' + file[11:-3] + '.out \n'
    hype = open(file[11:-3] + ".slm","w")
    for i in pbs2:
        hype.write(i)
    hype.close()