from os.path import dirname, join, basename, splitext
import re
from glob import glob
from xmlschema import XMLSchema

import logging

_xsd_root = join(dirname(__file__), 'assets')
_allow_name_pattern = re.compile(r'[a-zA-Z][a-zA-Z0-9-_]*')

class XSDNamePatternInvalid(Exception):
    def __init__(self, word):
        super().__init__(f'{word} not match [a-zA-Z][a-zA-Z0-9-_]*')

def camel_to_snake(word):
    if not _allow_name_pattern.match(word):
        raise XSDNamePatternInvalid(word)

    # input HTTPResponseCodeXYZ-20
    word = re.sub(r'-', r'_', word) # HTTPResponseCodeXYZ_20
    word = re.sub(r'([^_]+?)([A-Z][a-z]+)', r'\1_\2', word) #HTTP_Response_CodeXYZ_20

    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', word).lower() # http_response_code_xyz_20


def _load_xsd_file(root = _xsd_root):
    xsds = glob(join(root, '*.xsd'))

    retval = {}
    for file in xsds:
        fn = camel_to_snake(splitext(basename(file))[0])
        schema = XMLSchema(file)
        retval[fn] = schema

    return retval

XSD = _load_xsd_file()