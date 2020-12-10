#!/bin/bash

# ================================================
#
# build_lammps.sh
# 
# Version: 19Mar20
# System: Stampede2, TACC
# Created by: Albert Lu (alu@tacc.utexas.edu)
# Last modified: 04/14/2020
#
# ================================================

# MODULES

module reset
module load intel/18.0.2
module load impi/18.0.2

# DOWNLOAD LAMMPS

# VERSION=patch_19Mar2020
ROOT_DIR=`pwd`
# SRC_DIR=${ROOT_DIR}/${VERSION}

# git clone -b "${VERSION}" --single-branch https://github.com/lammps/lammps ${VERSION}

# CONFIGURE PACKAGES

# cd ${SRC_DIR}/src
cd src

make yes-all
make no-lib
make no-ext
make no-gpu
make package-status

# BUILD LAMMPS

cd ${SRC_DIR}/src

cat MAKE/OPTIONS/Makefile.intel_cpu_intelmpi | \
    sed 's/-xHost/-xCOMMON-AVX512 -axMIC-AVX512/g' | \
    sed 's/-restrict/-restrict -diag-disable=cpu-dispatch/g' > \
    MAKE/MACHINES/Makefile.stampede

make -j4 stampede

mkdir -p ${SRC_DIR}/bin
mv lmp_stampede ${SRC_DIR}/bin
