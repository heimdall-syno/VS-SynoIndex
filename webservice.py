import os, web, logging
from server import server
from parse import parse_cfg

## Parse the config
config_file = os.path.dirname(os.path.abspath(__file__)) + '/config.txt'
cfg = parse_cfg(config_file, "server")

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
		user_data = web.input(option="", filepath="")
		result = server(cfg, user_data.option, user_data.filepath)
		return result

if __name__ == "__main__":
	app = Webserver(urls, globals())
	app.run()