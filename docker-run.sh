#!/bin/bash

source vars.sh

docker run -it \
    --rm \
    --name ${CONTAINER_NAME}-${USER} \
    -v `pwd`:/opt/code/ \
    -p ${PORT_OUTSIDE}:${PORT_INSIDE} \
    ${IMAGE_NAME}:${TAG}
