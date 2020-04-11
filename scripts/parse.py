#################################################
##              Scope: Host system             ##
#################################################
import os, argparse

def parse_port(port):
    """ Parse a port number

    Arguments:
        port {string} -- Port number as string.

    Raises:
        argparse.ArgumentTypeError: If the port number is invalid

    Returns:
        int -- Port as integer
    """

    try:
        if 1 <= int(port) <= 65535:
            return int(port)
        else:
            raise argparse.ArgumentTypeError("Error: Invalid parameter for port argument")
    except ValueError:
        raise argparse.ArgumentTypeError("Error: Invalid parameter for port argument")

def parse_arguments():
    """ Parse the shell arguments

    Raises:
        argparse.ArgumentTypeError: If there are invalid arguments or parameters
    Returns:
        Namespace -- Namespace containing all shell arguments
    """

    ## Get the shell arguments
    args = argparse.Namespace()
    parser = argparse.ArgumentParser(description='Syno-Index server')
    parser.add_argument('-e','--hostport', help='Host port for the Syno-Index server', type=parse_port)
    parser.add_argument('-d','--dockerport', help='Docker port for the Syno-Index server', type=parse_port)
    parser.add_argument('-l','--log', help='server log directory path', required=True)
    args = parser.parse_args()

    ## Check whether only one port is passed
    if (args.dockerport != None and args.hostport != None):
        raise argparse.ArgumentTypeError("Error: Server can only run on one interface")

    ## Parse the log file
    if not os.path.isdir(args.log):
        argparse.ArgumentTypeError("Error: Invalid parameter for argument \"--log\"")
    server_log = os.path.join(args.log, "server.log")
    if not os.path.isfile(server_log): open(server_log, 'a').close()
    args.log = server_log
    return args