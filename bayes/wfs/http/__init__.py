from pileus import proxy, rpc, get, post, bp, request
import importlib
import logging

from bayes.wfs.core import Configuration


class NoWFSModuleFound(Exception):
    def __init__(self):
        super().__init__('No WFS Module Found in bayes.wfs.datasource')


bp = bp()


def load_wfs(cfg_path=None):
    from bayes.wfs.core.loader import load_datasource
    wfs_modules = load_datasource()
    if not wfs_modules:
        raise NoWFSModuleFound()

    cfg = Configuration(cfg_path)

    bp.wfs = wfs_modules[-1](cfg)  # use last. index by name may be better.
    logging.info(f'Find WFS Module {bp.wfs.version} {bp.wfs.service_identification}')

    bp.encoder = importlib.import_module(cfg.get('wfs.output_encoder', 'bayes.wfs.encoder.json'))


@bp.get('/wfs/capabilities')
def wfs():
    kwargs = {
        'accept_versions': [],
        'sections': ['ALL'],
        'update_sequence': None,
        'accept_formats': 'application/json'
    }

    if request.GET.accept_versions:
        kwargs['accept_versions'] = request.GET.accept_versions.split(',')
    if request.GET.sections:
        kwargs['sections'] = request.GET.sections.split(',')
    if request.GET.accept_formats:
        kwargs['accept_formats'] = request.GET.accept_formats

    caps = bp.wfs.get_capabilities(**kwargs)
    return bp.encoder.encode(caps)


@bp.get('/wfs/describe_feature_type')
def wfs():
    table_name = request.GET.tablenames.split(',')

    feature_types = bp.wfs.describe_feature_type(table_name)
    return {feature_type: bp.encoder.encode(feature_types.get(feature_type)) for feature_type in feature_types}
