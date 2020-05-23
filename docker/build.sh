#!/bin/bash

source docker/vars.sh

docker build \
    -f docker/Dockerfile \
    -t ${IMAGE_NAME}:${TAG} \
    .
