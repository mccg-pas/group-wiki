
# GET WHICH SUPERCOMPUTER
def host():
    """ Return host machine name. """
    import sys
    import subprocess as sp

    hw = False

    hostName = sp.getoutput("hostname")

    hostDict = {'raijin': 'rjn', 'msgln': 'gai', 'm3': 'mas',
                'magnus': 'mgs', 'monarch': 'mon',
                'stampede': 'stm'}

    for key, value in hostDict.items():
        if key in hostName:
            hw = value

    #try:
    #    hw
    #except:
    #    sys.exit("Could not identify host")

    return hw

# GET QUEUE OF USER
def get_queue(cmd):
    """Get queue of supercomputer
       and return it in queue var.
    """
    import sys, os
    import subprocess as sp

    # GET QUEUE
    print('Waiting for queue from system...')
    pipe  = sp.Popen(cmd, shell=True, stdout=sp.PIPE).stdout
    queue = pipe.read().decode("utf-8")
    queue = queue.split('\n')
    return queue


def rjn_q():
    import re
    import subprocess as sp

    queDicts = []

    user  = sp.getoutput("echo $USER")
    queue = get_queue("qstat -u " + user)

    i = 1
    for line in queue:
      if user in line:
        line = re.split(' |\.r-man2', line)
        line = list(filter(None, line))

        temp_dict           = {'id' : line[0]}
        temp_dict['num']    = i
        temp_dict['user']   = line[1]
        temp_dict['queue']  = line[2]
        temp_dict['name']   = line[3]
        temp_dict['sessid'] = line[4]
        temp_dict['nodes']  = line[5]
        temp_dict['cpus']   = line[6]
        temp_dict['mem']    = line[7]
        temp_dict['wtime']  = line[8]
        temp_dict['status'] = line[9]
        temp_dict['rtime']  = line[10].split('\n')[0]

        queDicts.append(temp_dict)
        i += 1

    return queDicts


def gai_q():
    import subprocess as sp

    queDicts = []

    user  = sp.getoutput("echo $USER")
    queue = get_queue("qstat")

    i = 1
    for line in queue:
      if user in line:
        line = line.split()
        # SOMETIMES #7 QUEUE IS NOT SHOWN
        temp_dict           = {'id' : line[0]}
        temp_dict['num']    = i
        temp_dict['name']   = line[2]
        temp_dict['user']   = line[3]
        temp_dict['status'] = line[4]
        temp_dict['start']  = line[5] + ' ' + line [6]
        temp_dict['cpus']   = line[-1]
        temp_dict['nodes']  = int(line[-1])/16

        queDicts.append(temp_dict)
        i += 1

    return queDicts


def mgs_q():
    import subprocess as sp

    queDicts = []

    user  = sp.getoutput("echo $USER")
    queue = get_queue("squeue -u " + user)

    i = 1
    for line in queue:
      if user in line:
        line = line.split()

        temp_dict           = {'id' : line[0]}
        temp_dict['num']    = i
        temp_dict['user']   = line[1]
        temp_dict['accou']  = line[2]
        temp_dict['name']   = line[3]
        temp_dict['status'] = line[5]
        temp_dict['start']  = line[6]
        temp_dict['nodes']  = line[10]

        queDicts.append(temp_dict)
        i += 1

    return queDicts

def stm_q():
    import subprocess as sp

    queDicts = []

    user  = sp.getoutput("echo $USER")
    queue = get_queue("squeue -u " + user)

    i = 1
    for line in queue:
      if user in line:
        line = line.split()

        temp_dict           = {'id' : line[0]}
        temp_dict['num']    = i
        temp_dict['queue']  = line[1]
        temp_dict['name']   = line[2]
        temp_dict['user']   = line[3]
        temp_dict['status'] = line[4]
        temp_dict['time']   = line[5]
        temp_dict['nodes']  = line[6]

        queDicts.append(temp_dict)
        i += 1

    return queDicts


def mas_q():
    import subprocess as sp

    queDicts = []

    user  = sp.getoutput("echo $USER")
    queue = get_queue("squeue -u " + user)

    i = 1
    for line in queue:
      if user in line:
        line = line.split()

        temp_dict           = {'id' : line[0]}
        temp_dict['num']    = i
        temp_dict['name']   = line[2]
        temp_dict['user']   = line[3]
        temp_dict['status'] = line[4]
        temp_dict['time']   = line[5]
        temp_dict['nodes']  = line[6]

        queDicts.append(temp_dict)
        i += 1

    return queDicts

def mon_q():
    import subprocess as sp

    queDicts = []

    user  = sp.getoutput("echo $USER")
    queue = get_queue("squeue -u " + user)

    i = 1
    for line in queue:
      if user in line:
        line = line.split()

        temp_dict           = {'id' : line[0]}
        temp_dict['num']    = i
        temp_dict['name']   = line[2]
        temp_dict['user']   = line[3]
        temp_dict['status'] = line[4]
        temp_dict['time']   = line[5]
        temp_dict['nodes']  = line[6]

        queDicts.append(temp_dict)
        i += 1

    return queDicts



### DELETE NUMBER OF JOBS FROM BOTTOM OF QUEUE
def deleteJob():
    import re, sys
    import subprocess as sp

    hw = host()

    if not hw:
        sys.exit('Could not resolve hostname. Exiting...')

    # GET QUEUE FROM APPROPRIATE FUNCTION
    call_q = {
             'rjn' : rjn_q,
             'gai' : gai_q,
             'mgs' : mgs_q,
             'mas' : mas_q,
             'mon' : mon_q,
             'stm' : stm_q
             }

    queDicts = call_q[hw]()
    #print(queDicts)
    # PRINT NUMBERS COUNTING UP FROM BOTTOM
    num_jobs = len(queDicts)

    # PRINT HEADER
    print('\n{:4}  {:10}  {:18} {:10} {:5}'.format('   #', 'ID', 'Name', 'Status', 'Nodes'))
    print('-'*54)
    for jobD in queDicts:
        # PRINT NUMBERS COUNTING UP FROM BOTTOM
        print('{:4}  {:10}  {:18} {:10} {:5}'.format(
            num_jobs + 1 - jobD.get('num'),
            jobD.get('id'),
            jobD.get('name'),
            jobD.get('status'),
            jobD.get('nodes')
            ))
    print('\n')

    # ASK USER NUMBER OF JOBS TO DELETE OR NAME
    typ = input("Delete by: 1: Number; 2: All; 3: Name; [Default=1] ")
    typ = typ or '1'

    # IF DELETING BY NUMBER
    if typ == '1' or typ == '2':
        if typ == '2':
            sure = input('Are you sure you want to delete all jobs? (y/n) ')
            if sure == 'y':
                n = num_jobs
            else:
                sys.exit('Exiting...')
        elif typ == '1':
            n = int(input("Number of jobs to delete from bottom of queue: "))

        # READ LIST OF DICTS BACKWARDS
        for val, jobD in enumerate(reversed(queDicts)):
            if val < n:
                if hw is 'rjn' or hw is 'gai':
                    sp.call("qdel "  + jobD['id'], shell=True)
                    print("Removed " + jobD['id'] + " from queue")
                elif hw is 'mgs' or hw is 'mas' or hw is 'stm' or hw is 'mon':
                    sp.call("scancel "  + jobD['id'], shell=True)
                    print("Removed "    + jobD['id'] + " from queue")
                # elif hw is 'mon':
                    # sp.call("scancel "  + jobD['id'], shell=True)
                    # print("Removed "    + jobD['id'] + " from queue")

    # IF DELETING BY NAME
    elif typ == '3':

        namePart = input("Part of name unique to all jobs to delete: ")

        # FIND JOBS WITH NAME
        toDel_list = []
        for jobD in queDicts:
            if namePart in jobD['name']:
                print("To delete: ", jobD['name'], jobD['id'])
                toDel_list.append(jobD['id'])

        # DELETE
        toDel = input("Are you sure? [y/n] ")
        if toDel == 'y':
            for ID in toDel_list:
                if hw is 'rjn' or hw is 'gai':
                    sp.call("qdel "  + ID, shell=True)
                    print("Removed " + ID + " from queue")

                elif hw is 'mgs' or hw is 'mas' or hw is 'mon' or hw is 'stm':
                    sp.call("scancel "  + ID, shell=True)
                    print("Removed "    + ID + " from queue")
        else:
            sys.exit('Exiting...')



def submit(File):
    import os, time
    import subprocess as sp

    hw = host()

    if hw == 'rjn':
        ID = sp.check_output(['qsub', File]).decode("utf-8").split('.')[0]
        print("Submitted: {:8}{}".format(ID, File))
        # SAVE SUBMIT DATA
        with open(os.path.expanduser('~/sub.txt'), 'a') as f:
            date = time.strftime("%d/%m/%Y")
            Time = time.strftime("%H:%M:%S")
            npath = os.getcwd()
            f.write('{:12}{:10}{:8} {:30}  {}\n'.format(date, Time, ID, File, npath))
    elif hw == 'stm':
        ID = sp.check_output(['sbatch', File]).decode("utf-8").strip().split(' ')[-1]
        print("Submitted: {:8}{}".format(ID, File))
    elif hw == 'mgs':
        ID = sp.check_output(['sbatch', File]).decode("utf-8").strip().split(' ')[3]
        print("Submitted: {:8}{}".format(ID, File))
    elif hw == 'mas':
        ID = sp.check_output(['sbatch', File]).decode("utf-8").strip().split(' ')[3]
        print("Submitted: {:8}{}".format(ID, File))
    elif hw == 'gai':
        ID = sp.check_output(['qsub', File]).decode("utf-8").strip().split(' ')[2]
        print("Submitted: {:8}{}".format(ID, File))
    elif hw == 'mon':
        ID = sp.check_output(['sbatch', File]).decode("utf-8").strip().split(' ')[3]
        print("Submitted: {:8}{}".format(ID, File))
