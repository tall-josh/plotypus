import os
from yamgal.make_chart import make_chart
from flask import Flask, redirect, send_file, request
from io import BytesIO
from uuid import uuid4
from pathlib import Path
import yaml
from urllib.parse import urlparse
import subprocess

import logging as log

log.basicConfig(level=log.DEBUG)

app = Flask(__name__)

YAMGAL='yamgal'
ERROR_IMAGE='error.png'

EXT='.svg'

def read_image_as_bytes(path):
    with open(path, 'rb') as f:
        image = f.read()
    return BytesIO(image)

def shell_command(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
    return result

def make_valid_yaml(d):
    d = d.replace(';','\n').replace(':', ': ')
    return d

def get_chart_type_from_parts(parts):
    return parts[0]

def get_chart_data_from_string(parts):
    data_str = parts[1]
    log.debug(f'data_str: {data_str}')
    data_yaml = make_valid_yaml(data_str)

    chart_data = yaml.load(data_yaml, Loader=yaml.FullLoader)
    log.debug(f'chart_data: {chart_data}')
    return chart_data

def get_chart_config_from_parts(parts):
   if len(parts) == 3:
       chart_config_str = parts[2]
       chart_config_yaml = make_valid_yaml(chart_config_str)
       chart_config = yaml.load(chart_config_yaml, Loader=yaml.FullLoader)
   else:
       chart_config = {}
   log.debug(f'chart_config: {chart_config}')
   return chart_config

def remove_underscore(config, to_remove_underscore):
    for key in to_remove_underscore:
        if key in config:
            val = config[key]
            if isinstance(val, list):
                val = [v.replace('_', ' ') for v in val]
            else:
                val = val.replace('_', ' ')

            config[key] = val
    return config

@app.route('/<path:text>')
def server(text):
    log.debug(f'remote_address: {request.remote_addr}')
    log.debug(f'remote_host: {request.host}')
    log.debug(f'remote_origin: {request.origin}')
    log.debug(f'text: {text}')

    if text == 'help':
        return redirect('https://colab.research.google.com/notebooks/intro.ipynb', code=302)

    try:
        chart_type = get_chart_type_from_parts(parts)
        chart_data = get_chart_data_from_string(parts)
        chart_config = get_chart_config_from_parts(parts)

        to_remove_underscore = [
            'title',
            'x_title',
            'y_title',
            'x_labels',
            'y_labels',
            'x_labels_major',
            'y_labels_major',
        ]

        chart_config = remove_underscore(chart_config,
                                         to_remove_underscore)

        chart_dict = {"chart_type": chart_type,
                      "data": chart_data,
                      "chart_config": chart_config}

        log.debug(f'chart_dict: {chart_dict}')

        chart = make_chart(chart_dict)
        image = BytesIO(chart.render())

        filename = f'{Path(text).name}_{str(uuid4())}{EXT}'
    except Exception as e:
        log.debug(e)
        image = read_image_as_bytes('error.png')
        filename = 'error'

    return send_file(image, attachment_filename=filename)

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=os.environ.get('PORT', 8080))

