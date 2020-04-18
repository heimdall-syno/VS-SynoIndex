#################################################
##              Scope: Host system             ##
#################################################
import os, sys, errno, fnmatch, subprocess, logging, shutil, glob
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
    ''' Find all files in a given path matching one or more extensions. '''

    exts = ext if isinstance(ext, str) else tuple(ext)

    ## if the passed path is a single file
    if os.path.isfile(path) and path.endswith(exts):
        if ("sample" not in os.path.basename(path)):
            return [path]

    ## If the passed path is a directory then search all files recursively
    ext_files = []
    for filename in glob.iglob(os.path.join(path, '') + '**/*', recursive=True):
        if os.path.isfile(filename) and filename.endswith(exts):
            if ("sample" not in filename):
                ext_files.append(filename)
    return sorted(ext_files)

def server_files_with_basename(path, basename):
    ''' Find all files in a path with a given file basename. '''

    files = []
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "%s.*" % basename):
            if ("sample" not in filename):
                files.append(os.path.join(root, filename))
    return files

def server_file_delete(directory, filename):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        logger.debug("Delete the RAR archive output file: {}".format(file_path))
        return True

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

def synoindex_oldfile_delete(original_file):
    logger.debug("Old file: {}".format(original_file))
    if os.path.isfile(original_file):
        synoindex_file_delete(original_file)

def server(target_file, move_from, original_file, original_mode):
    """ Validate the incoming query and add it to the SynoIndex database.

    Arguments:
        target_file {string}    -- Source file which will be added to the synoindex.
                                   If move_from is also set, it is the destination
                                   of the move_from file. It is added to the synoindex.
        move_from {string}      -- Path to the converted video file on the hostsystem.
        original_file {string}  -- Path to the original file which was converted.
        original_mode {string}  --  Mode, which specifies how the original is handled.

    Returns:
        string -- Message whether the addition process was succesful or not.
    """

    ## Print the current query
    logger.debug("-" * 25)
    logger.debug("Target: {}".format(target_file))
    logger.debug("Handbrake Output: {}".format(move_from))
    logger.debug("Original: {}".format(original_file))
    logger.debug("Original mode: {}".format(original_mode))

    ## Parse the original
    original_mode = server_parse_dig(original_mode, 0, 3)

    ## VS-Transmission - Nothing to move first - add the file
    if move_from == None or move_from == "":
        if not os.path.isfile(target_file):
            logger.error("Source File does not exist anymore")
            return "Source File does not exist anymore"
        synoindex_file_add(target_file)
        logging.debug("Query executed")
        return "Query executed"

    ## Move the handbrake output file first if needed
    target_file_dir = os.path.dirname(target_file)
    server_create_path(target_file_dir)
    shutil.move(move_from, target_file)
    logger.debug("Move and rename source file before indexing it")
    if not os.path.isfile(target_file):
        logger.error("Moving and renaming file failed")
        return "Error: Moving and renaming file failed"

    if original_mode == 0: ## (Leave) The source file remains unchanged -> add the converted file
        pass

    elif original_mode == 1: ## (Ignore) The source file remains unchanged but not synoindexed.
        synoindex_oldfile_delete(original_file)

    elif (original_mode == 2 or original_mode == 3): ## (Delete) If extracted from RAR archive delete the source file.
        rar_files = server_files_with_extension(target_file_dir, "rar")
        if rar_files:
            rar_file = rar_files[0]
            logger.debug("Found a RAR archive in the source directory: {}".format(rar_file))
            process = Popen(["unrar", "lb", rar_file], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0 and stdout:
                rar_outputs = list(filter(None, stdout.decode("UTF-8").split("\n")))
                deleted = [server_file_delete(target_file_dir, rar_output) for rar_output in rar_outputs]
                if not deleted: logger.debug("Nothing deleted due to none of the output files exist")
            else:
                logger.debug("Nothing deleted due to unrar failed: {}, {}".format(process.returncode, stderr))

        elif (original_mode == 3): ##  (Ignore|Delete): If extracted from RAR archive delete it otherwise ignore it.
            synoindex_oldfile_delete(original_file)

    synoindex_file_add(target_file)
    logging.debug("Query executed")
    return "Query executed"
