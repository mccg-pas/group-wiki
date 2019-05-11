def comp_tasks(task, path, filename, jobfile):
    import os.path
    from general        import find_files, software, softInp
    from system         import systemData
    from pprint         import stat_print, file_print, e_print
    from pprint         import noFiles
    from logFile        import sort

    # FORMAT EXPECTED
    if filename:
        if path is '':
            path = './'
        Files = [[path, filename]]
    else:
        Files = False

    # GENERATE JOB/INP FROM TEMPLATE
    # EXPECTS .template FILE IN PATH DIRECTORY
    if task == "1":
        from genJob  import g09, gms, psi, fmo, orc

        # fmoC         = False
        # level        = False                   # NO LEVELS
        # if not Files:
            # file_pattern = ['.xyz']            # FILES TO CHECK
            # Files        = find_files(path, level, file_pattern)
            # if len(Files) == 0:
                # noFiles()
        
        # RECURSIVE FILE CREATION
        if not Files:
            level        = False                   # ALL LEVELS
            level        = input("Number of subdirs [0-9]: ")
            file_pattern = ['.xyz']        # FILES TO CHECK
            Files        = find_files(path, level, file_pattern)
            if len(Files) == 0:
                noFiles()

        for path, File in Files:
            
            # CHECK IF ANY TEMPLATE FILES ARE FMO FOR CORRECT FRAGMENTATION
            fmoC = False
            for template in os.listdir(path):
                if template.endswith('template'):
                    with open(template, 'r+') as f:
                        for line in f:
                            if '$FMO' in line:
                                fmoC = True

            # CHECK IF JOB TEMPLATE
            jobTemp = False

            if jobfile:
                jobTemp = open(path + jobfile, 'r+').read()

            elif os.path.isfile(path + 'template.job'):
                jobTemp = open(path + 'template.job', 'r+').read()

            # SEARCH FILES
        # for path, File in Files:
            print('-'*40)
            file_print(path, File, "Using")
            # ONLY HAPPEN ONCE FOR EACH XYZ
            sysData = systemData(path, File, fmoC)
            # COMPLETE FOR EVERY TEMPLATE
            for template in os.listdir(path):
                if template.endswith('template'):
                    file_print(path, template, "With template")
                    soft = softInp(path, template)
                    if soft == 'g09':
                        # JOB INCLUDED IN INPUT
                        g09(path, File, template, sysData)
                    elif soft == 'gms':
                        gms(path, File, template, sysData, jobTemp)
                    elif soft == 'psi':
                        psi(path, File, template, sysData, jobTemp)
                    elif soft == 'fmo':
                        fmo(path, File, template, sysData, jobTemp)
                    elif soft == 'orc':
                        orc(path, File, template, sysData, jobTemp)
                    else:
                        g09(path, File, template, sysData)


    ### PULL ENERGIES
    elif task == "2":
        from energy import energy_g09, energy_gms, energy_psi
        from write  import write_energy
        energy       = []                           # TO PRINT AT END
        if not Files:
            level        = 100                      # ALL
            file_pattern = ['.log', '.out']         # FILES TO CHECK
            Files        = find_files(path, level, file_pattern)
            if len(Files) == 0:
                noFiles()
        # SEARCH FILES
        for path, File in Files:
            # DO NOT SORT PREVIOUS LOG FILES
            if not File.startswith('f-') and not File.startswith('slurm'):
                soft = software(path, File)
                if soft == 'gms':
                    energy = energy_gms(path, File, energy)
                elif soft == 'g09':
                    energy = energy_g09(path, File, energy)
                elif soft == 'psi':
                    energy = energy_psi(path, File, energy)
        mkfi = input("Write to file? (y/n) [n]")
        if mkfi == 'n' or mkfi == '':
            e_print(energy)
        elif mkfi == 'y':
            e_print(energy)
            write_energy(path, energy)


    ### SORT LOG FILES
    elif task == "3":
        if not Files:
            level        = False                   # ALL LEVELS
            level        = input("Number of subdirs [0-9]: ")
            file_pattern = ['.log', '.out']        # FILES TO CHECK
            Files        = find_files(path, level, file_pattern)
            if len(Files) == 0:
                noFiles()
        # SEARCH FILES
        for path, File in Files:
            # DO NOT SORT PREVIOUS LOG FILES
            if not File.startswith('f-'):
                # GET SOFTWARE OF LOG
                soft = software(path, File)
                if not soft:
                    stat_print(path, File, 5)
                else:
                    # MOVE INTO DIRECTORIES & CREATE XYZ's
                    sort(path, File, soft)

    # MASS SED
    elif task == "4":
        from clean import sed
        sed(path)

    # MASS RENAME
    elif task == "5":
        from clean import rename
        rename(path)

    # DELETE N JOBS FROM QUEUE
    elif task == "6":
        from supercomp import deleteJob
        deleteJob()

    # COUNTERPOISE
    elif task == '7':
        from genJob        import g09, gms, psi, fmo
        from genJobCP      import psi_cpoise, g09_cpoise

        if not Files:
            level        = False                   # ZERO LEVELS
            file_pattern = ['.xyz']                # FILES TO CHECK
            Files        = find_files(path, level, file_pattern)
            if len(Files) == 0:
                noFiles()

        # CHECK IF JOB TEMPLATE
        jobTemp = False
        if jobfile:
            jobTemp = open(path + jobfile, 'r+').read()
        elif os.path.isfile(path + 'template.job'):
            jobTemp = open(path + 'template.job', 'r+').read()

        # SEARCH FILES
        for path, File in Files:
            file_print(path, File, "Using")
            # ONLY HAPPEN ONCE FOR EACH XYZ
            sysData = systemData(path, File, True)
            # COMPLETE FOR EVERY TEMPLATE
            for template in os.listdir(path):
                if template.endswith('template'):
                    soft = softInp(path, template)
                    # PSI4 ONLY
                    if soft == 'g09':
                        # JOB INCLUDED IN INPUT
                        g09_cpoise(path, File, template, sysData)
                    elif soft == 'gms':
                        pass
                    elif soft == 'psi':
                        psi_cpoise(path, File, template, sysData, jobTemp)
                    elif soft == 'fmo':
                        pass

    # DISTANCES AND ANGLES
    elif task == '8':
        from geometry import sysGeom
        # GET PATHS
        if not Files:
            level        = 1
            file_pattern = ['.xyz']        # FILES TO CHECK
            Files        = find_files(path, level, file_pattern)
            Files = find_files(path, level, file_pattern)
            if len(Files) == 0:
                noFiles()

        # ASK USER QUESTIONS ABOUT WHAT THEY WANT
        task = input('                                    \n\
                          1. All interionic distances     \n\
                          2. H-bonding data               \n\
                          3. Intramolecular bond lengths  \n\
                                                           Task: ')

        for path, File in Files:
            file_print(path, File, "Using")
            sysData = systemData(path, File, True)
            sysGeom(sysData, task)

    # SUBMIT JOBS
    elif task == '9':

        from supercomp import submit
        # GET PATHS
        if not Files:
            level        = False                   # ALL LEVELS
            level = input("Number of subdirs [0-9]: ")
            file_pattern = ['.com', '.job']        # FILES TO CHECK
            Files        = find_files(path, level, file_pattern)
            if len(Files) == 0:
                noFiles()

        # ORIGINAL PATH
        os.chdir(path)
        cwd = os.getcwd()
        # SEARCH FILES
        for path2, File in Files:
            if File != 'template.job':
                os.chdir(path2)
                submit(File)
                os.chdir(cwd)


    # INFLATE SYSTEM
    # EXPECTS .xyz FILE IN PATH DIRECTORY
    elif task == "A":
        import sys
        from inflate  import expand

        fmoC         = True
        level        = False                   # NO LEVELS

        if not Files:
            file_pattern = ['.xyz']            # FILES TO CHECK
            Files        = find_files(path, level, file_pattern)
            if len(Files) == 0:
                noFiles()

        # DISTANCES BY USER
        print("Enter the minimum distance you want between fragments")
        dist = input("You can provide more than one separated by space: ")

        dists = []

        # CHECK FLOATS WERE GIVEN
        for i in dist.split():
            try:
                dists.append(float(i))
            except TypeError:
                sys.exit("Could not convert " + i + " into a float")

        # SEARCH FILES
        for path, File in Files:
            file_print(path, File, "Using")
            # ONLY HAPPEN ONCE FOR EACH XYZ
            sysData = systemData(path, File, True)
            expand(path, File, sysData, dists)

    # INTERACTION ENERGY
    elif task == 'B':

        from separate import separate_mols

        # MAKE SURE CORRECT FRAGMENTATION
        check_frags  = True
        level        = False                   # NO LEVELS

        if not Files:
            file_pattern = ['.xyz']            # FILES TO CHECK
            Files        = find_files(path, level, file_pattern)
            if len(Files) == 0:
                noFiles()

        # SEARCH FILES
        for path, File in Files:
            use = True
            skip = ['anion', 'cation', 'unknown', 'neutral']
            for i in skip:
                if i in File:
                    use = False

            if use:
                print('-'*40)
                file_print(path, File, "Using")
                # ONLY HAPPEN ONCE FOR EACH XYZ
                sysData = systemData(path, File, check_frags)
                separate_mols(path, File, sysData)

    elif task == 'C':
        from extras import get_fluorescence_data
     
        task = input('                                    \n\
                          1. Fluorescence Data            \n\
                                                           Task: ')
        if task == '1' or task == "":
            get_fluorescence_data()

    # CHECK COMPLETED JOBS
    elif task == '10':
        from supercomp import host, rjn_q

        if os.path.exists(os.path.expanduser('~/sub.txt')):

            to_write = []
            to_save  = []

            jobs = open(os.path.expanduser('~/sub.txt'), 'r+').readlines()
            hw = host()

            if hw == "rjn":

                queDicts = rjn_q()

                for job in jobs:
                    found = False
                    for jobDict in queDicts:
                        # CHECK IF FILES IN SAVED ARE IN QUEUE
                        #print(job)
                        #print(jobDict['id'])
                        if jobDict['id'] in job:
                            # IF FINISHED WRITE TO SAVE FILE
                            to_write.append(job)
                            found = True
                            #print('TRUE')
                            #print(jobDict['status'])
                            if jobDict['status'] == 'Q':
                                print('QUEUED\t' + job.replace('\n',''))

                            elif jobDict['status'] == 'R':
                                print('RUNNIN\t' + job.replace('\n',''))

                    if not found:
                        print('FINISH\t' + job.replace('\n',''))
                        to_save.append(job)

                write = input('Remove data of completed jobs (y/n)? ')

                if write == 'y' or write == 'Y':

                    # REWRITE FILE WITHOUT FINISHED JOBS
                    f = open(os.path.expanduser('~/sub.txt'), 'w+')
                    for line in to_write:
                        f.write(line)
                    f.close()

                    # WRITE FINISHED JOBS INTO NEW FILE
                    f = open(os.path.expanduser('~/jobLog.txt'), 'w+')
                    for line in to_save:
                        f.write(line)
                    f.close()

