import json
from chartist.chart import Chartist, load_config

#DATA="eval-metrics.json"
#CONFIG=".chartist/config.yaml"
#ENDPOINT = 'https://yamgal-server-c6l3dwv2sq-de.a.run.app'
#TARGET_FILE="README.md"
#ALT_TEXT="eval_metrics"
#
#def load_data(path):
#    with open(path, 'r') as f:
#        data = json.load(f)
#    return data
#
#data = load_data(DATA)

def add_ranges(target_file, alt_text, data, config_path=None):
    with open(target_file, 'r') as f:
        text = f.read()

    chart = Chartist.from_text(text, alt_text)
    chart.add_ranges(data)

    if config_path is not None:
        config = load_config(config_path)
        chart.config = config

    new_text = chart.insert_into_text(text, alt_text)
    with open(target_file, 'w') as f:
        f.write(new_text)

def append_to_ranges(target_file, alt_text, data, config_path=None):
    with open(target_file, 'r') as f:
        text = f.read()

    chart = Chartist.from_text(text, alt_text)
    chart.append_to_ranges(data)

    if config_path is not None:
        config = load_config(config_path)
        chart.config = config

    new_text = chart.insert_into_text(text, alt_text)
    with open(target_file, 'w') as f:
        f.write(new_text)

#def setup_hooks():
#
#
#if __name__ == "__main__":
#    setup_hooks()
