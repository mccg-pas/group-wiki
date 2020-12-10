#!/usr/bin/env bash                         
                                            
module purge                                
module load gcc/4.9.3                       
module load eigen/3.3.0                     
module load openmpi/1.10.3-gcc4-mlx-verbs   
module load fftw/3.3.5-gcc                  
                                            
mkdir bin                                   
cd src                                      
make yes-standard                           
make no-ext                                 
make no-lib                                 
make yes-molecule                           
make yes-user-drude                         
make yes-user-misc                          
make monarch                                
cd ..                                       
ln -s $(pwd)/src/lmp_monarch bin/lmp_monarch
# ln -s $(pwd)/src/lmp_monarch bin/lmp_m3 # for massive
