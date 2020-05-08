#!/bin/bash

export M5OUT_MODIFICATION_TIME=$(date +%Y.%m.%d'-'%H.%M.%S -r $GEM5_PATH/m5out)
export M5OUT_MODIFICATION_TIME_FIELD=$(date +%F'T'%T%z -r $GEM5_PATH/m5out)

rm -f data/registry/filebeat/data.json
cp $SimpleSSD_OUTPUT_PATH/DebugLogFile.txt $SimpleSSD_OUTPUT_PATH/DebugLogFileAll.txt
./filebeat setup
./filebeat modules enable gem
./filebeat -e
