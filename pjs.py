# /usr/bin/python

__author__ = 'peacepassion'

import BaseHTTPServer
import SocketServer

import config_parser

cfg = config_parser.MyConfigParser()

if cfg.is_verbose():
    print '[global config]'
    print cfg.global_config()

    print '[each section]'
    section_cfgs = cfg.section_configs()
    for key in section_cfgs.keys():
        print key
        print section_cfgs[key]


class JsonServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self._log_request()

        code, body = self.__build_response__()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(body)

    def __build_response__(self):
        body = cfg.global_config().response_body
        code = cfg.global_config().response_code

        request_path = self.path
        for _key in cfg.section_configs().keys():
            if _key in request_path:
                target_cfg = cfg.section_configs()[_key]
                body_file = open(target_cfg.response_file)

                try:
                    body = body_file.read()
                    code = target_cfg.response_code

                    break

                finally:
                    body_file.close()

        return code, body

    def do_POST(self):
        self.do_GET()

    def _log_request(self):
        SEP = '  '
        print str(self.command) + SEP + str(self.client_address) + SEP + str(self.path)


httpd = SocketServer.TCPServer((cfg.global_config().host, cfg.global_config().port), JsonServerHandler)
httpd.serve_forever()
