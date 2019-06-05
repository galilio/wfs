import json

from bayes.wfs.core.ogc_types import *


def _has_val(obj, k):
    return hasattr(obj, k) and getattr(obj, k)


def _encode_service_identification(obj):
    res_val = {}
    if _has_val(obj, 'service_type'):
        res_val['service_type'] = obj.service_type
    if _has_val(obj, 'service_type_version'):
        res_val['service_type_version'] = obj.service_type_version
    if _has_val(obj, 'profile'):
        res_val['profile'] = obj.profile
    if _has_val(obj, 'fees'):
        res_val['fees'] = obj.fees
    if _has_val(obj, 'access_constraints'):
        res_val['access_constraints'] = obj.access_constraints
    if _has_val(obj, 'description'):
        res_val['description'] = encode_json(obj.description)
    return res_val


def _encode_service_identification_description(obj):
    res_val = {}
    if _has_val(obj, 'title'):
        res_val['title'] = obj.title
    if _has_val(obj, 'abstract'):
        res_val['abstract'] = obj.abstract
    if _has_val(obj, 'keywords'):
        res_val['keywords'] = obj.keywords
    return res_val


def _encode_service_provider(obj):
    res_val = {}
    if _has_val(obj, 'provider_name'):
        res_val['provider_name'] = obj.provider_name
    if _has_val(obj, 'provider_site'):
        res_val['provider_site'] = obj.provider_site
    if _has_val(obj, 'service_contact'):
        res_val['service_contact'] = encode_json(obj.service_contact)
    return res_val


def _encode_service_provider_contact(obj):
    res_val = {}
    if _has_val(obj, 'name'):
        res_val['name'] = obj.name
    if _has_val(obj, 'tel'):
        res_val['tel'] = obj.tel
    return res_val


def _encode_operations_metadata(obj):
    res_val = {}
    if _has_val(obj, 'domains'):
        res_val['domains'] = obj.domains
    if _has_val(obj, 'operations'):
        res_val['operations'] = [encode_json(i) for i in obj.operations]
    return res_val


def _encode_operations_metadata_operation(obj):
    res_val = {}
    if _has_val(obj, 'name'):
        res_val['name'] = obj.name
    if _has_val(obj, 'request_method'):
        res_val['request_method'] = obj.request_method
    if _has_val(obj, 'link'):
        res_val['link'] = obj.link
    if _has_val(obj, 'about'):
        res_val['about'] = obj.about
    if _has_val(obj, 'domains'):
        res_val['domains'] = obj.domains
    return res_val


def _encode_service_meta(obj):
    res_val = {}
    if _has_val(obj, 'service_identification'):
        res_val['service_identification'] = encode_json(obj.service_identification)
    if _has_val(obj, 'service_provider'):
        res_val['service_provider'] = encode_json(obj.service_provider)
    if _has_val(obj, 'operations_metadata'):
        res_val['operations_metadata'] = encode_json(obj.operations_metadata)
    if _has_val(obj, 'version'):
        res_val['version'] = obj.version
    if _has_val(obj, 'update_sequence'):
        res_val['update_sequence'] = obj.update_sequence
    if _has_val(obj, 'contents'):
        res_val['contents'] = [encode_json(i) for i in obj.contents]
    return res_val


def _encode_feature_type(obj):
    res_val = {}
    if _has_val(obj, 'name'):
        res_val['name'] = obj.name
    if _has_val(obj, 'properties'):
        res_val['properties'] = [encode_json(i) for i in obj.properties]
    if _has_val(obj, 'abstract'):
        res_val['abstract'] = obj.abstract
    return res_val


def _encode_feature_type_property(obj):
    res_val = {}
    if _has_val(obj, 'nullable'):
        res_val['nullable'] = obj.nullable
    if _has_val(obj, 'pk'):
        res_val['pk'] = obj.pk
    if _has_val(obj, 'dtype'):
        res_val['dtype'] = str(obj.dtype)
    if _has_val(obj, 'max_length'):
        res_val['max_length'] = obj.max_length
    if _has_val(obj, 'min_length'):
        res_val['min_length'] = obj.min_length
    if _has_val(obj, 'name'):
        res_val['name'] = obj.name
    return res_val


__obj_map = {
    ServiceIdentification: _encode_service_identification,
    ServiceIdentification.Description: _encode_service_identification_description,
    ServiceProvider: _encode_service_provider,
    ServiceProvider.Contact: _encode_service_provider_contact,
    OperationsMetadata: _encode_operations_metadata,
    OperationsMetadata.Operation: _encode_operations_metadata_operation,
    ServiceMeta: _encode_service_meta,
    FeatureType: _encode_feature_type,
    FeatureType.Property: _encode_feature_type_property,

}


def encode_json(obj):
    return json.loads(json.dumps(obj, default=__obj_map.get(type(obj))))


def encode(obj):
    return encode_json(obj)
