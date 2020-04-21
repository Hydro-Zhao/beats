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
.PHONY: gem5-stats
gem5-stats:
	make create-fields MODULE=gem FILESET=stats
.PHONY: gem5-config
gem5-config:
	make create-fields MODULE=gem FILESET=config
.PHONY: gem5-pipeview
gem5-pipeview:
	make create-fields MODULE=gem FILESET=pipeview
.PHONY: gem5-dram
gem5-dram:
	make create-fields MODULE=gem FILESET=dram
.PHONY: gem5-configImg
gem5-configImg:
	make create-fields MODULE=gem FILESET=configImg
.PHONY: gem5-SimpleSSDDebugLog
gem5-SimpleSSDDebugLog:
	make create-fields MODULE=gem FILESET=SimpleSSDDebugLog
.PHONY: gem5-SimpleSSDLog
gem5-SimpleSSDLog:
	make create-fields MODULE=gem FILESET=SimpleSSDLog
.PHONY: gem5-GarnetSyntheticTraffic
gem5-GarnetSyntheticTraffic:
	make create-fields MODULE=gem FILESET=GarnetSyntheticTraffic
.PHONY: gem5-Ruby
gem5-Ruby:
	make create-fields MODULE=gem FILESET=Ruby
