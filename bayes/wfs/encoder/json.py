from bayes.wfs.core.ogc_types import *

def _encode_service_identification(obj):
    return {
        'service_type': obj.service_type,
        'service_type_version': obj.service_type_version,
        # 'description': encode_json(obj.)
    }

__obj_map = {
    ServiceIdentification: _encode_service_identification,

}

def encode_json(obj):
    pass

def encode(obj):
    return encode_json(obj)