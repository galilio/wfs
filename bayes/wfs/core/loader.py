from os import listdir
from os.path import dirname, join, isdir, splitext
import importlib

default_root = join(dirname(__file__), '..', 'datasource')
default_pkg = 'bayes.wfs.datasource'

def load_datasource(root = default_root, pkg = default_pkg):
    '''
    load python module of datasource from package bayes.wfs.datasource
    '''
    modules = []
    for entry in listdir(root):
        if entry == '__init__.py':
            continue # skip init

        if not isdir(join(root, entry)):
            module, ext = splitext(entry)
            if ext != '.py':
                continue
        else:
            module = entry

        m = importlib.import_module(pkg + '.' + module)
        if hasattr(m, '__wfs_version__'):
            modules.append(m.__wfs_cls__)
    return modules
