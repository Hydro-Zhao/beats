#!/bin/bash

export M5OUT_MODIFICATION_TIME=$(date +%Y.%m.%d'-'%H.%M.%S -r $GEM5_PATH/m5out)
export M5OUT_MODIFICATION_TIME_FIELD=$(date -r $GEM5_PATH/m5out)

./filebeat export dashboard -yml module/gem/module.yml
