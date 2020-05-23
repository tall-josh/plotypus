import ipaddress
import os
from yamgal.make_chart import make_chart
from flask import Flask, redirect, send_file, request
from io import BytesIO
import urllib3
from uuid import uuid4
from pathlib import Path
import yaml
from urllib.parse import urlparse
from tempfile import mkdtemp
import subprocess

import logging as log

log.basicConfig(level=log.DEBUG)

app = Flask(__name__)

YAMGAL='yamgal'
ERROR_IMAGE='error.png'

EXT='.svg'

def load_yaml(path):
    with path.open('r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def get_yaml(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)
    data = r.read()
    return yaml.load(data, Loader=yaml.FullLoader)

def read_image_as_bytes(path):
    with open(path, 'rb') as f:
        image = f.read()
    return BytesIO(image)

def invalid_chart_type_error(data):
    chart_type = data["chart_type"]
    message = f'Invalid chart_type: "{chart_type}"'
    log.error(message)
    return read_image_as_bytes('error.png')

def generic_error(message):
    log.error(message)
    return read_image_as_bytes('error.png')

def download_from_public_github(url):
    '''
    Args:
        url (str): github.com/tall-josh/yamgal/blob/master/examples/lines-01.yaml

    Converts to "raw" github url:

        https://raw.githubusercontent.com/tall-josh/yamgal/master/examples/lines-01.yaml

    Downloads file and parses to yaml
    '''
    path = Path(urlparse(url).path)
    log.debug(f'github path : {path}')
    parts = [p for p in path.parts[1:] if p != "blob"]
    url = 'http://' + str(Path("raw.githubusercontent.com")\
                          .joinpath(*[p for p in path.parts[1:] \
                                  if p != "blob"]))
    log.debug(f'github url : {url}')
    yml = get_yaml(url)
    log.debug(f'github yaml : {yml}')
    return yml

def local_loader(path):
    local_path = Path('.').joinpath(*Path(path).parts[1:])
    data = load_yaml(local_path)
    return data

def shell_command(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
    return result

def download_from_private_gitlab(url):
    # gitlab.com/silverpond/research/dvc-jupyter-project-example-demo.git/artefacts/example-metric.yaml
    TOKEN = "Ru9Fo1Vtey2NtoFjsmM1"
    USR   = "gitlab+deploy-token-167795"
    path = Path(urlparse(url).path)
    log.debug(f'gitlab path: {path}')
    url_parts = []
    repo_path = []
    for p in path.parts:
        url_parts += [p]
        if '.git' in p:
            break
    repo_url = f'https://{USR}:{TOKEN}@' + '/'.join(url_parts)
    log.debug(f'gitlab url: {repo_url}')
    path_in_repo = '/'.join(path.parts[len(url_parts):])
    log.debug(f'gitlab path_in_repo: {path_in_repo}')

    tmp = mkdtemp()
    _ = shell_command(['./scripts/sparse_clone.sh',
                       repo_url,
                       tmp,
                       path_in_repo])

    return load_yaml(Path(tmp) / path_in_repo)

def get_loader(site_key):
    '''ToDo make this switch on ip address

    '''
    loaders = {
    'github.com': download_from_public_github,
    'gitlab.com': download_from_private_gitlab,
    'local': local_loader,
    }
    return loaders[site_key]


@app.route('/<path:text>')
def server(text):
    log.debug(f'remote_address: {request.remote_addr}')
    log.debug(f'remote_host: {request.host}')
    log.debug(f'remote_origin: {request.origin}')
    log.debug(f'text: {text}')

    if text.startswith(YAMGAL) and (
        text.endswith('.yaml') or text.endswith('.json')):
        site_key = text.split('/')[1]
        log.debug(f'site_key: {site_key}')
        loader = get_loader(site_key)

        url = '/'.join(text.split('/')[1:])
        yml = loader(url)

        chart = make_chart(yml)
        image = BytesIO(chart.render())

        filename = f'{Path(text).name}_{str(uuid4())}{EXT}'
        return send_file(image, attachment_filename=filename)

    message = f'Invalid url error: "{text}"'
    return send_file(generic_error(message), attachment_filename='error.png')


if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=os.environ.get('PORT', 8080))

