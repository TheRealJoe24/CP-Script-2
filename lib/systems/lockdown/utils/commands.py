import subprocess, os

def run_command(command: str, ip=None):
    ''' Run command and return output. Answer from https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output. '''
    result = subprocess.run(command.split(
        ' '), stdout=subprocess.PIPE, input=ip)
    return result.stdout.decode('utf-8')


def search_from(root_dir: str, ext: str):
    ''' Run a search from root_dir for *.ext. Returns touple: list of directories in JSON format: { dir: [files_in_dir.ext] }, raw list of paths '''
    directories = []
    ext_format = ".{ext}".format(ext=ext)
    # loop through all directories starting with root
    for root, dirs, f in os.walk(root_dir):
        files = []  # list of files which end with *.ext in current directory
        for file in f:
            if file.lower().endswith(ext_format):
                files.append(file)
        if len(files) > 0:
            directories.append({
                root: files
            })
    raw_list = []
    for dir in directories:
        for root in dir:  # will only go once
            files = dir[root]
            for file in files:
                raw_list.append(root + '/' + file)

    return directories, raw_list
