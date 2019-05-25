from pileus import proxy, rpc, get, post, bp, request

import logging

from bayes.wfs.core import Configuration

class NoWFSModuleFound(Exception):
    def __init__(self):
        super().__init__('No WFS Module Found in bayes.wfs.datasource')

bp = bp()

def load_wfs(cfg_path = None):
    from bayes.wfs.core.loader import load_datasource
    wfs_modules = load_datasource()
    if not wfs_modules:
        raise NoWFSModuleFound()
    cfg = Configuration(cfg_path)
    bp.wfs = wfs_modules[-1](cfg) # use last. index by name may be better.
    logging.info(f'Find WFS Module {bp.wfs.version} {bp.wfs.service_identification}')

@bp.get('/wfs/caps')
def wfs():
    pass
