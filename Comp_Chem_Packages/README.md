# Input files and job scripts

Example files are stored in the templates folder. Includes GAUSSIAN, GAMESS and
Psi4 input files, along with job scripts compatible with the Magnus, Massive,
Monarch, Raijin and Stampede2 (Texas) supercomputers.

Note: Raijin uses the PBS scheduler while every other supercomputer currently
used by the group use the SLURM scheduler.

# LAMMPS compilation

Makefiles should be placed in src/MAKE/MACHINES, then the corresponding build script can be
run from the top directory.

Note: use these makefiles as a guide for which compiler flags are needed, but modify the makefiles
that are provided with each distribution otherwise errors will probably arise.
