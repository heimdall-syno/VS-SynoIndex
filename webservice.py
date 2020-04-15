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
        return web.httpserver.runsimple(func, (ip, args.dockerport))

class HostWebserver(web.application):
    def run(self, port=args.hostport, *middleware):
        func = self.wsgifunc(*middleware)
        netifaces.ifaddresses('lo')
        ip = netifaces.ifaddresses('lo')[netifaces.AF_INET][0]['addr']
        return web.httpserver.runsimple(func, (ip, args.hostport))

class webservice:
    def GET(self, name):
        user_data = web.input(source_host="", output_host="", original="0")
        result = server(user_data.source_host, user_data.output_host,
                        user_data.original)
        return result

if __name__ == "__main__":

    ## Start the Syno-Index server instances
    urls = ('/(synoindex)', 'webservice')
    if (args.dockerport != None):
        app = DockerWebserver(urls, globals())
    else:
        app = HostWebserver(urls, globals())
    app.run()