import yaml
from os import environ
import re


class InvalidKeyException(Exception):
    def __init__(self, key):
        super().__init__(f'yaml missing key {key}')

class Configuration(object):
    def __init__(self, path):
        super().__init__()
        self.config = yaml.load(open(path), Loader = yaml.Loader) or {}

    def get_value(self, obj):
        if not isinstance(obj, str):
            return obj

        m = re.match(r'\$\{(.*?)\}', obj)
        if not m:
            return obj

        return environ.get(m.group(1))

    def get(self, key, default = None):
        parts = key.split('.')

        obj = self.config
        for part in parts:
            obj = obj.get(part)
        
            if obj is None and default is None:
                raise InvalidKeyException(part)
            elif obj is None:
                return self.get_value(default)

        return self.get_value(obj) or default