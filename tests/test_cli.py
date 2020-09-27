import pytest as pt
from click.testing import CliRunner

from chartist.cli import _insert_chart

insert_expected = {
    "line": (
'<img src="http://localhost:8080/line/trainin_loss:[.9,.5,.2,.05,.02,.01]/title:test-title;x_title:test-x-title;style:dark0 alt="test_line" height="600" width="600" >'
'<img src="http://localhost:8080 alt="test_pie" height="600" width="600" >'
'<img src="http://localhost:8080 alt="test_xy" height="600" width="600" >'
),
    "pie": (
'<img src="http://localhost:8080 alt="test_line" height="600" width="600" >'
'<img src="http://localhost:8080/pie/trainin_loss:[.9,.5,.2,.05,.02,.01]/title:test-title;x_title:test-x-title;style:dark0 alt="test_pie" height="600" width="600" >'
'<img src="http://localhost:8080 alt="test_xy" height="600" width="600" >'
),
    "xy": (
'<img src="http://localhost:8080 alt="test_line" height="600" width="600" >'
'<img src="http://localhost:8080 alt="test_pie" height="600" width="600" >'
'<img src="http://localhost:8080/xy/trainin_loss:[[1,3,5],[2,4,6]]/title:test-title;x_title:test-x-title;style:dark0 alt="test_xy" height="600" width="600" >'
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
    assert result.output == insert_expected[chart_type]
