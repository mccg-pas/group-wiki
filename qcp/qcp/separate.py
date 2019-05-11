def separate_mols(path, File, sysData):

    from write import write_xyz

    # NAME FOR WRITING FILE, DIRS
    name = File.replace('.xyz','').split('_')[0]

    # UNPACK sysData
    fragList, atmList, totChrg, totMult = sysData

    ncat, nani, nntr, nunk = 0, 0, 0, 0

    # FOR EACH FRAGMENT
    for frag in fragList:
        ifrag = []
        for atm in atmList:
            if atm['id'] in frag['ids']:
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
                ion = 'neutral' + str(nntr)
                nntr += 1
        except:
            if frag['chrg'] == '?':
                ion = 'unknown' + str(nunk)
                nunk += 1

        # WRITE XYZ
        write_xyz(path, name + '-' + ion, ifrag)
