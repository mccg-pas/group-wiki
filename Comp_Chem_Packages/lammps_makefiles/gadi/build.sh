#!/usr/bin/env bash

# module purge
module load python3/3.8.5
module load intel-compiler/2020.2.254
module load intel-tbb/2020.2.254
module load intel-mkl/2020.2.254
module load fftw3-mkl/2020.2.254
module load openmpi/4.0.2
module load hdf5/1.10.5
module load plumed/2.6.0
module load eigen/3.3.7

ROOT=$(pwd)
cd $ROOT/src
make yes-all
make no-lib
make no-ext
make no-gpu
make no-user-intel
make nci
mkdir -p $ROOT/bin
mv lmp_nci $ROOT/bin
