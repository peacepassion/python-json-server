# /usr/bin/python

__author__ = 'peacepassion'

import optparse
import json
import BaseHTTPServer
import SocketServer
import json_utils
import ConfigParser
import StringIO


def usage():
    print 'usage: cmd [-c config-file] [-v] json-data'
    exit(1)


CONFIG_KEY_HOST = 'host'
CONFIG_KEY_PORT = 'port'
CONFIG_KEY_RESPONSE_CODE = 'response_code'

DEFAULT_CONFIG_HOST = 'localhost'
DEFAULT_CONFIG_PORT = 3000
DEFAULT_CONFIG_RESPONSE_CODE = 200

host = DEFAULT_CONFIG_HOST
port = DEFAULT_CONFIG_PORT
response_code = DEFAULT_CONFIG_RESPONSE_CODE

option_list = [optparse.make_option('-c', dest='config', default=''),
               optparse.make_option('-v', dest='verbose', action='store_true', default=False,
                                    help='print all information')]
parser = optparse.OptionParser(usage='Usage: %prog [-c config-file] [-v] json-data', option_list=option_list)
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


if opt.config != '':
    try:
        org_config_file = open(opt.config)
        org_config = org_config_file.read()
        fake_section = 'section'
        org_config = '[' + fake_section + ']' + '\n' + org_config
        cf = ConfigParser.RawConfigParser()
        cf.readfp(StringIO.StringIO(org_config))

        if cf.has_option(fake_section, CONFIG_KEY_HOST):
            host = cf.get(fake_section, CONFIG_KEY_HOST)
        if cf.has_option(fake_section, CONFIG_KEY_PORT):
            port = cf.getint(fake_section, CONFIG_KEY_PORT)
        if cf.has_option(fake_section, CONFIG_KEY_RESPONSE_CODE):
            response_code = cf.getint(fake_section, CONFIG_KEY_RESPONSE_CODE)

    finally:
        org_config_file.close()


if opt.verbose is True:
    print 'config as below: '
    print 'host: ' + str(host)
    print 'port: ' + str(port)
    print 'response_code: ' + str(response_code)

try:
    response_file = open(args[0])
    response = response_file.read()
    if json_utils.validate(response) is False:
        print 'response is an illegal json string'
        exit(1)
finally:
    response_file.close()
if opt.verbose:
    print 'response content: ' + str(response)


class JsonServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self._log_request()
        self.send_response(response_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        try:
            _response_file = open(args[0])
            _response = _response_file.read()
            self.wfile.write(_response)
        finally:
            response_file.close()

    def do_POST(self):
        self.do_GET()

    def _log_request(self):
        SEP = '  '
        print str(self.command) + SEP + str(self.client_address) + SEP + str(self.path)


httpd = SocketServer.TCPServer((host, port), JsonServerHandler)
httpd.serve_forever()
