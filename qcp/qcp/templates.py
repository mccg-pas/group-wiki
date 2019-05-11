### GAUSSIAN JOB IN GIVEN TEMPLATE FILE

### PSI4 JOB SCRIPT ONE NODE

def psi_rjnJob(name):
    # PSI4 MEMORY IN INP NEEDS >>> MEM IN JOB
    # CPUS FROM MEMORY
    #if (int(memory) % 2 == 0): #even
    #    cpus = int(memory / 5)
    #else: #odd
    #     cpus = int((memory + 1) / 5)
    #jobfs  = (int(memory/100) + 1) * 100
    #memory = str(memory)
    #cpus   = str(cpus)
    #jobfs  = str(jobfs)
    memory = '128'
    cpus   = '16'
    jobfs  = '1000'
    lines= ["#!/bin/bash\n",
    "#PBS -P k96\n",
    "#PBS -l mem=" + memory + "GB\n",
    "#PBS -l ncpus=" + cpus + "\n",
    "#PBS -l jobfs=" + jobfs + "GB\n",
    "#PBS -l walltime=48:00:00\n",
    #"#PBS -q normalbw\n"
    "#PBS -l wd\n\n",
    "module load psicode/4.0-19Aug16\n",
    "psi4 -n $PBS_NCPUS " + name + ".inp " + name + ".log"]
    return lines

def psi_gaiJob(name):
    lines = ["#!/bin/sh\n",
    "#$ -S /bin/sh\n",
    "#$ -cwd\n",
    "#$ -l h_rt=720:00:00\n",
    "#$ -l h_vmem=64G\n",
    "#$ -l h_stack=2G\n",
    "#$ -j y\n",
    "#$ -pe smp 32\n",
    "#$ -l passwd=izgoro\n\n",
    "export OMP_NUM_THREADS=32\n",
    "export MKL_NUM_THREADS=32\n\n",
    ". /etc/profile\n",
    "~/SHARED/apps/PSI4/4.0b5/bin/psi4 " + name + ".inp " + name + ".out"]
    return lines

def psi_masJob(name):
    lines=["#!/bin/env bash\n",
    "#SBATCH  --ntasks=16\n",
    "#SBATCH  --tasks-per-node=16\n",
    "#SBATCH --time=150:00:00\n",
    "#SBATCH --mem=32gb\n",
    "module load psi4/v1.1\n\n",
    "export PROJECT='sn29'\n",
    "export PSI_SCRATCH=$PWD\n\n",
    "psi4 " + name + ".inp " + name + ".log"]
    return lines

### GAMESS - NO FMO - 1 NODE  --------

### GAMESS ON RAIJIN JOB SCRIPT
def gms_rjnJob(name):
    # DOESN'T REQUIRE WHOLE NODE
    #mem, cpus, jobfs, wall = memFmo(nfrags, 'rjn', mwords, ddi)
    mem   = '16'
    cpus  = '8'
    jobfs = '100'
    wall  = '48:00:00'
    lines=["#!/bin/sh\n",
    "#PBS -P k96\n",
    "#PBS -l mem=" + mem + "gb\n",
    "#PBS -l ncpus=" + cpus + "\n",
    "#PBS -l jobfs=" + jobfs + "gb\n",
    "#PBS -l walltime=" + wall + "\n",
    "#PBS -l wd\n\n",
    "module unload openmpi/1.6.3\n",
    "module load openmpi/1.8.4\n",
    "/short/k96/apps/gamess16/rungms.rika " + name + ".inp $PBS_NCPUS > " + name + ".log"]
    return lines

def orc_rjnJob(name):
    lines=["#!/bin/sh\n",
    "#PBS -P k96\n",
    "#PBS -l mem=32gb\n",
    "#PBS -l ncpus=16\n",
    "#PBS -l jobfs=200gb\n",
    "#PBS -l walltime=200:00:00\n",
    "#PBS -l software=orca\n",
    "#PBS -l wd\n\n",
    "module load orca/4.0.1.2\n",
    "$ORCA_PATH/orca " + name + ".inp > " + name + ".log"]
    return lines


def gms_masJob(name):
    lines = ["#!/bin/bash\n",
             "#SBATCH --account=sn29\n",
             "#SBATCH --time=06:00:00\n",
             "#SBATCH --ntasks=8\n",
             "#SBATCH --tasks-per-node=8\n",
             "#SBATCH --cpus-per-task=1\n",
             "#SBATCH --mem=80G\n\n",
             'export PROJECT="sn29"\n\n',
             "module load gamess/16srs1-v2\n\n",
             "rungms.m3 " + name + ".inp 00 $SLURM_NTASKS > " + name + ".log"]
    return lines

def gms_mgsJob(name):
    lines = ["#!/bin/bash --login\n",
    "#SBATCH --nodes=8\n",
    "#SBATCH --account=pawsey0197\n",
    "#SBATCH --time=24:00:00\n",
    "#SBATCH --export=NONE\n\n",
    "module use /group/pawsey0197/software/cle52up04/modulefiles\n",
    "module load gamess/2016\n",
    "rungms " + name + ".inp 00 12 12"]
    return lines

def gms_stmJob(name):
    lines = ["#!/bin/bash\n\n",
    "#SBATCH -J " + name + "\n",      
    "#SBATCH -o " + name + ".log\n",  
    "#SBATCH -e " + name + ".e%j\n",        
    "#SBATCH -p skx-normal\n",     
    "#SBATCH -N 1\n",          
    "#SBATCH --tasks-per-node=22\n",
    "#SBATCH -t 24:00:00\n",        
    "#SBATCH --mail-user=thomas.mason1+stampede@monash.edu\n",
    "#SBATCH --mail-type=all\n\n",  
    "module load intel/18.0.2\n",
    "module load impi/18.0.2\n",
    "module load my_gamess/2017.04.20.srs-magnus\n\n",
    "export OMP_NUM_THREADS=1\n\n",
    "rungms " + name + ".inp 00 22 22"]
    return lines

def gms_gaiJob(name):
    lines=["#!/bin/sh\n",
    "#$ -S /bin/sh\n",
    "#$ -cwd\n",
    "#$ -l h_rt=700:00:00\n",
    "#$ -l h_vmem=30G\n",
    "#$ -l h_stack=2048M\n\n",
    "#$ -j y\n",
    "#$ -pe mpi_smp16 16\n",
    "#$ -l passwd=izgoro\n\n",
    "#$ -q gaia\n\n",
    "#$ -m ea\n\n",
    # OLD GAMESS
    "#module load openmpi/1.4.1-IB\n\n",
    "module load openmpi/1.7.5\n",
    "module load gamess/sacevedo\n\n",
    "INPUT=" + name + ".inp\n\n",
    "rungms.gaia ${INPUT} 01 $NSLOTS > " + name + ".log\n"]
    return lines

### FMO ------------------------------


### FMO ON RAIJIN JOB SCRIPT
def fmo_rjnJob(name, nfrags, mwords, ddi):
    mem, cpus, jobfs, wall = memFmo(nfrags, 'rjn', mwords, ddi)
    lines=["#!/bin/sh\n",
    "#PBS -P k96\n",
    "#PBS -l mem=" + mem + "gb\n",
    "#PBS -l ncpus=" + cpus + "\n",
    "#PBS -l jobfs=" + jobfs + "gb\n",
    "#PBS -l walltime=" + wall + "\n",
    "#PBS -l wd\n\n",
    "module unload openmpi/1.6.3\n",
    "module load openmpi/1.8.4\n",
    "/short/k96/apps/gamess16-srs/rungms.rika " + name + ".inp $PBS_NCPUS > " + name + ".log"]
    return lines


### FMO ON MAGNUS JOB SCRIPT
def fmo_mgsJob(name, nfrags, mwords, ddi):
    cpus = memFmo(nfrags, 'mgs', mwords, ddi)
    lines = ["#!/bin/bash --login\n",
    "#SBATCH --nodes=" + str(nfrags) + "\n",
    "#SBATCH --account=pawsey0197\n",
    "#SBATCH --time=24:00:00\n",
    "#SBATCH --output= " + name + ".log\n",
    "#SBATCH --export=NONE\n\n",
    "export OMP_NUM_THREADS=1\n",
    "/group/pawsey0197/software/cle60up05/apps/gamess_cray_build/rungms " + name + ".inp 00 " + cpus + " 24"]
    return lines

# Gamess on Stampede assume 22 servers per node- otherwise overclock memory requirements (48 available, and used on gaussian)
def fmo_stmJob(name, nfrags, mwords, ddi):
    cpus = memFmo(nfrags, 'stm', mwords, ddi)
    lines = ["#!/bin/bash\n\n",
    "#SBATCH -J " + name + "\n",      
    "#SBATCH -o " + name + ".log\n",  
    "#SBATCH -e " + name + ".e%j\n",        
    "#SBATCH -p skx-normal\n",     
    "#SBATCH -N " + str(int(float(cpus) / 22)) + "\n",          
    "#SBATCH --tasks-per-node=22\n",
    "#SBATCH -t 24:00:00\n",        
    "#SBATCH --mail-user=thomas.mason1+stampede@monash.edu\n",
    "#SBATCH --mail-type=all\n\n",  
    "module load intel/18.0.2\n",
    "module load impi/18.0.2\n",
    "module load my_gamess/2017.04.20.srs-magnus\n\n",
    "export OMP_NUM_THREADS=1\n\n",
    "rungms " + name + ".inp 00 " + cpus  + " 22"]
    return lines

### FMO ON GAIA JOB SCRIPT //
# FROM PHILIP NOT YET ESTABLISHED FOR MANY NODES
def fmo_gaiJob(name):
    ## NOT USED YET ***
    #mem, cpus, jobfs, wall = memFmo(nfrags, 'gai', mwords, ddi)
    lines = ["#!/bin/sh\n\n",
    "#$ -N sample_fmo\n",
    "#$ -l h_vmem=16G\n",
    "#$ -l h_rt=24:00:00\n",
    "#$ -pe short 16\n",
    "#$ -cwd\n\n",
    "module load gamess/16srs1\n\n",
    "rungms " + name + ".inp 00 1 $NSLOTS > " + name + ".out"]
    return lines




### USES MWORDS, MEMDDI AND HARDWARE TO DETERMINE PARAMS
def memFmo(nfrags, hw, mwords, ddi):

    import math

    mwords     = float(mwords)
    ddi        = float(ddi)
    # RAIJIN
    if hw == 'rjn':
        cpuPerNode = 16
        cpus       = nfrags * cpuPerNode
        if not ddi:
            gbsPerCpu = mwords * 8/1024
            if gbsPerCpu < 2:
                mem = cpus * 2
            else:
                mem = cpus * 4
        else:
            gbsPerCpu = (mwords + ddi/cpus) * 8/1024
            if gbsPerCpu < 2:
                mem = cpus * 2
            elif gbsPerCpu < 4:
                mem = cpus * 4
            else:
                print("Based off of your template memory you require 8GB "\
                + "cpus - consider less memory for a more efficient run")
                mem = cpus * 8

        if cpus < 32:
            wall = '150:00:00'
        elif cpus < 255:
            wall = '48:00:00'
        elif cpus < 512:
            wall = '96:00:00'
        elif cpus < 1024:
            # FUNCTION OF MINUTES VS CPUS GOT BY:
            # nf_limits -P k96 -n 1024 -q normal
            wall = -10.044 * cpus + 10850
            wall = int(wall / 60)
            wall = str(wall) + ':00:00'
        else:
            wall = '5:00:00'
        jobfs = int(144.27 * math.log(cpus) - 100)

        mem   = str(mem)
        cpus  = str(cpus)
        jobfs = str(jobfs)

        return mem, cpus, jobfs, wall

    # MAGNUS AND GAIA
    elif hw == 'gai':
        cpuPerNode = 12
        cpus       = nfrags * cpuPerNode
        mem        = cpus   * 2
        if not ddi:
            gbsPerCpu = mwords * 8/1024
            if gbsPerCpu > 2:
                print("The amount of mwords in your template "\
                + "is > than the 2GB cpus - consider <256")
        else:
            gbsPerCpu = (mwords + ddi/cpus) * 8/1024
            if gbsPerCpu > 2:
                print("The amount of mwords & ddi in your template "\
                + "is > than the 2GB CPUs - consider <256 total per CPU")
        return str(cpus)

    elif hw == 'mgs':
        cpuPerNode = 24
        cpus       = nfrags * cpuPerNode
        mem        = cpus   * 4
        if not ddi:
            gbsPerCpu = mwords * 8/1024
            if gbsPerCpu > 4:
                print("The amount of mwords in your template "\
                + "is > than the 4GB cpus - consider <400")
        else:
            gbsPerCpu = (mwords + ddi/cpus) * 8/1024
            if gbsPerCpu > 4:
                print("The amount of mwords & ddi in your template "\
                + "is > than the 4GB CPUs - consider <400 total per CPU")
        return str(cpus)

    elif hw == 'stm':
        cpuPerNode = 22
        cpus       = nfrags * cpuPerNode
        mem        = cpus   * 4
        if not ddi:
            gbsPerCpu = mwords * 8/1024
            if gbsPerCpu > 4:
                print("The amount of mwords in your template "\
                + "is > than the 4GB cpus - consider <400")
        else:
            gbsPerCpu = (mwords + ddi/cpus) * 8/1024
            if gbsPerCpu > 4:
                print("The amount of mwords & ddi in your template "\
                + "is > than the 4GB CPUs - consider <400 total per CPU")
        return str(cpus)




### UNUSED ----------------------------------------------

### NON SRS GAMESS ON GAIA
def oldFmo_gaiJob(name):
    lines=["#!/bin/sh\n",
    "#$ -S /bin/sh\n",
    "#$ -cwd\n",
    "#$ -l h_rt=700:00:00\n",
    "#$ -l h_vmem=60G\n",
    "#$ -l h_stack=2048M\n\n",
    "#$ -j y\n",
    "#$ -pe mpi_smp16 256\n",
    "#$ -l passwd=izgoro\n\n",
    "#$ -q gaia\n\n",
    "#$ -M zlsee3@student.monash.edu\n",
    "#$ -m ea\n\n",
    "#module load openmpi/1.4.1-IB\n\n",
    "module load openmpi/1.7.5\n",
    "module load gamess/sacevedo\n\n",
    "INPUT=" + name + ".inp\n\n",
    "rungms.gaia ${INPUT} 01 $NSLOTS > " + name + ".log\n"]

def fmo_HF_inp(name, calcType, charg, bs):
    mwords, memddi = mw_ddi(frags, calcType)
    lines = [" $SYSTEM MWORDS="+mwords+" MEMDDI="+memddi+" $END \n",
    " $CONTRL SCFTYP=RHF RUNTYP="+calcType+" MAXIT=200 ISPHER=1\n",
    " ICHARG="+charg+" $END\n",
    " $SCF DIRSCF=.TRUE. FDIFF=.FALSE. DIIS=.TRUE. $END\n",
    " $BASIS GBASIS="+bs+" $END\n",
    " $DATA\n",
    name+"-HF-"+calcType+"\n",
    "C1\n"]
    return lines


# CALC MEMDDI FOR USER
def mw_ddi(frags, calcType):
    cpus = frags * 16
    mwords = 400
    if calcType == "energy":
        memddi = 0
    if calcType == "optimize":
        memddi = ((cpus * 4 - cpus * 4 * 1/8) * 1024)/8 - 400 * cpus
    return mwords, memddi

### INPUT FROM USER
def user_job_params():
    wall  = user("Walltime[24]: ")
    ncpus = user("Cpus     [8]: ")
    jobfs = user("Jobfs  [100]: ")

    wall  = wall  or '24'
    ncpus  = ncpus or '8'
    jobfs = jobfs or '100'

    wall  = wall.split(':')
    wall  = wall[0]

    return wall, ncpus, jobfs

### PSI4 JOB FROM LUKE
def psi4_jobComp():
    lines = ["#!/bin/csh",
    "#PBS -P k96",
    "#PBS -l mem=20GB",
    "#PBS -l ncpus=4",
    "#PBS -l jobfs=100Gb",
    "#PBS -l walltime=10:00",
    "#PBS -l wd",

    "module load psicode",

    "setenv OMP_NUM_THREADS $PBS_NCPUS",
    "setenv MKL_NUM_THREADS $PBS_NCPUS",

    "psi4 pyrdcaconf2conf3.inp pyrdcaconf2conf3.out"]



