from flask import Flask, redirect, send_file
from mlsvg.charts.line_chart import make_chart
from io import BytesIO
import tempfile
from pathlib import Path
from uuid import uuid4

app = Flask(__name__)

@app.route('/<path:text>')
def hello(text):
    if text.startswith('line-chart') and text.endswith('.svg'):
        chart = make_chart('/home/jp/Documents/repos/metrics-svg/test/train-acc.yaml')
        image = BytesIO(chart.render())
        #tmp = tempfile.mkdtemp()
        #path = Path(tmp) / 'poop.svg'
        #chart.render_to_file(path)

        filename = str(uuid4()) + '.svg'
        #mimetype='text/svg+xml', 
        return send_file(image, attachment_filename=filename)

    return redirect('404_error')


if __name__ == '__main__':
    app.run()
