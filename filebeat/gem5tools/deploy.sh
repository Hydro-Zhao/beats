#!/bin/bash

export M5OUT_MODIFICATION_TIME=$(date +%Y.%m.%d'-'%H.%M.%S -r $GEM5_PATH/m5out)
export M5OUT_MODIFICATION_TIME_FIELD=$(date +%F'T'%T%z -r $GEM5_PATH/m5out)

rm -f data/registry/filebeat/data.json
./filebeat setup
./filebeat modules enable gem
./filebeat -e
