import pygal
import re
from time import time
from pygal.graph.graph import Graph
from typing import List, Dict, Any, Optional, OrderedDict
import ruamel.yaml as yaml
from collections import OrderedDict as ODict

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

    # yaml.round_trip_load perserves order key-value pairs appear
    # returning an ordered dict
    chart_data = yaml.round_trip_load(data_yaml)
    return chart_data

def get_chart_config_from_parts(parts):
   if len(parts) == 3:
       chart_config_str = parts[2]
       chart_config_yaml = make_valid_yaml(chart_config_str)
       chart_config = yaml.round_trip_load(chart_config_yaml)
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

def _nd_data_to_str(data, prec=2):
    """
    data: {"rangeA": [[x1,y1,z1],[x2,y2,z2],...],
           "rangeB": ...}

    """
    s = []
    for k,v in data.items():
        v_str = str([list_to_str(point,prec=prec) for point in v]).replace(' ','').replace('"','').replace("'",'')
        s += [f'{k}:{v_str}']
    return ';'.join(s)

def _guess_data_converter(data):
    _data_types = {type(v) for v in data.values()}
    if len(_data_types) > 1:
        raise  ValueError((
            "Cannot specify data consisting of interables "
            "AND scalars. Pick one!"))

    return {list: _nd_data_to_str,
            tuple: _nd_data_to_str}.get(list(_data_types)[0], _1d_data_to_str)

#def make_data_str(chart_type, data, prec=2):
#    converter = _get_data_converter(data)
#    return converter(data, prec=prec)

#def make_data_str(chart_type, data, prec=2):
#    s = []
#    for k,v in data:
#        if isinstance(v, (list,tuple)):
#            converter = _nd_data_to_str
#        else:
#            converter = _1d_data_to_str
#        v_str = converter(k,v)
#        s += [f'{k}:{v_str}']



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

def remove_query_string(url):
    q_idx = get_idx(url, '?')
    if q_idx is not None:
        url = url[:q_idx]
    return url

class Chartist:

    def __init__(
        self,
        chart_type: str,
        data: OrderedDict[str, List[Any]],
        config: Optional[Dict[str, List[Any]]]={},
        endpoint: Optional[str] = 'http://localhost:8080',
        precision: Optional[int] = 2
    ):
        self.chart_type = chart_type
        self.data = data
        self.config = config

        self.endpoint = endpoint
        self.precision = precision

        self.converter = _guess_data_converter(self.data)

        # If True, will append a random query string
        # to the end of urls so the browser is forced
        # to reload the image rather than use the cache.
        self._debug = False

    @classmethod
    def from_url(cls, url):
        """Convert chartist formatted url into a Chartis object
        """
        if url.endswith('/'):
            url = url[:-1]

        url = remove_query_string(url)

        parts = url.split('/')
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
        chartist_url = None
        token = f'![{alt_text}]'
        tag_start = get_idx(text, token)
        if tag_start is not None:
            chartist_url = get_chartist_url_from_line(line, tag_start, token, ')')

        token = f'alt="{alt_text}"'
        alt_idx = get_idx(text, token)
        if alt_idx is not None:
            chartist_url = get_chartist_url_from_text(text, alt_idx, '<img', '" ')

        if chartist_url is None:
            raise KeyError(f"Failed to find alt_text: '{alt_text}' in text.")

        return cls.from_url(chartist_url)


    def to_url(self):
        data_str = self.converter(self.data, prec=self.precision)
        style_str = dict_to_style_str(self.config)
        parts = [self.endpoint, self.chart_type, data_str, style_str]

        if self._debug:
            s = parts[-1]
            parts[-1] = f"{s}?{int(time())}"

        url = '/'.join(parts)


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

    def _replace_chart_source(self, text, alt_text, src):
        token = f'![{alt_text}]'
        tag_start = get_idx(text, token)
        if tag_start is not None:
            src_start = _step_forward_to_token(text, tag_start, '(')
            src_end = _step_forward_to_token(text, src_start, ')')
            new_text = ''.join([text[:src_start+1], src, text[src_end:]])
        else:
            token = f'alt="{alt_text}"'
            alt_idx = get_idx(text, token)
            if alt_idx is not None:
                tag_start = _step_back_to_token(text, alt_idx, '<img')
                src_start = _step_forward_to_token(text, tag_start, 'http')
                src_end = _step_forward_to_token(text, src_start, ' ')
                new_text = ''.join([text[:src_start], src, text[src_end-1:]])

        return new_text


    def _insert_chart_url(self, text, alt_text):
        url = self.to_url()
        return self._replace_chart_source(text, alt_text, url)


    def _insert_chart_local(self, text, alt_text, local_path):
        svg = self.to_svg(save_path=local_path)
        return self._replace_chart_source(text, alt_text, local_path)

    def insert_into_text(self,
                         text: str,
                         alt_text: str,
                         local_path: Optional[str]=None):
        """Inserts Chartist url into text

        Finds the Markdown or HTML image tag in the 'text'
        with specified 'alt_text' and replaces the url.

        Markdown: ![alt_text](url)
        HTML:     <img str="url" alt="alt_text" height="###" width="###" >

        The order with whihc src, alt, height and width
        are defined are not important. height and width are optional.
        Other attributes are also ok.
        """
        if local_path is None:
            new_text = self._insert_chart_url(text, alt_text)
        else:
            new_text = self._insert_chart_local(text, alt_text, local_path)

        return new_text



    def add_ranges(self, new_ranges: OrderedDict[str, Any]):
        """Adds one or more ranges to an existing Chartist url

        Finds the Markdown or HTML image tag in the 'text'
        with specified 'alt_text'. Parses it into a Chartist.Chart
        object. Adds the 'new_ranges'.

        Markdown: ![alt_text](url)
        HTML:     <img str="url" alt="alt_text" height="###" width="###" >
        The order with whihc src, alt, height and width
        are defined are not important. height and width are optional.
        Other attributes are also ok.

        Use insert_chart to overwrite the existing url in a document.

        **Duplicate Range Names**: If duplicate range names are found
        this will append '_xx' to the ranges with duplications.
        Chartist uses the existing url to preserve previous chart
        state, and OrderedDicts to preserve order, so.
        For example if an existing chart has data:

            'train:[1,2,3];eval:[4,5,6]'

        and:

            new_ranges={'train': [7,8,9]}

        Then the resulting chart data would be:

            'train_00:[1,2,3];eval:[4,5,6];train_01:[7,8,9]'
        """
        def rename_duplicates( old ):
            seen = {}
            for x in old:
                if old.count(x) == 1:
                    range_name = x
                elif x in seen:
                    seen[x] += 1
                    range_name = "{}_{:02}".format(x, seen[x])
                else:
                    seen[x] = 0
                    range_name = "{}_{:02}".format(x, seen[x])
                yield range_name

        vs = list(self.data.values()) + list(new_ranges.values())
        ks = list(self.data.keys()) + list(new_ranges.keys())
        _re = r'_\d{2}$'  # Regex pattern to match 
        ks_stripped = [re.sub(_re,'',k) for k in ks]

        ks_incremented = list(rename_duplicates(ks_stripped))
        self.data = ODict([(k,v) for k,v in zip(ks_incremented,vs)])

    def append_to_ranges(self, new_data: Dict[str, Any]):
        """Appends data to ranges to an existing Chartist url

        Finds the Markdown or HTML image tag in the 'text'
        with specified 'alt_text'. Parses it into a Chartist.Chart
        object. Adds the 'new_ranges'.

        The order with whihc src, alt, height and width
        are defined are not important. height and width are optional.
        Other attributes are also ok.

        Use insert_chart to overwrite the existing url in a document.
        """

        for k, v in new_data.items():
            self.data[k] += v

    def to_svg(self, save_path:Optional[str]=None):
        cfg = self.config.copy()
        style_str = cfg.get('style', 'default').lower()
        cfg['style'] = STYLE_FROM_NAME_STR[style_str]

        chart_constructor = CHART_FROM_NAME_STR[self.chart_type.lower()]
        chart = chart_constructor(**cfg)
        for k,v in self.data.items():
            chart.add(k, v)

        if save_path:
            chart.save(save_path)
            return None

        return chart

