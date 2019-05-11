### EDIT template.job FOR JOB FILE
def job_replace(name, jobTemp):
    # MATCHES ANY AMOUNT OF WHITE SPACES FOLLOWED BY .inp
    # RETURNS WHATS IN BRACKETS
    import re

    match_b4_inp = re.compile('([^\s=]*)\.inp')
    match_b4_chk = re.compile('([^\s=]*)\.chk')
    match_b4_log = re.compile('([^\s=]*)\.log')
    match_b4_out = re.compile('([^\s=]*)\.out')
    match_b4_err = re.compile('([^\s=]*)\.err')

    match_b4_inp  = match_b4_inp.findall(jobTemp)  # TURN OBJECT TO STRING
    match_b4_chk  = match_b4_chk.findall(jobTemp)  # TURN OBJECT TO STRING
    match_b4_log  = match_b4_log.findall(jobTemp)  # TURN OBJECT TO STRING
    match_b4_out  = match_b4_out.findall(jobTemp)  # TURN OBJECT TO STRING
    match_b4_err  = match_b4_err.findall(jobTemp)  # TURN OBJECT TO STRING

    swapDict = {
            '.inp' : match_b4_inp,
            '.chk' : match_b4_chk,
            '.log' : match_b4_log,
            '.out' : match_b4_out,
            '.err' : match_b4_err,
            }

    for match, matches in swapDict.items():
        for this in matches:
            jobTemp = jobTemp.replace(this + match, name + match)

    return jobTemp




### NUMBER OF TEMPLATE FILES IN FOLDER
def numTemp(path):
    import os
    # NUMBER OF TEMPLATE SO DON'T OVERWRITE
    temp = 0
    for File in os.listdir(path):
        if File.endswith('template'):
            temp += 1
    return temp


### ADD COORDS TO TEMPLATE
def xyzTemp(path, template, coords):
    import re
    input    = []
    xyzIn    = False
    pattern  = '[A-Za-z]{1,2}\s*-?[0-9]*\.[0-9]*\s*-?[0-9]*\.[0-9]*'
    template = open(path + template, 'r+')
    for line in template:
        if 'xyz_data' in line:
            for i in coords:
                input.append(i[:])
                xyzIn = True
        elif re.search(pattern, line):
            if not xyzIn:
                for i in coords:
                    input.append(i[:])
                xyzIn = True
        else:
            input.append(line)
    return input


### NEW DIR FOR JOB // PSI4 AND GAMESS
def newDir(path, File, template):
    import os
    from shutil import copyfile

    temp = numTemp(path)

    # INCASE I APPENDED TO END OF FILE
    trFile = File.split('_')[0].replace('.xyz','')

    # MAKE DIRECTORY FOR NEW JOB/INP

    if temp > 1:
        name = trFile.replace('.xyz','') + '-' +\
        template.replace('.template', '')
        if not os.path.isdir(path + name):
            os.mkdir(path + name)
        npath = path + name + '/'
        print(path+File)
        print(npath+trFile)
        copyfile(path + File, npath + trFile + '.xyz')

    else:
        name = trFile.replace('.xyz','')
        if not os.path.isdir(path + name):
            os.mkdir(path + name)
        npath = path + name + '/'
        copyfile(path + File, npath + trFile + '.xyz')

    return npath


### FOR ALL GAUSSIAN AS JOB IN INP
def g09(path, File, template, sysData):

    # CREATES JOB FILE FROM TEMPLATE AND .xyz

    import re
    from write   import write_job

    name = File.replace('.xyz','').split('_')[0]

    # FOR MORE THAN ONE TEMPLATE IN DIR
    temp = numTemp(path)
    if temp > 1:
        name = name + '-' + template.replace('.template', '')\
        .replace('template', '')

    # UNPACK LIST
    fragList, atmList, totChrg, totMult = sysData

    # CREATE xyzData
    xyzData = []
    for frag in fragList:
        for atm in atmList:
            if atm['id'] in frag['ids']:
                xyzData.append([atm['sym'], atm['nu'], atm["x"], atm["y"], atm["z"]])

    # PUT XYZ COORDS IN TEMPLATE
    input = xyzTemp(path, template, xyzData)

    # ADD COORDS IN TEMPLATE
    for i in range(len(input)):
        if type(input[i]) != list:

            # CHANGE NAMES BEFORE LOG ETC.
            input[i] = job_replace(name, input[i])

            # CHANGE CHARGE AND MULT
            if re.search('^\s*-?[0-9]\s*-?[0-9]\s*$', input[i]):
                # DON'T CHANGE IF NOT KNOWN
                if totChrg == '?':
                    print("Cannot determine chrg/mult, using template values")
                # IF CHRG = MULT COULD BE TRICKY
                else:
                    input[i] = str(totChrg) + ' ' + str(totMult) + '\n'

    write_job(path, name, input)


### GAMESS - NOT FMO - ONE NODE
def gms(path, File, template, sysData, jobTemp):

    import re
    from supercomp  import host
    from templates  import gms_rjnJob
    from templates  import gms_mgsJob
    from templates  import gms_gaiJob
    from templates  import gms_masJob
    from templates  import gms_stmJob
    from write      import write_gmsInp
    from write      import write_job

    name = File.replace('.xyz','').split('_')[0]

    # MAKE NEW DIR AND NEW PATH
    npath  = newDir(path, File, template)

    # UNPACK sysData
    fragList, atmList, totChrg, totMult = sysData

    # CREATE xyzData
    xyzData = []
    for frag in fragList:
        for atm in atmList:
            if atm['id'] in frag['ids']:
                xyzData.append([atm['sym'], atm['nu'], atm["x"], atm["y"], atm["z"]])

    # GET TEMPLATE LINES WITH COORDS
    input = xyzTemp(path, template, xyzData)

    # CHARGE AND MULT
    for ind in range(len(input)):
        if 'ICHARG' in input[ind]:
            if totChrg == '?':
                print("Cannot determine chrg/mult, using template values")
            else:
                spl_line = re.split('=| ', input[ind])
                for val, bit in enumerate(spl_line):
                    if bit == 'ICHARG':
                        oldChrg = spl_line[val+1]
                input[ind] = input[ind].replace('ICHARG=' + \
                oldChrg, 'ICHARG=' + str(totChrg))

        if totMult != 0:
            if 'CONTRL' in input[ind]:
                if totChrg == '?':
                    print("Cannot determine chrg/mult, using template values")
                elif not 'MULT' in input[ind]:
                    input[ind] = input[ind].\
                    replace(' RUN',' MULT=' + str(totMult) + ' RUN')


        # MEMORY USED IN INPUT
        if 'MWORDS' in input[ind]:
            spl_line = re.split('=| ', input[ind])
            for val, bit in enumerate(spl_line):
                if bit == 'MWORDS' in input[ind]:
                    memory = spl_line[val+1]

        # MEMORY USED IN INPUT
        ddi = False
        if 'MEMDDI' in input[ind]:
            spl_line = re.split('=| ', input[ind])
            for val, bit in enumerate(spl_line):
                if bit == 'MEMDDI' in input[ind]:
                    ddi = spl_line[val+1]

    # WRITE INP
    write_gmsInp(npath, name, input)

    # WRITE JOB
    lines = False
    if jobTemp:
        lines = job_replace(name, jobTemp)
    else:
        hw = host()
        if hw == 'rjn':
            lines = gms_rjnJob(name)
        elif hw == 'mgs':
            lines = gms_mgsJob(name)
        elif hw == 'gai':
            lines = gms_gaiJob(name)
        elif hw == 'mas':
            lines = gms_masJob(name)
        elif hw == 'stm':
            lines = gms_stmJob(name)

    if lines:
        write_job(npath, name, lines)


### PSI4 - ONE NODE
def psi(path, File, template, sysData, jobTemp):

    import re
    from supercomp  import host
    from templates  import psi_rjnJob
    from templates  import psi_gaiJob
    from write      import write_inp
    from write      import write_job

    name = File.replace('.xyz','').split('_')[0]

    # MAKE NEW DIR AND NEW PATH
    npath = newDir(path, File, template)

    # UNPACK sysData
    fragList, atmList, totChrg, totMult = sysData

    # CREATE xyzData
    xyzData = []
    for frag in fragList:
        for atm in atmList:
            if atm['id'] in frag['ids']:
                xyzData.append([atm['sym'], atm['nu'], atm["x"], atm["y"], atm["z"]])

    # PUT XYZ IN TEMPLATE
    input = xyzTemp(path, template, xyzData)

    for i in range(len(input)):
        if type(input[i]) != list:
            # CHANGE CHRG AND MULT
            if re.search('^\s*-?[0-9]\s*-?[0-9]\s*$', input[i]):
                if totChrg == '?':
                    print("Cannot determine chrg/mult, using template values")
                # IF CHRG = MULT COULD BE TRICKY
                else:
                    input[i] = ' ' + str(totChrg) + ' ' + str(totMult) + '\n'

    # WRITE INP
    write_inp(npath, name, input)

    # MEMORY
    for line in input:
        if 'memory' in line:
            line = line.split()
            memory  = int(line[1])

    # WRITE JOB
    lines = False
    if jobTemp:
        lines = job_replace(name, jobTemp)
    else:
        hw = host()
        if hw == 'rjn':
            lines = psi_rjnJob(name)
        elif hw == 'gai':
            lines = psi_gaiJob(name)

    if lines:
        write_job(npath, name, lines)


### FMO - MANY NODES ON RAIJIN AND MAGNUS \\
# ONE NODE ON GAIA - CAN CHANGE TO OLD VER. GAMESS
def fmo(path, File, template, sysData, jobTemp):

    import os, re
    from supercomp  import host
    from chemData   import pTable
    from templates  import fmo_rjnJob
    from templates  import fmo_mgsJob
    from templates  import fmo_stmJob
    from templates  import fmo_gaiJob
    from templates  import gms_rjnJob
    from templates  import gms_mgsJob
    from templates  import gms_masJob
    from templates  import gms_gaiJob
    from templates  import gms_stmJob
    from tempInp    import fmo_ions
    from write      import write_xyz
    from write      import write_gmsInp
    from write      import write_job

    # NAME FOR WRITING FILE, DIRS
    ions = False
    name = File.replace('.xyz','').split('_')[0]

    # MAKE NEW DIR AND NEW PATH
    npath = newDir(path, File, template)

    # UNPACK sysData
    mp2 = False
    fragList, atmList, totChrg, totMult = sysData

    # NUMBER OF FRAGS
    nfrags = len(fragList)

    # CREATE xyzData
    xyzData = []
    for frag in fragList:
        for atm in atmList:
            if atm['id'] in frag['ids']:
                xyzData.append([atm['sym'], atm['nu'], atm["x"], atm["y"], atm["z"]])

    # TEMPLATE LINES
    input = xyzTemp(path, template, xyzData)
    #print(input)
    fmo_input = []
    # ONE LINE REPLACEMENTS - NO MULT YET ***
    # IF RUNTYP IS ENERGY MAKE ION JOBS

    for ind in range(len(input)):
        if 'NGROUP' in input[ind]:
            spl_line = re.split('=| ', input[ind])
            for val, bit in enumerate(spl_line):
                if bit == 'NGROUP':
                    in_grp = spl_line[val+1]
                    if in_grp != str(nfrags):
                        #print('Changing NGROUP to', nfrags)
                        input[ind] = input[ind].\
                        replace('NGROUP=' + in_grp, 'NGROUP=' + str(nfrags))

        # CHECK NFRAG = NO. OF FOUND FRAGMENTS
        if 'NFRAG' in input[ind]:
            spl_line = re.split('=| ', input[ind])
            for val, bit in enumerate(spl_line):
                if bit == 'NFRAG':
                    in_nfrags = spl_line[val+1]
                    if in_nfrags != str(nfrags):
                        #print('Changing NFRAG  to', nfrags)
                        input[ind] = input[ind].\
                        replace('NFRAG=' + in_nfrags, 'NFRAG=' + str(nfrags))

        # LIST OF CHARGES FOR FRAGMENTS
        if 'ICHARG' in input[ind]:
            spl_line = re.split('=| ', input[ind])
            for val, bit in enumerate(spl_line):
                if 'ICHARG' in bit:
                    in_chrg = spl_line[val+1]
                    chrgs = []
                    for frag in fragList:
                        chrgs.append(frag['chrg'])
                    input[ind] = input[ind].replace('ICHARG(1)=' + in_chrg, \
                            'ICHARG(1)=' + ','.join(str(p) for p in chrgs) + '\n')

        # MULT
        if 'MULT' in input[ind]:
            spl_line = re.split('=', input[ind])
            for val, bit in enumerate(spl_line):
                if 'MULT' in bit:
                    mults = []
                    for frag in fragList:
                        mults.append(frag['mult'])
                    in_chrg = spl_line[val+1]
                    input[ind] = input[ind].replace('MULT(1)=' + in_chrg,\
                    'MULT(1)=' + ','.join(str(p) for p in mults) + '\n')


        # CHECK IF SPEC FOR ION CALCS
        if 'RUNTYP' in input[ind]:
            spl_line = re.split('=| ', input[ind])
            for val, bit in enumerate(spl_line):
                if 'RUNTYP' in bit:
                    if spl_line[val+1] == 'ENERGY':
                        ions = True


        # MEMORY USED IN INPUT USED FOR JOB MEMORY
        if 'MWORDS' in input[ind]:
            spl_line = re.split('=| ', input[ind])
            for val, bit in enumerate(spl_line):
                if bit == 'MWORDS' in input[ind]:
                    memory = spl_line[val+1]

        # MEMORY USED IN INPUT FOR JOB MEMORY
        ddi = False
        if 'MEMDDI' in input[ind]:
            spl_line = re.split('=| ', input[ind])
            for val, bit in enumerate(spl_line):
                if bit == 'MEMDDI' in input[ind]:
                    ddi = spl_line[val+1]

        # FOR FMO_IONS
        if '$MP2' in input[ind]:
            mp2 = input[ind]

        if "GBASIS" in input[ind]:
            spl_line = re.split('=| ', input[ind])
            for val, bit in enumerate(spl_line):
                if bit == 'GBASIS' in input[ind]:
                    bset = spl_line[val+1]


    # REMOVE LINES FROM INPUT WITH NEW LIST
    # FOR MANY LINE CHANGES - COORDS, INDAT, ATM LIST
    atmUniq = []
    numUniq = []
    seenA   = False
    for line in input:
        if type(line) != list:
            # INDAT MAY BE DIFF NUMBER OF LINES TO NEW INDAT
            if 'INDAT' in line:
                fmo_input.append('    INDAT(1)=0,1,-' + str(len(fragList[0]['ids'])) + ',\n')
                # REMEMBER WHERE LAST FRAG FINISHED
                n = len(fragList[0]['ids']) + 1
                for frag in fragList:
                    if not frag is fragList[0]:
                        fmo_input.append(' '*13 + '0,' + str(n) + \
                                ',-' + str(n + len(frag['ids']) - 1) + ',\n')
                        n += len(frag['ids'])
                fmo_input.append(' '*13 + '0\n')

            # SO NOT PASSED TO ELSE // EXTRA LINES TO DETERMINE FRAGMENT
            elif re.search('^\s*0,[0-9]{1,3},-[0-9]{1,3},\s*$', line) or \
                      re.search('^\s*0\s*$', line):
                pass

            # ATOM LIST MAY BE DIFF NUMBER OF LINES TO NEW ATOM LIST
            elif re.search('^\s*[A-Za-z]*\s*[0-9]*\.0*$', line):
                if not seenA:
                    for i in xyzData:
                        atmUniq.append(i[0])
                        numUniq.append(i[1])
                    atmUniq = list(set(atmUniq))
                    for i in range(len(atmUniq)):
                        for sym, data in pTable.items():
                            if sym == atmUniq[i]:
                                fmo_input.append(' ' + str(atmUniq[i]) + ' ' + \
                                str(data[0]) + '\n')
                    seenA = True

            # EVERY OTHER LINE AS IS
            else:
                fmo_input.append(line)
        else:
            fmo_input.append(line)

    # HARDWARE FOR WRITING
    hw = host()

    # XYZ OF IONS ------------------------------------
    if ions:
        ncat = 0
        nani = 0
        nnrt = 0
        nunk = 0
        # FOR EACH FRAGMENT
        for frag in fragList:
            ifrag = []
            for ID in frag['ids']:
                atm = atmList[ID]
                ifrag.append([atm['sym'], atm['nu'], atm["x"], atm["y"], atm["z"]])

            # IN CASE QUESTION MARK
            try:
                if frag['chrg'] < 0:
                    ion = 'anion' + str(nani)
                    nani += 1
                elif frag['chrg'] > 0:
                    ion = 'cation' + str(ncat)
                    ncat += 1
                else:
                    ion = 'neutral' + str(nnrt)
                    nnrt += 1
            except:
                if frag['chrg'] == '?':
                    ion = 'unknown' + str(nunk)
                    nunk += 1

            # MAKE FOLDER AND XYZ
            if not os.path.isdir(npath + name + '-'+ ion):
                os.mkdir(npath + name + '-'+ ion)
            write_xyz(npath + name + '-'+ ion + '/', name + '-'+ ion, ifrag)

            # INPUT AND OUTPUT FOR JOB
            input = fmo_ions(str(frag['chrg']), ifrag, bset, mp2)
            write_gmsInp(npath + name + '-'+ ion + '/', name + '-'+ ion, input)

            # WRITE JOB
            lines = False

            if jobTemp:
                # lines = job_replace(name, jobTemp)
                lines = job_replace(name + '-' + ion, jobTemp)
            else:
                if hw == 'rjn':
                    lines = gms_rjnJob(name + '-'+ ion)
                elif hw == 'mgs':
                    lines = gms_mgsJob(name + '-'+ ion)
                elif hw == 'gai':
                    lines = gms_gaiJob(name + '-'+ ion)
                elif hw == 'mas':
                    lines = gms_masJob(name + '-'+ ion)
                elif hw == 'stm':
                    lines = gms_stmJob(name + '-'+ ion)

            if lines:
                write_job(npath + name + '-'+ ion + '/', name + '-'+ ion, lines)

    # -------------------------------------------------

    # WRITE INP
    write_gmsInp(npath, name, fmo_input)

    # WRITE JOB
    lines = False

    if jobTemp:
        lines = job_replace(name, jobTemp)
    else:
        if hw == 'rjn':
            lines = fmo_rjnJob(name, nfrags, memory, ddi)
        elif hw == 'mgs':
            lines = fmo_mgsJob(name, nfrags, memory, ddi)
        elif hw == 'stm':
            lines = fmo_stmJob(name, nfrags, memory, ddi)
        elif hw == 'gai':
            lines = fmo_gaiJob(name)#, nfrags, memory, ddi)
        elif hw == 'mas':
            lines = gms_masJob(name)

    if lines:
        write_job(npath, name, lines)



### PSI4 - ONE NODE
def orc(path, File, template, sysData, jobTemp):

    import re
    from supercomp  import host
    from templates  import orc_rjnJob
    from write      import write_inp
    from write      import write_job

    name = File.replace('.xyz','').split('_')[0]

    # MAKE NEW DIR AND NEW PATH
    npath  = newDir(path, File, template)

    # UNPACK sysData
    fragList, atmList, totChrg, totMult = sysData

    # CREATE xyzData
    xyzData = []
    for frag in fragList:
        for atm in atmList:
            if atm['id'] in frag['ids']:
                xyzData.append([atm['sym'], atm['nu'], atm["x"], atm["y"], atm["z"]])

    # PUT XYZ IN TEMPLATE
    input = xyzTemp(path, template, xyzData)

    for i in range(len(input)):
        if type(input[i]) != list:
            # CHANGE CHRG AND MULT
            if re.search('^\*xyzfile\s*-?[0-9]\s*-?[0-9]\s*', input[i]):
                if totChrg == '?':
                    print("Cannot determine chrg/mult, using template values")
                # IF CHRG = MULT COULD BE TRICKY
                else:
                    line = input[i].split()
                    if '.xyz' in line[-1]:
                        input[i] = '*xyzfile ' + str(totChrg) + ' ' + str(totMult) + ' '+line[-1]

            if re.search('.xyz', input[i]):
                line     = input[i].strip()
                line     = line.rsplit(' ', 1)[0]
                input[i] = line+' '+name+'.xyz\n'

    # WRITE INP
    write_inp(npath, name, input)

    # WRITE JOB
    lines = False

    if jobTemp:
        lines = job_replace(name, jobTemp)
    else:
        hw = host()
        if hw == 'rjn':
            lines = orc_rjnJob(name)

    if lines:
        write_job(npath, name, lines)
