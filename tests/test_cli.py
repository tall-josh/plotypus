import pytest as pt
from click.testing import CliRunner

from chartist.cli import _insert_chart, _append_to_ranges, _add_ranges

insert_expected = {
    "line": (
'<img src="http://localhost:8080/line/training_loss:[.9,.5,.2,.05,.02,.01]/title:test-title;x_title:test-x-title;style:dark" alt="test_line" height="600" width="600" >\n'
'<img src="http://localhost:8080" alt="test_pie" height="600" width="600" >\n'
'<img src="http://localhost:8080" alt="test_xy" height="600" width="600" >\n'
),
    "pie": (
'<img src="http://localhost:8080" alt="test_line" height="600" width="600" >\n'
'<img src="http://localhost:8080/pie/training_loss:[.9,.5,.2,.05,.02,.01]/title:test-title;x_title:test-x-title;style:dark" alt="test_pie" height="600" width="600" >\n'
'<img src="http://localhost:8080" alt="test_xy" height="600" width="600" >\n'
),
    "xy": (
'<img src="http://localhost:8080" alt="test_line" height="600" width="600" >\n'
'<img src="http://localhost:8080" alt="test_pie" height="600" width="600" >\n'
'<img src="http://localhost:8080/xy/training_loss:[[1,1],[2,2],[3,3],[4,4]]/title:test-title;x_title:test-x-title;style:dark" alt="test_xy" height="600" width="600" >\n'
),
}

@pt.mark.parametrize(
  "params",
    [
        [
            "-t", "line",
            "-f", "tests/data/test-file.txt",
            "-a", "test_line",
            "-d", "tests/data/test-data-line.yaml",
            "-c", "tests/data/test-config.yaml",
            "-e", "http://localhost:8080",
        ],
        [
            "-t", "xy",
            "-f", "tests/data/test-file.txt",
            "-a", "test_xy",
            "-d", "tests/data/test-data-xy.yaml",
            "-c", "tests/data/test-config.yaml",
            "-e", "http://localhost:8080",
        ],
        [
            "-t", "pie",
            "-f", "tests/data/test-file.txt",
            "-a", "test_pie",
            "-d", "tests/data/test-data-pie.yaml",
            "-c", "tests/data/test-config.yaml",
            "-e", "http://localhost:8080",
            "-fn", "tests/data/test-transform-fn.py",
        ],

    ]
)
def test_insert_chart(params, tmp_path):
    '''
    Options:
  -f, --file-path TEXT            File to insert Chartist url  [required]
  -a, --alt-text TEXT             The alternate text for image ie:![<THIS
                                  BIT!!!>](http://...)<img alt="<THIS BIT!!!>"
                                  src="http://..." >  [required]

  -t, --chart-type TEXT           line | dot | pie | ...  [required]
  -d, --data-path TEXT            Path to data file  [required]
  -c, --config-path TEXT          Path to chart config file
  -e, --endpoint TEXT             Location of Chartist server
  -fn, --transform-function TEXT  Path to data transform function
  -i, --inplace                   Edit the file at 'file-path' in place. Else
                                  print to terminal
    '''
    chart_type = params[1]
    runner = CliRunner()
    result = runner.invoke(_insert_chart, params)
    assert result.exit_code == 0, result.exception
    assert result.output == insert_expected[chart_type], f'\nexpected:\n{insert_expected[chart_type]}\n---\ngot:\n{result.output}'


add_expected = {
    "line": (
'<img src="http://localhost:8080/line/training_loss_00:[.9,.5,.2,.05,.02,.01];training_loss_01:[.9,.5,.2,.05,.02,.01]/title:test-title;x_title:test-x-title;style:dark" alt="test_line" height="600" width="600" >\n'
'<img src="http://localhost:8080" alt="test_pie" height="600" width="600" >\n'
'<img src="http://localhost:8080" alt="test_xy" height="600" width="600" >\n'
    ),
    "xy": 123
}

@pt.mark.parametrize(
  "params",
    [
        [
            "-f", "tests/data/test-file-add-ranges.txt",
            "-a", "test_line",
            "-d", "tests/data/test-data-line.yaml",
        ],
        [
            "-f", "tests/data/test-file-add-ranges.txt",
            "-a", "test_xy",
            "-d", "tests/data/test-data-xy.yaml",
        ],

    ]
)
def test_add_ranges(params, tmp_path):
    '''
    Options:
      -f, --file-path TEXT            File to insert Chartist url  [required]
      -a, --alt-text TEXT             The alternate text for image ie:![<THIS
                                      BIT!!!>](http://...)<img alt="<THIS BIT!!!>"
                                      src="http://..." >  [required]

      -d, --data-path TEXT            Path to data file  [required]
      -fn, --transform-function TEXT  Path to data transform function
      -i, --inplace                   Edit the file at 'file-path' in place. Else
                                      print to terminal
    '''
    runner = CliRunner()
    result = runner.invoke(_add_ranges, params)
    assert result.exit_code == 0, result.exception
    assert result.output == add_expected[chart_type], f'\nexpected:\n{add_expected[chart_type]}\n---\ngot:\n{result.output}'


append_expected = {}

@pt.mark.parametrize(
  "params",
    [
        [
            "-t", "line",
            "-f", "tests/data/test-file.txt",
            "-a", "test_line",
            "-d", "tests/data/test-data-line.yaml",
            "-c", "tests/data/test-config.yaml",
            "-e", "http://localhost:8080",
        ],
        [
            "-t", "xy",
            "-f", "tests/data/test-file.txt",
            "-a", "test_xy",
            "-d", "tests/data/test-data-xy.yaml",
            "-c", "tests/data/test-config.yaml",
            "-e", "http://localhost:8080",
        ],
        [
            "-t", "pie",
            "-f", "tests/data/test-file.txt",
            "-a", "test_pie",
            "-d", "tests/data/test-data-pie.yaml",
            "-c", "tests/data/test-config.yaml",
            "-e", "http://localhost:8080",
            "-fn", "tests/data/test-transform-fn.py",
        ],

    ]
)

def test_append_to_ranges(params, tmp_path):
    assert False
    runner = CliRunner()
    result = runner.invoke(_insert_chart, params)
    assert result.exit_code == 0, result.exception
    assert result.output == append_expected[chart_type], f'\nexpected:\n{append_expected[chart_type]}\n---\ngot:\n{result.output}'
