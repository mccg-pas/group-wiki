#!/short/k96/zls565/installations/bin/python3

import subprocess as sp
import os.path

#The Periodic Table of Elements

# H 1.00784
# C 15.99903

pTable = {
"H"    :   [1.0, 1.007825       , 0.430],
"He"   :   [2.0, 4.0026022      , 0.741],
"Li"   :   [3.0, 6.938          , 0.880],
"Be"   :   [4.0, 9.01218315     , 0.550],
"B"    :   [5.0, 10.806         , 1.030],
"C"    :   [6.0, 12.0096        , 0.900],
"N"    :   [7.0, 14.00643       , 0.880],
"O"    :   [8.0, 15.99491       , 0.880],
"F"    :   [9.0, 18.99840316    , 0.840],
"Ne"   :   [10.0, 20.17976      , 0.815],
"Na"   :   [11.0, 22.98976928   , 1.170],
"Mg"   :   [12.0, 24.304        , 1.300],
"Al"   :   [13.0, 26.98153857   , 1.550],
"Si"   :   [14.0, 28.084        , 1.400],
"P"    :   [15.0, 30.973762     , 1.250],
"S"    :   [16.0, 32.059        , 1.220],
"Cl"   :   [17.0, 35.446        , 1.190],
"Ar"   :   [18.0, 39.9481       , 0.995],
"K"    :   [19.0, 39.09831      , 1.530],
"Ca"   :   [20.0, 40.0784       , 1.190],
"Sc"   :   [21.0, 44.9559085    , 1.640],
"Ti"   :   [22.0, 47.8671       , 1.670],
"V"    :   [23.0, 50.94151      , 1.530],
"Cr"   :   [24.0, 51.99616      , 1.550],
"Mn"   :   [25.0, 54.9380443    , 1.555],
"Fe"   :   [26.0, 55.8452       , 1.540],
"Co"   :   [27.0, 58.9331944    , 1.530],
"Ni"   :   [28.0, 58.69344      , 1.700],
"Cu"   :   [29.0, 63.5463       , 1.720],
"Zn"   :   [30.0, 65.382        , 1.650],
"Ga"   :   [31.0, 69.7231       , 1.420],
"Ge"   :   [32.0, 72.6308       , 1.370],
"As"   :   [33.0, 74.9215956    , 1.410],
"Se"   :   [34.0, 78.9718       , 1.420],
"Br"   :   [35.0, 79.901        , 1.410],
"Kr"   :   [36.0, 83.7982       , 1.069],
"Rb"   :   [37.0, 85.46783      , 1.670],
"Sr"   :   [38.0, 87.621        , 1.320],
"Y"    :   [39.0, 88.905842     , 1.980],
"Zr"   :   [40.0, 91.2242       , 1.760],
"Nb"   :   [41.0, 92.906372     , 1.680],
"Mo"   :   [42.0, 95.951        , 1.670],
"Tc"   :   [43.0, 98            , 1.550],
"Ru"   :   [44.0, 101.072       , 1.600],
"Rh"   :   [45.0, 102.905502    , 1.650],
"Pd"   :   [46.0, 106.421       , 1.700],
"Ag"   :   [47.0, 107.86822     , 1.790],
"Cd"   :   [48.0, 112.4144      , 1.890],
"In"   :   [49.0, 114.8181      , 1.830],
"Sn"   :   [50.0, 118.7107      , 1.660],
}


### ANIONS --------------------------------------------------
AnionDB = {"br"     : ["Br"]}
AnionDB["cl"]       = ["Cl"]
AnionDB["bf4"]      = ['B', 'F', 'F', 'F', 'F']
AnionDB["dca"]      = ['N', 'C', 'N', 'C', 'N']
AnionDB["pf6"]      = ['F', 'P', 'F', 'F', 'F', 'F', 'F']
AnionDB["mes"]      = ['S', 'O', 'O', 'O', 'C', 'H', 'H', 'H']
AnionDB["ntf2"]     = ['F', 'F', 'F', 'F', 'F', 'N', 'S', 'S',
                       'O', 'O', 'O', 'O', 'C', 'C', 'F']
AnionDB["tos"]      = ['C', 'C', 'C', 'C', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H', 'S', 'O', 'O', 'O', 'C',
                       'C', 'C']
AnionDB["h2po4"]    = ['H', 'H', 'P', 'O', 'O', 'O', 'O']
AnionDB["acetate"]  = ['H', 'H', 'H', 'C', 'C', 'O', 'O']
AnionDB["otf"]      = ['C', 'F', 'F', 'F', 'S', 'O', 'O', 'O']
AnionDB["nitrate"]  = ['N', 'O', 'O', 'O']
AnionDB["sulfate"]  = ['H', 'S', 'O', 'O', 'O', 'O']
AnionDB["saccharinate"] = ['C', 'C', 'C', 'C', 'C', 'C', 'C',
                           'H', 'H', 'H', 'H', 'S', 'N', 'O',
                                                      'O', 'O']
AnionDB["nitrate"]  = ['N', 'O', 'O', 'O']
AnionDB["formate"]  = ['C', 'O', 'O', 'H']
AnionDB["glycolate"]= ['C', 'C', 'H', 'H', 'H', 'O', 'O', 'O']
AnionDB["mOSO3"]    = ['H', 'H', 'H', 'O', 'O', 'O', 'O', 'C',
                       'S']
AnionDB["tfa"]      = ['F', 'O', 'C', 'F', 'O', 'C', 'F']
### CATIONS --------------------------------------------------
CationDB = {"c1mim" : ['C', 'N', 'C', 'N', 'C', 'C', 'C', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']}
CationDB["c1mpyr"]  = ['C', 'C', 'C', 'N', 'C', 'C', 'C', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H']
CationDB["c1py"]    = ['C', 'H', 'C', 'H', 'N', 'C', 'H', 'C',
                       'H', 'C', 'H', 'C', 'H', 'H', 'H']
CationDB["c2mim"]   = ['C', 'N', 'C', 'N', 'C', 'C', 'C', 'C',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H']
CationDB["c2mpyr"]  = ['N', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
CationDB["c2py"]    = ['C', 'H', 'C', 'H', 'N', 'C', 'H', 'C',
                       'H', 'C', 'H', 'C', 'H', 'H', 'C', 'H',
                       'H', 'H']
CationDB["c3mim"]   = ['N', 'C', 'N', 'C', 'C', 'C', 'C', 'H',
                       'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H']
CationDB["c3mpyr"]  = ['N', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
                       'C', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H']
CationDB["c3py"]    = ['C', 'H', 'C', 'H', 'N', 'C', 'H', 'C',
                       'H', 'C', 'H', 'C', 'H', 'H', 'C', 'H',
                       'H', 'C', 'H', 'H', 'H']
CationDB["c4mim"]   = ['C', 'N', 'C', 'C', 'N', 'C', 'C', 'H',
                       'C', 'C', 'C', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H']
CationDB["c4mpyr"]  = ['N', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
                       'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H']
CationDB["c4py"]    = ['C', 'H', 'C', 'H', 'N', 'C', 'H', 'C',
                       'H', 'C', 'H', 'C', 'H', 'H', 'C', 'H',
                       'H', 'C', 'H', 'H', 'C', 'H', 'H', 'H']
CationDB["mpyr"]    = ['C', 'N', 'C', 'C', 'C', 'C', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H']
CationDB["mim"]     = ['C', 'N', 'C', 'N', 'C', 'C', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H']
CationDB["choline"] = ['H', 'H', 'H', 'C', 'H', 'H', 'H', 'C',
                       'H', 'H', 'H', 'C', 'N', 'C', 'H', 'H',
                       'C', 'H', 'H', 'O', 'H']
CationDB["dema"]    = ['C', 'H', 'H', 'H', 'C', 'H', 'H', 'C',
                       'H', 'H', 'H', 'C', 'H', 'H', 'C', 'H',
                       'H', 'H', 'N', 'H']
CationDB["pme4"]    = ['P', 'C', 'H', 'H', 'H','C', 'H', 'H',
                       'H', 'C', 'H', 'H', 'H','C', 'H', 'H',
                       'H']
CationDB["diethanolamine"]  \
                    = ['C', 'H', 'H', 'H', 'C', 'H', 'H', 'O',
                       'H', 'C', 'H', 'H', 'H', 'C', 'H', 'H',
                       'O', 'H', 'N', 'H', 'H']
CationDB["Li"]      = ['Li']
CationDB["Na"]      = ['Na']
CationDB["demda+"]  = ['C', 'N', 'C', 'C', 'C', 'N', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H']
CationDB["nme4"]    = ['N', 'C', 'C', 'C', 'C', 'H', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H']
CationDB["ethylammonium"] \
                    = ['C', 'C', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'N']
CationDB["ethanolammonium"] \
                    = ['C', 'C', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'N', 'O']

### NEUTRAL MOLECULES --------------------------------------
NeutralDB           = {"ch4": ['C', 'H', 'H', 'H', 'H']}
NeutralDB["h2"]     = ['H', 'H']
NeutralDB["water"]  = ["H", "H", "O"]
NeutralDB["asa"]    = ['C', 'C', 'C', 'O', 'O', 'C', 'H', 'C',
                       'H', 'C', 'H', 'C', 'H', 'C', 'O', 'O',
                       'H', 'C', 'H', 'H', 'H']
NeutralDB["bz"]     = ['C', 'H', 'C', 'H', 'C', 'H', 'C', 'H',
                       'C', 'H', 'C', 'H']
NeutralDB["odh"]    = ['C', 'O', 'N', 'H', 'N', 'H', 'H', 'C',
                       'O', 'N', 'H', 'N', 'H', 'H']
NeutralDB["phenol"] = ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'O']
NeutralDB["phenol_deriv"]       = ['C', 'C', 'C', 'C', 'C', 'C',
                                   'C', 'C', 'C', 'C', 'C', 'C',
                                   'C', 'C', 'C', 'C', 'H', 'H',
                                   'H', 'H', 'H', 'H', 'H', 'H',
                                   'H', 'H', 'H', 'H', 'H', 'H',
                                   'H', 'H', 'H', 'H', 'O', 'O']
NeutralDB["cisplatin"]          = ['Pt', 'Cl', 'N', 'H']
NeutralDB["carboplatin"]        = ['Pt', 'C', 'N', 'H', 'O']
NeutralDB["vinyl chloride"]     = ['H', 'H', 'C', 'C', 'H', 'Cl']
NeutralDB["meth methacrylate"]  = ['H', 'H', 'C', 'C', 'C', 'H',
                                   'H', 'H', 'C', 'O', 'O', 'C',
                                   'H', 'H', 'H']
NeutralDB["ethylene"]           = ['H', 'H', 'C', 'C', 'H', 'H']
NeutralDB["acronitrile"]        = ['H', 'H', 'C', 'C', 'H', 'C',
                                   'N']
### NEUTRAL RADICALS ----------------------------------------
RadicalDB = {"nitroxide": ['N', 'O', 'C', 'C', 'H', 'H', 'H',
                           'H', 'H', 'H']}
RadicalDB["tempo"]  = ['N', 'O', 'C', 'C', 'C', 'C', 'C', 'C',
                       'C', 'C', 'C', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H']
RadicalDB["tmpo_1"] = ['N', 'O', 'O', 'O', 'C', 'C', 'C', 'C',
                       'C', 'C', 'C', 'C', 'H', 'H', 'H', 'H',
                       'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H',
                       'H', 'H', 'C']
RadicalDB["phenyl_rad"]    = ['C', 'C', 'C', 'C', 'C', 'C',
                              'C', 'C', 'H', 'H', 'H', 'H',
                              'H', 'H', 'H', 'H', 'H', 'O']
RadicalDB["phenol_dim_rad"]= ['C', 'C', 'C', 'C', 'C', 'C',
                              'C', 'C', 'C', 'C', 'C', 'C',
                              'C', 'C', 'C', 'C', 'H', 'H',
                              'H', 'H', 'H', 'H', 'H', 'H',
                              'H', 'H', 'H', 'H', 'H', 'H',
                              'H', 'H', 'H', 'O', 'O']

# VALUES CAN BE ASSIGNED IN USER TEMPLATE my.Molecules.qcp
NegRadDB = {}
PosRadDB = {}

# TEMPLATE OF USER DEFINED MOLECULES
def mol_template():
    lines = [
            "# Molecules should be laid out in four lines as follows\n",
            "# name=<NAME>\n",
            "# charge=<CHARGE>\n",
            "# multiplicity=<MULTIPLICITY>\n",
            "# atoms=<list of individual atoms in any order>\n",
            "# hashed lines are not read by python\n",
            "# below is an example for hydrogen peroxide\n",
            "name=h2o2\n",
            "charge=0\n",
            "multiplicity=1\n",
            "atoms=O,H,H,O\n"
            ]
    return lines



homeFile = sp.getoutput("echo $HOME") + '/myMolecules.qcp'
#print("Checking user defined molecules in " + homeFile)

# CREATE TEMPLATE FILE IF NOT EXISTS
if not os.path.isfile(homeFile):
    open(homeFile, 'w+').writelines(mol_template())
# READ USER MOLECULES IF FILE EXISTS
else:
    name   = False
    charge = False
    mult   = False
    atoms  = False
    with open(homeFile, 'r+') as f:
        for line in f:
            # GET RID OF EXTRA SPACES AND ANYTHING AFTER A HASH
            line = line.strip()
            line = line.split('#')[0]
            # SPLIT INTO DESCRIPTOR AND VALUE
            line = line.split('=')
            # FIND IF ONE OF THE DESCRIPTORS AND ASSIGN VALUE
            if 'name' in line[0]:
                name = line[1]
            elif 'charge' in line[0]:
                charge = int(line[1])
            elif 'multiplicity' in line[0]:
                mult = int(line[1])
            elif 'atoms' in line[0]:
                atoms = line[1].split(',')
                for i in range(len(atoms)):
                    atoms[i] = atoms[i].strip()

            # ONCE ALL DEFINED ADD TO DICTIONARY
            if not name is False and not charge is False:
                if not mult is False and not atoms is False:
                    if charge is 0 and mult is 1:
                        NeutralDB[name] = atoms
                    elif charge is -1 and mult is 1:
                        AnionDB[name] = atoms
                    if charge is 1 and mult is 1:
                        CationDB[name] = atoms
                    if charge is 0 and mult is 2:
                        RadicalDB[name] = atoms
                    if charge is -1 and mult is 2:
                        NegRadDB[name] = atoms
                    if charge is 1 and mult is 2:
                        PosRadDB[name] = atoms
                    # RESET VARS
                    name   = False
                    charge = False
                    mult   = False
                    atoms  = False








#"vinyl chloride": ['H', 'H', 'C', 'C', 'H', 'Cl']}
#RadicalDB["methylmethacrylate"] \
#                            = ['H', 'H', 'C', 'C', 'C', 'H',
#                               'H', 'H', 'C', 'O', 'O', 'C',
#                               'H', 'H', 'H']
#RadicalDB["ethylene"]      = ['H', 'H', 'C', 'C', 'H', 'H']
#RadicalDB["acronitrile"]   = ['H', 'H', 'C', 'C', 'H', 'C', 'N'] # NOT THE RADICALS

