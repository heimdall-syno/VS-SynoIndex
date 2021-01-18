#################################################
##              Scope: Host system             ##
#################################################
import os, sys, web, logging
import socket, fcntl, struct

## Add the scripts subdirectory to the python path
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, "scripts"))
from server import server
from parse import parse_arguments

## Parse the shell arguments
args = parse_arguments()
logging.basicConfig(filename=args.log, filemode='a', format='[%(asctime)s] Server - %(levelname)s: %(message)s')

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15], 'utf-8')))[20:24])

class DockerWebserver(web.application):
    def run(self, port=args.dockerport, *middleware):
        func = self.wsgifunc(*middleware)
        ip = get_ip_address('docker0')
        try:
            web.httpserver.runsimple(func, (ip, args.dockerport))
        except OSError:
            exit("Error: Port is already in use")
        return

class HostWebserver(web.application):
    def run(self, port=args.hostport, *middleware):
        func = self.wsgifunc(*middleware)
        ip = get_ip_address('lo')
        try:
            web.httpserver.runsimple(func, (ip, args.hostport))
        except OSError:
            exit("Error: Port is already in use")
        return

class webservice:
    def GET(self, name):
        query = web.input(source_host="", output_host="", original_host="", original_mode="0")
        result = server(query.source_host, query.output_host, query.original_host, query.original_mode)
        return result

if __name__ == "__main__":

    ## Start the Syno-Index server instances
    urls = ('/(synoindex)', 'webservice')
    if (args.dockerport != None):
        app = DockerWebserver(urls, globals())
    else:
        app = HostWebserver(urls, globals())
    app.run()