#!/bin/bash

source vars.sh

docker build \
    -f Dockerfile \
    -t ${IMAGE_NAME}:${TAG} \
    .
