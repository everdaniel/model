#!/usr/bin/env python2.7
# coding: utf-8
# @author: SENOO, Ken
# (Last Update: 2014-05-28T09:32+09:00)

"""flow
1. import module.
2. open file.
3. get projection.
4. get point(observation) position and convert.
5. extract point data.
"""

import netCDF4
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import os, sys
import datetime

model_type="WRF"
ROOTDIR="~/run/20140528_WIND_MTG/"
ROOTDIR=os.path.expanduser(ROOTDIR)
INDIR=ROOTDIR+"output/"
POSDIR=ROOTDIR+"observation/"
POS_FILE="observation-position-d2.csv"

#FR=INDIR+INFILE
OUTDIR=ROOTDIR+"point/"

if not os.path.exists(OUTDIR): os.makedirs(OUTDIR)

START_DATE=datetime.datetime(2013,6,1)
END_DATE=datetime.datetime(2013,6,4)

DAYS=END_DATE-START_DATE


for day in range(DAYS.days):
    NOW=START_DATE+datetime.timedelta(day)
    print(NOW.isoformat())
    INFILE="wrfout_d01_{date}_00:00:00".format(date=NOW.strftime("%Y-%m-%d"))
    MODEL_NC=netCDF4.Dataset(INDIR+INFILE)
    
    if day == 0:
        ## get variable list and unit list
        #varlist=MODEL_NC.variables.keys()
        #varlist=MODEL_NC.getncattr("VAR-LIST").split()
        #varlist="MAPFAC_MX MAPFAC_MY SINALPHA COSALPHA Q2 PSFC T2 TH2 U10 V10 RAINC RAINSH RAINNC SNOWNC".split()
        varlist="Q2 PSFC T2 TH2 U10 V10 RAINC RAINSH RAINNC SNOWNC".split()
        varlist.sort()
        UNITLIST=[MODEL_NC.variables[var].units.strip() for var in varlist]
        DESCLIST=[MODEL_NC.variables[var].description for var in varlist]
#        varlist.extend("PM0.1 PM2.5 PM10".split())
#        UNITLIST=[word.replace("micrograms","ug") for word in UNITLIST]
#        UNITLIST=[word.replace("**","") for word in UNITLIST]
#        UNITLIST=UNITLIST+["ug/m3"]*3

        ## get projection information
        XCENT=MODEL_NC.CEN_LON
        YCENT=MODEL_NC.CEN_LAT

        DX=MODEL_NC.DX
        DY=MODEL_NC.DY

        P_ALP=MODEL_NC.TRUELAT1
        P_BET=MODEL_NC.TRUELAT2

        NCOLS=MODEL_NC.getncattr("WEST-EAST_PATCH_END_UNSTAG")
        NROWS=MODEL_NC.getncattr("SOUTH-NORTH_PATCH_END_UNSTAG")

        ## basemap
        BM=Basemap(resolution="c", projection="lcc", lat_1=P_ALP, lat_2=P_BET, width=DX*(NCOLS-1), height=DY*(NROWS-1), lat_0=YCENT, lon_0=XCENT, rsphere=(6370000.0, 6370000.0))

        plt.ion()
        plt.clf()
        PARAMS={
                "font.size": 18,
                "legend.fontsize": "medium",
                "lines.markersize": 10,
                }
        plt.rcParams.update(PARAMS)

        BM.drawcoastlines()
        BM.fillcontinents(color=(0.8,1,0.8))
        #BM.drawparallels(np.arange(-90,90,1),labels=[0,1,0,0])
        #BM.drawmeridians(np.arange(-180,180,1),labels=[0,0,0,1])
        BM.drawparallels(np.arange(np.floor(BM.llcrnrlat), np.ceil(BM.urcrnrlat), 0.1),labels=[1,0,0,0])
        BM.drawmeridians(np.arange(np.floor(BM.llcrnrlon), np.ceil(BM.urcrnrlon), 0.1),labels=[0,0,0,1])


        pos_array=np.genfromtxt(POSDIR+POS_FILE,delimiter=",",names=True,dtype=None)

        ## automatically get lattitude laongitude column header from character  "lat", "lon".
        ## automatically get position column header  from character "loc" or "cit" or "cap".
        LON_LABEL="".join(filter(lambda x: "lon" in x.lower(), pos_array.dtype.names))
        LAT_LABEL="".join(filter(lambda x: "lat" in x.lower(), pos_array.dtype.names))
        POS_LABEL="".join(filter(lambda x: "loc" in x.lower() or "cit" in x.lower() or  "cap" in x.lower(), pos_array.dtype.names))
        ## get array of longitude, latitude, position name.
        pos_lon=pos_array[LON_LABEL]
        pos_lat=pos_array[LAT_LABEL]
        pos_city=pos_array[POS_LABEL]

        markers="o p d D < > ^ v p s d D * d x 6 7".split()

        ## convert 1-D list of position  to 2-D mesh
        base_lon,base_lat=BM(pos_lon,pos_lat)

        ## plot observation
        for i,city in enumerate(range(len(pos_array))):
            plt.plot(base_lon[i],base_lat[i],c=plt.cm.rainbow(i*290/len(pos_array)),marker=markers[i],label=pos_city[i],alpha=1)

        plt.legend(loc="best")
        obstitle="Position of Observation"
        plt.title(obstitle)

        #plt.savefig(ROOTDIR+"fig/position.pdf",bbox_inches="tight")
        plt.savefig(OUTDIR+"/position.png",bbox_inches="tight")
        plt.savefig(OUTDIR+"/position.pdf",bbox_inches="tight")

        ## convert projected x, y to model col, row.
        model_col=np.vectorize(round)(base_lon/DX -1.0).astype(int)
        model_row=np.vectorize(round)(base_lat/DY -1.0).astype(int)

    for ipos,position in enumerate(pos_city):
        if day ==0: ## write header
            FW=open(OUTDIR+"/"+position+".csv","w")
            FW.write("# comment,"+"This data is extracted from surface {model} output.".format(model=model_type.upper())+"\n")
            FW.write("# position,"+position+"\n")
            FW.write("# lon,"+str(pos_lon[ipos])+"\n")
            FW.write("# lat,"+str(pos_lat[ipos])+"\n")
            FW.write("# col,"+str(model_col[ipos])+"\n")
            FW.write("# row,"+str(model_row[ipos])+"\n")
            FW.write("# MAPFAC_MX,"+str(MODEL_NC.variables["MAPFAC_MX"][0,model_row[ipos], model_col[ipos]])+"\n")
            FW.write("# MAPFAC_MY,"+str(MODEL_NC.variables["MAPFAC_MY"][0,model_row[ipos], model_col[ipos]])+"\n")
            FW.write("# COSALPHA,"+str(MODEL_NC.variables["COSALPHA"][0,model_row[ipos], model_col[ipos]])+"\n")
            FW.write("# SINALPHA,"+str(MODEL_NC.variables["SINALPHA"][0,model_row[ipos], model_col[ipos]])+"\n")
            FW.write("# variable,"+",".join(varlist)+"\n")
            FW.write("# description,"+",".join(DESCLIST)+"\n")
            FW.write("# unit,"+",".join(UNITLIST)+"\n")
            FW.write("Date,"+",".join(varlist)+"\n")
            FW.close()
        for hour in range(24):
            FW=open(OUTDIR+"/"+position+".csv","aw")
            line=[NOW.strftime("%Y%m%d")+"T"+str(hour).zfill(2)+"00Z"]
            for var in varlist:
                line.append(MODEL_NC.variables[var][hour,model_row[ipos],model_col[ipos]])
            FW.write(",".join(map(str,line))+"\n")
            FW.close()
FW.close()

