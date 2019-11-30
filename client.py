import os, sys, urllib, urllib2, logging

## Add the VS-Utils submodule to the python path
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, "VS-Utils"))
from parse import parse_cfg, synoindex_modes

### Synoindex-Client
def client(cfg, option, filepath):

	## Setup the client logging file
	client_log = "%s/%s" % (cfg.client_logs, "client.log")
	logging.basicConfig(filename=client_log, filemode='a',
						format='%(asctime)s - %(levelname)s: %(message)s')

	## Set the logger and its level
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	## Validation of the arguments
	if(option not in synoindex_modes):
		logger.error("Passed option not supported"); exit()
	if not os.path.exists(filepath):
		logger.error("Passed file does not exist"); exit()

	## Call the url and get the answer of the server
	query_vars = {'option': option, 'filepath': filepath}
	url = "%s/synoindex?" % cfg.url
	url = url + urllib.urlencode(query_vars)
	logger.debug(url)
	contents = urllib2.urlopen(url).read()
	logger.debug(contents)