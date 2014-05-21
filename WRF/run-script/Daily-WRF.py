#!/usr/bin/env python2.7
# coding: utf-8
# @author: SENOO, Ken
# (Last Update: 2014-05-21T08:11+09:00)

import os, sys
import datetime
import subprocess

START=datetime.datetime(2013,6,1)

START_DATE=datetime.datetime(2013,6,1)
END_DATE=datetime.datetime(2013,6,3)
NOW=START_DATE
DAYS=END_DATE-START_DATE


PWD=os.getcwd()
WPS_DIR=PWD+"/WPS/"
WRF_DIR=PWD+"/WRFV3/run/"


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
    MET="/home/senooken/model/WRF/NCEP-FNL/fnl_{DATE}*".format(DATE=NOW.strftime("%Y%m%d"))

    os.system("./link_grib.csh {MET}".format(MET=MET))
    os.system("ln -fs ./ungrib/Variable_Tables/Vtable.GFS Vtable")
    os.system("./ungrib.exe > ungrib.log") # Output for ungrib.exe result.

    ## metgrid
    os.system("./metgrid.exe > metgrid.log")
    os.chdir(PWD)

    os.chdir(WRF_DIR)
    
    os.system("ln -fs ../../WPS/met_em* .")

    if NOW == START:
        IS_RESTART = ".false."
    else:
        IS_RESTART = ".true."


    os.system("""sed '
    s/(YEAR1)/{year1}/g;
    s/(MONTH1)/{month1}/g;
    s/(DAY1)/{day1}/g;
    s/(YEAR2)/{year2}/g;
    s/(MONTH2)/{month2}/g;
    s/(DAY2)/{day2}/g;
    s/(IS_RESTART)/{is_start}/g;
    ' namelist.input.tmpl > namelist.input""".format(
        year1=NOW.year,
        month1=NOW.month,
        day1=NOW.day,
        year2=TOMORROW.year,
        month2=TOMORROW.month,
        day2=TOMORROW.day,
        is_start=IS_RESTART
        )
    )
 
    #os.system("time mpirun -n 2 ./real.exe > real.log" )
    #os.system("time mpirun -n 2 ./wrf.exe > wrf.log" )
    os.system("time ./real.exe > real.log" )
    os.system("time ./wrf.exe > wrf.log 2>&1")

