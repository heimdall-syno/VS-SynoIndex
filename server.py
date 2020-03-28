#################################################
##              Scope: Host system             ##
#################################################
import os, sys, subprocess, logging, shutil

## Add the VS-Utils submodule to the python path
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, "VS-Utils"))
from files import create_path_directories, files_find_ext
from files import files_find_basename

## Set the logger and its level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
        create_path_directories(os.path.dirname(source_host))
        shutil.move(output_host, source_host)
        logger.debug("Moved file first")
        if not os.path.isfile(source_host):
            logger.error("[-] Error: Moving file failed")
            return "[-] Error: Moving file failed"
        if delete_rar:
            cur_dir = os.path.curdir(source_host)
            rar_files = files_find_ext(cur_dir, "rar")
            if rar_files:
                basename = [os.path.splitext(os.path.basename(r))[0] for r in rar_files][0]
                files = files_find_basename(cur_dir, basename)
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
