#!/usr/bin/env python2.7
# coding: utf-8
# @author: SENOO, Ken
# (Last Update: 2014-05-19T23:11+09:00)

import os, sys
import datetime
import subprocess

START=datetime.datetime(2013,6,1)

START_DATE=datetime.datetime(2013,6,1)
END_DATE=datetime.datetime(2013,6,2)
NOW=START_DATE
DAYS=END_DATE-START_DATE


PWD=os.getcwd()
WPS_DIR=PWD+"/WPS/"
WRF_DIR=PWD+"/WRFV3/"


for day in range(DAYS.days):
    NOW=START_DATE+datetime.timedelta(day)
    TOMORROW=NOW+datetime.timedelta(1)
    print(NOW)
    os.chdir(WPS_DIR)
   
    ## geogrid
    if NOW==START:
        print("first date run geogrid")
        os.system("sed 's/(START_DATE)/{DATE1}/g; s/(END_DATE)/{DATE2}/g' namelist.wps.tmpl > namelist.wps".format(
            DATE1=NOW.isoformat().replace("T","_"),
            DATE2=TOMORROW.isoformat().replace("T","_")))
        os.system("./geogrid.exe > geogrid.log")

    ## ungrib
    MET="/home/senooken/model/WRF/NCEP-FNL/fnl_{DATE}".format(DATE=NOW.strftime("%Y%m%d"))

    os.system("./link_grib.csh {MET}".format(MET=MET))
    os.system("ln -fs ./ungrib/Variable_Tables/Vtable.GFS Vtable")
    os.system("./ungrib.exe >ungrib.log") # Output for ungrib.exe result.

    ## metgrid
    os.system("./metgrid.exe > metgrid.log")
    os.chdir(PWD)

    os.chdir(WRF_DIR)
    
    os.system("ln -fs ../../WPS/met_em* .")


   # os.system("sed 's/(START_DATE)/{DATE1}/g; s/(END_DATE)/{DATE2}/g' namelist.wps.tmpl > namelist.wps".format(





