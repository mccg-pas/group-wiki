def add_frag_name(fragList):
    from chemData import CationDB, AnionDB, NeutralDB, RadicalDB, NegRadDB, PosRadDB

    def add_name(frag, db):
        for mol, atoms in db.items():
            if sorted(atoms) == sorted(frag['syms']):
                frag['name'] = mol
        return frag

    for frag in fragList:
        for db in (CationDB, AnionDB, NeutralDB, RadicalDB, NegRadDB, PosRadDB):
            frag = add_name(frag, db)

    return fragList

def formula(lst):
    counts = {}
    for atom in lst:
        if atom not in counts:
            counts[atom] = 1
        else:
            counts[atom] += 1
    ret = ''
    for k, v in counts.items():
        ret += f'{k}{v}'
    return ret

def add_fragment_to_atoms(atmList, fragList):
    for atom in atmList:
        for frag in fragList:
            if atom['grp'] == frag['grp']:
                try:
                    atom['fragment'] = frag['name']
                except KeyError: #unknown fragment
                    atom['fragment'] = formula(frag['syms'])
    return atmList


def sysGeom(sysData, task):
    # SYSDATA
    # fragList = {'ids': [21], 'syms': ['Cl'], 'grp': 1, 'chrg': -1, 'mult': 1}
    # atmList = {'id': 710, 'sym': 'H', 'x': 11.5, 'y': 7.0, 'z': -18.5, 'grp': 80, 'nu': 1.0}
    # totChrg (int or '?')
    # totMult (int or '?')
    fragList, atmList, totChrg, totMult = sysData

    fragList = add_frag_name(fragList)
    atmList = add_fragment_to_atoms(atmList, fragList)

    # ALL DISTANCES CALCULATED
    if task == '1':
        print('-'*40)
        print('All interionic distances')
        print('-'*40)
        for frag in fragList:
            for atm1 in atmList:
                if atm1['grp'] == frag['grp']:
                    for atm2 in atmList:
                        # SECOND ATOM FRAG FROM FRAG GREATER THAN FIRST
                        if atm2['grp'] > frag['grp']:
                            print('{:>4}{:<4}{:>4}{:<4}{:5}{:4}{:8.3f}'.format(
                                  atm1['sym'],atm1['id']+1,
                                  atm2['sym'],atm2['id']+1,
                                  atm1['grp']+1, atm2['grp']+1,
                                  dist_between(atm1, atm2)))

    # CHOOSE PARTICULAR ATOMS
    #if task == '3':

    # ANGLES
#    print('-'*40)
#    print('')
#    print('-'*40)

    # H-BONDING STUFF etc.
    if task == '2':

        h_cutoff = 2.5
        h_atoms  = ['N', 'O', 'F']
        bonds = []
        angs  = []
        bond_format = '{:<4}{:<4}{:<4}{:<4}{:<7.3f}{:<10}{:<10}'
        angl_format = '{:<4}{:<4}{:<4}{:<4}{:<4}{:<4}{:<9.3f}{:<10}{:<10}'
        # FOR INTERMOLECULAR :: DIFFERENT FRAGS
        print('-'*40)
        print('H-bonding distances: N, O, F only')
        print('-'*40)
        for frag in fragList:
            for atm1 in atmList:

                # FOR ATOMS IN FRAG
                if atm1['grp'] == frag['grp']:
                    for atm2 in atmList:
                        # SECOND ATOM FRAG FROM FRAG GREATER THAN FIRST
                        if atm2['grp'] > frag['grp']:
                            dist = dist_between(atm1, atm2)
                            if dist < h_cutoff:
                                # CHECK THAT CORRECT ATOMS INVOLVED
                                if atm1['sym'] in h_atoms and atm2['sym'] is 'H':
                                    # ASSUME ONLY ONE BOND TO HYDROGEN
                                    bond_id = atm2['con'][0]
                                    # ORDER OF ANGLE MATTERS
                                    hy, donor = atm2, atm1

                                elif atm1['sym'] is 'H' and atm2['sym'] in h_atoms:
                                    # ASSUME ONLY ONE BOND TO HYDROGEN
                                    bond_id = atm1['con'][0]
                                    # ORDER OF ANGLE MATTERS
                                    hy, donor = atm1, atm2

                                if atm1['sym'] in h_atoms and atm2['sym'] is 'H' or\
                                   atm1['sym'] is 'H' and atm2['sym'] in h_atoms:

                                    for bond_atm in atmList:
                                        if bond_atm["id"] == bond_id:
                                            break
                                    if bond_atm["sym"] in h_atoms:
                                        # FIND ANGLE AND PRINT
                                        angle = ang(hy, donor, bond_atm)
                                        if 180-45 < angle < 180+45:
                                            angs.append(angl_format.format(
                                                    donor['sym'],
                                                    hy['sym'],
                                                    bond_atm['sym'],
                                                    donor['id']+1,
                                                    hy['id']+1,
                                                    bond_atm['id']+1,
                                                    ang(hy, donor, bond_atm),
                                                    donor['fragment'],
                                                    hy['fragment']))

                                            bonds.append(bond_format.format(
                                                    donor['sym'],
                                                    hy['sym'],
                                                    donor['id']+1,
                                                    hy['id']+1,
                                                    dist_between(atm1, atm2),
                                                    donor['fragment'],
                                                    hy['fragment']))



        bond_format = bond_format.replace('f', '')
        print(bond_format.format('don', 'hy', 'id1', 'id2', 'dist', 'frag1', 'frag2'))
        for line in bonds:
            print(line)
        print()
        angl_format = angl_format.replace('f', '')
        print(angl_format.format('don', 'hy', 'acc', 'id1', 'id2', 'id3', 'ang', 'frag1', 'frag2'))
        for line in angs:
            print(line)
    
    ### Intramolecular distances ###
    if task == '3':
        for frag in fragList:
            try:
                print(frag['name'])
            except KeyError:
                print(formula(frag['syms']))
            dists = {}
            for atm1 in atmList:
                if atm1['grp'] == frag['grp']: 
                    for atm2 in atmList:
                        if atm1 != atm2:
                        # SECOND ATOM IN SAME FRAGMENT AS FIRST
                            if atm2['grp'] == frag['grp']:
                                atoms = [atm1['id'], atm2['id']]
                                atoms.sort()
                                atoms = tuple(atoms) #prevent duplicates
                                if atoms not in dists:
                                    dists[atoms] = [atm1['sym'], 
                                                    atm2['sym'], 
                                                    dist_between(atm1, atm2)]
            for atm in atmList:
                for connection in atm['con']:
                    if (atm['id'], connection) in dists.keys():
                        atm1_id, atm2_id = atm['id'] + 1, connection + 1
                        atm1_sym, atm2_sym, dist = dists[(atm['id'], connection)]
                        print(f'{atm1_sym:>4}{atm1_id:<4}{atm2_sym:>4}{atm2_id:<4}{dist:8.3f}')

def dist_vec(atom1_dict, atom2_dict):
    i = atom1_dict
    j = atom2_dict
    return [i['x'] - j['x'], \
            i['y'] - j['y'], \
            i['z'] - j['z']  ]

def dist_between(atom1_dict, atom2_dict):
    import math
    i = atom1_dict
    j = atom2_dict
    return math.sqrt((i['x'] - j['x'])**2 \
                   + (i['y'] - j['y'])**2 \
                   + (i['z'] - j['z'])**2 )

def dot_prod(vec1, vec2):
    # dot product in 3dims // 2d : a·b = a1b1 + a2b2 + a3b3
    i = vec1
    j = vec2
    return i[0]*j[0] + i[1]*j[1] + i[2]*j[2]

def ang(atom1_dict, atom2_dict, atom3_dict):
    import math
    ### atom1 MUST BE THE CORNER OF THE ANGLE TO FIND
    i = atom1_dict
    j = atom2_dict
    k = atom3_dict
    dij = dist_between(i, j)
    dik = dist_between(i, k)
    vec_ij = dist_vec(i, j)
    vec_ik = dist_vec(i, k)
    #print(dij)
    #print(dik)
    #print(vec_ij)
    #print(vec_ik)
    # theta = arccos(a dot b / |a||b|)
    rad = dot_prod(vec_ij, vec_ik) / (dij * dik)
    # acos returned in radians
    return 180/math.pi * math.acos(rad)
