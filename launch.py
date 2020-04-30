import pygal
from string import capwords
from flask import Flask, redirect, send_file
from io import BytesIO
import urllib3
from uuid import uuid4
from pathlib import Path
import yaml

app = Flask(__name__)

RAW_GITHUB_PREFIX='https://raw.githubusercontent.com/'
CHART_TYPE='line-chart/'

EXT='.svg'

def make_chart(data):
    #with open(data_yaml, 'r') as f:
    #    data = yaml.load(f,  Loader=yaml.FullLoader)
    assert 'data' in data, 'Must have at least "data" key'

    # Default title
    if not('title' in data):
        data['title'] = capwords(Path(data_yaml)\
                                       .stem\
                                       .replace('-', ' ')\
                                       .replace('_', ' '))

    line_chart = pygal.Line(x_label_rotation=0,
                            title   = data['title'],
                            x_title = data.get('x_title',''),
                            y_title = data.get('y_title',''),
                            interpolate = data.get('interpolate', None),
                            human_readable = True,
                            width = data.get('width', 400),
                            height = data.get('height', 300),
                           )
    x_count = 0
    for run, values in data['data'].items():
        line_chart.add(run, values)
        if len(values) > x_count:
            x_count = len(values)

    line_chart.x_labels = data.get('x_labels', range(x_count))
    line_chart.y_labels = data.get('y_labels', [])

    #path = img_name + '_' + str(str(uuid4())) + ".svg"
    return line_chart

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
    print(f'text: {text}')
    if text.startswith(CHART_TYPE) and text.endswith('.yaml'):
        url = get_url(text)
        print(f'downloading: {url}')
        yml = get_yaml(url)
        chart = make_chart(yml)
        image = BytesIO(chart.render())

        filename = f'{Path(text).name}_{str(uuid4())}{EXT}'
        return send_file(image, attachment_filename=filename)

    return 'Womp womp ¯\_(ツ)_/¯'


if __name__ == '__main__':
    app.run()

