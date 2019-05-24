from geojson import Feature, FeatureCollection
from geoalchemy2.elements import WKBElement
from shapely import wkb

def _pack_first_feature(result_proxy):
    row = result_proxy.fetchone()

    keys, values = row.keys(), row.values()

    wkb_idx = -1
    for i, v in enumerate(values):
        if isinstance(v, WKBElement):
            wkb_idx = i
            break
    if wkb_idx < 0:
        geo = None
    else:
        geo = wkb.loads(bytes(values[wkb_idx].data), hex = False)
        del values[wkb_idx]
        del keys[wkb_idx]
    return wkb_idx, keys, Feature(geometry = geo, properties = dict(zip(keys, values)))

def pack_result_proxy(tables, result_proxy):
    features = []

    idx, keys, feature = _pack_first_feature(result_proxy)
    print(idx)
    features.append(feature)

    for row in result_proxy:
        values = row.values()

        geometry = None
        if idx >= 0:
            geometry = wkb.loads(bytes(values[idx].data), hex = False)
            del values[idx]
    
        feature = Feature(geometry = geometry, properties = dict(zip(keys, values)))
        features.append(feature)
    return FeatureCollection(features)
