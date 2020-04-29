import pygal
import yaml
from pathlib import Path
from string import capwords

def make_chart(data_yaml):
    with open(data_yaml, 'r') as f:
        data = yaml.load(f,  Loader=yaml.FullLoader)
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
