import os
from argparse import ArgumentParser


def is_number(num):  # A simple function to check if an argument is a number; self-explanitory
    try:
        float(num)
        return True
    except ValueError:
        return False


def fetchList(filePath, splitString, indexingStart, indexingEnd='None', skipBlankSplit=False, *args):  # Takes in a file path to open, what string you start splitting at, and the indexing for each line
    readMode = False
    openedFile = open(filePath, 'r')
    listArray = []
    currentLine = ''
    for line in openedFile:
        previousLine = currentLine
        currentLine = str(line)
        if currentLine.isspace() and readMode is True:  # In each line, check if it's purely white space
            if splitString not in previousLine or skipBlankSplit is False:  # If the previous line doesn't countain the spliting string (i.e. this isn't the line directly after the split), stop reading; only occurs if the skipBlankSplit option is set to True
                readMode = False
        if currentLine[0] == '[':  # The same is true if it's the start of a new section, signalled by '['
            readMode = False
        if readMode is True:
            if line[0] != ';' and currentLine.isspace() is False:  # If the line isn't a comment
                if indexingEnd == 'None':
                    importantLine = (currentLine.split())[indexingStart:]  # Just split with a start point, and take the rest
                else:
                    importantLine = (currentLine.split())[indexingStart:indexingEnd]  # Define the bigt we care about as the area between index start and end
                for ar in args:  # If any additional arguments were given (and they're numbers), also add this specific index in
                    if is_number(ar):
                        importantLine += [(currentLine.split())[ar]]
                listArray.append(importantLine)  # Append the important line to the list array
        if splitString in currentLine:  # Check at the end because we only want to start splitting after the string; if found, it'll split all further lines till it gets to white space
            readMode = True
    openedFile.close()
    return listArray  # Return the array containing all associations


def readITP(itpPath):
    atomTypeList = fetchList(itpPath, '[ atomtypes ]', 0, 7)  # 0-6 is the key area
    atomsList = fetchList(itpPath, '[ atoms ]', 0, 8)  # 0-7 is the key area
    associatedAtomList = []
    bondTypeList = []
    for atom in atomsList:  # A simple bit of  neatening; make an associated atom list, as we don't care about the comments or punctuation
        atomNum = atom[0]
        atomType = atom[1]
        bondType = atom[4]
        bondTypeList.append(bondType)
        associationList = [atomNum, atomType, bondType]
        associatedAtomList.append(associationList)  # Make a list of the above, and append it to the overarching list
    bondsList = fetchList(itpPath, '[ bonds ]', 0, 5)  # Call fetchList with the string associated with bonds in a .itp OPLS file; 0-1 is just the bonding atoms, 3-4 is the parameter
    anglesList = fetchList(itpPath, '[ angles ]', 0, 6)
    dihedralsList = fetchList(itpPath, ' PROPER DIHEDRAL', 0, 11)  # [ dihedral ] no longer works, as both proper and improper are under the heading
    impropersList = fetchList(itpPath, 'IMPROPER DIHEDRAL', 0, 7)
    return [associatedAtomList, atomsList, bondsList, anglesList, dihedralsList, impropersList, atomTypeList, bondTypeList]


def makeBondingTypeAssociation(associations, featureList, featureAtomCount, improper=False):  # We take in a list of associations (atom 1 is atom type x and bond type y, a list of features (e.g. bonds/angles/dihedrals), and how many atoms are involved in those features (2/3/4 respectively); see makeAllAssocciations for more details)
    totalFeatureList = []
    for feature in featureList:  # for each feature (bond/angle/dihedral)
        intList = [int(i) for i in feature[0:featureAtomCount]]  # We convert from strings to integers
        bondingTypeList = []
        for atom in intList:  # For each atom in the feature (currently represented as a number)
            for assoc in associations:  # We compare it against each of the atom number, atomtype, and bonding type associations
                atomNum = int(assoc[0])
                if atom == atomNum:  # If the atom number of this feature matches that of the association, then append the bonding type of that association to the list
                    bondingTypeList.append(assoc[2])
        if featureAtomCount == 2 or featureAtomCount == 3:
            bondingTypeList = bondingTypeList + feature[-2:]
        if featureAtomCount == 4 and improper is False:
            bondingTypeList = bondingTypeList + feature[-6:]
        if featureAtomCount == 4 and improper is True:
            bondingTypeList = bondingTypeList + [0.000, 0.000, feature[-1], 0.000, 0.000]
        totalFeatureList.append(bondingTypeList)  # When we've looped through all the atoms in that feature, append the resultant set of bonding types to the master list
    return(totalFeatureList)


def makeAllAssocciations(itpPath):
    readITPHolder = readITP(itpPath)  # Call the readIPT function, returning a list of lists (of lists) and function as a holder
    associationList = readITPHolder[0]  # Read the list of lists for the associations; where it says atom 1 is atomtype x and bondtype y
    bondsList = readITPHolder[2]  # Read the list of lists for the bonds in the form of '1    2', meaning 1 and 2 are bonded
    anglesList = readITPHolder[3]
    dihedralsList = readITPHolder[4]
    impropersList = readITPHolder[5]
    for improper in impropersList:  # We need to make some modifications, because the central atom definition is changed in LAMMPS from GROMACS
        tempImproperStorage = improper[0:4]
        improper[0] = tempImproperStorage[2]
        improper[1] = tempImproperStorage[3]
        improper[2] = tempImproperStorage[1]
        improper[3] = tempImproperStorage[0]
    totalBondList = makeBondingTypeAssociation(associationList, bondsList, 2)  # Call the makeBondingTypeAssociation function, getting the bond associations
    totalAnglesList = makeBondingTypeAssociation(associationList, anglesList, 3)  # Call the makeBondingTypeAssociation function, getting the angle associations
    totalDihedralsList = makeBondingTypeAssociation(associationList, dihedralsList, 4, improper=False)  # Call the makeBondingTypeAssociation function, getting the dihedral associations
    totalImpropersList = makeBondingTypeAssociation(associationList, impropersList, 4, improper=True)
    return[readITPHolder[1], totalBondList, totalAnglesList, totalDihedralsList, totalImpropersList, readITPHolder[6], readITPHolder[7]]


def uniqueList(list):  # A pretty self-explanatory little function; it takes a list, and returns that list in order with any duplicates removed
    uniqueList = []
    for item in list:
        if item not in uniqueList:
            uniqueList.append(item)
    return uniqueList


def formatILFF(paramType, paramList, output):  # A function that takes in the parameter list and types, and outputs the correctly formatted bonded parameters
    writeFile = open(output, 'a')
    outputLines = []
    if paramType == 'bond':  # We have to format this differently for each type of parameter
        writeFile.write('\nBONDS\n')
        for param in paramList:
            equilBondLength = format(float(param[2])*10, '.3f')  # We define the equilibrium bond length as the bond length from the OPLS force field x 10 (to convert to Angstrom), and to 3 decimal places
            bondConstant = format(float(param[3])/100, '.1f')  # The bond constant requires only 1 decimal place, but must be converted by dividing by 100
            while len(param[0]) < 4:
                param[0] = param[0] + ' '
            while len(param[1]) < 5:
                param[1] = param[1] + ' '
            if 'H' in param[0][0] or 'H' in param[1][0]:  # For bonds, we need to check if the first letter of the bonding type is H; if it is, that's a hydrogen bond and is written with 'cons' to ensure SHAKE works
                outputLine = str(param[0]) + param[1] + 'cons   ' + str(equilBondLength) + '   ' + str(bondConstant) + '\n'
                if outputLine not in outputLines:  # One last little check to ensure uniqueness; we put in the formatted line above in a list to check against, and then write it
                    outputLines.append(outputLine)
                    writeFile.write(outputLine)
            else:  # We repeat the above with 'harm' for harmonic, as the bond isn't frozen
                outputLine = str(param[0]) + param[1] + 'harm   ' + str(equilBondLength) + '   ' + str(bondConstant) + '\n'
                if outputLine not in outputLines:
                    outputLines.append(outputLine)
                    writeFile.write(outputLine)
    elif paramType == 'angle':  # We repeat the 'bond' process for angles, with some minor changes
        writeFile.write('ANGLES\n')
        for param in paramList:
            equilAngle = format(float(param[3]), '.1f')  # No conversion of values for angles; both are needed to 1 decimal place
            angleConstant = format(float(param[4]), '.1f')
            while len(param[0]) < 4:
                param[0] = param[0] + ' '
            while len(param[1]) < 4:
                param[1] = param[1] + ' '
            while len(param[2]) < 5:
                param[2] = param[2] + ' '
            outputLine = str(param[0]) + param[1] + param[2] + 'harm   ' + str(equilAngle) + '   ' + str(angleConstant) + '\n'
            if outputLine not in outputLines:  # Also no need for the 'H' check; we're not freezing angles
                outputLines.append(outputLine)
                writeFile.write(outputLine)
    elif paramType == 'dihedral' or paramType == 'improper':  # Finally we have dihedrals; these are very similar to the angles above
        if paramType == 'dihedral':
            writeFile.write('DIHEDRALS\n')
        elif paramType == 'improper':
            writeFile.write('IMPROPERS\n')
        for param in paramList:
            dihedralConstant1 = str(format(abs(float(param[5])), '.4f'))  # We define the dihedral constants as strings with 4 decimal places
            dihedralConstant2 = str(format(abs(float(param[6])), '.4f'))
            dihedralConstant3 = str(format(abs(float(param[7])), '.4f'))
            dihedralConstant4 = str(format(abs(float(param[8])), '.4f'))
            dihedralConstantList = [dihedralConstant2, dihedralConstant3, dihedralConstant4]  # We put these in a list; we want to make sure they have the correct spacing, and the last 3 have the same spacing requirements
            while len(param[0]) < 4:
                param[0] = param[0] + ' '
            while len(param[1]) < 4:
                param[1] = param[1] + ' '
            while len(param[2]) < 4:
                param[2] = param[2] + ' '
            while len(param[3]) < 5:
                param[3] = param[3] + ' '
            outputLine = (param[0] + param[1] + param[2] + param[3] + 'opls')  # We define the first half of the output, which is constant in spacing
            while len(dihedralConstant1) < 9:  # To ensure the spacing is correct, we know that from the end of the 'opls' to the end of the first dihedral constant is 9 characters
                dihedralConstant1 = ' ' + dihedralConstant1  # We add the appropriate space beforehand until this is true
            outputLine = outputLine + dihedralConstant1  # and add this string to the output line
            for constant in dihedralConstantList:  # The other 3 have 10 characters before the end, so we repeat the process
                while len(constant) < 10:
                    constant = ' ' + constant
                outputLine = outputLine + constant
            outputLine = outputLine + '\n'  # We then add the new line character at the end, and write it
            writeFile.write(outputLine)
    else:
        print('Unknown parameter type')  # A warning if this somehow happens, likely a typo
    writeFile.write('\n')  # We write one final newline character to make sure there's a space between each section
    writeFile.close()


def fetchNonBonded(atomtype, atomTypeList):  # A short function that looks through the non-bonded atomtypes in the OPLS force field, and returns the LJ parameters of the given atomtype
    for param in atomTypeList:
        if param[0] == atomtype:
            epsilon = float(param[-1])
            sigma = float(param[-2])*10  # These are coming in as nm, and we need them in Angstrom
            return([sigma, epsilon])


def makeFFNonBonded(atomList, atomTypeList, outputPath):  # A function that organizes and writes the non-bonded section of the ff file; optionally, a monomerSize argument can be passed which will prevent writing more atomtypes than necessary for polymeric units
    writeFile = open(outputPath, 'a')
    writeFile.write('ATOMS\n')
    writeCount = 0
    totalAtomicCharge = 0
    atomCount = 0
    for atom in atomList:  # For each atom in the list of atom types
        atomCount += 1
        atomName = atom[4]
        bondingType = atom[4]  # The bonding type is then added separately
        while len(atomName) < 6:  # There should be 6 characters from the start of the atom name to the start of the bonding type; this ensures it
            atomName = atomName + ' '
        while len(bondingType) < 5:
            bondingType = bondingType + ' '
        atomicMass = format(float(atom[7]), '.3f')  # The atomic mass is defined as the atomic mass from the atomic list to 3 decimal places, and the spacing is corrected
        while len(atomicMass) < 8:
            atomicMass = ' ' + atomicMass
        if float(atom[6]) >= 0:  # Atomic charge is defined to 2 decimal places, with a slight change in output based on the presence of the '-' character
            atomicCharge = format(float(atom[6][1:]), '.4f')
        elif float(atom[6]) < 0:
            atomicCharge = format(float(atom[6]), '.4f')
        totalAtomicCharge += float(atomicCharge)  # We keep track of the total atomic charge to make sure it's an integer later
        chargeDifference = (round(totalAtomicCharge, 0) - totalAtomicCharge)
        if atomCount == len(atomList) and chargeDifference < 0.001 > -0.001:  # If the total charge is off by a very small amount -  4 decimal places - just fix it on the last atom
            atomicCharge = format(float(atomicCharge) + chargeDifference, '.4f')
        elif atomCount == len(atomList) and (chargeDifference > 0.001 or chargeDifference < -0.001):
            print('You have relatively significant (>0.001) divergences in partial charge')
        while len(atomicCharge) < 9:  # The spacing is corrected
            atomicCharge = ' ' + atomicCharge
        atomType = atom[1]
        ljParam = fetchNonBonded(atomType, atomTypeList)  # The atom type is defined, and the fetchNonBonded function is called to return the LJ parameters
        sigma = str(format(ljParam[0], '.2f'))  # Sigma is defined to 2 decimal places, and spacing corrected
        while len(sigma) < 8:
            sigma = ' ' + sigma
        epsilon = str(format(ljParam[1], '.5f'))  # Epsilon is defined to 5 decimal places, and spacing corrected
        while len(epsilon) < 10:
            epsilon = ' ' + epsilon
        outputLine = (atomName + bondingType + atomicMass + atomicCharge + '   lj' + sigma + epsilon + '\n')  # The total line is written to file
        writeFile.write(outputLine)
        writeCount += 1
    writeFile.close()


def fetchXYZ(lammpsTopology, atomsList):  # A function that extracts the x/y/z coordinates and atom names from the lammps topology files
    atomsStart = fetchList(lammpsTopology, 'Atoms', 0, 7, skipBlankSplit=True)  # The LAMMPS topologies have a space in them, so we need to extract it with an increased tolerance for blank lines
    totalList = []
    for atom in atomsStart:  # For each atom taken from the lammps topology file
        atomNumber = atom[0]  # We define the atom number and XYZ coordinates
        atomXYZ = atom[-3:]
        for match in atomsList:  # For each atom in the list of atoms we already have, check if the atom numbers match
            if atomNumber == match[0]:
                atomName = [match[4]]  # If they do, we give the atom name it should have (as we just have a number right now) based off of the atom list
        finalLine = atomName + atomXYZ  # We make a list containin the atom name and XYZ coordinates, and append that to a list; when the loop is completed, we return the list
        totalList.append(finalLine)
    return totalList


def renameMonomer_old(monomer, outName, atomNames):  # This function, and renameXYZ_old are kept here for a little while in case they're needed; they function off of an input .xyz, instead of recreating an .xyz from the LAMMPS data file
    writeFile = open(outName, 'a')
    residueCounter = 0
    finalList = []
    for residue in monomer:
        residue[0] = atomNames[residueCounter]
        residueCounter += 1
        finalList.append(residue)
    for line in monomer:
        xVar = str(format(float(line[1]), '.6f'))
        while len(xVar) < 19:
            xVar = ' ' + xVar
        yVar = str(format(float(line[2]), '.6f'))
        while len(yVar) < 16:
            yVar = ' ' + yVar
        zVar = str(format(float(line[3]), '.6f'))
        while len(zVar) < 16:
            zVar = ' ' + zVar
        outputLine = ' ' + line[0] + xVar + yVar + zVar + '\n'
        writeFile.write(outputLine)


def renameXYZ_old(inputFile, atomNames, outName, ffName):
    if os.path.isfile(outName):
        os.remove(outName)
    readFile = open(inputFile, 'r')
    lineCounter = 1
    fullResidueList = []
    header = []
    for line in readFile:
        currentLine = str(line)
        if lineCounter > 2 and not currentLine.isspace():
            fullResidueList.append(currentLine.split())
        else:
            header.append(currentLine)
        lineCounter += 1
    renameMonomer_old(monomer=fullResidueList, outName=outName, atomNames=atomNames)
    with open(outName, 'r+') as writeFile:
        content = writeFile.read()
        writeFile.seek(0, 0)
        line = header[0] + ' probe1 ' + ffName
        print(line)
        writeFile.write(line.rstrip('\r\n') + '\n' + content)


def makeXYZ(inputFile, atomNames, outName, ffName):  # A function to make the required .xyz file for fftool
    if os.path.isfile(outName):  # If the file already exists, delete it; we don't want anything overlapping here
        os.remove(outName)
    fullResidueList = inputFile
    header = str(len(fullResidueList)) + '\n ' + ffName[:-3] + ' ' + ffName  # We define the header of the .xyz (the first two lines) as the number of residues, an arbritrary name, and then the force field file it'll require
    with open(outName, 'w') as writeFile:
        writeFile.write(header + '\n')  # We write this header
    writeFile = open(outName, 'a')  # We then open the output xyz in appending mode
    for line in fullResidueList:  # For each line in the full residue list
        xVar = str(format(float(line[1]), '.6f'))  # We define the coordinate to 6 decimal places
        while len(xVar) < 19:  # And adjust the spacing to make sure we've got it formatted correctly
            xVar = ' ' + xVar
        yVar = str(format(float(line[2]), '.6f'))  # We do the same for Y and Z, with slightly different spacing
        while len(yVar) < 16:
            yVar = ' ' + yVar
        zVar = str(format(float(line[3]), '.6f'))
        while len(zVar) < 16:
            zVar = ' ' + zVar
        outputLine = ' ' + line[0] + xVar + yVar + zVar + '\n'  # We define the line to write, and then write it, and repeat this for all other lines
        writeFile.write(outputLine)


def convertToIlFF(itpPath, outputPath, lammpsTopology, crystalOutput='placeholder'):
    if os.path.isfile(outputPath):  # If the output already exists, delete it so the appending doesn't work very badly
        os.remove(outputPath)
    if crystalOutput == 'placeholder':  # If we didn't provide a name (i.e. it's still the default), we split by / and take the final one (in case it was a path rather than just a file), get rid of the .ff in the input and just add '.xyz'
        crystalOutput = outputPath.split('/')[-1][:-3] + '.xyz'
    associationList = makeAllAssocciations(itpPath)  # Calls makeAllAssocciations to get all the bonded and nonbonded associations
    atomsList = associationList[0]
    bondParams = associationList[1]
    angleParams = associationList[2]
    dihedralParams = associationList[3]
    improperParams = associationList[4]
    atomTypeList = associationList[5]
    atomNameList = associationList[6]
    tempXYZ = fetchXYZ(lammpsTopology, atomsList)  # Generate a temporary XYZ from the LAMMPS topology file
    makeXYZ(inputFile=tempXYZ, atomNames=atomNameList, outName=crystalOutput, ffName=outputPath)  # Make the XYZ required from the temporary file
    makeFFNonBonded(atomsList, atomTypeList, outputPath)  # Call the function that makes the nonbonded part of the FF file
    formatILFF(paramType='bond', paramList=bondParams, output=outputPath)  # Call the formatILFF function, giving the final unique list of parameters to write out
    formatILFF(paramType='angle', paramList=angleParams, output=outputPath)
    formatILFF(paramType='dihedral', paramList=dihedralParams, output=outputPath)
    formatILFF(paramType='improper', paramList=improperParams, output=outputPath)


# convertToIlFF(itpPath='cellulose.itp', lammpsTopology='cellulose.lmp', outputPath='cellulose.ff', crystalOutput='cellulose.xyz')

parser = ArgumentParser(usage='OPLS_ligParGenFF.py -g [.itp file] -l [.lmp file] -o [output name]', description="A script that converts the output of the LigParGen webserver to a format that is compatible with Agilio Padua's fftool ecosystem")
parser.add_argument("-g", "--gromacs", required=True, help="The required .itp file generated by LigParGen")
parser.add_argument("-l", "--lammps", required=True, help="The required .lmp file generated by LigParGen")
parser.add_argument("-o", "--output", required=True, help="The name of the forcefield file generated")
parser.add_argument("-xyz" "--xyzFile", required=False, help="An optional argument; this specifies the name of the .xyz file output. If not given, it's the same name as the .ff file, but with the .xyz suffix")
args = parser.parse_args()

if args.xyz__xyzFile is None:
    convertToIlFF(itpPath=args.gromacs, outputPath=args.output, lammpsTopology=args.lammps)
else:
    convertToIlFF(itpPath=args.gromacs, outputPath=args.output, lammpsTopology=args.lammps, crystalOutput=args.xyz_xyzFile)
