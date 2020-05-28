# Usage

```
./docker/build.sh
./docker/run.sh
```

# Markdown


`![demo](https://yamlgal-py3-alpine-c6l3dwv2sq-de.a.run.app/pie/one:0.1;two:0.2;three:0.3;four:0.4/style:neon;title:Pie_Chart)`

![demo](https://yamlgal-py3-alpine-c6l3dwv2sq-de.a.run.app/pie/one:0.1;two:0.2;three:0.3;four:0.4/style:neon;title:Pie_Chart)

# Gotcha

Browsers tend to cache the images, so if your plat changes you can
add a random `?<random strnig>` at the end of the url.

`![test](http://127.0.0.1:5000/get-chart/tall-josh/yamgal/master/examples/lines-01.yaml?<change this each time the plot changes>)`

# ToDo

  - [ ] Githook the does the finds image urls ending in `.yaml`. Taking hash of file and appending it to the url string.

