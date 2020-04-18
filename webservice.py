#################################################
##              Scope: Host system             ##
#################################################
import os, sys, web, netifaces, logging

## Add the scripts subdirectory to the python path
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, "scripts"))
from server import server
from parse import parse_arguments

## Parse the shell arguments
args = parse_arguments()
logging.basicConfig(filename=args.log, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')

class DockerWebserver(web.application):
    def run(self, port=args.dockerport, *middleware):
        func = self.wsgifunc(*middleware)
        netifaces.ifaddresses('docker0')
        ip = netifaces.ifaddresses('docker0')[netifaces.AF_INET][0]['addr']
        try:
            web.httpserver.runsimple(func, (ip, args.dockerport))
        except OSError:
            exit("Error: Port is already in use")
        return

class HostWebserver(web.application):
    def run(self, port=args.hostport, *middleware):
        func = self.wsgifunc(*middleware)
        netifaces.ifaddresses('lo')
        ip = netifaces.ifaddresses('lo')[netifaces.AF_INET][0]['addr']
        try:
            web.httpserver.runsimple(func, (ip, args.dockerport))
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