import click
import ruamel.yaml as yaml
from pathlib import Path

from chartist import Chartist

def load_module_fn(path):
    pass

def get_transform_function(transform_function):
    if transform_function is None:
        def fn(data_path):
            with Path(data_path).open('r') as f:
                data = yaml.round_trip_load(f)
            return data
    else:
        fn = load_module_fn(transform_function)

def get_config(config_path):
    if config_path is None:
        config = {}
    else:
        with Path(config_path).open('r') as f:
            config = yaml.round_trip_load(f)

@click.group()
def entrypoint():
    pass


@click.command("insert-chart", help=(
"Insert Chartist url into a text document.\n\n"
"Will read document and look for HTML or Markdown "
"image tags with the specified 'alt_text'. It will "
"then replace the existing source url with a new one "
"generated using the data and (optional) style "
"provided.\n"
"If 'transform' is provided is 'data-path' will be "
"passed directly to the transform function. That is "
"to say the transform function must hander reading "
"the data from file as well as parsing. For more "
"information see docs @ http://todo...:-p"
))
@click.option("-f", "--file-path", type=str,
              required=True,
              help="File to insert Chartist url")
@click.option("-a", "--alt-text", type=str,
              required=True,
              help=("The alternate text for image ie:"
                    "![<THIS BIT!!!>](http://...)"
                    '<img alt="<THIS BIT!!!>" src="http://..." >')
              )
@click.option("-t", "--chart-type", type=str,
              required=True,
              help="line | dot | pie | ...")
@click.option("-d", "--data-path", type=str,
              required=True,
              help="Path to data file")
@click.option("-c", "--config-path", type=str,
              required=False, default=None,
              help="Path to chart config file")
@click.option("-e", "--endpoint", type=str,
              required=False, default="http://localhost:8080",
              help="Location of Chartist server")
@click.option("-fn", "--transform-function", type=str,
              required=False, default=None,
              help="Path to data transform function")
def _insert_chart(file_path,
                  alt_text,
                  chart_type,
                  data_path,
                  config_path,
                  endpoint,
                  transform_function):
    fn = get_transform_function(transform_function)
    data = fn(data_path)
    config = get_config(config_path)

    chart = Chartist(
        chart_type,
        data,
        config,
        endpoint,
    )

    with Path(file_path).open('r') as f:
        text = f.read()

    new_text = chart.insert_into_text(text, alt_text)
    with Path(file_path).open('w') as f:
        f.write(new_text)

@click.command("add-ranges")
def _add_ranges():
    fn = get_transform_function(transform_function)
    data = fn(data_path)

    with Path(file_path).open('r') as f:
        text = f.read()

    chart = Chartist.from_text(text, alt_text)


    chart.add_ranges(data)
    new_text = chart.insert_into_text(text, alt_text)
    with Path(file_path).open('w') as f:
        f.write(new_text)

@click.command("append-to-ranges")
def _append_to_ranges():
    fn = get_transform_function(transform_function)
    data = fn(data_path)

    with Path(file_path).open('r') as f:
        text = f.read()

    chart = Chartist.from_text(text, alt_text)

    chart.append_to_ranges(data)

    new_text = chart.insert_into_text(text, alt_text)
    with Path(file_path).open('w') as f:
        f.write(new_text)

entrypoint.add_command(_insert_chart)
entrypoint.add_command(_add_ranges)
entrypoint.add_command(_append_to_ranges)

if __name__ == "__main__":
    entrypoint()
