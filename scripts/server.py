#################################################
##              Scope: Host system             ##
#################################################
import os, sys, errno, fnmatch, subprocess, logging, shutil

## Set the logger and its level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def server_create_path(path):
    """ Create all directories along a given path.

    Arguments:
        path {string} -- Path to the directory.
    """

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

def server(source_host, output_host, delete_rar=False):
    """ Validate the incoming query and add it to the SynoIndex database.

    Arguments:
        source_host {string} -- Encoded path to the video file on the hostsystem.
        output_host {string} -- Encoded path to the converted video file on the
                                hostsystem. If it is set, move it to the destination.

    Returns:
        string -- Message whether the addition process was succesful or not.
    """

    ## Check whether the source file exists
    logger.debug("Source: %s" % source_host)
    logger.debug("Output: %s" , output_host)
    logger.debug("Delete-RAR: %s" , delete_rar)

    if not output_host:
        if not os.path.isfile(source_host):
            logger.error("[-] Error: File does not exist")
            return "[-] Error: File does not exist"

    ## Move the converted output file first if needed
    else:
        server_create_path(os.path.dirname(source_host))
        shutil.move(output_host, source_host)
        logger.debug("Moved file first")
        if not os.path.isfile(source_host):
            logger.error("[-] Error: Moving file failed")
            return "[-] Error: Moving file failed"
        if delete_rar:
            source_host_dir = os.path.curdir(source_host)
            rar_files = server_files_with_extension(source_host_dir, "rar")
            if rar_files:
                basename = [os.path.splitext(os.path.basename(r))[0] for r in rar_files][0]
                files = server_files_with_basename(source_host_dir, basename)
                original_file = [f for f in files if os.path.splitext(f)[1] in ["mkv", "mp4", "avi"]][0]
                os.remove(original_file)

    ## Add the file to synoindex database
    cmds = ['synoindex', '-A', source_host.encode('UTF-8')]
    logger.debug("Add video file to SynoIndex")
    p = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    p.communicate()
    logger.debug("[x] Executed query")
    logger.debug("")

    return "[x] Executed query"
