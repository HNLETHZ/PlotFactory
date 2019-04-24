CC = g++
CFLAGS = -Wall -c -g -fpermissive 

INCLUDES = -I. -I.. -I$(ROOTSYS)/include -I$(ROOFIT_INCLUDE)/ -I$(CMSSW_BASE)/src -I$(CMSSW_BASE)/src/CommonTools -I$(CMSSW_BASE)/src/CondFormats/JetMETObjects/interface 

ROOTSYS ?= ERROR_RootSysIsNotDefined

ROOTFLAG = `${ROOTSYS}/bin/root-config --cflags --libs`


all:  map_FR

map_FR: map_FR.cpp 
	$(CC) -Wall $(INCLUDES) -o map_FR map_FR.cpp $(ROOTFLAG) $(EXTRALIBS) -fpermissive
