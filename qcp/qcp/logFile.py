# CHECK FOR RAIJIN WALLTIME EXCEEDED
def rjn_wall(path, File, err, ext, stat):
    import os, re, glob
    from datetime import timedelta as td
    t_tak = 0
    t_lim = 1

    name      = File.replace('.log', '').replace('.out', '')
    file_stat = glob.glob(path + name + '*.j*.o*') + glob.glob(path + name + '*.j*.o*')

    if len(file_stat) > 0:
        file_stat.sort()
        # GLOBGLOB RETURNS PATH - NO PATH NEEDED BEFORE FILE2
        File2 = file_stat[-1]
        f = open(File2, 'r+')
        for line in f:
            if "Walltime" in line:
                line = line.split()
                fmt = '%H:%M:%S'
                t_lim = line[2].split(':')
                t_tak = line[5].split(':')
                t_lim = td(hours=int(t_lim[0]),
                           minutes=int(t_lim[1]), seconds=int(t_lim[2]))
                t_tak = td(hours=int(t_tak[0]),
                           minutes=int(t_tak[1]), seconds=int(t_tak[2]))

    # WILL RUN EVEN IF .job.o ISN'T FOUND
    if t_tak > t_lim:
        stat = 11
        err = 'time'
        ext = '_timeExdd'

    return err, ext, stat

### LOG FILE MANIPULATION

### FIND END STATUS GAUSSIAN
def g09_log(path, File, spec):
    import os, re
    from general  import eof
    err  = False
    ext  = False
    stat = False

    # CHECK FOR RAIJIN WALLTIME EXCEEDED
    err, ext, stat = rjn_wall(path, File, err, ext, stat)
    # IF NOT WALLTIME EXCEEDED
    if not ext:
        # LINES AT END OF FILE
        lines = eof(path, File, 0.3)

        for line in lines:
            if 'Normal termination' in line:
                stat = 7
                ext = '_eGeom'
                break
            # COMMON ERRORS
            if "Erroneous write" in line:
                stat = 13
                err = 'mem'
                ext = '_diskError'
                break
            elif "link 9999" in line:
                stat = 14
                err = 'conv'
                ext = '_convError'
                break
            elif "NtrErr" in line:
                stat = 13
                err = 'mem'
                ext = '_diskError'
                break
            elif "Convergence fail" in line:
                stat = 14
                err = 'conv'
                ext = '_convError'
                break
            elif "NtrErr Called from FileIO" in line:
                stat = 14
                err = 'conv'
                ext = '_convError'
                break
            elif "galloc" in line or "GetChg" in line:
                stat = 10
                err = 'mem'
                ext = '_memError'
                break
            elif "Out-of-memory" in line:
                stat = 10
                err = 'mem'
                ext = '_memError'
                break
        if not ext:
            stat = 12
            err = 'unk'
            ext = '_unknown'

    return err, ext, stat



### FIND END STATUS GAMESS
def gms_log(path, File, spec):
    import os
    from general  import eof
    from pprint   import stat_print
    err  = False
    ext  = False
    stat = False

    # CHECK FOR RAIJIN WALLTIME EXCEEDED
    err, ext, stat = rjn_wall(path, File, err, ext, stat)

    # IF NOT WALLTIME EXCEEDED
    if not ext:
        # LINES AT END OF FILE
        lines = eof(path, File, 0.2)
        for line in lines:
            if "CHECK YOUR INPUT CHARGE AND MULT" in line:
                stat = 8
                err  = 'inp'
                ext  = '_inpError'
                break
            elif "ERROR READING VARIABLE IDUM" in line:
                stat = 9
                err  = 'inp'
                ext  = '_inpError'
                break
            elif "FAILURE TO LOCATE STATIONARY" in line:
                stat = 4
                err  = 'max'
                ext  = '_maxIters'
                break
            elif "DDI Process" in line:
                stat = 10
                err  = 'mem'
                ext  = '_memError'
                break
            elif "CORRUPTION OF THE HESSIAN" in line:
                stat = 17
                err  = 'hes'
                ext  = '_hesError'
                break
            elif "ION OF GAMESS TERMINATED NORMA" in line:
                    stat = 7
                    ext  = '_eGeom'
                    break
        if not ext:
            stat = 10
            err  = 'unk'
            ext  = '_unknown'

    return err, ext, stat


### FIND END STATUS GAMESS
def psi_log(path, File, spec):
    import os
    from general  import eof
    err  = False
    ext  = False
    stat = False

    # CHECK FOR RAIJIN WALLTIME EXCEEDED
    err, ext, stat = rjn_wall(path, File, err, ext, stat)

    if not ext:
        # LINES AT END OF FILE
        lines = eof(path, File, 0.1)

        #for line in lines:

        if '4 exiting successfully' in lines[len(lines)-1]:
            stat = 7
            ext = '_eGeom'
            #break
            # COMMON ERRORS
        if not ext:
            stat = 10
            err = 'unk'
            ext = '_unknown'

    return err, ext, stat

### SORT LOG FILES AND MAKE XYZ
def sort(path, File, soft):
    import os, re
    from shutil   import copyfile
    from general  import software
    from general  import gms_check_spec
    from general  import g09_check_spec
    from general  import psi_check_spec
    from pprint   import stat_print
    from write    import write_xyz


    if soft:
        # CHECK IF SPEC AND CHECK IF LOG TERMINA
        if   soft == 'gms':
            spec           = gms_check_spec(path, File)
            err, ext, stat = gms_log(path, File, spec)
        elif soft == 'g09':
            spec           = g09_check_spec(path, File)
            err, ext, stat = g09_log(path, File, spec)
        elif soft == 'psi':
            spec           = psi_check_spec(path, File)
            err, ext, stat = psi_log(path, File, spec)

        # NAME WITH EXTENSION
        name = File.replace('.log', ext).replace('.out', ext)
        # PRINT MESSAGE
        if spec and not err:
            stat_print(path, File, 2)
        if not spec:
            # SUCCESSFUL JOB
            if not err:
                stat_print(path, File, stat)
                # GET GEOMETRY
                id = "spec/"
                if soft == 'gms':
                    geom = gms_geom(path, File, True)
                elif soft == 'g09':
                    geom = g09_geom(path, File, True)
                elif soft == 'psi':
                    geom = psi_geom(path, File, True)

                if not os.path.isdir(path + id):
                    os.makedirs(path + id)
                #copyfile(path + File, path + id +'c-'+ File)
                # WRITE XYZ
                write_xyz(path + id, name, geom)
            # FOR ALL UNFINISHED
            else:
                # GET GEOMETRY
                if soft == 'gms':
                    geom = gms_geom(path, File, False)
                elif soft == 'g09':
                    geom = g09_geom(path, File, False)
                elif soft == 'psi':
                    geom = psi_geom(path, File, False)

                # IF NO STEPS IN OPTIMISATION
                if len(geom) == 0:
                    stat_print(path, File, 6)
                    name = File.replace('.out','').replace('.log','')
                    nam1 = name + '.xyz'
                    nam2 = name + '_'
                    nam3 = name + '_Fail.xyz'
                    # REGULAR XYZ NAME
                    try:
                        copyfile(path + nam1, path + "rerun/" + nam3)
                    except:
                        # IF XYZ NAME WITH EXTENTION
                        for fILE in os.listdir(path):
                            if nam2 in fILE:
                                if not os.path.exists(path + 'rerun'):
                                    os.mkdir(path + 'rerun')
                                try:
                                    copyfile(path + fILE, path + "rerun/" + nam3)
                                except:
                                    print(File + ": could not pull geom, zero steps")

                # RETURNED GEOMETRY
                else:
                    stat_print(path, File, stat)
                    if err in ['conv', 'hes']:
                        id = 'notConv/'
                    elif err in ['inp', 'max', 'mem', 'time']:
                        id = 'rerun/'
                    elif err in ['unk']:
                        id = 'unknown/'
                    if not os.path.isdir(path + id):
                        os.makedirs(path + id)
                    copyfile(path + File, path + id +'f-'+ File)
                    write_xyz(path + id, name, geom)

        # IF FAILED SPEC
        elif spec and err:

            xyz  = File.replace('.out', '.xyz') \
            .replace('.log', '.xyz')
            xyz_ = File.replace('.out', '_.+xyz') \
            .replace('.log', '_.+xyz')

            found = False
            for file in os.listdir(path):
                if xyz == file or re.search(xyz_, file):
                    if not os.path.exists(path + "rerun"):
                        os.mkdir(path + "rerun")
                    newExt = file.split('_')[0] + ext + '.xyz'
                    copyfile(path + file, path + "rerun/" + newExt)
                    stat_print(path, File, 16)
                    found = True
            if not found:
                stat_print(path, File, 15)



### GAMESS GET GEOM
def gms_geom(path, File, opt):
    import re, sys

    pattern = '[A-Za-z]{1,2}\s*[0-9]*\.[0-9]*\s*-?[0-9]*\.[0-9]*\s*-?[0-9]*\.'
    geom  = []
    coord = []
    found = False
    find  = False
    # IF UNFINISHED PULL ALL GEOMS
    # SECOND LAST GEOM SAVED IN coords
    if not opt:
        with open(path + File, 'r+') as f:
            try:
                for line in f:
                    if "COORDINATES" in line:
                        find = True
                    if find:
                        if "CPU" in line or line == '\n':
                            find = False
                            if coord:
                                geom = coord
                                coord = []
                        elif re.search(pattern, line):
                            coord.append(line)
                    line_corrupt = line
            except:
                print("gms_geom has passed a corrupt line in file ", File)

    else:
        with open(path + File, 'r') as f:
            try:
                for line in f:
                    if re.search("EQUILIBRIUM GEOMETRY", line):
                        found = True
                    elif re.search("ALWAYS THE LAST POINT COMPUTED!", line):
                        find = True
                    elif line is "\n":
                        found = False
                        find = False
                    if found:
                        geom.append(line)
                    if find:
                        geom.append(line)
            except:
                print("gms_geom has passed a corrupt line in file ", File)
        # remove header lines
        geom = geom[4:]

    for i in range(len(geom)):
        geom[i] = geom[i].split()

    f.close()
    return geom


### GAUSSIAN GET GEOM
def g09_geom(path, File, opt):
    import os,re
    from general  import eof
    from chemData import pTable

    ginc   = False
    vals   = False
    end    = False
    coords = []
    geom   = []
    hold   = []
    pattern = "-?[0-9]*\.[0-9]*\s*"

    lines = eof(path, File, 0.4)
    # GRAB GINC VALUES
    if opt:
        for line in lines:
            if re.search("GINC", line):
                # FINDS LAST CASE OF 'GINC'
                coords = []
                ginc = True
            if ginc:
                coords.append(line)
        j = ''
        # FOR ALL LINES
        for i in coords:
            # SUM ALL LINES TOGETHER AS CONTINUOUR STRING
            j = j + i
        j = j.replace('\n', '')
        j = j.replace(' ', '')
        j = j.split('\\')

        # AND OPT GEOM
        geom = []
        pat = ",-?[0-9]*\.[0-9]*"
        for line in j:
            if re.search("^[A-Z]{1,2},?[a-z]?[0-9]*" + \
            pat + pat + pat + "$", line):
                line = line.split(',')
                # SOMETIMES AN EXTRA COLUMN RETRIEVED?
                geom.append([line[0], line[len(line) - 3],\
                line[len(line) - 2], line[len(line) - 1]])

    # FIND SECOND LAST STEP; LAST MAY NOT BE FINISHED
    else:
        with open(path + File, 'r+') as f:
            try:
                for line in f:
                    if vals:
                        if end:
                            if re.search("------------*", line):
                                vals = False
                        if re.search(pattern + pattern + pattern, line):
                            hold.append(line)
                            end = True
                    if "Coordinates" in line:
                        vals = True
                        end = False
                        coords = hold
                        hold = []
            except:
                print("Corrupt line passed in file ", File)

            hold = []
            for i in coords:
                i = i.split()
                hold.append([i[1], i[3], i[4], i[5]])
            for i in hold:
                for el, data in pTable.items():
                    if data[0] == int(i[0]):
                        geom.append([el, i[1], i[2], i[3]])
                        break

    return geom



### PSI4 GET GEOM
def psi_geom(path, File, opt):
    import re

    pattern = "-?[0-9]*\.[0-9]*\s*"
    geom = []
    coord = []
    look = False
    found = False

    with open(path + File, 'r+') as f:
        if opt:
            try:
                for line in f:
                    if 'Final optimized geometry and variables' in line:
                        look = True
                    if look:
                        if re.search(pattern + pattern + pattern, line):
                            geom.append(line)
                            found = True
                        elif found:
                            if "\n" == line:
                                found = False
                                look = False
            except:
                print("Corrupt line passed in file ", File)
        else:
            for line in f.readlines():
                if 'Cartesian Geometry (in Angstrom)' in line:
                    found = True
                    geom = coord
                    coord = []
                elif found:
                    if re.search(pattern + pattern + pattern, line):
                        coord.append(line)
                    else:
                        found = False

        for i in range(len(geom)):
            geom[i] = geom[i].split()

    return geom
