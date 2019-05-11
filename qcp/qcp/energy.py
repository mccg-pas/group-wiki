def energy_gms(path, File, energy):
    from logFile import gms_log
    from general import gms_check_spec
    from general import eof

    spec            = gms_check_spec(path, File)
    err, ext, stat  = gms_log(path, File, spec)

    scs     = False
    HF      = ''
    ZP      = ''
    MP2     = ''
    sysDict = {}

    if spec:
        typ = 'spe'
    else:
        typ = 'opt'
    if not err:
        # CHECK IF FMO
        fmo = False
        with open(path + File) as f:
            for line in f:
                if 'FMO' in line:
                    fmo = True
                elif 'SCSOPO' in line:
                    scs = True
                elif 'THE POINT GROUP OF THE M' in line:
                    break

        lines = eof(path, File, 0.2)
        if scs:
            for line in lines:
                if "E corr SCS" in line:
                    MP2 = line.split()
                    MP2 = MP2[len(MP2) - 1]
                elif 'Euncorr HF' in line:
                    HF  = line.split()
                    HF  = HF[len(HF) - 1]
        if fmo and HF == '':
            for line in lines:
                if "Ecorr" in line:
                    MP2 = line.split()
                    MP2 = MP2[len(MP2) - 1]
                elif 'Euncorr' in line:
                    HF  = line.split()
                    HF  = HF[len(HF) - 1]

        if not fmo:
            for line in lines:
                if "SCS-MP2" in line:
                    MP2 = line.split()
                    MP2 = MP2[1]
                    # E(MP2)=       -76.2919350192  ACTUALLY, THIS IS THE SCS-MP2 ENERGY
                elif 'E(0)=' in line:
                    HF  = line.split()
                    HF  = HF[len(HF) - 1]

    # FINDING ZP NOT INCLUDED
    # CREATE DICTIONARY OF FILE
    sysDict["Path"] = path
    sysDict["File"] = File
    sysDict["Type"] = typ
    sysDict["HF"  ] = HF
    sysDict["ZP"  ] = ZP
    sysDict["MP2" ] = MP2

    energy.append(sysDict)
    return energy




def energy_g09(path, File, energy):
    import re
    from logFile import g09_log
    from general import g09_check_spec
    from general import eof

    HF      = ''
    ZP      = ''
    MP2     = ''
    sysDict = {}

    spec = g09_check_spec(path, File)
    err, ext, stat  = g09_log(path, File, spec)

    if spec:
        typ = 'spe'
    else:
        typ = 'opt'

    coords = []
    if not err:
        lines = eof(path, File, 0.1)
        ginc = False
        for line in lines:
            if re.search("GINC", line):
                # FINDS LAST CASE OF 'GINC'
                ginc = True
            if ginc:
                coords.append(line)

        if not coords:
            lines = eof(path, File, 0.4)
            for line in lines:
                if re.search("GINC", line):
                    # FINDS LAST CASE OF 'GINC'
                    ginc = True
                if ginc:
                    coords.append(line)


        j = ''
        # FOR ALL LINES
        for i in coords:
        # SUM ALL LINES TOGETHER AS CONTINUOUS STRING
            j = j + i
        j = j.replace('\n', '')
        j = j.replace(' ','')
        j = j.split('\\')

        # FIND HF AND ZPVE
        for line in j:
            if 'HF=' in line:
                HF = line.split('=')
                HF = HF[1]
                pass
            if 'ZeroPoint' in line:
                ZP = line.split('=')
                ZP = line.split('=')
                ZP = ZP[1]
            if 'MP2' in line:
                MP2 = line.split('=')
                MP2 = MP2[1]

    # CREATE DICTIONARY OF FILE
    sysDict["Path"] = path
    sysDict["File"] = File
    sysDict["Type"] = typ
    sysDict["HF"  ] = HF
    sysDict["ZP"  ] = ZP
    sysDict["MP2" ] = MP2

    energy.append(sysDict)

    return energy



def energy_psi(path, File, energy):
    from logFile import psi_log
    from general import psi_check_spec
    from general import eof

    HF      = ''
    ZP      = ''
    MP2     = ''
    sysDict = {}

    spec = psi_check_spec(path, File)
    err, ext, stat  = psi_log(path, File, spec)

    if spec:
        typ = 'spe'
    else:
        typ = 'opt'

    if not err:
        lines = eof(path, File, 0.1)

        for line in lines:
            if "Total Energy              =" in line:
                MP2 = line.split()
                MP2 = MP2[len(MP2) - 2]
            elif 'Reference Energy' in line:
                HF  = line.split()
                HF  = HF[len(HF) - 2]

    # FINDING ZP NOT INCLUDED

    # CREATE DICTIONARY OF FILE
    sysDict["Path"] = path
    sysDict["File"] = File
    sysDict["Type"] = typ
    sysDict["HF"  ] = HF
    sysDict["ZP"  ] = ZP
    sysDict["MP2" ] = MP2

    energy.append(sysDict)

    return energy
