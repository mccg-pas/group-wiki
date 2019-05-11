--QUANTUM COMPUTATIONAL PROCESSOR--

(1) OPTIONAL ARGUMENTS:

    -h, --help            show this help message and exit
    -f FILE, --file FILE  path to xyz/log file
    -t TASK, --task TASK  task option
    -j JOBFILE, --jobfile JOBFILE
                          job template file
    --info INFO           information

(2) PATHS:

/path-to-apps/bin/qcp

Alternatively, the path "/path-to-apps/apps/bin" can be
added to either "~/.bash_profile" or "~/.bashrc" such
that "qcp" can be excecuted without the preceeding
path. If "~/.bash_profile" or "~/.bashrc" do not exist
you can simply create one (e.g. vim ~/bash_profile)
and add the above path to your $PATH using:

export PATH=/path-to-apps/bin:$PATH

within the file. Note: The path will not be appended
until you log in again, as these files are only read
when your environment is initially set upon login.
You can also run source ~/.bash_profile to reload the
settings of your environment as defined in the file.

(3) TO USE:

usage: qcp [-h] [-f FILE] [-t TASK] [-j JOBFILE] [--info]

-h, --help : will print help which shows optional arguments
-f, --file : allows the user to identify just one file
             for qcp otherwise qcp will use either all .xyz
             or all .log/.out in folder
-t, --task : user can specify the task performed and skip
             printing of menu
-j, --jobfile
           : user can specify a file to use as a template
             job file, otherwise if none is specified a
             pre-prepared template will be used or if
             job.template exists in the current directory
             that will be used
--info     : prints a summary of README


(4) SOFTWARE:

Currently configured for:-
Clusters:
    Gaia (MCC)
    Raijin
    Magnus
    Monarch
Packages:
    GAMESS
    GAMESS-FMO
    Gaussian
    PSI4

(5) DEPENDENCIES:

Most functions will work on any linux clusters as
the functions employed are generic operations. The
excecuting file qcp must be directed in the first
line to a working python3 with installed packages:
 - numpy
Options to delete and submit jobs will fail on any
cluster not recognides under cluster above

(6) FUNCTIONS:

Upon excecution the program will give a numerical list
of options. In all cases, text in square brackets is
default response and will be used as the response
if nothing is entered. For example, in example output 1
below, the default is zero ([0]) and the programme
will quit if nothing is typed before pressing enter.
The task will be performed in the current directory
the programme is run from.

Example output start:
======================================================
Python Version: 3.6.2
Quantum Chemistry Processor
What would you like to do? [0]
                1. Generate inp/job files from template
                2. Pull energies
                3. Check log files and sort
                4. Mass sed
                5. Mass rename
                6. Delete jobs from queue
                7. Counterpoise correction
                8. Distance and angles
                9. Submit com/job in folder
                0. Quit
                                            Task:
======================================================


Generate inp/job files from template-----------------
 - Generates input files for all xyz files in folder
 - Expects a file in folder called *.template which
   is a GAMESS, PSI4 or GAUSSIAN input file
 - Optional: If a template.job file is found it will
   be used as a template as a job file otherwise
   a stock one is generated
 - Can have old coordinates or simply 'xyz_data'
   which will be replaced by the coordinates in each
   xyz file
 - Will change charge and multiplicity if the
   molecules are found in the database, else will
   keep those found in the file
 - Also changes the name of the generated output
   file specified in the input
 - Multiple template files can be stored in the
   directory and files will be created for all xyz
   for each template
 - Ion calculations are automatically created for
   energy FMO calculations
 - New directories are created for PSI4 and GAMESS
   jobs that require only one job per folder while
   Gaussian jobs are made the same folder
 - Naming has been taken care of such that
   different templates will produce different
   names of files
 - If the optional argument --file is used only
   the provided file will be put into the template
 - If --jobfile is specified, stock template and
   job.template are not used. The specified file is
   instead used to make job files and the .log and
   .out and .chk are replaced with name of xyz file

Example output 1:
======================================================
Using                ./c1mim-dca-p1.xyz
----------------------------------------
SYSTEM:
Cation detected      c1mim
Anion detected       dca
Cation detected      c1mim
Anion detected       dca
Total charge = 0, Total multiplicity = 1
----------------------------------------
With template        ./g09-spec.template
With template        ./psi4.template
With template        ./gms.template
With template        ./g09-opt.template
With template        ./fmo.template
======================================================

 - In Example (2), the folder contained an xyz file
   in which four cations were identified and for
   each of the 5 template files ("With template")
   an input and job was created with exception to
   the Gaussian templates where the job and input
   file is within the same file

Pull energies------------------------------
 - Pulls energies from *log and *out files
 - Extracts MP2, HF, DFT and ZPVE if they are found
 - Energies are pulled from files of all
   subdirectories of the folder qcp is excecuted
   in
 - After extraction the user is given the
   option to save the data as a CSV file
   which can be downloaded and opened in
   excel and separated by the delimiter '|'
 - Energies written to file called out
   "out_energies.csv"

Example output 2:
======================================================
Write to file? (y/n) [n] y
--------------------------------------------------------------------------------
File                                    Type  HF/DFT           ZPVE     MP2/SRS             Path
--------------------------------------------------------------------------------
hexene-rad-product.log                  opt   -235.0476303     0.1512056                    ./
gamess-energy.log                       spe   -1452.844195056           -1457.360566128     ./
hej.log                                 opt                                                 ./
fmo.log                                 spe                                                 ./
c3mim-bf4-p1.log                        opt                                                 ./
cation.log                              spe   -303.3727384613           -304.5932077305     ./
hexene-reactant.log                     opt                                                 ./
ts2.log                                 opt   -235.0464623     0.1517278                    ./
ts8.log                                 opt   -235.0464623     0.1517273                    ./
ts5.log                                 opt   -235.0464623     0.1517278                    ./
psi4.log                                opt                                                 ./
reactant-.log                           spe   -235.1198196                                  ./
c1mim-bf4-p4.log                        spe   -1452.859036394           -1457.363772017     ./
c1mim-cl-p2.out                         opt   -1526.193718031           -1529.086971817     ./
c1mim-bf4-p4.out                        opt                                                 ./
psi4-energy.out                         spe   -303.2916115069           -304.2948976560     ./
gauss-energy.out                        spe   -235.1604603                                  ./
======================================================

Check log files and sort------------------------------

 - All files ending with '.out' or '.log' will be
   processed except those starting with 'f-'
 - Log files are determined to be either single point
   or optimisations
 - New xyz files are generated for optimisation if
   they have completed at least one geometry step
 - New xyz files are put in folders notConv, rerun
   spec or unknown which are for optimisations that
   did not converge, those that exceeded memory
   or time, optimisations that finished and unknown
   errors, respectively
 - The log files for errors of notConv, rerun and
   unknown are also copied into the folders with
   the xyz so the user may easily source the
   problem
 - The error of the log file is appended to the
   name of the xyz file separated by '_' for easy
   analysis when looking back at files however this
   is removed again when generating the next inp
   files
 - The error "Optimisation did not complete one full
   step" will copy the existing xyz file into the
   appropriate folder if the xyz exists as the same
   name as the log file
 - Walltime errors are looked at for raijin jobs by
   first searching the job.o file


Example output 3:
======================================================
Normal termination   ./hexene-rad-product.log       Creating xyz
Single point calcu   ./gamess-energy.log            No xyz needed
Unknown error unkn   ./hej.log                      Creating xyz
Unknown error unkn   ./sub2-a1c2d3e2f3.log          Creating xyz
Memory has exceede   ./fmo.log                      Creating xyz
Not recongnise inp   ./c1mpyr-bf4-p1.log            File software not found
Maximum iterations   ./c3mim-bf4-p1.log             Creating xyz
Single point calcu   ./cation.log                   No xyz needed
Convergence errors   ./hexene-reactant.log          Creating xyz
Normal termination   ./ts2.log                      Creating xyz
Normal termination   ./ts8.log                      Creating xyz
Normal termination   ./ts5.log                      Creating xyz
Failed optimisatio   ./psi4.log                     Optimisation did not complete one full step
Single point calcu   ./reactant-.log                No xyz needed
Normal termination   ./c1mim-bf4-p4.log             Creating xyz
Normal termination   ./c1mim-cl-p2.out              Creating xyz
Failed optimisatio   ./c1mim-bf4-p4.out             Optimisation did not complete one full step
Single point calcu   ./psi4-energy.out              No xyz needed
Single point calcu   ./gauss-energy.out             No xyz needed
======================================================

Mass sed----------------------------------------------

 - For easily swapping out strings
 - Can swap more than one string by separating each
   one by the & symbol
 - For example output 5 will change 'honey2' -> milk
   and change both -> a cheese for all files ending
   with .txt within the current directory and two
   directories down

Example output 4:
======================================================
Only sed files with extention  [all]: txt
Change text in files from           : honey2&both
Change text in files to             : milk&a cheese
Number of levels down to change[all]: 2
Using:  other5.txt
Changed:  honey2 from both
to     :  milk from both

Changed:  milk from both
to     :  milk from a cheese
======================================================

Mass rename-------------------------------------------

 - Swap any part of a name with another string\n
 - Can specify extention of those to change\n

Example output 5:
======================================================
Only rename files with extention[all]:
Part of name to replace              : low
Replace with                         : high
Number of levels down to change [all]: 1
Renaming  ./low3.job.o7391046 ./high3.job.o7391046
Renaming  ./low1.job.e7391050 ./high1.job.e7391050
Renaming  ./low2.job.e7391048 ./high2.job.e7391048
Renaming  ./low3.job.e7391046 ./high3.job.e7391046
Renaming  ./low1.job.o7391050 ./high1.job.o7391050
Renaming  ./low2.job.o7391048 ./high2.job.o7391048
======================================================

Delete jobs from queue--------------------------------

 - Choose by:
 1. Number - Removes the number of jobs defined by the
    user from the bottom of the queue; wil remove the
    last submitted jobs
 2. All - Will double check
 3. Name - Any part of the name (visible by the queue)
    that matches the string will be deleted

Example output 6:
======================================================
Waiting for queue from system...

#  ID          Name               Status     Nodes
------------------------------------------------------
8  400764      opt-c1mim-         Q          1
7  400765      opt-pyr-bf         Q          1
6  400766      opt-c1mim-         Q          1
5  400767      opt-nme4-b         Q          1
4  400768      opt-nme4-c         Q          1
3  400769      opt-c1mpyr         Q          1
2  400770      opt-pyr-cl         Q          1
1  400771      opt-c1mpyr         Q          1

Delete by: 1: Number; 2: All; 3: Name; [Default=1] 1

Number of jobs to delete from bottom of queue: 3
Removed 400771 from queue
Removed 400770 from queue
Removed 400769 from queue
=====================================================

Counterpoise correction------------------------------
- PSI4 and Gaussian
- Creates folder 'CP_' + filename with molecule
  calculations, the total energy calculations and
  one for a single job counterpoise correction in the
  case of Gaussian

Example output 7:
======================================================
Using                ./shmozzle.xyz
----------------------------------------
SYSTEM:
Cation detected     c1mim      1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
unknown             B1F3       16 17 18 19
Cation detected     c1mim      21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36

./shmozzle-psi4/shmozzle
======================================================

Distance and angles-----------------------------------

 - Choose between printing all interionic distances
   and all hydrogen bond distances and angles
 - Cut off angle for hydrogen bond length is 180 +/-
   45 degrees and cut off distance is 2.5 Angstrom
   Hydrogen bonds are only detected between N, O and
   F so far

Example output 8:
======================================================

    1. All interionic distances
    2. H-bonding data
                                Task: 1
----------------------------------------
All interionic distances
----------------------------------------
C  F     1  17  3.031
C  B     1  18  3.985
C  F     1  19  5.229
C  F     1  20  4.343
C  F     1  21  3.954
C  C     1  22  8.150
----------------------------------------
======================================================

Submit all com/job in folder--------------------------

Example output 9:
Number of subdirs [0-9]:
======================================================
Submitted: 400764  opt-c1mim-cl.job
Submitted: 400765  opt-pyr-bf4.job
Submitted: 400766  opt-c1mim-bf4.job
Submitted: 400767  opt-nme4-bf4.job
Submitted: 400768  opt-nme4-cl.job
Submitted: 400769  opt-c1mpyr-bf4.job
Submitted: 400770  opt-pyr-cl.job
Submitted: 400771  opt-c1mpyr-cl.job
======================================================

0. Quit-----------------------------------------------


(7) FILES:

Files contain the following functions:

supercomp.py
    host()
    get_queue(cmd)
    rjn_q()
    gai_q()
    mgs_q()
    mas_q()
    mon_q()
    deleteJob()
    submit(path, cwd, File)
clean.py
    sed(path)
    rename(path)
    deleteJob()
pprint.py
    e_print(energy)
    stat_print(path, File, q_mess, l_mess = False)
    file_print(path, File, q_mess)
    detec(Type, nums, mol)
    noFiles()
gen_job.py
    job_replace(name, jobTemp)
    numTemp(path)
    xyzTemp(path, template, coords)
    newDir(path, File, template)
    g09(path, File, template, sysData)
    gms(path, File, template, sysData, jobTemp)
    psi(path, File, template, sysData, jobTemp)
    fmo(path, File, template, sysData, jobTemp)
logFile.py
    rjn_wall(path, File, err, ext, stat)
    g09_log(path, File, spec)
    gms_log(path, File, spec)
    psi_log(path, File, spec)
    sort(path, File, soft)
    gms_geom(path, File, opt)
    g09_geom(path, File, opt)
    psi_geom(path, File, opt)
qcp
    main()
    check_exist_args_file(File)
    giveUserInfo()
tempInp.py
    inpDetail()
    psi_inp()
    fmo_ions(chrg, coords, bset, mp2)
gen_jobCP.py
    newDirCP(path, File, template)
gen_jobCP.py
    psi_cpoise(path, File, template, sysData, jobTemp)
    g09_cpoise(path, File, template, sysData)
write.py
    write_xyz(path, name, geom)
    write_gmsInp(path, name, lines)
    write_inp(path, name, lines)
    write_job(path, name, lines, cp = False)
    write_energy(path, energy)
general.py
    software(path, File)
    softInp(path, template)
    hardware()
    find_files(path, level, file_pattern)
    walklevel(some_dir, level)
    xyzPull(path, File)
    eof(path, File, percFile)
    gms_check_spec(path, File)
    g09_check_spec(path, File)
    psi_check_spec(path, File)
    xyzPull(path, File)
geometry.py
    sysGeom(sysData)
    dist_vec(atom1_dict, atom2_dict)
    dist_between(atom1_dict, atom2_dict)
    dot_prod(vec1, vec2)
    ang(atom1_dict, atom2_dict, atom3_dict)
energy.py
    energy_gms(path, File, energy)
    energy_g09(path, File, energy)
    energy_psi(path, File, energy)
run_tasks.py
    comp_tasks(task, path, filename, jobfile)
templates.py
    psi_rjnJob(name)
    psi_gaiJob(name)
    gms_rjnJob(name, mwords, ddi)
    gms_mgsJob(name)
    gms_gaiJob(name)
    fmo_rjnJob(name, nfrags, mwords, ddi)
    fmo_mgsJob(name, nfrags, mwords, ddi)
    fmo_gaiJob(name)
    memFmo(nfrags, hw, mwords, ddi)
    oldFmo_gaiJob(name)
    fmo_HF_inp(name, calcType, charg, bs)
    mw_ddi(frags, calcType)
    user_job_params()
    psi4_jobComp()
system.py
    systemData(path, File, check)
    sep_mol(coords, distca)
    isCation(a, b, q = False)
    isAnion(a, b, q = False)
    isNeutral(a, b, q = False)
    isRadical(a, b, q = False)
