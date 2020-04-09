#!/bin/bash

touch $GEM5_PATH/m5out/tmp
rm $GEM5_PATH/m5out/tmp
export M5OUT_MODIFICATION_TIME=$(date +%Y.%m.%d'-'%H.%M.%S -r $GEM5_PATH/m5out)
export M5OUT_MODIFICATION_TIME_FIELD=$(date -r $GEM5_PATH/m5out)
rm -f data/registry/filebeat/data.json
make update
cp filebeat.gem.yml filebeat.yml
./filebeat setup
./filebeat modules enable gem
./filebeat -e
