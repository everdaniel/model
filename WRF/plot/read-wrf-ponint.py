#!/usr/bin/env python2.7
# coding: utf-8
# @author: SENOO, Ken
# (Last Update: 2014-05-21T10:08+09:00)

import netCDF4
from mpl_toolkits.basemap import Basemap
import numpy as np
import os

INDIR="/home/senooken/model/WRF/WRF-3.6-single/WRFV3/run/"
INFILE="observation-position.csv"
FR=INDIR+INFILE
OUTDIR="./point/"

if not os.path.exists(OUTDIR): os.makedirs(OUTDIR)

MODEL_NC=netCDF4.Dataset(FR)

## get projection information
XCENT=MODEL_NC.CEN_LON
YCENT=MODEL_NC.getncattr("CEN_LAT")

DX=MODEL_NC.DX
DY=MODEL_NC.DY

P_ALP=MODEL_NC.TRUELAT1
P_BET=MODEL_NC.TRUELAT2

NCOLS=MODEL_NC.getncattr("WEST-EAST_PATCH_END_UNSTAG")
NROWS=MODEL_NC.getncattr("SOUTH-NORTH_PATCH_END_UNSTAG")

## basemap
BM=Basemap(resolution="c", projection="lcc", lat_1=P_ALP, lat_2=P_BET, width=DX*(NCOLS-1), height=DY*(NROWS-1), lat_0=YCENT, lon_0=XCENT, rsphere=(6370000.0, 6370000.0))

#BM.drawcoastlines()
#BM.fillcontinents()
#BM.drawparallels(range(-90,90,10),labels=[1,0,0,0])
#BM.drawmeridians(range(-180,180,10),labels=[0,0,01])

## XLAT, XLONG

MODEL_NC.variables["XLAT"][0]
MODEL_NC.variables["XLONG"][0]

#BM(MODEL_NC.variables["XLAT"][0], MODEL_NC.variables["XLONG"][0])

# Y0=MODEL_NC.variables["XLAT"][0,0,0]
# X0=MODEL_NC.variables["XLONG"][0,0,0]
# 
# XORIG,YORIG=BM(X0,Y0)
# PROJ_X=[XORIG+DX*j for j in range(NCOLS)]
# PROJ_Y=[YORIG+DY*i for i in range(NROWS)]
# MESH_PROJ_X,MESH_PROJ_Y=np.meshgrid(PROJ_X,PROJ_Y)

MESH_PROJ_X,MESH_PROJ_Y=BM(MODEL_NC.variables["XLONG"][0],MODEL_NC.variables["XLAT"][0])
## plt.plot(PROJ_X,PROJ_Y,"o") # test
#plt.pcolormesh(MESH_PROJ_X,MESH_PROJ_Y,MODEL_NC.variables["T2"][0])
#plt.colorbar(fraction=0.1,pad=0.01)

#plt.savefig(OUTDIR+"T2.png",bbox_inches="tight")

POS_FILE=+"./observation-position.csv"
pos_array=np.genfromtxt(POS_FILE,delimiter=",",names=True,dtype=None)

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
base_lon,base_lat=m(pos_lon,pos_lat)

## plot observation
for i,city in enumerate(range(len(pos_array))):
    plt.plot(base_lon[i],base_lat[i],c=plt.cm.rainbow(i*290/len(pos_array)),marker=markers[i],label=pos_city[i],alpha=1,ms=8)

plt.legend(loc="lower left")
obstitle="Position of Observation"
#plt.title(obstitle,size=18)

if not os.path.exists(OUTDIR): os.makedirs(OUTDIR) 
plt.savefig(OUTDIR+"/met_pos.png",bbox_inches="tight")

## convert projected x, y to model col, row.
model_col=np.vectorize(round)(base_lon/DX -1.0).astype(int)
model_row=np.vectorize(round)(base_lat/DY -1.0).astype(int)

for day in range(days):
    stime=stime0+datetime.timedelta(days=day)
    print("open",stime,model_type)
#    fr=mydata+"/CCTM_parallel_cb05tucl_ae5_aq_CONC.EA.1201-1303_{y}{m:02}{d:02}_D1.nc".format(y=stime.year,m=stime.month,d=stime.day) 
    #MODEL_FILE=mydata+"/CCTM_parallel_saprc99_ae5_aq_CONC.{APPL}_{y}{m:02}{d:02}_D1.nc".format(y=stime.year,m=stime.month,d=stime.day,APPL=APPL) 
    MODEL_FILE=mydata+"/wrfout_d01_{y}{m:02}-{d:02}_00:00:00".format(y=stime.year,m=stime.month,d=stime.day,APPL=APPL) 
    #model_nc=netcdf.netcdf_file(MODEL_FILE,"r")
    model_nc=netCDF4.Dataset(MODEL_FILE)

    if day == 0: ## extract variable list and variable unit
        varlist=model_nc.getncattr("VAR-LIST").split()
        varlist.sort()
        UNITLIST=[model_nc.variables[var].units.strip() for var in varlist]
#        varlist.extend("PM0.1 PM2.5 PM10".split())
#        UNITLIST=[word.replace("micrograms","ug") for word in UNITLIST]
#        UNITLIST=[word.replace("**","") for word in UNITLIST]
#        UNITLIST=UNITLIST+["ug/m3"]*3


    for ipos,position in enumerate(pos_city):
        if day ==0: ## write header
            FW=open(OUTDIR+"/"+position+".csv","w")
            FW.write("# description,"+"This data is extracted surface {model} output.".format(model=model_type.upper())+"\n")
            FW.write("# position,"+position+"\n")
            FW.write("# lon,"+str(pos_lon[ipos])+"\n")
            FW.write("# lat,"+str(pos_lat[ipos])+"\n")
            FW.write("# col,"+str(model_col[ipos])+"\n")
            FW.write("# row,"+str(model_row[ipos])+"\n")
            FW.write("# unit,"+",".join(UNITLIST)+"\n")
            FW.write("Date,"+",".join(varlist)+"\n")
            FW.close()
        for hour in range(24):
            FW=open(OUTDIR+"/"+position+".csv","aw")
            line=[stime.strftime("%Y%m%d")+"T"+str(hour).zfill(2)+"00Z"]
            for var in varlist:
                line.append(model_nc.variables[var][hour,0,model_row[ipos],model_col[ipos]])
            FW.write(",".join(map(str,line))+"\n")
            FW.close()
FW.close()

