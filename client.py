#################################################
##           Scope: Docker-Container           ##
#################################################
import os, sys, urllib, logging
from urllib.request import urlopen
from urllib.parse import urlencode

## Add the VS-Utils submodule to the python path
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, "VS-Utils"))
from parse import parse_cfg
from prints import debugmsg, errmsg

### Synoindex-Client
def client(source_host, output_host=None):

	## Parse the config
	config_file = os.path.join(cur_dir, "config.txt")
	cfg = parse_cfg(config_file, "vs-synoindex", "docker")

	## Call the url and get the answer of the server
	if not output_host:
		query_vars = {'source_host': source_host}
	else:
		query_vars = {'source_host': source_host, 'output_host': output_host}
	url = "%s/synoindex?" % cfg.url
	url = url + urlencode(query_vars)
	debugmsg("Sent to SynoIndex-Server", "SynoClient")
	contents = urlopen(url).read()
	debugmsg("SynoIndex-Server answered with", "SynoClient", (contents,))