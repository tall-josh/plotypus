# Metrics SVG

The ultimate goal for this is to emulate teh GitHub Shield's functionality 
but for simple charts This is what I'm working towards.

Say I have a ML model with a metrics file.

```yaml
# training-loss.yaml

run-01:
  - 0.1
  - 0.2
  - 0.3
  - 0.4
run-02:
  - 0.2
  - 0.3
  - 0.4
  - 0.5
```

Well I would love to be able to reference this in my README.md

```
![train loss](http://metrics-svg/line-chart/tall-josh/metrics-svg/blob/master/test/train-acc.yaml)
```

And have it render a nice chart for me.

We could even add some additional keys to the `yaml`

```yaml
title: Train Accuracy
x_title: Accuracy
y_title: Poop
x_labels: [a,b,c,d,e,f,g]
y_labels: [a,b,c,d,e,f,g,h,i]

# Valid values: cubic, quadratic, lagrange, trigonometric, hermite
# or ommit from yaml
# See: http://www.pygal.org/en/stable/documentation/configuration/interpolations.html
#interpolate: lagrange
data:
    run-01:
        - 0.1959999918937683
        - 0.1069999814033508
        - 0.1539999723434448
        - 0.1889999985694885
        - 0.1999999761581421
        - 0.1160000085830688
        - 0.1340000152587891
...
```

This is a pre-baked example. Using Pygal. 

![train metrics](https://k3l1upy16j.execute-api.ap-southeast-2.amazonaws.com/dev/line-chart/tall-josh/metrics-svg/master/test/train-acc_run-05.yaml)
