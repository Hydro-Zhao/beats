#!/bin/bash


# this is originally from Makefile
#.PHONY: gem5-stats
#gem5-stats:
#	make create-fields MODULE=gem FILESET=stats
#.PHONY: gem5-config
#gem5-config:
#	make create-fields MODULE=gem FILESET=config
#.PHONY: gem5-pipeview
#gem5-pipeview:
#	make create-fields MODULE=gem FILESET=pipeview
#.PHONY: gem5-dram
#gem5-dram:
#	make create-fields MODULE=gem FILESET=dram
#.PHONY: gem5-configImg
#gem5-configImg:
#	make create-fields MODULE=gem FILESET=configImg
#.PHONY: gem5-SimpleSSDDebugLog
#gem5-SimpleSSDDebugLog:
#	make create-fields MODULE=gem FILESET=SimpleSSDDebugLog
#.PHONY: gem5-SimpleSSDLog
#gem5-SimpleSSDLog:
#	make create-fields MODULE=gem FILESET=SimpleSSDLog
#.PHONY: gem5-GarnetSyntheticTraffic
#gem5-GarnetSyntheticTraffic:
#	make create-fields MODULE=gem FILESET=GarnetSyntheticTraffic
#.PHONY: gem5-Ruby
#gem5-Ruby:
#	make create-fields MODULE=gem FILESET=Ruby

# TODO add command line options
make create-fields MODULE=gem FILESET=stats
make create-fields MODULE=gem FILESET=config
make create-fields MODULE=gem FILESET=pipeview
make create-fields MODULE=gem FILESET=dram
make create-fields MODULE=gem FILESET=configImg
make create-fields MODULE=gem FILESET=SimpleSSDDebugLog
make create-fields MODULE=gem FILESET=SimpleSSDLog
make create-fields MODULE=gem FILESET=GarnetSyntheticTraffic
make create-fields MODULE=gem FILESET=Ruby
make create-fields MODULE=gem FILESET=RubyTopology
make create-fields MODULE=gem FILESET=exec
