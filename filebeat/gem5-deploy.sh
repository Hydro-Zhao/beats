#!/bin/bash

# TODO an option to specific the name of the simulation output, pass it as an option of ./filebeat 

# 
curl -X DELETE "localhost:5601/s/gem5/api/saved_objects/index-pattern/gem5-filebeat-*" -H 'kbn-xsrf: true'
curl -X DELETE "localhost:5601/api/spaces/space/gem5" -H 'kbn-xsrf: true'
curl -X POST "localhost:5601/api/spaces/space" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d'
{
  "id": "gem5",
  "name": "gem5",
  "description" : "This is the gem5 Space",
  "color": "#FFFFFF",
  "disabledFeatures": ["monitoring","ml","siem","uptime","apm","map","maps","graph"],
  "imageUrl": "data:image/png;base64,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"
}
'
curl -X POST "localhost:5601/s/gem5/api/saved_objects/index-pattern/gem5-filebeat-*" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d'
{
  "attributes": {
    "title": "gem5-filebeat-*",
    "timeFieldName": "@timestamp"
  }
}
'


# for easily to test, delete later
curl -XDELETE 'http://localhost:9200/gem5-filebeat-*'


# deploy
export M5OUT_MODIFICATION_TIME=$(date +%Y.%m.%d'-'%H.%M.%S -r $GEM5_PATH/m5out)
export M5OUT_MODIFICATION_TIME_FIELD=$(date +%F'T'%T%z -r $GEM5_PATH/m5out)

rm -f data/registry/filebeat/data.json

make update

cp filebeat.gem.yml filebeat.yml

rm -rf kibana
mkdir -p kibana/7/dashboard
cp -pr module/gem/_meta/kibana/7/dashboard/* kibana/7/dashboard

./filebeat setup
./filebeat modules enable gem
./filebeat -e
