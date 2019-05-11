def write_xyz(path, name, geom):
    with open(path + name + '.xyz', 'w+') as f:
        f.write(str(len(geom)) + "\n\n")
        c = len(geom[0])
        for i in geom:
            # DON'T INCLUDE SYMBOL?
            f.write('{:3}{:17.9f}{:17.9f}{:17.9f}\n'.\
                format(i[0], float(i[c-3]), float(i[c-2]), float(i[c-1])))

def write_gmsInp(path, name, lines):
    with open(path + name + '.inp', 'w+') as f:
        for i in lines:
            if type(i) is str:
                f.write(i)
            else:
                f.write(' {:3}{:5}{:17.9f}{:17.9f}{:17.9f}\n'.\
                    format(i[0], i[1], float(i[2]), float(i[3]), float(i[4])))


def write_inp(path, name, lines):
    with open(path + name + '.inp', 'w+') as f:
        for i in lines:
            if type(i) is str:
                f.write(i)
            else:
                c = len(i)
                f.write('{:3}{:17.9f}{:17.9f}{:17.9f}\n'.\
                    format(i[0], float(i[c-3]), float(i[c-2]), float(i[c-1])))


def write_job(path, name, lines, cp = False):
    with open(path + name + '.job', 'w+') as f:
        for i in lines:
            # GAUSSIAN
            if cp and type(i) == list:
                c = len(i)
                f.write('{:3}{:17.9f}{:17.9f}{:17.9f}{:>3}\n'.\
                format(i[0], float(i[c-4]), float(i[c-3]), float(i[c-2]), i[c-1]))
            elif type(i) == list:
                c = len(i)
                f.write('{:3}{:17.9f}{:17.9f}{:17.9f}\n'.\
                format(i[0], float(i[c-3]), float(i[c-2]), float(i[c-1])))
            else:
                f.write(i)

def write_energy(path, energy):
    import csv
    with open(path + 'out_energies.csv', 'w') as csvfile:
         Write = csv.writer(csvfile, delimiter='|')
         ZP  = []
         MP2 = []
         for d in energy:
             if d["ZP"]:
                 ZP.append(True)
             if d["MP2"]:
                 MP2.append(True)

         if True in ZP and True in MP2:
             Write.writerow(['File', 'Type', 'HF/DFT', 'ZPVE', 'MP2/SRS', 'Path'])
             for d in energy:
                 Write.writerow([d["File"], d["Type"], d["HF"], d["ZP"], d["MP2"], d["Path"]])

         elif True in ZP:
             Write.writerow(['File', 'Type', 'HF/DFT', 'ZPVE', 'Path'])
             for d in energy:
                 Write.writerow([d["File"], d["Type"], d["HF"], d["ZP"], d["Path"]])

         elif True in MP2:
             Write.writerow(['File', 'Type', 'HF/DFT', 'MP2/SRS', 'Path'])
             for d in energy:
                 Write.writerow([d["File"], d["Type"], d["HF"], d["MP2"], d["Path"]])
         else:
             Write.writerow(['File', 'Type', 'HF/DFT','Path'])
             for d in energy:
                 Write.writerow([d["File"], d["Type"], d["HF"], d["Path"]])
