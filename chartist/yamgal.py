import logging as log
import ruamel.yaml as yaml

'''
Example usage:

# In a script

# Run your evaluation script
metrics = eval_model(data)

# look in README.md for markdown or html image tags:
# ie:
#    ![my_metric](http://plotypus/<your-chart>.svg)
# or
#    <img alt="my_metrics" src="img_girl.svg" width="500" height="600">
#
# and replace with the new plotypus link.
# If width and/or height are defined the inserted string will
# always be the html version
pus.update_file(metrics=metrics,
                file_path=["README.md"],
                name="my_metrcis",
                height=200,  # Optional
                width=200)  # Opitonal

# If it is the first time you insert a plot into a file
# simply plcae dummy tags in the location you wish to
# insert the plot. Just be sure to use the alt text because
# this is what Plotypus uses to find which tag to replace.
# ie:
#    ![my_metric](Blah blah raa raa raa)
# or
#    <img alt="my_metrics" omm ahh laa laa laa>
#
'''
def clip_if_float(x, prec):
    """Converts numbers to string
    To save on chars:
      - If it can be an in I will do so.
      - It there are leading/trailing '0's I will strip them
    """
    if isinstance(x, float):
        _x = f'{x:.{prec}f}'
        if float(_x) % 1:
            return _x.strip('0')
        else:
            return str(int(float(_x)))
    else:
        _x = str(x)
        if x != 0:
            return _x.strip('0')
        else:
            return _x

def list_to_str(l, prec=2):
    return str([clip_if_float(x,prec) for x in l]).replace(' ','').replace('"','').replace("'",'')

def dict_to_style_str(chart_config):
    s = []
    for k,v in chart_config.items():
        s += [f'{k}:{v}']
    return ';'.join(s).replace(' ','').replace('"','').replace("'",'')

def _1d_data_to_str(data, prec):
    """
    data: {"rangeA": [y1,y2,...],
           "rangeB": ...
           }
    """
    s = []
    for k,v in data.items():
        v_str = list_to_str(v, prec=prec)
        s += [f'{k}:{v_str}']
    return ';'.join(s)

def _2d_data_to_str(data, prec=2):
    """
    data: {"rangeA": [[x1,x2,x3],[y1,y2,y3]],
           "rangeB": ...}
    """
    s = []
    for k,v in data.items():
        v_str = str([list_to_str(point,prec=prec) for point in zip(*v)]).replace(' ','').replace('"','').replace("'",'')
        s += [f'{k}:{v_str}']
    return ';'.join(s)


_data_to_string_converters = {
    "xy": _2d_data_to_str,
    "line": _1d_data_to_str,
    "dot": _1d_data_to_str,
}

def make_data_str(chart_type, data, prec=2):
    return _data_to_string_converters[chart_type](data, prec=prec)


def make_valid_yaml(d):
    d = d.replace(';','\n').replace(':', ': ')
    return d


def get_chart_type_from_parts(parts):
    return parts[0]

def get_chart_data_from_string(parts):
    data_str = parts[1]
    log.debug(f'data_str: {data_str}')
    data_yaml = make_valid_yaml(data_str)

    chart_data = yaml.round_trip_load(data_yaml)
    #chart_data = yaml.load(data_yaml, Loader=yaml.SafeLoader)
    log.debug(f'chart_data: {chart_data}')
    return chart_data

def get_chart_config_from_parts(parts):
   if len(parts) == 3:
       chart_config_str = parts[2]
       chart_config_yaml = make_valid_yaml(chart_config_str)
       chart_config = yaml.round_trip_load(chart_config_yaml)
       #chart_config = yaml.load(chart_config_yaml, Loader=yaml.SafeLoader)
   else:
       chart_config = {}
   log.debug(f'chart_config: {chart_config}')
   return chart_config

def remove_underscore(config):
    to_remove_underscore = [
        'title',
        'x_title',
        'y_title',
        'x_labels',
        'y_labels',
        'x_labels_major',
        'y_labels_major',
    ]
    for key in to_remove_underscore:
        if key in config:
            val = config[key]
            if isinstance(val, list):
                val = [v.replace('_', ' ') for v in val]
            else:
                val = val.replace('_', ' ')

            config[key] = val
    return config


def chart_dict_from_chartist_url(text):
    if text.endswith('/'):
        text = text[:-1]

    parts = text.split('/')[3:]
    print(f'parts: {parts}')
    chart_type = get_chart_type_from_parts(parts)
    chart_data = get_chart_data_from_string(parts)
    chart_config = get_chart_config_from_parts(parts)

    chart_config = remove_underscore(chart_config)

    return {"chart_type": chart_type,
                  "data": chart_data,
                  "chart_config": chart_config}

def make_chartist_url(
    data,
    chart_type,
    chart_config={},
    prec=2,
    _url = 'http://chartist-server-c6l3dwv2sq-de.a.run.app'):
    data_str = make_data_str(chart_type, data, prec=prec)
    style_str = dict_to_style_str(chart_config)
    s = '/'.join([_url, chart_type, data_str, style_str])
    return s

def from_df(df, chart_type, ranges=None, _url='http://localhost:8080'):
    if isinstance(ranges, list):
        data = df[ranges].to_dict(orient="list")
    elif isinstance(ranges, dict):
        data = {}
        for k,v in ranges.items():
            d = df[ranges[k]].to_dict(orient="list")
            data[k] = [d[r] for r in ranges[k]]
    else:
        data = df.to_dict(orient="list")

def get_chartist_url_from_line(line, idx, start_token, end_token):
    """
    eg = 'fdsdfdf <img alt="bailey" src="http://localhost:8080/line/one:[2,3,4];two:[5,6,7]" width="500" height="600">'
    """
    open_tag = _step_back_to_token(line, idx, start_token)
    http_start = _step_forward_to_token(line, open_tag, 'http')
    end = _step_forward_to_token(line, http_start, end_token)
    return line[http_start:end]

def _step_back_to_token(line, idx, token):
    if line[idx:len(token)+idx] == token:
        return idx

    for i in range(idx, -1, -1):
        if line[i-len(token):i] == token:
            return i-len(token)
    raise ValueError(f"Failed to find token '{token}': '{line}'")

def get_html_start(line, idx):
    return _step_back_to_token(line, idx, '<')

def _step_forward_to_token(line, idx, token):
    for i in range(idx-1, len(line)):
        if line[i:i+len(token)] == token:
            return i
    raise ValueError(f"Failed to find end of tag: '{line}'")

def get_html_end(line, idx):
    return _step_forward_to_token(line, idx, '>')

def get_md_end(line, idx):
    return _step_forward_to_token(line, idx, ')')

def get_idx(l, pattern):
    try:
        return l.index(pattern)
    except ValueError:
        return None

def insert_chart_in_line(line, alt, to_insert):
    token = f'![{alt}]'
    idx = get_idx(line, token)
    if idx is not None:
        start = idx
        end = get_md_end(line, idx)
        line = ''.join([line[:start], to_insert, line[end+1:]])

    token = f'alt="{alt}"'
    idx = get_idx(line, token)
    if idx is not None:
        start = get_html_start(line, idx)
        http_start = _step_forward_to_token(line, start, 'http')
        http_end = _step_forward_to_token(line, http_start, ' ')
        line = ''.join([line[:http_start], to_insert, line[http_end-1:]])

    return line

def find_and_replace_chartist_url(lines, alt, to_insert, height=None, width=None):
    for i in range(len(lines)):
        lines[i] = insert_chart_in_line(lines[i], alt, to_insert, height=height, width=width)
    return lines

def from_df(df, chart_type, ranges=None, _url='http://localhost:8080'):
    if isinstance(ranges, list):
        data = df[ranges].to_dict(orient="list")
    elif isinstance(ranges, dict):
        data = {}
        for k,v in ranges.items():
            d = df[ranges[k]].to_dict(orient="list")
            data[k] = [d[r] for r in ranges[k]]
    else:
        data = df.to_dict(orient="list")

    return make_chartist_url(data, chart_type, _url=_url)

def make_html_tag(url, alt, height=None, width=None, md=False):
    if md:
        tag = f'![{alt}]({url})'
    else:
        tag = [f'<img alt="{alt}" src="{url}"']
        if height is not None:
            tag += [f'height="{height}"']
        if width is not None:
            tag += [f'width="{width}"']
        tag += ['>']
        tag = ' '.join(tag)
    return tag

def get_chartist_url_from_line(line, idx, start_token, end_token):
    """
    eg = 'fdsdfdf <img alt="bailey" src="http://localhost:8080/line/one:[2,3,4];two:[5,6,7]" width="500" height="600">'
    """
    open_tag = _step_back_to_token(line, idx, start_token)
    http_start = _step_forward_to_token(line, open_tag, 'http')
    end = _step_forward_to_token(line, http_start, end_token)
    return line[http_start:end]

def _update_chart(lines, alt, new_values, fn):
    for i in range(len(lines)):
        line = lines[i]
        token = f'![{alt}]'
        idx = get_idx(line, token)
        chartist_url = None
        if idx is not None:
            chartist_url = get_chartist_url_from_line(line, idx, token, ')')

        token = f'alt="{alt}"'
        idx = get_idx(line, token)
        if idx is not None:
            chartist_url = get_chartist_url_from_line(line, idx, '<img', '" ')

        if chartist_url is not None:
            chart_dict = chart_dict_from_chartist_url(chartist_url)

            chart_dict = fn(chart_dict, new_values)
            new_chartist = make_chartist_url(chart_dict['data'],
                                        chart_dict['chart_type'],
                                        chart_config=chart_dict.get('chart_config', {}),
                                        prec=2,
                                        _url = 'http://localhost:8080')

            line = insert_chart_in_line(line, alt, new_chartist)
        lines[i] = line
    return lines

# insert_chart_in_line
def add_ranges(lines, alt, new_values):
    """
    new_ranges = {
      "new_rangeA" : List,
      "new_rangeB" : List,
      ...
    }
    Where the ranges in new_values are compatible with
    the existing data in chart_dict['data']
    """
    def fn(chart_dict, new_ranges):
        chart_dict['data'].update(new_ranges)
        return chart_dict
    return _update_chart(lines, alt, new_values, fn)

def append_to_ranges(chart_dict, alt, new_values):
    """
    new_values = {
        "range1": List,
        "range2": List,
        ...
    }
    where each range's List must have the same dims
    as the existing data in chart_dict['data'].
    """
    def fn(chart_dict, new_values):
        for k,v in new_values.items():
            chart_dict['data'][k] += v
        return chart_dict
    return _update_chart(chart_dict, alt, nchart_config, fn)
