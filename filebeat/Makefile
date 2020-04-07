BEAT_NAME?=filebeat
BEAT_TITLE?=Filebeat
SYSTEM_TESTS?=true
TEST_ENVIRONMENT?=true
GOX_FLAGS=-arch="amd64 386 arm ppc64 ppc64le"
ES_BEATS?=..
EXCLUDE_COMMON_UPDATE_TARGET=true

include ${ES_BEATS}/libbeat/scripts/Makefile

.PHONY: update
update: mage
	mage update

# Creates a new module. Requires the params MODULE.
.PHONY: create-module
create-module:
	@go run ${ES_BEATS}/filebeat/scripts/generator/module/main.go --path=$(PWD) --beats_path=$(BEAT_GOPATH)/src/$(BEAT_PATH) --module=$(MODULE)

# Creates a new fileset. Requires the params MODULE and FILESET.
.PHONY: create-fileset
create-fileset:
	@go run ${ES_BEATS}/filebeat/scripts/generator/fileset/main.go --path=$(PWD) --beats_path=$(BEAT_GOPATH)/src/$(BEAT_PATH) --module=$(MODULE) --fileset=$(FILESET)

# Creates a fields.yml based on a pipeline.json file. Requires the params MODULE and FILESET.
.PHONY: create-fields
create-fields:
	@go run ${ES_BEATS}/filebeat/scripts/generator/fields/main.go --beats_path=$(BEAT_GOPATH)/src/$(BEAT_PATH) --module=$(MODULE) --fileset=$(FILESET)







# this is my own,,,,,,,,
.PHONY: dashboard-gem
dashboard-gem:
	@./filebeat export dashboard -yml module/gem/module.yml

.PHONY: kibana-gem
kibana-gem:
	@rm -rf kibana
	@mkdir -p kibana/7/dashboard
	@-cp -pr module/gem/_meta/kibana/7/dashboard/* kibana/7/dashboard

.PHONY: deploy
deploy:
	@rm -f data/registry/filebeat/data.json
	#@curl -X DELETE "localhost:5601/s/gem5/api/saved_objects/index-pattern/gem5-filebeat-*" -H 'kbn-xsrf: true'
	@make update
	@cp fields.gem.yml fields.yml
	@cp filebeat.gem.yml filebeat.yml
	@./filebeat setup
	@./filebeat modules enable gem
	@./filebeat -e

.PHONY: stats
stats:
	@make create-fields MODULE=gem FILESET=stats
.PHONY: config
config:
	@make create-fields MODULE=gem FILESET=config
.PHONY: pipeview
pipeview:
	@make create-fields MODULE=gem FILESET=pipeview

#TODO remove other modules under module folder, other config files under modules.d, and other dashboards
.PHONY: small
small:
	@make kibana-gem
