# Usage

```
pip install -r requirements.txt
python launch.py
```

# Markdown

`![test](https://rphzfmonf1.execute-api.ap-southeast-2.amazonaws.com/dev/get-chart/tall-josh/yamgal/master/examples/lines-01.yaml?ercwddfdd2)`
![test](https://rphzfmonf1.execute-api.ap-southeast-2.amazonaws.com/dev/get-chart/tall-josh/yamgal/master/examples/lines-01.yaml?ercwddfdd2)


# Gotcha

Browsers tend to cache the images, so if your plat changes you can
add a random `?<random strnig>` at the end of the url.

`![test](http://127.0.0.1:5000/get-chart/tall-josh/yamgal/master/examples/lines-01.yaml?<change this each time the plot changes>)`

# ToDo

  - [ ] Githook the does the finds image urls ending in `.yaml`. Taking hash of file and appending it to the url string.

