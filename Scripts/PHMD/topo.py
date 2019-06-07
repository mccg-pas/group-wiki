# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 10:24:37 2018

@author: Peter
"""

#Make sure VMD is in the directory of your labelled xyz
import glob

totopo = glob.glob("*.xyz")

#to be stacked in
cmd = []

#Conjure a set of commands to copy into VMD
for top in totopo:
    cmd.append("mol new " + top + " \n")
    cmd.append("topo retypebonds \n")
    cmd.append("topo guessangles \n")
    cmd.append("topo guessdihedrals \n")
    cmd.append("topo guessimpropers \n")
    cmd.append("topo writelammpsdata " + top[:-4] + ".data \n")
    cmd.append("mol delete all \n")

#Make a text file
output = open("toposcript.txt","w")

for i in cmd:
    output.write(i)
output.close()
#Pack her up boys
