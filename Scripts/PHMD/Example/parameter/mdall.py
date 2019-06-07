# -*- coding: utf-8 -*-
"""
Created on Thu Jul 05 22:25:56 2018

@author: Peter
"""
#Importing relevant packages
import glob
import math
#Importing my dictionary file
#you would change this line if you make your own dictionary
import PHILFF as PH

#looking for all the .data files in the directory
datas = glob.glob("*.data")

#for each data file
for data in datas:
    hype = open(data, 'r')
    hype2 = hype.readlines()
    hype.close()

	#Searching for pair coeffs part in .data file
    for i in range(len(hype2)):
        if 'Pair Coeffs' in hype2[i]:
            hype2[i] = 'Pair Coeffs \n'
            hype2[i+1] = '\n'
            start = i + 2
        if 'Bond Coeffs' in hype2[i]:
            end = i - 1
    #Adding pair coeffs from the dictionary file
    for j in range(start,end):
        spl = hype2[j].split()
        if spl[-1] in PH.atoms:
            spl[:2] = [spl[1],PH.atoms[spl[-1]][0],PH.atoms[spl[-1]][1],'#']
        for i in range(len(spl)):
            spl[i] = str(spl[i]) + ' '
        hype2[j] = ''.join(spl) + '\n'

	#Searching for bond coeffs part in .data file
    for i in range(len(hype2)):
        if 'Bond Coeffs' in hype2[i]:
            hype2[i] = 'Bond Coeffs \n'
            hype2[i+1] = '\n'
            start = i + 2
        if 'Angle Coeffs' in hype2[i]:
            end = i - 1
    #Adding bond coeffs from the dictionary
    for j in range(start,end):
        spl = hype2[j].split()
        if spl[-1] in PH.bonds:
            spl[:2] = [spl[1],PH.bonds[spl[-1]][0],PH.bonds[spl[-1]][1],'#']
        for i in range(len(spl)):
            spl[i] = str(spl[i]) + ' '
        hype2[j] = ''.join(spl) + '\n'

	#Searching for angle coeffs part in .data file
    for i in range(len(hype2)):
        if 'Angle Coeffs' in hype2[i]:
            hype2[i] = 'Angle Coeffs \n'
            hype2[i+1] = '\n'
            start = i + 2
        if 'Dihedral Coeffs' in hype2[i]:
            end = i - 1
    #Adding angle coeffs from dictionary
    for j in range(start,end):
        spl = hype2[j].split()
        if spl[-1] in PH.angles:
            spl[:2] = [spl[1],PH.angles[spl[-1]][0],PH.angles[spl[-1]][1],'#']
        for i in range(len(spl)):
            spl[i] = str(spl[i]) + ' '
        hype2[j] = ''.join(spl) + '\n'

	#Finding dihedral coeffs part in .data file
    END = False
    for i in range(len(hype2)):
        if 'Dihedral Coeffs' in hype2[i]:
            hype2[i] = 'Dihedral Coeffs \n'
            hype2[i+1] = '\n'
            start = i + 2
        #Checking if impropers are in the .data file
        if 'Improper Coeffs' in hype2[i]:
            end = i - 1
            END = True
        if 'Masses' in hype2[i] and not END:
            end = i - 1
            END = True

    #Adding dihedral coeffs from dictionary
    for j in range(start,end):
        spl = hype2[j].split()
        if spl[-1] in PH.dihedrals:
            spl[:2] = [spl[1],PH.dihedrals[spl[-1]][0],PH.dihedrals[spl[-1]][1],
            PH.dihedrals[spl[-1]][2],PH.dihedrals[spl[-1]][3],'#']
        for i in range(len(spl)):
            spl[i] = str(spl[i]) + ' '
        hype2[j] = ''.join(spl) + '\n'

	#Searching for improper part in coeffs
    for i in range(len(hype2)):
        if 'Improper Coeffs' in hype2[i]:
            hype2[i] = 'Improper Coeffs \n'
            hype2[i+1] = '\n'
            start = i + 2
        if 'Masses' in hype2[i]:
            end = i - 1
    #Adding impropers parameters
    for j in range(start,end):
        spl = hype2[j].split()
        if spl[-1] in PH.impropers:
            spl[:2] = [spl[1],PH.impropers[spl[-1]][0],-1,2,'#']
        for i in range(len(spl)):
            spl[i] = str(spl[i]) + ' '
        hype2[j] = ''.join(spl) + '\n'

	#Scouting lines or partial charge and box lengths
    for i in range(len(hype2)):
        if 'Atoms' and 'full' in hype2[i]:
            start = i + 2
        if 'Bonds' in hype2[i]:
            end = i - 1
        if 'xlo xhi' in hype2[i]:
            xloc = i
            xline = hype2[i].split()
        if 'ylo yhi' in hype2[i]:
            yloc = i
            yline = hype2[i].split()
        if 'zlo zhi' in hype2[i]:
            zloc = i
            zline = hype2[i].split()
    #finding the box size
    box = [[],[],[]]
    for j in range(start,end):
        spl = hype2[j].split()
        #Appending x y z coordinates in a list
        box[0].append(float(spl[4]))
        box[1].append(float(spl[5]))
        box[2].append(float(spl[6]))
        #Adding partial charges
        if spl[-1] in PH.atoms:
            spl[3] = PH.atoms[spl[-1]][2]
        for i in range(len(spl)):
            spl[i] = str(spl[i]) + ' '
        hype2[j] = ''.join(spl) + '\n'
	 #Partial charges added

    #Throwing in the box size
    #Changing xlo and xhigh from x coordinates
    xlo = math.floor(min(box[0])) - 1
    xline[0] = xlo
    xhi = math.ceil(max(box[0])) + 1
    xline[1] = xhi
    for i in range(len(xline)):
        xline[i] = str(xline[i]) + ' '
    hype2[xloc] = ''.join(xline) + '\n'

    #Changing ylo and yhi from x coordinates
    ylo = math.floor(min(box[1])) - 1
    yline[0] = ylo
    yhi = math.ceil(max(box[1])) + 1
    yline[1] = yhi
    for i in range(len(yline)):
        yline[i] = str(yline[i]) + ' '
    hype2[yloc] = ''.join(yline) + '\n'

    #Changing zlo and zhi from x coordinates
    zlo = math.floor(min(box[2])) - 1
    zline[0] = zlo
    zhi = math.ceil(max(box[2])) + 1
    zline[1] = zhi
    for i in range(len(zline)):
        zline[i] = str(zline[i]) + ' '
    hype2[zloc] = ''.join(zline) + '\n'

    #Output the result into the data file
    output = open(data, "w")
    for i in hype2:
        output.write(i)
    output.close()
