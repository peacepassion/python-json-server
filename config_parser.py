import ConfigParser
import StringIO
import json_utils

import optparse

__author__ = 'peacepassion'

CONFIG_KEY_HOST = 'host'
CONFIG_KEY_PORT = 'port'
CONFIG_KEY_RESPONSE_FILE = 'response_file'
CONFIG_KEY_RESPONSE_CODE = 'response_code'

DEFAULT_CONFIG_HOST = 'localhost'
DEFAULT_CONFIG_PORT = 3000
DEFAULT_CONFIG_RESPONSE_CODE = 200


def _usage():
    print 'usage: cmd [-c config-file] [-v] json-data'
    exit(1)


def _validate_response_file(file_path):
    _response_file = open(file_path)

    try:
        response = _response_file.read()
        if not json_utils.validate(response):
            return False
        return True

    finally:
        _response_file.close()


class GlobalConfig:
    host = DEFAULT_CONFIG_HOST
    port = DEFAULT_CONFIG_PORT
    response_code = DEFAULT_CONFIG_RESPONSE_CODE
    response_body = ''

    def __init__(self):
        pass

    def __str__(self):
        return 'host: ' + str(self.host) + '\n' \
               + 'port: ' + str(self.port) + '\n' \
               + 'response_code: ' + str(self.response_code) + '\n' \
               + 'response_body: ' + str(self.response_body) + '\n'


class MyConfigUnit:
    def __init__(self, path_key='', response_file_path='', response_code=200):
        self.path_key = path_key
        self.response_file = response_file_path
        self.response_code = response_code

    def __str__(self):
        return 'path_key: ' + str(self.path_key) + '\n' \
               + 'response_file_path: ' + str(self.response_file) + '\n' \
               + 'response_code: ' + str(self.response_code) + '\n'


class MyConfigParser:
    __global_config = None
    __section_configs = {}
    __fake_global_section = '__global_section__'

    def __init__(self):
        self.__parse_cmd()
        self.__parse_config_file()

    def __parse_cmd(self):
        option_list = [optparse.make_option('-v', dest='verbose', action='store_true', default=False,
                                            help='print all information')]
        parser = optparse.OptionParser(usage='Usage: %prog [-v] config-file', option_list=option_list)
        self.__opt, self.__args = parser.parse_args()

        if self.__opt.verbose:
            print 'opt: %s' % str(self.__opt)
            print 'args: %s' % str(self.__args)
        if self.__args is False:  # judge if list's length does not equals zero
            print 'fail to find config-file'
            exit(1)

        self.__config_file = self.__args[0]

    def is_verbose(self):
        return self.__opt.verbose

    def __parse_config_file(self):
        self.__global_config = GlobalConfig()

        if self.__config_file:  # '' means False in python
            org_config_file = open(self.__config_file)

            try:
                org_config = org_config_file.read()
                org_config = '[' + self.__fake_global_section + ']' + '\n' + org_config
                cf = ConfigParser.RawConfigParser()
                cf.readfp(StringIO.StringIO(org_config))

                self.__parse_global_config__(cf)
                self.__parse_each_section__(cf)

            finally:
                org_config_file.close()

    def __parse_global_config__(self, cf):
        if cf.has_option(self.__fake_global_section, CONFIG_KEY_HOST):
            self.__global_config.host = cf.get(self.__fake_global_section, CONFIG_KEY_HOST)
        if cf.has_option(self.__fake_global_section, CONFIG_KEY_PORT):
            self.__global_config.port = cf.getint(self.__fake_global_section, CONFIG_KEY_PORT)
        if cf.has_option(self.__fake_global_section, CONFIG_KEY_RESPONSE_CODE):
            self.__global_config.response_code = cf.getint(self.__fake_global_section, CONFIG_KEY_RESPONSE_CODE)

    def __parse_each_section__(self, cf):
        section_list = cf.sections()

        for section in section_list:
            if section == self.__fake_global_section:
                continue

            config_unit = MyConfigUnit()
            config_unit.path_key = section

            options = cf.options(section)

            if CONFIG_KEY_RESPONSE_FILE not in options:
                print "fail to find response_file configuration under section %s" % section
                exit(1)
            response_file_path = cf.get(section, CONFIG_KEY_RESPONSE_FILE)
            if not _validate_response_file(response_file_path):
                print 'response_file: %s is an illegal json string' % response_file_path
                exit(1)
            config_unit.response_file = response_file_path

            config_unit.response_code = cf.getint(section, CONFIG_KEY_RESPONSE_CODE) \
                if CONFIG_KEY_RESPONSE_CODE in options \
                else DEFAULT_CONFIG_RESPONSE_CODE

            self.__section_configs[config_unit.path_key] = config_unit

    def global_config(self):
        return self.__global_config

    def section_configs(self):
        return self.__section_configs


if __name__ == '__main__':
    print 'test config_parser usage'
    cfg = MyConfigParser()

    if cfg.is_verbose():
        print '[global config]'
        print cfg.global_config()

        print '[each section]'
        section_cfgs = cfg.section_configs()
        for key in section_cfgs:
            print '----%s \n%s' % (key, section_cfgs[key])
