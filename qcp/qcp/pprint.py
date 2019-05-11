def e_print(energy):
    from operator import itemgetter

    ZP  = []
    MP2 = []
    for d in energy:
        if d["ZP"]:
            ZP.append(True)
        if d["MP2"]:
            MP2.append(True)
    energy = sorted(energy, key=itemgetter('Path', 'File'))
    if True in ZP and True in MP2:
        print('-' * 80)
        print('{:40}{:6}{:17.15}{:9}{:17.15}   {}'.\
        format('File', 'Type', 'HF/DFT', 'ZPVE', 'MP2/SRS', 'Path'))
        print('-' * 80)
        for d in energy:
            print('{:40}{:6}{:17.15}{:9}{:17.15}   {}'.\
            format(d["File"], d["Type"], d["HF"], d["ZP"], d["MP2"], d["Path"]))
        print('-' * 80)

    elif True in ZP:
        print('-' * 80)
        print('{:40}{:6}{:17.15}{:9}   {}'.\
        format('File', 'Type', 'HF/DFT', 'ZPVE', 'Path'))
        print('-' * 80)
        for d in energy:
            print('{:40}{:6}{:17.15}{:9}   {}'.\
            format(d["File"], d["Type"], d["HF"], d["ZP"], d["Path"]))
        print('-' * 80)

    elif True in MP2:
        print('-' * 80)
        print('{:40}{:6}{:17.15}{:17.15}   {}'.\
        format('File', 'Type', 'HF/DFT', 'MP2/SRS', 'Path'))
        print('-' * 80)
        for d in energy:
            print('{:40}{:6}{:17.15}{:17.15}   {}'.\
            format(d["File"], d["Type"], d["HF"], d["MP2"], d["Path"]))
        print('-' * 80)
    else:
        print('-' * 80)
        print('{:40}{:6}{:17.15}   {}'.\
        format('File', 'Type', 'HF/DFT','Path'))
        print('-' * 80)
        for d in energy:
            print('{:40}{:6}{:17.15}   {}'.\
            format(d["File"], d["Type"], d["HF"], d["Path"]))
        print('-' * 80)




def stat_print(path, File, q_mess, l_mess = False):
    # MESSAGE ASSIGNMENT
    if q_mess == 1:
        q_mess = "Equ geometry found"
        l_mess = "Creating xyz"
    elif q_mess == 2:
        q_mess = "Single point calcu"
        l_mess = "No xyz needed"
    elif q_mess == 3:
        q_mess = "Error in terminati"
        l_mess = "Creating xyz"
    elif q_mess == 4:
        q_mess = "Maximum iterations"
        l_mess = "Creating xyz"
    elif q_mess == 5:
        q_mess = "Not recongnise inp"
        l_mess = "File software not found"
    elif q_mess == 6:
        q_mess = "Failed optimisatio"
        l_mess = "Optimisation did not complete one full step"
    elif q_mess == 7:
        q_mess = "Normal termination"
        l_mess = "Creating xyz"
    elif q_mess == 8:
        q_mess = "Error charge/multi"
    elif q_mess == 9:
        q_mess = "Error in input fil"
        l_mess = "Do you have a space before all $"
    elif q_mess == 10:
        q_mess = "Memory has exceede"
        l_mess = "Creating xyz"
    elif q_mess == 11:
        q_mess = "Walltime has excee"
        l_mess = "Creating xyz"
    elif q_mess == 12:
        q_mess = "Unknown error unkn"
        l_mess = "Creating xyz"
    elif q_mess == 13:
        q_mess = "Disk space error ?"
        l_mess = "Creating xyz"
    elif q_mess == 14:
        q_mess = "Convergence errors"
        l_mess = "Creating xyz"
    elif q_mess == 15:
        q_mess = "Error single point"
        l_mess = "No xyz found in dir"
    elif q_mess == 16:
        q_mess = "Error single point"
        l_mess = "Copying xyz"
    elif q_mess == 17:
        q_mess = "Hessian corruption"
        l_mess = "Creating xyz"

    if l_mess:
        print('{:20} {:30} {}'.format(q_mess, path + File, l_mess))
    else:
        print('{:20} {}'.format(q_mess, path + File))

def file_print(path, File, q_mess):
    print('{:20} {}'.format(q_mess, path + File))


def detec(Type, nums, mol):
    print('{:19} {:10} {}'.format(Type, nums, mol))

def noFiles():
    import os, sys
    print("No files were found to operate on in directory")
    sys.exit(os.getcwd())


