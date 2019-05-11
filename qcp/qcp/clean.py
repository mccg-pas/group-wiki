### SED FILES WITH SOME EXTENSION
def sed(path):
    import re, sys
    import subprocess as sp
    from general import find_files

    print("Changes separated by &, any spaces will be included in the sed")
    ext = input("Only sed files with extention  [all]: ")
    old = input("Change text in files from           : ")
    new = input("Change text in files to             : ")
    num = input("Number of levels down to change[all]: ")

    ext = ext or '*'
    if ext == 'all':
        ext = '*'
    ext = re.split('&', ext)

    old = re.split('&', old)
    new = re.split('&', new)

    if len(old) != len(new):
        sys.exit("Length of changes not equal. Exiting...")

    # DEFAULT False
    num = num or 100
    if num == 'all':
        num = 100
    # CONVERT NUMBER STR TO INT
    if type(num) == str:
        num = int(num)

    if old == ['']:
        sys.exit('As you have not identified anything to substitute the text\n'\
        +        'to.  Exiting...')

    files = find_files(path, num, ext)

    for path, File in files:
        print("Using: ", File)
        File = path + File
        lines = ''
        with open(File, 'r+') as read:
            for line in read:
                for ii, jj in zip(old, new):
                    if ii in line:
                        linei = line
                        line  = line.replace(ii, jj)
                        print("Changed:", linei + "to     :", line)
                    lines += line
        open(File, 'w+').write(lines)


### RENAME FILES IN FOLDER
def rename(path):
    import re, sys
    import subprocess as sp
    from general import find_files

    sp.call('ls')

    ext = input("Only rename files with extention[all]: ")
    old = input("Part of name to replace              : ")
    new = input("Replace with                         : ")
    num = input("Number of levels down to change [all]: ")

    ext = ext or '*'
    if ext == 'all':
        ext = '*'
    ext = re.split(' |,', ext)

    # DEFAULT False
    num = num or 100
    if num == 'all':
        num = 100
    # CONVERT NUMBER STR TO INT
    if type(num) == str:
        num = int(num)

    if old == '':
        sys.exit('As you have not identified anything to substitute the text\n'\
        +        'to - system exit as assuming user made a mistake')

    files = find_files(path, num, ext)

    for path, File in files:
        if old in File:
            name = File.replace(old, new)
            print("Renaming ", path+File, path+name)
            sp.call('mv ' + path+File + ' ' + path+name, shell=True)


### DELETE NUMBER OF JOBS FROM BOTTOM OF QUEUE
def deleteJob():
    import re, sys
    import subprocess as sp
    from   supercomp import host

    que = []
    IDs_list = []
    nms_list = []
    dict_IDs = {}
    toDel_list = []

    user = sp.Popen("echo $USER", shell=True, stdout=sp.PIPE).stdout
    user = user.read().decode("utf-8").split()[0]

    hw = host()

    if hw == 'rjn':
        # GET QUEUE
        print('Waiting for qstat from Raijin...')
        #print("qstat -u " + user)
        pipe = sp.Popen("qstat -u " + user, shell=True, stdout=sp.PIPE).stdout
        queue = pipe.read().decode("utf-8")
        queue = queue.split('\n')
        # REMOVE OTHER LINES
        for line in queue:
            if user in line:
                que.append(line)

        # PRINT FOR USER
        num_lin = len(que)
        for val, line in enumerate(que):
            print("{:5}{}".format(str(num_lin - val), line))

        # ASK USER NUMBER OF JOBS TO DELETE OR NAME
        typ = input("Delete by: 1: Number; 2: All; 3: Name; [Default=1] ")
        typ = typ or '1'

        # SAVE JOB NUMBERS AND NAMES
        for line in que:
            #print(que)
            ID = re.split(' |\.', line)
            ID = list(filter(None, ID))
            IDs_list.append(ID[0])
            nms_list.append(ID[4])
            dict_IDs[ID[0]] = ID[4]

        # IF DELETING BY NUMBER
        if typ == '1' or typ == '2':
            if typ == '2':
                sure = input('Are you sure you want to delete all jobs? (y/n) ')
                if sure == 'y':
                    n = len(IDs_list)
                else:
                    n = 0
            elif typ == '1':
                n = input("Number of jobs to delete from bottom of queue: ")

            # IF NO USER INPUT
            if not n:
                sys.exit("No user input given, exiting",)


            start = len(IDs_list) - int(n)
            finish = len(IDs_list)

            for i in range(len(IDs_list)):
                if start <= i < finish:
                    sp.call("qdel " + IDs_list[i], shell=True)
                    print("Removed " + IDs_list[i] + " from queue")

        # IF DELETING BY NAME
        elif typ == '3':
            subnm = input("Part of name unique to all jobs to delete: ")

            # FIND JOBS WITH NAME
            for ID, name in dict_IDs.items():
                if subnm in name:
                    print("To delete: ", name, ID)
                    toDel_list.append(ID)

            # DELETE
            toDel = input("Are you sure? y/n ")
            if toDel == 'y':
                for ID in toDel_list:
                    sp.call("qdel " + ID, shell=True)
                    print("Removed " + ID + " from queue")

    elif hw == 'mgs':
        print('Not written for magnus yet')

    elif hw == 'gai':
        print('Waiting for qstat from MCC...')

        pipe = sp.Popen("qstat -u " + user, shell=True, stdout=sp.PIPE).stdout
        queue = pipe.read().decode("utf-8")
        queue = queue.split('\n')
        # REMOVE OTHER LINES
        for line in queue:
            if user in line:
                que.append(line)

        # PRINT FOR USER
        num_lin = len(que)
        for val, line in enumerate(que):
            print("{:5}{}".format(str(num_lin - val), line))

        # ASK USER NUMBER OF JOBS TO DELETE OR NAME
        typ = input("Delete by: 1: Number; 2: All; 3: Name; [Default=1] ")
        typ = typ or '1'

        # SAVE JOB NUMBERS AND NAMES
        for line in que:
            #print(que)
            ID = re.split(' |\.', line)
            ID = list(filter(None, ID))
            IDs_list.append(ID[0])
            nms_list.append(ID[3])
            dict_IDs[ID[0]] = ID[3]

        # IF DELETING BY NUMBER
        if typ == '1' or typ == '2':
            if typ == '2':
                sure = input('Are you sure you want to delete all jobs? (y/n) ')
                if sure == 'y':
                    n = len(IDs_list)
                else:
                    n = 0
            elif typ == '1':
                n = input("Number of jobs to delete from bottom of queue: ")
            start = len(IDs_list) - int(n)
            finish = len(IDs_list)

            for i in range(len(IDs_list)):
                if start <= i < finish:
                    sp.call("qdel " + IDs_list[i], shell=True)
                    print("Removed " + IDs_list[i] + " from queue")

        # IF DELETING BY NAME
        elif typ == '3':
            subnm = input("Part of name unique to all jobs to delete: ")
            print(subnm)
            print(dict_IDs)
            # FIND JOBS WITH NAME
            for ID, name in dict_IDs.items():
                if subnm in name:
                    print("To delete: ", name, ID)
                    toDel_list.append(ID)

            # DELETE
            toDel = input("Are you sure? y/n ")
            if toDel == 'y':
                for ID in toDel_list:
                    sp.call("qdel " + ID, shell=True)
                    print("Removed " + ID + " from queue")
