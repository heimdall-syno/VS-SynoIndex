#################################################
##              Scope: Host system             ##
#################################################
import os, sys, web, logging

## Add the VS-Utils submodule to the python path
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, "VS-Utils"))
sys.path.append(os.path.join(cur_dir, "scripts"))
from parse import parse_cfg
from server import server

## Parse the config
config_file = os.path.join(cur_dir, "config.txt")
cfg = parse_cfg(config_file, "vs-synoindex", "host")

## Setup the logging files
server_log = "%s/%s" % (cfg.server_logs, "server.log")
client_log = "%s/%s" % (cfg.server_logs, "client.log")
if not os.path.isfile(server_log): open(server_log, 'a').close()
if not os.path.isfile(client_log): open(client_log, 'a').close()

## Setup the logging format
logging.basicConfig(filename=server_log, filemode='a',
					format='%(asctime)s - %(levelname)s: %(message)s')

## URLs
urls = (
	'/(synoindex)', 'webservice'
)

class Webserver(web.application):
	def run(self, port=cfg.port, *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, (cfg.ip, cfg.port))

class webservice:
	def GET(self, name):
		user_data = web.input(source_host="", output_host="")
		result = server(user_data.source_host, user_data.output_host)
		return result

if __name__ == "__main__":
	app = Webserver(urls, globals())
	app.run()