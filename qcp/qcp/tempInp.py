def inpDetail():
    type = input('opt or sp: ')
    meth = input('method:    ')
    bset = input('basis set: ')

    if type == 'opt':
        type = 'optimize'
    elif type == 'sp':
        type = 'energy'
    # IF PSI4 BASIS GUESS?
    return type, meth, bset

def psi_inp():

    type, meth, bset = inpDetail()

    df = ['mp2', 'MP2', 'dfmp2', 'DFMP2']

    if meth in df:
        lines = ["memory 64 Gb\n",
        "molecule complex {\n",
        "0 1\n",
        "xyz_data",
        "}\n",
        "set globals {\n",
        "   basis " + bset + "\n",
        "   scf_type df\n",
        "   freeze_core True\n",
        "   basis_guess cc-pVDZ\n",
        "   guess sad\n",
        "   s_orthogonalization canonical\n",
        "   reference rohf\n",
        "}\n",
        "set cachelevel 0\n",
        "set print 2\n",
        type + "('" + meth + "')"]

def fmo_ions(chrg, coords, bset, mp2): # MP
    if not mp2:
        mp2 = ''
    lines = [" $SYSTEM MWORDS=200 $END\n",
    " $CONTRL MPLEVL=2 SCFTYP=RHF RUNTYP=ENERGY MAXIT=200 ISPHER=1\n",
    " ICHARG=" + chrg + " $END\n",
    " $SCF DIRSCF=.TRUE. FDIFF=.FALSE. DIIS=.TRUE. $END\n",
    " $BASIS GBASIS=" + bset + " $END\n",
    mp2, # E.G. $MP2 CODE=IMS SCSPT=SCS SCSOPO=1.05 SCSPAR=0.68 $END
    " $DATA\n",
    "cation2-MP2-energy\n",
    "C1\n",
    "xyz_data",
    " $END"]

    input = []
    for line in lines:
        if 'xyz_data' in line:
            for i in coords:
                input.append(i)
                xyzIn = True
        else:
            input.append(line)

    return input


