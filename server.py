import os, sys, subprocess, logging
from parse import parse_cfg, validate_input

## Set the logger and its level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def server(cfg, option, filepath):
    ''' Validate the query, get all media infos and add it. '''

    logger.debug("[!] Get new query with arguments: %s, %s" %(option, filepath))
    ## Read input
    filepath = validate_input(cfg.mapping, option, filepath)
    if(filepath == -1):
        logger.error("[-] Error: Option not supported")
        return "[-] Error: Option not supported"
    if(filepath == -2):
        logger.error("[-] Error: Filepath seems invalid")
        return "[-] Error: Filepath seems invalid"

    cmds = ['synoindex', '-A', filepath.encode('UTF-8')]
    logger.debug("synoindex -A %s " % filepath.encode('UTF-8'))
    p = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    output, _ = p.communicate()
    logger.debug("[x] Executed query")
    logger.debug("")
    return "[x] Executed query"
