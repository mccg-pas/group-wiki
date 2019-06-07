-----
Guide to using these codes
-----
Note:
These codes are not perfect and I encourage you to optimise them for your needs.
All of the codes read all files of a certain type, which might require you to
backup files before subjecting them to the codes.
The codes don't dig into subfolders.

----
topo.py
----
This script is designed to read all .xyz files inside its directory and output
a list of commands in a .txt file. These commands are designed to be copied into
a VMD console and create LAMMPS format data files from each .xyz file.

Launch VMD and go to the directory of your target .xyz files. Then copy in the
output of the code into the console of VMD (TK console is my preference).

These .data files will not contain parameters, which the next code will fix.

Note: Make sure your atoms are labelled by their atom type, such as
C1 = terminal carbon. VMD only reads in the chemical symbol and doesn't care
about any following numbers.

----
mdall.py and PHILFF.py
----

These two scripts work in tandem, where PHILFF.py is a dictionary imported into
mdall.py. I encourage you to make a dictionary for your own systems, and edit
mdall.py accordingly to import that dictionary in.

The labelling of atoms in the dictionary should match the labelling of the atoms
in your .xyz files, and consequently whatever is displayed in your blank .data
file. Look through the .data files from the previous step to see in which order
atoms are listed for bonds, angles and dihedrals.

One route for optimisation here is that you can group each atom into its
relevant bond, angle and dihedral group (for example terminal carbons).
Sometimes you may need to omit certain angles to achieve a particular isomer,
so proceed with judgement.

mdall.py is designed to edit the .data files created from the previous step and
import forcefield parameters from the dictionary file, creating a filled LAMMPS
data file which can be imported in inputs.

mdall.py also changes the box boundaries in the data file, depending on the most
extreme x,y and z coordinates.

To import these data files in LAMMPS inputs, the command is

read_data [filename.data]

for example,

read_data c4mimeFAP.data

It's worth noting that mdall.py is designed for the following styles:
-atom_style      full
-bond_style      harmonic
-angle_style     harmonic
-dihedral_style  opls
-improper_style  cvff

I'm unsure of how other styles differ, and mdall could work just fine for other
styles.

As general advice, please check the units of your parameters, and compare their
mathematical formulation to how LAMMPS reads in parameters. For example, some
papers list constants in terms of (1/2)*K instead of just K.

To use these scripts, paste the .data files from the previous step, mdall.py
and your dictionary file into the same directory. Then run mdall.py. If all is
well then your .data files should be ready to go.

From here you're welcome to use your now ready .data files for however you make
your inputs and job files, or you can read on to check out some more codes.

----
coordintemp.py, coordinpbs.py and cmd.py
----

These three codes help me create numerous inputs at once based off the same
template. I tweak these codes depending on what kind of job I'm running.

coordintemp.py creates an input file for all of the .data files you have ready.
In this case the only thing different in each input is what data file the input
reads. Note that each input will produce a traj.lmp file which will be
overwritten, so I'd recommend running each simulation in a different folder on
a cluster.

coordinpbs.py reads in any input files and creates .pbs (job files) for each
input. This is just achieved by changing one line of each pbs file to read in a
different input file. The temp.pbs file is required for this and can be edited.

Finally, cmd.py creates a output text file that contains commands to run jobs
in the cluster. This is more handy for QM calculations where I have multiple
jobs in the same directory.

My process for using each of these codes is the following:
-Firstly I would place all of the .data files edited by mdall.py into a folder
called "Data"
-Then also have a folder called "temp", in which is a template input
-I would then run coordintemp.py, and place the output files into a folder
called dataintemp (as per the code)
-I would then run coordinpbs.py and throw those outputs into dataintemp
-I would then transfer the .data files from Data into dataintemp, and run
amdatomlabel.py in the dataintemp folder, which would hopefully edit the
dump_modify line correctly.

The files in dataintemp are now ready to be copied into clusters and run.

See Example/tosub to see how I've laid out these codes.

----
Amdatomlabel.py
----

This script modifies one line in each input file: the line containing
dump_modify. This is important for exporting trajectories for post processing.
I use TRAVIS for post processing, and would recommend checking that out.

amdatomlabel.py scans through all .data files in a directory, counts the
separate elements in the data and then adjusts the input file appropriately.
It's important to note that the chemical symbols should be in alphabetical
order.

amdatomlabel.py is the final script I run before transferring inputs and job
files across to the cluster. It should be used in the folder where both the
.data files and .in files are.

----
Fin
----

Finally, the folder "Example" contains an example of how I use these codes.
My folder structure is just there to protect other files from the codes.
Thank you for reading, and I hope you find these to be helpful.
