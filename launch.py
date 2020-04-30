from yamgal.make_chart import make_chart
from flask import Flask, redirect, send_file
from io import BytesIO
import urllib3
from uuid import uuid4
from pathlib import Path
import yaml
import logging as log

log.basicConfig(level=log.DEBUG)

app = Flask(__name__)

RAW_GITHUB_PREFIX='https://raw.githubusercontent.com/'
GET_CHART='get-chart/'
CHART_TYPE='chart_type'
ERROR_IMAGE='error.png'

EXT='.svg'


def get_yaml(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)
    data = r.read()
    return yaml.load(data, Loader=yaml.FullLoader)

def get_url(text):
    i = text.index(GET_CHART)
    loc = text[i+len(GET_CHART):]
    return f'{RAW_GITHUB_PREFIX}{loc}'

def read_image_as_bytes(path):
    with open(path, 'rb') as f:
        image = f.read()
    return BytesIO(image)

def invalid_chart_type_error(data):
    message = f'invalid chart type: "{data[chart_type]}"'
    log.error(message)
    return read_image_as_bytes('error.png')

def generic_error(message):
    log.error(message)
    return read_image_as_bytes('error.png')

@app.route('/<path:text>')
def hello(text):
    log.info(f'text: {text}')
    if text.startswith(GET_CHART) and text.endswith('.yaml'):
        url = get_url(text)
        log.info(f'downloading: {url}')
        yml = get_yaml(url)
        chart = make_chart(yml)
        image = BytesIO(chart.render())

        filename = f'{Path(text).name}_{str(uuid4())}{EXT}'
        return send_file(image, attachment_filename=filename)

    message = f'Invalid url error: "{text}"'
    return send_file(generic_error(message), attachment_filename='error.png')


if __name__ == '__main__':
    app.run()

