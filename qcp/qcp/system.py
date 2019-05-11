### GET DATA AND PASS TO sep_mol
# ONLY WANT TO DO ONCE PER XYZ
def systemData(path, File, check):
    from general import xyzPull

    # CUTOFF BETWEEN FRAGS
    distca = 1.7

    # PULL COORDS FROM XYZ
    coords = xyzPull(path, File)

    # CHECK CORRECT FRAGMENTS IF FMO
    if check:

        # UNLESS CHANGED
        comp   = 'nn'

        # WILL FIRST USE VDW ALGORITHM
        atmList, fragList, totChrg, totMult = \
            sep_mol(coords, distca, Type='check_vdw')

        # CREATE GROUP BY DIST OR VDW DEPENDING ON USER // HERE BY DIST
        for i in atmList:
            i["grp"] = i["grp_vdw"]
            #print(i)

        # IF HAS NOT FOUND A TOTAL MULTIPLICITY UNDEFINED MOLECULES // ASK USER
        if totMult == '?':
            while comp != 'n' and comp != 'y':
                comp = input('Does your cluster have '+ str(len(fragList)) + ' frags? (y/n) ')

            # IF THE CLUSTER NOT CORRECTLY IDENTIFIED GO INTO LOOP ASKING FOR DISTCA
            while comp == 'n':

                distca = float(input("Covalent bond cutoff distance: "))
                atmList, fragList, totChrg, totMult = \
                    sep_mol(coords, distca, Type='check_dist')

                # RENAME TO GROUP
                for i in atmList:
                    i["grp"] = i["grp_dist"]
                    #print(i)

                # IF TOTMULT NOT DEFINED ASK IF CORRECT
                if totMult == '?':
                    comp = input('Does your cluster have '+ str(len(fragList)) +' frags? (y/n) ')
                else:
                    comp = 'y'


    # DOES NOT MATTER WITH OTHER CALC TYPES
    else:
        atmList, fragList, totChrg, totMult = \
            sep_mol(coords, distca, Type='check_vdw')
        for i in atmList:
            i["grp"] = i["grp_vdw"]


    # SORT DICT
    atmList = sorted(atmList, key=lambda k: k['grp'])

    #print(atmList)

    #for i in atmList:
    #    print(i)

    return [fragList, atmList, totChrg, totMult]

### SEPARATE MOLECULES INTO IONS/MOLECULES
# RETURN totChrg, mult, chrgList, frgIndx, xyzData
# frgList["sym"], nu, x, y, z, ifrag, chrg : LIST OF DICTS
def sep_mol(coords, distca, Type):

    import math
    import numpy       as np
    from   pprint      import detec
    from   chemData    import pTable

    atmList = []

    for ID, line in enumerate(coords):
        #print(line)
        atmDict             = {}
        atmDict["id"]       = ID
        atmDict["sym"]      = line[0]
        atmDict["x"]        = float(line[1])
        atmDict["y"]        = float(line[2])
        atmDict["z"]        = float(line[3])
        atmDict["con"]      = []
        atmDict["grp_dist"] = False
        atmDict["grp_vdw"]  = False

        for sym, data in pTable.items():
            if atmDict["sym"]  == sym:
                atmDict["nu"]  = data[0]
                atmDict["vdw"] = data[2]
        atmList.append(atmDict)

    natoms = len(atmList)
    dist   = np.zeros((natoms,natoms))
    # FIND DISTS BETWEEN ALL ATOMS i & j
    group_dist = 0
    group_vdw  = 0
    for val, i in enumerate(atmList):
        con_vwd  = False
        con_dist = False
        # SECOND ATOM < DISTCA
        for vals, j in enumerate(atmList):
            if i != j:
                a = (i["x"]-j["x"])**2 + (i["y"]-j["y"])**2\
                + (i["z"]-j["z"])**2
                dist[val,vals] = math.sqrt(a)

                # IF UNDER DISTCA ---------------------------------------
                if dist[val, vals] < distca:
                    con_dist = True
                    # IF NEITHER I NOR J PART OF A GROUP
                    # ADD THEM TO A NEW GROUP
                    if i["grp_dist"] is False and j["grp_dist"] is False:
                        i["grp_dist"], j["grp_dist"] = group_dist, group_dist
                        group_dist += 1
                    # IF BOTH HAVE BEEN ASSIGNED TO A DIFF GROUP
                    elif not i["grp_dist"] is False and not j["grp_dist"] is False:
                        if i["grp_dist"] != j["grp_dist"]:
                            grp_chng = j["grp_dist"]
                            for k in atmList:
                                if k["grp_dist"] is grp_chng:
                                    k["grp_dist"] = i["grp_dist"]
                    # IF j NOT ASSIGNED
                    elif not i["grp_dist"] is False and j["grp_dist"] is False:
                        j["grp_dist"] = i["grp_dist"]
                    # IF i NOT ASSIGNED
                    elif not j["grp_dist"] is False and i["grp_dist"] is False:
                        i["grp_dist"] = j["grp_dist"]

                # CHECK IF CONNECTED USING VDW DATA -----------------------
                #print(i["vdw"] + j["vdw"])
                if dist[val, vals] < i["vdw"] + j["vdw"]:
                    # ADD TO ATOM LIST
                    if not j["id"] in i["con"]:
                        i["con"].append(j["id"])
                        j["con"].append(i["id"])

                    con_vwd = True
                    # IF NEITHER I NOR J PART OF A GROUP
                    # ADD THEM TO A NEW GROUP
                    if i["grp_vdw"] is False and j["grp_vdw"] is False:
                        i["grp_vdw"], j["grp_vdw"] = group_vdw, group_vdw
                        group_vdw += 1
                    # IF BOTH HAVE BEEN ASSIGNED TO A DIFF GROUP
                    elif not i["grp_vdw"] is False and not j["grp_vdw"] is False:
                        if i["grp_vdw"] != j["grp_vdw"]:
                            grp_chng = j["grp_vdw"]
                            for k in atmList:
                                if k["grp_vdw"] is grp_chng:
                                    k["grp_vdw"] = i["grp_vdw"]
                    # IF j NOT ASSIGNED
                    elif not i["grp_vdw"] is False and j["grp_vdw"] is False:
                        j["grp_vdw"] = i["grp_vdw"]
                    # IF i NOT ASSIGNED
                    elif not j["grp_vdw"] is False and i["grp_vdw"] is False:
                        i["grp_vdw"] = j["grp_vdw"]


        # IF LONER ATOM PUT IN ITS OWN GROUP
        if not con_dist:
            i["grp_dist"] = group_dist
            group_dist += 1
        if not con_vwd:
            i["grp_vdw"] = group_vdw
            group_vdw += 1


    # REORDER GROUPS STARTING FROM 0
    # CREATE fragList ----------------------------------------------------------------


    if Type == 'check_dist':

        print("-"*40)
        print("SYSTEM USING CUTOFF DISTANCE:")
        #
        totChrg  = 0
        totMult  = 1
        #
        nfrags_dist = 0
        fragList = []
        for grp_dist in range(group_dist):
            fragDict_dist = {}
            fragDict_dist['ids'] = []
            fragDict_dist['syms'] = []
            foundnew = False
            for atm in atmList:
                if atm["grp_dist"] == grp_dist:
                    foundnew = True
                    atm["grp_dist"] = nfrags_dist
                    fragDict_dist['syms'].append(atm['sym'])
                    fragDict_dist['ids'].append(atm['id'])

            if foundnew:
                fragDict_dist['grp'] = nfrags_dist
                # FIND CHARGE/MULT
                if isCation(fragDict_dist['syms'], fragDict_dist['ids']):
                    fragDict_dist["chrg"] = 1
                    fragDict_dist["mult"] = 1
                    if totChrg != '?':
                        totChrg += 1

                elif isAnion(fragDict_dist['syms'], fragDict_dist['ids']):
                    fragDict_dist["chrg"] = -1
                    fragDict_dist["mult"] = 1
                    if totChrg != '?':
                        totChrg += -1

                elif isNeutral(fragDict_dist['syms'], fragDict_dist['ids']):
                    fragDict_dist["chrg"] = 0
                    fragDict_dist["mult"] = 1

                elif isRadical(fragDict_dist['syms'], fragDict_dist['ids']):
                    fragDict_dist["chrg"] = 0
                    fragDict_dist["mult"] = 2
                    totMult = 2

                else:
                    # FIND CHEMICAL FORMULA
                    syms = []
                    chemForm = ''
                    for sym in fragDict_dist['syms']:
                        if sym not in syms:
                            numTimes = fragDict_dist['syms'].count(sym)
                            chemForm += sym + str(numTimes)
                            syms.append(sym)
                    detec("unknown", chemForm, " ".join(str(x+1) for x in fragDict_dist['ids']))
                    fragDict_dist["chrg"] = '?'
                    fragDict_dist["mult"] = '?'
                    totChrg = '?'
                    totMult = '?'


                # FOR NEXT FRAGMENT
                fragList.append(fragDict_dist)
                nfrags_dist += 1


    elif Type == 'check_vdw':

        # WON'T USE THESE
        fragList = totChrg = totMult = False

        # CREATE fragList --------------------------------------------------------
        print("-"*40)
        print("SYSTEM USING VDW's RADII:")

        totChrg = 0
        totMult = 1
        #
        nfrags_vdw = 0
        fragList = []
        for grp_vdw in range(group_vdw):
            fragDict_vdw = {}
            fragDict_vdw['ids'] = []
            fragDict_vdw['syms'] = []
            foundnew = False
            for atm in atmList:
                if atm["grp_vdw"] == grp_vdw:
                    foundnew = True
                    atm["grp_vdw"] = nfrags_vdw
                    fragDict_vdw['syms'].append(atm['sym'])
                    fragDict_vdw['ids'].append(atm['id'])

            if foundnew:
                fragDict_vdw['grp'] = nfrags_vdw
                # FIND CHARGE/MULT
                if isCation(fragDict_vdw['syms'], fragDict_vdw['ids']):
                    fragDict_vdw["chrg"] = 1
                    fragDict_vdw["mult"] = 1
                    if totChrg != '?':
                        totChrg += 1

                elif isAnion(fragDict_vdw['syms'], fragDict_vdw['ids']):
                    fragDict_vdw["chrg"] = -1
                    fragDict_vdw["mult"] = 1
                    if totChrg != '?':
                        totChrg += -1

                elif isNeutral(fragDict_vdw['syms'], fragDict_vdw['ids']):
                    fragDict_vdw["chrg"] = 0
                    fragDict_vdw["mult"] = 1

                elif isRadical(fragDict_vdw['syms'], fragDict_vdw['ids']):
                    fragDict_vdw["chrg"] = 0
                    fragDict_vdw["mult"] = 2
                    totMult = 2

                else:
                    # FIND CHEMICAL FORMULA
                    syms = []
                    chemForm = ''
                    for sym in fragDict_vdw['syms']:
                        if sym not in syms:
                            numTimes = fragDict_vdw['syms'].count(sym)
                            chemForm += sym + str(numTimes)
                            syms.append(sym)
                    detec("unknown", chemForm, " ".join(str(x+1) for x in fragDict_vdw['ids']))
                    fragDict_vdw["chrg"] = '?'
                    fragDict_vdw["mult"] = '?'
                    totChrg = '?'
                    totMult = '?'

                # FOR NEXT FRAGMENT
                fragList.append(fragDict_vdw)
                nfrags_vdw += 1

        print('-'*40)

    ### fragList = {'ids': [21], 'syms': ['Cl'], 'grp_dist': 1, 'chrg': -1, 'mult': 1}
    #for i in fragList:
    #    print(i)

    ### atmList = {'id': 710, 'sym': 'H', 'x': 11.5282, 'y': 7.0276, 'z': -18.5563, 'grp_dist': 80, 'nu': 1.0}
    #for i in atmList:
    #    print(i)
    #print(fragList, atmList, totChrg, totMult)

    return atmList, fragList, totChrg, totMult

#
#
# ----------- FUNCTIONS ADAPTED FROM PPQC Samual Tan


def isCation(a, b, q = False):

    import collections as col
    from chemData import CationDB
    from pprint   import detec

    #a = mol.atomListAsElem_Sym()
    isCat = False
    for key, cation in CationDB.items():
        if col.Counter(a) == col.Counter(cation):
            if not q:
                atmList = ''
                for i in b:
                    # START FROM 1 INSTEAD OF ZERO
                    atmList += str(i+1) + ' '
                detec("Cation detected", key, atmList)
            #return True
            isCat = True
            break
    return isCat

def isAnion(a, b, q = False):

    import collections as col
    from chemData import AnionDB
    from pprint   import detec

    # q for quiet
    #a = mol.atomListAsElem_Sym()
    # note the next only returns the first value--no duplicates allowed, or detected
    # checking done via Counter() from collections, no sorting required, duplicates included
    #return next((key for key, anion in AnionDB.items()
    #             if col.Counter(a) == col.Counter(anion)), None)
    isAni = False
    for key, anion in AnionDB.items():
        if col.Counter(a) == col.Counter(anion):
            if not q:
                atmList = ''
                for i in b:
                    # START FROM 1 INSTEAD OF ZERO
                    atmList += str(i+1) + ' '
                detec("Anion detected", key, atmList)
            isAni = True
            break
            #return True
        #else:
        #    print("no match ", col.Counter(a), col.Counter(anion))
        #    return False
    return isAni


def isNeutral(a, b, q = False):
    import collections as col
    from chemData import NeutralDB
    from pprint   import detec

    isNeu = False
    for key, molec in NeutralDB.items():
        if col.Counter(a) == col.Counter(molec):
            if not q:
                atmList = ''
                for i in b:
                    # START FROM 1 INSTEAD OF ZERO
                    atmList += str(i+1) + ' '
                detec("Neutral detected", key, atmList)
            isNeu = True
            break
    return isNeu


def isRadical(a, b, q = False):
    import collections as col
    from chemData import RadicalDB
    from pprint   import detec

    isRad = False
    for key, molec in RadicalDB.items():
        if col.Counter(a) == col.Counter(molec):
            if not q:
                atmList = ''
                for i in b:
                    # START FROM 1 INSTEAD OF ZERO
                    atmList += str(i+1) + ' '
                detec("Radical detected", key, atmList)
            isRad = True
            break
    return isRad
