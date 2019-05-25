from pileus import app, run, proxy
from os.path import join, dirname

from bayes.wfs.http import bp, load_wfs
from bayes.geojson import leaflet

load_wfs(join(dirname(__file__), 'config.yaml'))

app.mount('/api', bp)

if __name__ == '__main__':
    run(host = '0.0.0.0', port = 8080, reloader = True, debug = True, threaded = True)