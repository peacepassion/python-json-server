# /usr/bin/python

import json

__author__ = 'peacepassion'


def validate(_json_str):
    try:
        json.loads(_json_str)
    except Exception:
        return False
    return True
