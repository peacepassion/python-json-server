# /usr/bin/python

__author__ = 'peacepassion'

import optparse
import json
import json_utils
import SimpleHTTPServer
import SocketServer


def usage():
    print 'usage: cmd [-c config-file] [-v] json-data'
    exit(1)


CONFIG_KEY_HOST = 'host'
CONFIG_KEY_PORT = 'port'
CONFIG_KEY_RESPONSE_CODE = 'response_code'
DEFAULT_CONFIG = {CONFIG_KEY_HOST: 'localhost', CONFIG_KEY_PORT: 3000, CONFIG_KEY_RESPONSE_CODE: 200}

parser = optparse.OptionParser()
parser.add_option('-c', dest='config', default='')
parser.add_option('-v', dest='verbose', action='store_true', default=False, help='print all information')
opt, args = parser.parse_args()

if opt.verbose is True:
    print 'opt: ' + str(opt)
    print 'args: ' + str(args)

if len(args) == 0:
    print 'please provide a json file'
    usage()
    exit(1)

if len(args) > 1:
    print 'only support one json file'
    usage()
    exit(1)


config = DEFAULT_CONFIG
if opt.config != '':
    config_file = open(opt.config)
    try:
        user_config = json.load(config_file)
        if CONFIG_KEY_HOST in user_config:
            config[CONFIG_KEY_HOST] = user_config[CONFIG_KEY_HOST]
        if CONFIG_KEY_PORT in user_config:
            config[CONFIG_KEY_PORT] = user_config[CONFIG_KEY_PORT]
        if CONFIG_KEY_RESPONSE_CODE in user_config:
            config[CONFIG_KEY_RESPONSE_CODE] = user_config[CONFIG_KEY_RESPONSE_CODE]
    finally:
        config_file.close()
if opt.verbose is True:
    print 'config: ' + str(config)


try:
    response_file = open(args[0])
    response = response_file.read()
    if json_utils.validate(response) is False:
        print 'response is not an illegal json string'
        exit(1)
finally:
    response_file.close()
if opt.verbose:
    print 'response content: ' + str(response)


class JsonServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self._log_request()
        self.send_response(config[CONFIG_KEY_RESPONSE_CODE])
        self.wfile.write(response)

    def do_POST(self):
        self.do_GET()

    def _log_request(self):
        SEP = '  '
        print str(self.command) + SEP + str(self.client_address) + SEP + str(self.path)


httpd = SocketServer.TCPServer((config[CONFIG_KEY_HOST], config[CONFIG_KEY_PORT]), JsonServerHandler)
httpd.serve_forever()
