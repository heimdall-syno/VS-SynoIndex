#################################################
##              Scope: Host system             ##
#################################################
import os, sys, subprocess, logging

## Set the logger and its level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def server(cfg, filepath):
    """ Validate the incoming query and add it to the SynoIndex database.

    Arguments:
        cfg {Namspace} -- Configuration Namespace.
        filepath {string} -- Encoded path to the video file on the hostsystem.

    Returns:
        string -- Message whether the addition process was succesful or not.
    """

    logger.debug("[!] Get new query with arguments: %s" % filepath)
    if not os.path.isfile(filepath):
        logger.error("[-] Error: File does not exist")
        return "[-] Error: File does not exist"

    cmds = ['synoindex', '-A', filepath.encode('UTF-8')]
    logger.debug("synoindex -A %s " % filepath.encode('UTF-8'))
    p = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    p.communicate()
    logger.debug("[x] Executed query")
    logger.debug("")
    return "[x] Executed query"
