=== LAMMPS with GPU ===

git clone https://github.com/lammps/lammps.git
git tag -l
git checkout tags/patch_5Feb2018 -b 5Feb2018

mv lammps  20180205-gpu

module purge
module load gcc/4.9.3
module load eigen/3.3.0
module load voro++/0.4.6
module load cuda/7.5
module load openmpi/1.10.3-gcc4-mlx-verbs-cuda75
module load fftw/3.3.5-gcc

cd /usr/local/src/LAMMPS/20180205-gpu/lib/gpu

export CUDA_HOME=$CUDA_DIR

make -f Makefile.linux

cd /usr/local/src/LAMMPS/20180205-gpu/src/MAKE

cp Makefile.mpi Makefile.trungn.openmpi

[trungn@m3-login2 MAKE]$ diff Makefile.trungn.openmpi Makefile.mpi
9,10c9,10
< CC =        mpic++
< CCFLAGS =    -O2 -DLAMMPS_MEMALIGN=64 -funroll-loops -fstrict-aliasing -Wall -W -Wno-uninitialized
---
> CC =        mpicxx
> CCFLAGS =    -g -O3
14,16c14,16
< LINK =        mpic++
< LINKFLAGS =    -O
< LIB =         -lstdc++
---
> LINK =        mpicxx
> LINKFLAGS =    -g -O
> LIB =
20c20
< ARFLAGS =    -rcsv
---
> ARFLAGS =    -rc
42,44c42,44
< MPI_INC =       -I/usr/local/openmpi/1.10.3-gcc4-mlx-verbs-cuda75/include
< MPI_PATH =     -L/usr/local/openmpi/1.10.3-gcc4-mlx-verbs-cuda75/lib
< MPI_LIB =    -lpthread
---
> MPI_INC =       -DMPICH_SKIP_MPICXX -DOMPI_SKIP_MPICXX=1
> MPI_PATH =
> MPI_LIB =
53,55c53,55
< FFT_INC =        -DFFT_FFTW3 -DFFTW_SIZE -I/usr/local/fftw/3.3.5-gcc/include
< FFT_PATH =     -L/usr/local/fftw/3.3.5-gcc/lib
< FFT_LIB =    -lfftw3
---
> FFT_INC =
> FFT_PATH =
> FFT_LIB =
75c75
< EXTRA_INC = $(CPPFLAGS) $(LMP_INC) $(PKG_INC) $(MPI_INC) $(FFT_INC) $(JPG_INC) $(PKG_SYSINC)
---
> EXTRA_INC = $(LMP_INC) $(PKG_INC) $(MPI_INC) $(FFT_INC) $(JPG_INC) $(PKG_SYSINC)
77a78,79
> EXTRA_CPP_DEPENDS = $(PKG_CPP_DEPENDS)
> EXTRA_LINK_DEPENDS = $(PKG_LINK_DEPENDS)
92c94
< lib:    $(OBJ)
---
> lib:    $(OBJ) $(EXTRA_LINK_DEPENDS)
95c97
< shlib: $(OBJ)
---
> shlib:    $(OBJ) $(EXTRA_LINK_DEPENDS)
97c99
<     $(OBJ) $(EXTRA_LIB) $(LIB)
---
>         $(OBJ) $(EXTRA_LIB) $(LIB)
102c104
<     $(CC) $(LDFLAGS) $(CCFLAGS) $(SHFLAGS) $(EXTRA_INC) -c $<
---
>     $(CC) $(CCFLAGS) $(SHFLAGS) $(EXTRA_INC) -c $<
104,108d105
< %.d:%.cpp
<     $(CC) $(LDFLAGS) $(CCFLAGS) $(EXTRA_INC) $(DEPFLAGS) $< > $@
<
< %.o:%.cu
<     $(CC) $(LDFLAGS) $(CCFLAGS) $(SHFLAGS) $(EXTRA_INC) -c $<

cd /usr/local/src/LAMMPS/20180205-gpu/lammps/src

 make yes-asphere
 make yes-kspace
 make yes-gpu

make trungn.openmpi 2>&1 | tee ./trungn.log

 cp /usr/local/src/LAMMPS/20180205-gpu/src/lmp_trungn.openmpi /usr/local/lammps/20180205-gpu/

cd /usr/local/lammps/20180205-gpu/

ln -s lmp_trungn.openmpi lmp

=== LAMMPS without GPU ===

git clone (as above)

module purge
module load gcc/4.9.3
module load eigen/3.3.0
module load voro++/0.4.6
module load openmpi/1.10.3-gcc4-mlx-verbs
module load fftw/3.3.5-gcc

cd /usr/local/src/LAMMPS/20180205/lammps

cd /usr/local/src/LAMMPS/20180205/lammps/lib/meam
make -f Makefile.gfortran

cd /usr/local/src/LAMMPS/20180205/lammps/lib/reax/
 make -f Makefile.gfortran
cd /usr/local/src/LAMMPS/20180205/lammps/lib/poems/
 make -f Makefile.g++
cd /usr/local/src/LAMMPS/20180205/lammps/lib/awpmd/
 make -f Makefile.mpicc
cd /usr/local/src/LAMMPS/20180205/lammps/lib/colvars/
 make -f Makefile.g++
cd /usr/local/src/LAMMPS/20180205/lammps/lib/qmmm/
 make -f Makefile.gfortran
cd /usr/local/src/LAMMPS/20180205/lammps/lib/atc/
 make -f Makefile.g++

 cd /usr/local/src/LAMMPS/20180205/lammps/src/


cp /usr/local/src/LAMMPS/Makefile.trungn.openmpi /usr/local/src/LAMMPS/20180205/lammps/src/MAKE/

diff Makefile.trungn.openmpi Makefile.mpi
[trungn@m3-login2 MAKE]$ diff Makefile.trungn.openmpi Makefile.mpi
9,10c9,10
< CC =        mpic++
< CCFLAGS =    -O2 -DLAMMPS_MEMALIGN=64 -funroll-loops -fstrict-aliasing -Wall -W -Wno-uninitialized
---
> CC =        mpicxx
> CCFLAGS =    -g -O3
14,16c14,16
< LINK =        mpic++
< LINKFLAGS =    -O
< LIB =         -lstdc++ -L/usr/local/voro++/0.4.6/lib
---
> LINK =        mpicxx
> LINKFLAGS =    -g -O
> LIB =
20c20
< ARFLAGS =    -rcsv
---
> ARFLAGS =    -rc
42,44c42,44
< MPI_INC =       -I/usr/local/openmpi/1.10.3-gcc4-mlx-verbs/include
< MPI_PATH =     -L/usr/local/openmpi/1.10.3-gcc4-mlx-verbs/lib
< MPI_LIB =    -lpthread
---
> MPI_INC =       -DMPICH_SKIP_MPICXX -DOMPI_SKIP_MPICXX=1
> MPI_PATH =
> MPI_LIB =
53,55c53,55
< FFT_INC =        -DFFT_FFTW3 -DFFTW_SIZE -I/usr/local/fftw/3.3.5-gcc/include
< FFT_PATH =     -L/usr/local/fftw/3.3.5-gcc/lib
< FFT_LIB =    -lfftw3
---
> FFT_INC =
> FFT_PATH =
> FFT_LIB =
75c75
< EXTRA_INC = $(CPPFLAGS) $(LMP_INC) $(PKG_INC) $(MPI_INC) $(FFT_INC) $(JPG_INC) $(PKG_SYSINC)
---
> EXTRA_INC = $(LMP_INC) $(PKG_INC) $(MPI_INC) $(FFT_INC) $(JPG_INC) $(PKG_SYSINC)
77a78,79
> EXTRA_CPP_DEPENDS = $(PKG_CPP_DEPENDS)
> EXTRA_LINK_DEPENDS = $(PKG_LINK_DEPENDS)
92c94
< lib:    $(OBJ)
---
> lib:    $(OBJ) $(EXTRA_LINK_DEPENDS)
95c97
< shlib: $(OBJ)
---
> shlib:    $(OBJ) $(EXTRA_LINK_DEPENDS)
97c99
<     $(OBJ) $(EXTRA_LIB) $(LIB)
---
>         $(OBJ) $(EXTRA_LIB) $(LIB)
102c104
<     $(CC) $(LDFLAGS) $(CCFLAGS) $(SHFLAGS) $(EXTRA_INC) -c $<
---
>     $(CC) $(CCFLAGS) $(SHFLAGS) $(EXTRA_INC) -c $<
104,108d105
< %.d:%.cpp
<     $(CC) $(LDFLAGS) $(CCFLAGS) $(EXTRA_INC) $(DEPFLAGS) $< > $@
<
< %.o:%.cu
<     $(CC) $(LDFLAGS) $(CCFLAGS) $(SHFLAGS) $(EXTRA_INC) -c $<


make no-all
make yes-atc
make yes-asphere
make yes-body
make yes-class2
make yes-colloid
make yes-compress
make yes-coreshell
make yes-dipole
make yes-granular
make yes-kspace
make lib-latte args="-b -m gfortran"
make yes-latte
make yes-manybody
make yes-mc
make lib-meam args="-m mpi"
make yes-meam
make yes-misc
make yes-molecule
make yes-mpiio
make yes-opt
make yes-peri
make lib-poems args="-m mpi"
make yes-poems
make yes-python
make yes-qeq
make yes-replica
make yes-rigid
make yes-shock
make yes-snap
make yes-srd

make trungn.openmpi 2>&1 | tee ./trungn.log

cp /usr/local/src/LAMMPS/20180205/lammps/src/lmp_trungn.openmpi /usr/local/lammps/20180205/

cd /usr/local/lammps/20180205/

 ln -s lmp_trungn.openmpi lmp

Edit module file
