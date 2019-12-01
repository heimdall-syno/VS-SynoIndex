#################################################
##           Scope: Docker-Container           ##
#################################################
import os, sys, urllib, urllib2, logging

## Add the VS-Utils submodule to the python path
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, "VS-Utils"))
from parse import parse_cfg

### Synoindex-Client
def client(source_host, output_host=None):

	## Parse the config
	config_file = os.path.join(cur_dir, "config.txt")
	cfg = parse_cfg(config_file, "vs-synoindex", "docker")

	## Setup the client logging file
	client_log = "%s/%s" % (cfg.client_logs, "client.log")
	logging.basicConfig(filename=client_log, filemode='a',
						format='%(asctime)s - %(levelname)s: %(message)s')

	## Set the logger and its level
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	## Call the url and get the answer of the server
	if not output_host:
		query_vars = {'source_host': source_host}
	else:
		query_vars = {'source_host': source_host, 'output_host': output_host}
	url = "%s/synoindex?" % cfg.url
	url = url + urllib.urlencode(query_vars)
	logger.debug(url)
	contents = urllib2.urlopen(url).read()
	logger.debug(contents)