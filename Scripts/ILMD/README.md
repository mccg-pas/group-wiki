# ILMD
A series of scripts designed to integrate into Agilio Padua's [fftool](https://github.com/agiliopadua/fftool) ecosystem for the creation of MD input files

## convertLigParGen.py - Automated MD Parameter Generation
A python script for the conversion of parameters from the formats generated by the [LigParGen](http://zarbi.chem.yale.edu/ligpargen/index.html) webserver.
These parameters are OPLS-style parameters, and are available directly in a wide variety of formats, but the fftool system is a recent development and not supported by the webserver.
This script requires the LAMMPS and GROMACS output of the LigParGen results, and will convert these into the fftool-style parameters and topology required for an MD simulation.
Using the script is simple, using the following format:

python convertLigParGen.py -g [.top/.itp file] -l [.lmp file] -o [output name]

Where the -g flag signals the GROMACS .top/.itp file, -l signals the LAMMPS .lmp file (both from the LigParGen webserver), -o flags the desired output name, and -xyz is an optional argument for the name of the .xyz file generated; otherwise it will be based on the output name.
Calling the script with the -h flag will instead show the documentation for the script.

NOTE: The extension of the GROMACS topology file generated on LigParGen has changed from .itp to .top previously, and recent reports have mentioned that it has changed back to .itp. Until further clarification, please investigate if either a .itp or .top file is available from LigParGen; they are the same formatting internally, and either of them should work with the -g argument in this script.
