from pathlib import Path
import ruamel.yaml as yaml

def fn(data_path):
    with Path(data_path).open('r') as f:
        data = yaml.round_trip_load(f)
    return data
