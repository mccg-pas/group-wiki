#!/bin/bash
#SBATCH --account=sn29
#SBATCH --time=48:00:00
#SBATCH --ntasks=32
#SBATCH --tasks-per-node=16
#SBATCH --mem=16000

module load lammps

srun --export=all -n 32 lmp_dam.openmpi -in TEAP.in > TEAP.out