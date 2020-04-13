#!/bin/bash

curl -XDELETE 'http://localhost:9200/gem5-filebeat-*'
export M5OUT_MODIFICATION_TIME=$(date +%Y.%m.%d'-'%H.%M.%S -r $GEM5_PATH/m5out)
export M5OUT_MODIFICATION_TIME_FIELD=$(date -r $GEM5_PATH/m5out)
rm -f data/registry/filebeat/data.json
make update
cp filebeat.gem.yml filebeat.yml
./filebeat setup
./filebeat modules enable gem
./filebeat -e
