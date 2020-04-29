from flask import Flask, redirect, send_file
from mlsvg.charts.line_chart import make_chart
from io import BytesIO
import urllib3
from uuid import uuid4
from pathlib import Path
import yaml

app = Flask(__name__)

RAW_GITHUB_PREFIX='https://raw.githubusercontent.com/'
CHART_TYPE='line-chart/'

EXT='.svg'

def get_yaml(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)
    data = r.read()
    return yaml.load(data, Loader=yaml.FullLoader)

def get_url(text):
    i = text.index(CHART_TYPE)
    loc = text[i+len(CHART_TYPE):]
    return f'{RAW_GITHUB_PREFIX}{loc}'

@app.route('/<path:text>')
def hello(text):
    if text.startswith(CHART_TYPE) and text.endswith('.yaml'):
        url = get_url(text)
        yml = get_yaml(url)
        chart = make_chart(yml)
        image = BytesIO(chart.render())

        filename = f'{Path(text).name}_{str(uuid4())}{EXT}'
        return send_file(image, attachment_filename=filename)

    return redirect('404_error')


if __name__ == '__main__':
    app.run()

