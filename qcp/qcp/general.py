# FUNCTIONS
# ---------
# software
# softInp
# xyzPull
# eof
# gms_check_spec
# g09_check_spec
# psi_check_spec

# ----------- GENERAL FUNCTIONS ----------------

### FIND WHICH SOFTWARE USED
# NEED LOG FILE PROVIDED
def software(path, File):

    soft = False

    # BREAKS AFTER A KEY WORD FOUND
    # SHOULD NOT READ MORE THAN A FEW LINES
    with open(path + File, 'r') as f:
        for line in f:
            if "GAMESS" in line:
                soft = "gms"
                break
            elif "Gaussian" in line:
                soft = "g09"
                break
            elif "PSI4" in line:
                soft = "psi"
                break
            elif "Psi4" in line:
                soft = "psi"
                break


    return soft


### FIND SOFTWARE BY TEMPLATE FILE
def softInp(path, template):

    soft = False

    with open(path + template, 'r') as f:
        for line in f:
            if 'module load gaussian' in line:
                soft = 'g09'
                break
            elif 'SYSTEM' in line:
                soft = 'gms'
            elif 'FMO' in line:
                soft = 'fmo'
                break
            elif 'memory' in line:
                soft = 'psi'

            elif "%pal" in line:
                soft = "orc"
                break

    return soft


### RETURN LIST OF FILES
# level EXPECTS int OR False
# OUTPUT LIST OF [PATH, FILE] COMB PER FILE
def find_files(path, level, file_pattern):

    import os, sys
    import fnmatch

    # file_pattern IS LIST OF PATTERNS
    # IF GIVEN AS ONLY ONE PATTERN - MAKE LIST
    if type(file_pattern) == str:
        file_pattern = [file_pattern]

    # DELETES DIRECTORIES BELOW LEVEL
    def walklevel(some_dir, level):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    Files = [] # RETURN LIST OF PATHS
    # ONLY CURRENT LEVEL
    if not level:
        level = 0
    if level == 0:
        for pat in file_pattern:
            for File in os.listdir('.'):
                #print(File)
                #print(pat)
                if fnmatch.fnmatch(File, '*' + pat):
                    #print(pat)
                    Files.append(['./', File])
        return Files
    # WITH LEVEL DOWN
    elif type(int(level)) == int:
        level = int(level)
        for root, dirs, files in walklevel(path, level):
            # MATCHING FILE IN PATH
            for pat in file_pattern:
                for File in files:
                    if fnmatch.fnmatch(File, '*' + pat):
                        if not path == root + '/':
                            root_ = root.replace('./', '', 1)
                            long_path = path + root_ + '/'
                        else:
                            long_path = path
                        Files.append([long_path, File])
        return Files
    else:
        sys.exit("Error with specified levels")


### GET XYZ DATA FROM .xyz
# def xyzPull(path, File):
#     import re
#
#     coords = []
#
#     with open(path + File, 'r') as f:
#         for num, line in enumerate(f):
#             if re.search('[A-Z]\s*', line) and num > 1:
#                 # MAKE SECOND CHARACTER LOWER CASE
#                 spl_line = line.split()
#                 for val, chrtr in enumerate(spl_line[0]):
#                     if val == 0:
#                         first = chrtr
#                     elif val == 1:
#                         second = chrtr.lower()
#                         sym = first + second
#                         line = line.replace(spl_line[0], sym)
#                 coords.append(line.split())
#     #print(coords)
#     #sys.exit()
#     return coords


### RETURN END OF FILE
# percFile IS PERCENTAGE OF END OF FILE
def eof(path, File, percFile):
    # OPEN IN BYTES
    with open(path + File, "rb") as f:
        f.seek(0, 2)                      # Seek @ EOF
        fsize = f.tell()                  # Get size
        Dsize = int(percFile * fsize)
        f.seek (max (fsize-Dsize, 0), 0)  # Set pos @ last n chars lines
        lines = f.readlines()             # Read to end

    # RETURN DECODED LINES
    for i in range(len(lines)):
        try:
            lines[i] = lines[i].decode("utf-8")
        except:
            lines[i] = "CORRUPTLINE"
            print("eof function passed a corrupt line in file ", File)
        # FOR LETTER IN SYMBOL
    return lines

# --------- LOG FILE FUNCTIONS ------------


### CHECK IF GAMESS LOG SINGLE POINT CALC
# RETURNS BOOLEAN
def gms_check_spec(path, File):
    found = False
    with open(path + File, 'r') as f:
        for line in f:
            if "RUNTYP=OPTIMIZE" in line:
                spec = False
                found = True
                break
            elif "RUNTYP=ENERGY" in line:
                spec = True
                found = True
                break
    if not found:
        spec = False
        print("Runtype not recognised", path, File)
    return spec


### CHECK IF GAUSSIAN LOG SINGLE POINT CALC
# RETURNS BOOLEAN
def g09_check_spec(path, File):
    import re
    spec = True
    with open(path + File, 'r') as f:
        for line_no, line in enumerate(f):
            if line_no < 200:
                if re.search("#.*opt", line):
                    spec = False
                    break
            else:
                break
    return spec


### CHECK IF PSI4 LOG SINGLE POINT CALC
# RETURNS BOOLEAN
def psi_check_spec(path, File):
    with open(path + File, 'r') as f:
        for line in f:
            if "optimize" in line:
                spec = False
                break
            elif "energy" in line:
                spec = True
                break
    return spec


### GET XYZ DATA FROM .xyz
def xyzPull(path, File):
    import re

    coords = []

    with open(path + File, 'r') as f:
        for num, line in enumerate(f):
            if re.search('[A-Z]\s*', line) and num > 1:
                # MAKE SECOND CHARACTER LOWER CASE
                spl_line = line.split()
                for val, chrtr in enumerate(spl_line[0]):
                    if val == 0:
                        first = chrtr
                    elif val == 1:
                        second = chrtr.lower()
                        sym = first + second
                        line = line.replace(spl_line[0], sym)
                coords.append(line.split())
    #print(coords)
    #sys.exit()
    return coords
