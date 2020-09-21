import os
from flask import Flask, redirect, send_file, request, make_response
from werkzeug.datastructures import Headers
from io import BytesIO
from uuid import uuid4
from pathlib import Path
import subprocess

import logging as log

from chartist.chartist import Chartist

log.basicConfig(level=log.DEBUG)

app = Flask(__name__)

EXT='.svg'

def read_image_as_bytes(path):
    with open(path, 'rb') as f:
        image = f.read()
    return BytesIO(image)

# https://yamgal-server-c6l3dwv2sq-de.a.run.app/favicon.ico
@app.route('/<path:text>')
def server(text):
    log.info(f'remote_address: {request.remote_addr}')
    log.info(f'remote_host: {request.host}')
    log.info(f'remote_origin: {request.origin}')
    log.info(f'text: {text}')

    if text == 'help':
        return redirect('https://colab.research.google.com/github/tall-josh/graphite/blob/master/notebooks/Yamgal_Demo_Notebook.ipynb', code=302)
    if text == 'favicon.ico':
        return redirect('https://raw.githubusercontent.com/tall-josh/graphite/master/Bailey.jpg')

    try:
        url = f'https://{request.host}/{text}'
        chart = Chartist.from_url(url)
        log.info(f'chart: {chart}')
        svg = chart.to_svg()
        image = BytesIO(svg.render())
        filename = f'{Path(text).name}_{str(uuid4())}{EXT}'
    except Exception as e:
        log.info(e)
        image = read_image_as_bytes('error.png')
        filename = 'error'

    response = make_response(send_file(image, attachment_filename=filename))

    return response

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=os.environ.get('PORT', 8080))
