#################################################
##              Scope: Host system             ##
#################################################
import os, sys, subprocess, logging, shutil

## Add the VS-Utils submodule to the python path
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, "VS-Utils"))
from files import create_path_directories

## Set the logger and its level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def server(source_host, output_host):
    """ Validate the incoming query and add it to the SynoIndex database.

    Arguments:
        source_host {string} -- Encoded path to the video file on the hostsystem.
        output_host {string} -- Encoded path to the converted video file on the
                                hostsystem. If it is set, move it to the destination.

    Returns:
        string -- Message whether the addition process was succesful or not.
    """

    ## Check whether the source file exists
    logger.debug("[!] Get new query with arguments: %s, %s" % (source_host, output_host))

    if not output_host:
        if not os.path.isfile(source_host):
            logger.error("[-] Error: File does not exist")
            return "[-] Error: File does not exist"

    ## Move the converted output file first if needed
    else:
        create_path_directories(os.path.dirname(source_host))
        shutil.move(output_host, source_host)
        if not os.path.isfile(source_host):
            logger.error("[-] Error: Moving file failed")
            return "[-] Error: Moving file failed"

    ## Add the file to synoindex database
    cmds = ['synoindex', '-A', source_host.encode('UTF-8')]
    logger.debug("synoindex -A %s " % source_host.encode('UTF-8'))
    p = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    p.communicate()
    logger.debug("[x] Executed query")
    logger.debug("")

    return "[x] Executed query"
