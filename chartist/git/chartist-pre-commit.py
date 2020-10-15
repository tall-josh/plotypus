import yaml
import sys
import importlib
from chartist.git.hooks import add_ranges, append_to_ranges

fns = {"append": append_to_ranges,
       "add": add_ranges}

def load_data_loader_fn(module_path):
    module = importlib.machinery.SourceFileLoader('module', module_path).load_module()
    return getattr(module, "fn")

with open(".chartist/tracked.yaml", 'r') as f:
    tracked = yaml.load(f, Loader=yaml.SafeLoader)

added_files = sys.argv[1:]
try:
    updated = ["0"]
    for f in tracked:
        if f["data_file"] in added_files:
            loader_fn = load_data_loader_fn(f["loader_fn"])
            data = loader_fn(f["data_file"])
            fns[f["mode"]](f["file"], f["alt_text"], data, config_path=f.get("config", None))
            updated += [f["file"]]
    print(" ".join(updated))
except Exception as e:
    print(f"1 something went wrong: {e}")


