import os
from yamgal.make_chart import make_chart
from flask import Flask, redirect, send_file, request, make_response
from werkzeug.datastructures import Headers
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

# https://yamgal-server-c6l3dwv2sq-de.a.run.app/favicon.ico
@app.route('/<path:text>')
def server(text):
    log.debug(f'remote_address: {request.remote_addr}')
    log.debug(f'remote_host: {request.host}')
    log.debug(f'remote_origin: {request.origin}')
    log.debug(f'text: {text}')

    if text == 'help':
        return redirect('https://colab.research.google.com/github/tall-josh/graphite/blob/master/notebooks/Yamgal_Demo_Notebook.ipynb', code=302)
    if text == 'favicon.ico':
        return redirect('https://raw.githubusercontent.com/tall-josh/graphite/master/Bailey.jpg')

    parts = text.split('/')
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

    response = make_response(send_file(image, attachment_filename=filename))

    chart_title = "josh hosh"
    git_url = "https://github.com/tall-josh/graphite"
    chart_url = "https://yamgal-server-c6l3dwv2sq-de.a.run.app/pie/one:0.1;two:0.2;three:0.3;four:0.4/style:neon;title:Pie_Chart"
    chart_url = "https://pbs.twimg.com/profile_images/654244539159420928/rgbZ5vnR_400x400.jpg"

    headers = (
        'property="og:type" content="website", '
        f'property="og:url" content="{git_url}", '
        f'property="og:title" content="{chart_title}", '
        'property="og:description" content="Powered by Josh", '
        f'property="og:image" content="{chart_url}", '

        'name="twitter:card" content="summary_large_imag, '
        'name="twitter:domain" value="ruraljuror.com", '
        f'name="twitter:title" value="{chart_title}", '
        'name="twitter:description" value="Powered by Josh", '
        f'name="twitter:image" content="{chart_url}", '
        f'name="twitter:url" value="{git_url}"')
    print(f'headers: {headers}')
    response.headers['meta'] = headers.encode('utf-8')
    log.debug(response)
    return response

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=os.environ.get('PORT', 8080))
