import pygal
from time import time
from pygal.graph.graph import Graph
from typing import List, Dict, Any, Optional
import ruamel.yaml as yaml

CHART_FROM_NAME_STR = {
    "line" : pygal.Line,
    "stackedline": pygal.StackedLine,
    "bar": pygal.Bar,
    "stackedbar": pygal.StackedBar,
    "horizontalbar": pygal.HorizontalBar,
    "pie": pygal.Pie,
    "histogram": pygal.Histogram,
    "xy": pygal.XY,
    "dot": pygal.Dot,
}

STYLE_FROM_NAME_STR = {
    "default": pygal.style.DefaultStyle,
    "dark": pygal.style.DarkStyle,
    "neon": pygal.style.NeonStyle,
    "darksolarized": pygal.style.DarkSolarizedStyle,
    "lightsolarized": pygal.style.LightSolarizedStyle,
    "light": pygal.style.LightStyle,
    "clean": pygal.style.CleanStyle,
    "redblue": pygal.style.RedBlueStyle,
    "darkcolorized": pygal.style.DarkColorizedStyle,
    "lightcolorized": pygal.style.LightColorizedStyle,
    "turquoise": pygal.style.TurquoiseStyle,
    "lightgreen": pygal.style.LightGreenStyle,
    "darkgreen": pygal.style.DarkGreenStyle,
    "darkgreenblue": pygal.style.DarkGreenBlueStyle,
    "blue": pygal.style.BlueStyle,
}

CHART_TYPE = 'chart_type'
DATA = 'data'


def make_valid_yaml(d):
    d = d.replace(';','\n').replace(':', ': ')
    return d

def get_chart_type_from_parts(parts):
    return parts[0]

def get_chart_data_from_parts(parts):
    data_str = parts[1]
    data_yaml = make_valid_yaml(data_str)

    chart_data = yaml.round_trip_load(data_yaml)
    #chart_data = yaml.load(data_yaml, Loader=yaml.SafeLoader)
    return chart_data

def get_chart_config_from_parts(parts):
   if len(parts) == 3:
       chart_config_str = parts[2]
       chart_config_yaml = make_valid_yaml(chart_config_str)
       chart_config = yaml.round_trip_load(chart_config_yaml)
       #chart_config = yaml.load(chart_config_yaml, Loader=yaml.SafeLoader)
   else:
       chart_config = {}
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


#def chart_dict_from_chartist_url(text):
#    if text.endswith('/'):
#        text = text[:-1]
#
#    parts = text.split('/')[3:]
#    chart_type = get_chart_type_from_parts(parts)
#    chart_data = get_chart_data_from_parts(parts)
#    chart_config = get_chart_config_from_parts(parts)
#
#    chart_config = remove_underscore(chart_config)
#
#    return {"chart_type": chart_type,
#                  "data": chart_data,
#                  "chart_config": chart_config}
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


def get_chartist_url_from_text(text, idx, start_token, end_token):
    """
    eg = 'fdsdfdf <img alt="bailey" src="http://localhost:8080/line/one:[2,3,4];two:[5,6,7]" width="500" height="600">'
    """
    open_tag = _step_back_to_token(text, idx, start_token)
    http_start = _step_forward_to_token(text, open_tag, 'http')
    end = _step_forward_to_token(text, http_start, end_token)
    return text[http_start:end]

def _step_back_to_token(text, idx, token):
    if text[idx:len(token)+idx] == token:
        return idx

    for i in range(idx, -1, -1):
        if text[i-len(token):i] == token:
            return i-len(token)
    raise ValueError(f"Failed to find token '{token}': '{text}'")

def get_html_start(text, idx):
    return _step_back_to_token(text, idx, '<')

def _step_forward_to_token(text, idx, token):
    for i in range(idx-1, len(text)):
        if text[i:i+len(token)] == token:
            return i
    raise ValueError(f"Failed to find end of tag: '{text}'")

def get_html_end(text, idx):
    return _step_forward_to_token(text, idx, '>')

def get_md_end(text, idx):
    return _step_forward_to_token(text, idx, ')')

def get_idx(l, pattern):
    try:
        return l.index(pattern)
    except ValueError:
        return None

class Chartist:

    def __init__(
        self,
        chart_type: str,
        data: Dict[str, List[Any]],
        config: Dict[str, List[Any]],
        endpoint: Optional[str] = 'http://localhost:8080',
        precision: Optional[int] = 2
    ):
        self.chart_type = chart_type
        self.data = data
        self.config = config
        style = self.config.get('style', 'default').lower()
        self.update_style(style)

        self.endpoint = endpoint
        self.precision = precision

    def update_style(self, style: str):
        _style = STYLE_FROM_NAME_STR[style]
        self.config['style'] = _style

    def add_ranges(self, new_ranges: Dict[str, Any]):
        for k, v in new_ranges.items():
            self.data.update({k: v})

    def append_to_ranges(self, new_data: Dict[str, Any]):
        for k, v in new_data.items():
            self.data[k] += v

    @classmethod
    def from_url(cls, url):
        """Convert chartist formatted url into a Chartis object
        """
        if url.endswith('/'):
            url = url[:-1]

        parts = url.split('/')
        print(parts)
        chart_endpoint = '/'.join(parts[:3])
        chart_type = get_chart_type_from_parts(parts[3:])
        chart_data = get_chart_data_from_parts(parts[3:])
        chart_config = get_chart_config_from_parts(parts[3:])
        chart_config = remove_underscore(chart_config)

        return cls(
            chart_type,
            chart_data,
            chart_config,
            endpoint=chart_endpoint)

    @classmethod
    def from_text(cls, text, alt_text):
        token = f'![{alt_text}]'
        tag_start = get_idx(text, token)
        if tag_start is not None:
            chartist_url = get_chartist_url_from_line(line, tag_start, token, ')')

        token = f'alt="{alt_text}"'
        alt_idx = get_idx(text, token)
        if alt_idx is not None:
            chartist_url = get_chartist_url_from_text(text, alt_idx, '<img', '" ')

        return cls.from_url(chartist_url)


    def to_url(self):
        data_str = make_data_str(self.chart_type, self.data, prec=self.precision)
        style_str = dict_to_style_str(self.config)
        url = '/'.join([self.endpoint, self.chart_type, data_str, style_str])
        return url

    def to_html_tag(self, alt_text: str, height: Optional[int]=None, width: Optional[int]=None) -> str:
        url = self.to_url()
        parts = [f'<img src="{url}" alt="{alt_text}"']
        if height is not None:
            parts += [f'height="{height}"']

        if width is not None:
            parts += [f'width="{width}"']

        parts += '>'
        return ' '.join(parts)

    def to_markdown_tag(self, alt_text: str) -> str:
        url = self.to_url()
        return f'![{alt_text}]({url})'

    def insert_into_text(self,
                         text: str,
                         alt_text: str):
        """Inserts Chartist url into text

        Finds the Markdown or HTML image tag in the 'text'
        with specified 'alt_text' and replaces the url.

        Markdown: ![alt_text](url)
        HTML:     <img str="url" alt="alt_text" height="###" width="###" >

        The order with whihc src, alt, height and width
        are defined are not important. height and width are optional.
        Other attributes are also ok.
        """
        url = self.to_url()
        token = f'![{alt_text}]'
        tag_start = get_idx(text, token)
        if tag_start is not None:
            url_start = _step_forward_to_token(text, tag_start, '(')
            url_end = _step_forward_to_token(text, url_start, ')')
            text = ''.join([text[:url_start+1], url, text[url_end:]])
        else:
            token = f'alt="{alt_text}"'
            alt_idx = get_idx(text, token)
            if alt_idx is not None:
                tag_start = _step_back_to_token(text, alt_idx, '<img')
                url_start = _step_forward_to_token(text, tag_start, 'http')
                url_end = _step_forward_to_token(text, url_start, ' ')
                text = ''.join([text[:url_start], url, text[url_end-1:]])

        return text


    def to_svg(self):
        _chart_cls = CHART_FROM_NAME_STR[self.chart_type.lower()]
        chart = _chart_cls(**self.config)
        for k,v in self.data.items():
            chart.add(k, v)
        return chart

