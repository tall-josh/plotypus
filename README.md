# Usage

```
pip install -r requirements.txt
python launch.py
```

# Markdown

`![test](http://127.0.0.1:5000/get-chart/tall-josh/yamgal/master/examples/lines-01.yaml)`
![test](http://127.0.0.1:5000/get-chart/tall-josh/yamgal/master/examples/lines-01.yaml)


# Gotcha

Browsers tend to cache the images, so if your plat changes you can
add a random `?<random strnig>` at the end of the url.

`![test](http://127.0.0.1:5000/get-chart/tall-josh/yamgal/master/examples/lines-01.yaml?<change this each time the plot changes>)`

# ToDo

  - [ ] Githook the does the finds image urls ending in `.yaml`. Taking hash of file and appending it to the url string.

