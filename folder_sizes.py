#!/usr/bin/env python3

import subprocess

def human_readable_sizes(dirs):
    """
    Returns a dictionary with folders as keys and folder sizes as
    values in a nested dictionary value. Folder sizes found using
    `du -h -d 1`, or if `-d` is not supported with the version of 
    du installed, `du -h --max-depth=1` (GNU vs BSD).
    """
    try:
        readable = subprocess.run(['du', '-h', '-d', '1'], encoding = 'utf-8',
                   stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        readable = readable.stdout.split('\n')[:-1]

        for line in readable[:-1]:
            if 'Operation not permitted' not in line:
                size, folder = line.split('\t')
                folder = folder[2:]
                dirs[folder] = {'readable': size.strip()}

    except ValueError:
        readable = subprocess.run(['du', '-h', '--max-depth=1'], encoding = 'utf-8',
                   stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        readable = readable.stdout.split('\n')[:-1]

        for line in readable[:-1]:
            if 'Operation not permitted' not in line:
                size, folder = line.split('\t')
                folder = folder[2:]
                dirs[folder] = {'readable': size.strip()}

    total_size = readable[-1].split('\t')[0].strip()
    return dirs, total_size

def readable_to_comparable(dirs):
    """
    Saves having to call `du -d 1` to get the sizes in terms of blocks.
    Instead, parse the output of the `du` command once, then convert size
    to a floating point value and use that to sort folders.
    """
    byte_sizes = {
        'B': 10 ** 0, 
        'K': 10 ** 3,  # kilo  
        'M': 10 ** 6,  # mega  
        'G': 10 ** 9,  # giga  
        'T': 10 ** 12, # tera   
        'P': 10 ** 15, # penta  
    }

    for k, v in dirs.items():
        value = v['readable']
        value = float(value[:-1]) * byte_sizes[value[-1]]
        v['size'] = value
    return dirs

def folder_owners(dirs):
    """
    Adds the owner of each folder to the output of `folder_sizes` or
    `human_readable_sizes`.
    """
    owners = subprocess.run(['ls', '-la'], encoding = 'utf-8', stdout = subprocess.PIPE)
    owners = owners.stdout.split('\n')[1:] # remove total = ...

    for line in owners[:-1]:
        line   = line.split()
        owner  = line[2]
        folder = line[-1]
        for k, v in dirs.items():
            if folder == k:
                v['owner'] = owner
    return dirs

def sort_dict_by_size(dirs):
    """
    Returns a sorted list, largest folder first.
    """
    lst = []
    for k, v in dirs.items():
        lst.append([k, int(v['size'])])

    lst = sorted(lst, key = lambda kv: kv[1], reverse = True)

    return lst

def print_table(dirs, lst, total):
    """
    Print results, using the list of folders sorted
    by size. The first column of the table is 
    reponsive to match the longest folder name,
    avoiding any strange loooking tables with lines of 
    different lengths.
    """
    longest_folder_name = max(dirs.keys(), key = len)
    folder_col_size = len(longest_folder_name)
    length_dashes = folder_col_size + 31
    print('+' + '-' * length_dashes + '+')
    print("| {:^{}} | {:^{}} | {:^{}} |".format(
        'Folder', folder_col_size,
        'Owner', 15, 
        'Size', 8))
    print('+' + '-' * length_dashes + '+')
    for d in lst:
        folder, size = d
        try:
            print("| {:^{}} | {:^{}} | {:^{}} |".format(
                folder, folder_col_size,
                dirs[folder]['owner'], 15, 
                dirs[folder]['readable'], 8))
        except KeyError:
            continue
    print('+' + '-' * length_dashes + '+')
    print(f"\nTotal size: {total}")

def print_disclaimer():
    """
    The shell command `du` can take a long time
    to find all folder sizes if directory is large.
    """
    print("""\
This may take a while...

Calling the shell `du` command will 
take a while if the directory is large.

""")

def main():
    print_disclaimer()
    dirs = {}
    dirs, total = human_readable_sizes(dirs)
    dirs = folder_owners(dirs)
    dirs = readable_to_comparable(dirs)
    lst = sort_dict_by_size(dirs)
    print_table(dirs, lst, total)

if __name__ == '__main__':
    main()
