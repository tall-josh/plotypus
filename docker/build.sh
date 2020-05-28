#!/bin/bash

source docker/vars.sh

echo "docker build \
    -f docker/Dockerfile \
    -t ${IMAGE_NAME}:${TAG} \
    ."
