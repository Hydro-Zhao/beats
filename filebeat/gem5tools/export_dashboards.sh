#!/bin/bash

# This script has some bugs.
# If there are some changes of m5out between the create of index and export of dashboard,
# this script would not work, and event makes the dashboard never been exported using ./filebeat

export M5OUT_MODIFICATION_TIME=$(date +%Y.%m.%d'-'%H.%M.%S -r $GEM5_PATH/m5out)
export M5OUT_MODIFICATION_TIME_FIELD=$(date -r $GEM5_PATH/m5out)

./filebeat export dashboard -yml module/gem/module.yml

rm -rf kibana
mkdir -p kibana/7/dashboard
cp -pr module/gem/_meta/kibana/7/dashboard/* kibana/7/dashboard
