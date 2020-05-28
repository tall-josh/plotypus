import pygal
import yaml

CHART_FROM_NAME_STR = {
    "line" : pygal.Line,
    "stackedline": pygal.StackedLine,
    "bar": pygal.Bar,
    "stackedbar": pygal.StackedBar,
    "horizontalbar": pygal.HorizontalBar,
    "pie": pygal.Pie,
    "histogram": pygal.Histogram,
    "xy": pygal.XY
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

def validate_chart_dict(chart_dict):
    if not(CHART_TYPE in chart_dict):
        raise KeyError(f'"{CHART_TYPE}" must be specified')
    if not(chart_dict[CHART_TYPE].lower() in CHART_FROM_NAME_STR):
        raise ValueError(f'Invalid chart_type: "{chart_dict[CHART_TYPE]}"')
    if not(DATA in chart_dict):
        raise KeyError('"data" MUST be specified')

def get_chart_style(chart_dict):
    style_name = chart_dict['chart_config'].get('style', 'default').lower()
    return STYLE_FROM_NAME_STR[style_name]

def get_chart_constructor(chart_dict):
    chart_name = chart_dict['chart_type'].lower()
    return CHART_FROM_NAME_STR[chart_name]

def add_data_to_chart(chart, data):
    for k, v in data.items():
        chart.add(k, v)
    return chart

def make_chart(chart_dict):

    validate_chart_dict(chart_dict)

    chart_dict['chart_config']['style'] = get_chart_style(chart_dict)
    chart_constructor = get_chart_constructor(chart_dict)
    chart = chart_constructor(**chart_dict['chart_config'])
    chart = add_data_to_chart(chart, chart_dict['data'])

    return chart
