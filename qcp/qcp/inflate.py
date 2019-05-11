import math
import numpy as np


def get_min_interionic_dist(atmList):

    # PUT IN relxyz
    mindist = 10000
    for i in atmList:
        for j in atmList:
            if i["id"] < j["id"] and i["grp"] != j["grp"]:
                s = (i["x"] - j["x"]) ** 2 + (i["y"] - j["y"]) ** 2 + (i["z"] - j["z"]) ** 2
                s = math.sqrt(s)
                if s < mindist:
                    mindist = s

    return mindist


def rearrange_list(atmList, fragList):
    from geometry import dist_between

    # ALL INTERIONIC DISTANCES
    dists = []
    for frag in fragList:
        for val, atm1 in enumerate(atmList):
            if atm1['grp'] == frag['grp']:
                for val2, atm2 in enumerate(atmList):
                    # SECOND ATOM FRAG FROM FRAG GREATER THAN FIRST
                    if atm2['grp'] > frag['grp']:
                            x = dist_between(atm1, atm2)

                            if not atm1.get("dist"):
                                atm1["dist"] = x

                            elif x < atm1.get("dist"):
                                atm1["dist"] = x

                            if not atm2.get("dist"):
                                atm2["dist"] = x
                            elif x < atm2.get("dist"):
                                atm2["dist"] = x

    # ATOM LIST SORTED WITH SMALLER DISTS AT START OF DICT
    # CAN NO LONGER USE ID TO IDENTIFY COORD
    atmList = sorted(atmList, key=lambda k: (k['grp'], k['dist']))

    for frag in fragList:
        frag["ids_by_int_dist"] = []
        for atm in atmList:
            if atm["id"] in frag["ids"]:
                frag["ids_by_int_dist"].append(atm["id"])

    return atmList, fragList



def get_relative_coords(atmList, fragList):
    # HOLD FIRST ELEM OF EACH FRAG
    coords = np.zeros(shape=(len(atmList), 3))

    # ALL ATOMS RELATIVE TO FIRST ATOM
    relxyz = np.zeros(shape=(len(atmList), 3))

    # PUT IN ACTUAL COORDS
    # ATOM LIST SORTED WITH SMALLER DISTS AT START OF DICT
    # USE ORDER IN FRAGLIST TO ORGANISE COORDS
    i = 0

    for frag in fragList:
        for atm in atmList:
            if atm["id"] in frag['ids_by_int_dist']:
                # FIRST ATOM OF FRAG
                if atm["id"] == frag['ids_by_int_dist'][0]:
                    atm_dic = atm

                # RELXYZ AND COORDS IN ORDER OF APPEARANCE IN FRAGLIST
                coords[i, 0], coords[i, 1], coords[i, 2] = atm_dic["x"], atm_dic["y"], atm_dic["z"]
                relxyz[i, 0] = atm["x"] - atm_dic["x"]
                relxyz[i, 1] = atm["y"] - atm_dic["y"]
                relxyz[i, 2] = atm["z"] - atm_dic["z"]

                i += 1

    return relxyz, coords


def expand(path, File, sysData, dists):
    from write import write_xyz

    fragList, atmList, totChrg, totMult = sysData

    # GET SMALLEST INTERIONIC DISTANCE
    # a, b ARE INDEX OF SMALLEST DIST ATOMS
    dmin = get_min_interionic_dist(atmList)

    atmList, fragList = rearrange_list(atmList, fragList)

    relxyz, coords = get_relative_coords(atmList, fragList)

    # FIND NEW ORIGIN // MEAN OF ALL POINTS
    d_origin = np.mean(coords, axis=0)

    # REDEFINE POINTS W.R.T NEW ORIGIN
    coords = coords - d_origin

    # FOR EACH DISTANCE
    for dist in dists:
        scale = dist / dmin
        # SCALE
        coords_new = scale * coords

        # PLUS POSITION OF EACH TO ALL RELATIVE POSITIONS TO GET NEW XYZ
        coords_new = coords_new + relxyz

        # RELXYZ AND COORDS IN ORDER OF APPEARANCE IN FRAGLIST
        i = 0
        newxyz = []
        for frag in fragList:
            for atm in atmList:
                if atm["id"] in frag['ids_by_int_dist']:
                    newxyz.append([atm["sym"], coords_new[i][0], coords_new[i][1], coords_new[i][2]])
                    i += 1

        name = File.replace('.xyz', '_' + str(dist) + 'A')
        write_xyz(path, name, newxyz)
