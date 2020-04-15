#################################################
##              Scope: Host system             ##
#################################################
import os, sys, errno, fnmatch, subprocess, logging, shutil
from subprocess import Popen, PIPE

## Set the logger and its level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def server_parse_dig(dig, imin, imax):
    ''' Parse a digit '''

    try:
        if imin <= int(dig) <= imax: return int(dig)
        else: logger.error("Invalid original value"); exit()
    except ValueError:
        logger.error("Invalid original value"); exit()

def server_create_path(path):
    ''' Create all directories along a given path. '''

    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path): pass
        else: raise

def server_files_with_extension(path, ext):
    ''' Find all files in a path with a given file extension. '''

    files = []
    if os.path.isfile(path):
        path_ext = os.path.splitext(path)[1].split(".")[-1]
        if (path_ext in ext and "sample" not in os.path.basename(path)):
            return [path]
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "*.%s" % ext):
            if ("sample" not in filename):
                files.append(os.path.join(root, filename))
    return files

def server_files_with_basename(path, basename):
    ''' Find all files in a path with a given file basename. '''

    files = []
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "%s.*" % basename):
            if ("sample" not in filename):
                files.append(os.path.join(root, filename))
    return files

def synoindex_file_add(filename):
    ''' Add the converted file to synoindex database. '''

    cmds = ['synoindex', '-a', filename.encode('UTF-8')]
    logger.debug("Add video file to SynoIndex: {}".format(filename))
    process = Popen(cmds, stdout=PIPE, stderr=PIPE)
    process.communicate()

def synoindex_file_delete(filename):
    ''' Add the converted file to synoindex database. '''

    cmds = ['synoindex', '-d', filename.encode('UTF-8')]
    logger.debug("Delete video file from SynoIndex: {}".format(filename))
    process = Popen(cmds, stdout=PIPE, stderr=PIPE)
    process.communicate()

def server_oldfile_delete(source_host, output_host):
    old_file = os.path.join(os.path.curdir(source_host), os.path.basename(output_host))
    if os.path.isfile(old_file):
        synoindex_file_delete(old_file)

def server(source_host, output_host, original):
    """ Validate the incoming query and add it to the SynoIndex database.

    Arguments:
        source_host {string} -- Encoded path to the video file on the hostsystem.
        output_host {string} -- Encoded path to the converted video file on the
                                hostsystem. If it is set, move it to the destination.

    Returns:
        string -- Message whether the addition process was succesful or not.
    """

    ## Parse the original
    original = server_parse_dig(original, 1, 3)

    ## Check whether source file exists
    logger.debug("Source: {}, Output: {}, Original: {}".format(source_host, output_host, original))

    ## VS-Transmission - No converted output file -> add the source file and ignore original
    if not output_host:
        if not os.path.isfile(source_host):
            logger.error("Source File does not exist anymore")
            return "Source File does not exist anymore"
        synoindex_file_add(source_host)
        return "Query executed"

    ## Move the converted output file first if needed
    server_create_path(os.path.dirname(source_host))
    shutil.move(output_host, source_host)
    logger.debug("Move and rename source file before indexing it")
    if not os.path.isfile(source_host):
        logger.error("Moving and renaming file failed")
        return "Error: Moving and renaming file failed"

    if original == 0: ## (Leave) The source file remains unchanged -> add the converted file
        pass

    elif original == 1: ## (Ignore) The source file remains unchanged but not synoindexed.
        server_oldfile_delete(source_host, output_host)

    elif (original == 2 or original == 3): ## (Delete) If extracted from RAR archive delete the source file.
        source_host_dir = os.path.curdir(source_host)
        rar_files = server_files_with_extension(source_host_dir, "rar")
        if rar_files:
            rar_file = [os.path.splitext(os.path.basename(r))[0] for r in rar_files][0]
            process = Popen(["unrar", "lb", rar_file], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0 and stdout:
                for rar_output in stdout.split("\n"):
                    rar_output = os.path.join(source_host_dir, rar_output)
                    if os.path.isfile(rar_output):
                        os.remove(rar_output)
            else:
                logger.debug("Nothing deleted due to unrar failed: {}, {}".format(process.returncode, stderr))

        elif (original == 3): ##  (Ignore|Delete): If extracted from RAR archive delete it otherwise ignore it.
            server_oldfile_delete(source_host, output_host)

    synoindex_file_add(source_host)
    return "Query executed"
