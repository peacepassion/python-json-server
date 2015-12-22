# /usr/bin/python

import BaseHTTPServer
import SocketServer
import config_parser

__author__ = 'peacepassion'


def _read_config():
    cfg = config_parser.MyConfigParser()
    return cfg


def main():
    cfg = _read_config()

    if cfg.is_verbose():
        print '[global config]'
        print cfg.global_config()

        print '[each section]'
        section_cfgs = cfg.section_configs()
        for key in section_cfgs:
            print '----%s \n%s' % (key, section_cfgs[key])

    _start_server(cfg)
    return 0


def _start_server(_cfg):
    httpd = SocketServer.TCPServer((_cfg.global_config().host, _cfg.global_config().port), JsonServerHandler)
    httpd.serve_forever()


class JsonServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.__log_request()

        code, body = self.__build_response()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(body)

    def __build_response(self):
        cfg = _read_config()

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

    def do_PUT(self):
        self.do_PUT()

    def __log_request(self):
        sep = '  '
        print sep.join([str(self.command), str(self.client_address), str(self.path)])


if __name__ == '__main__':
    status = main()
    exit(status)
