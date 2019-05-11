#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 17:33:30 2018

@author: phal11
"""

import glob

pbsboys = glob.glob("coordintemp/*.slm")

cmd = []

for boy in pbsboys:
    cmd.append("sbatch " + boy[12:] + " \n")
    
output = open("output.txt","w")

for i in cmd:
    output.write(i)
output.close()

    