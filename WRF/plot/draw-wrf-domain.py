#!/bin/env python2.7
# -*- coding: utf-8 -*-

#import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from matplotlib.patches import Polygon

def draw_screen_poly( lats, lons, m):
    x, y =  lons, lats 
    xy = zip(x,y)
    poly = Polygon( xy, edgecolor="b",fc="none", lw=2, alpha=1)
    plt.gca().add_patch(poly)

# clear previous figure 
plt.clf()

## setting namelist.wps domain information

d_malaysia = [80000.0, 80000.0]
d_ID = [16000.0, 16000.0]
d_yanagi = [80000.0, 80000.0]

dx = 36000
dy = 36000
max_dom = 1

parent_malaysia = [1.0,3.0,5.0,5.0]
parent_ID = [1.0,5.0,5.0,5.0]
parent_yanagi = [1.0,5.0,5.0,5.0]
parent_grid_ratio = parent_yanagi

ij_malaysia=[[1,35, 35, 29],[1,16,25,27]]
ij_ID=[[1,75,44],[1,41,35]]
ij_yanagi=[[1,75,44],[1,41,35]]

i_start = ij_yanagi[0]
j_start = ij_yanagi[1]

we_sn_malaysia = [[120, 61, 61,61],[105,61,61,61]]
we_sn_ID = [[120,91,126],[105,91,106]]
we_sn_yanagi = [[120,91,126],[105,91,106]]

e_we = [147,0]
e_sn = [111,0]

ref_malaysia = [21.0,112.0]
ref_ID = [2.0, 100.0]
ref_yanagi = [21.0, 112.0]

ref_lat=  40
ref_lon= -97

true_malaysia = [10.0, 30.0]
true_ID = [0.0, 20.0]
true_yanagi = [10.0, 30.0]

true_lat1 = 33
true_lat2 = 45

## draw map
m = Basemap(resolution="i", projection="lcc", rsphere=(6370000.0, 6370000.0), 
lat_1=true_lat1, lat_2=true_lat2, lat_0=ref_lat, lon_0=ref_lon, 
width=dx*(e_we[0]-1), height=dy*(e_sn[0]-1))

m.drawcoastlines()
#m.drawcountries(linewidth=2)
m.drawcountries()

#m.fillcontinents()
m.fillcontinents(color="green")
m.drawmapboundary()
#m.fillcontinents(lake_color="aqua")
#m.drawmapboundary(fill_color="aqua")

m.drawparallels(range(-90, 90, 10), labels = [1,0,0,0], fontsize=16,dashes=[1,1])
m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=16,dashes=[1,1])


## plot center position
cenlon=range(max_dom); cenlat=range(max_dom)
cenlon_model=dx*(e_we[0]-1)/2.0
cenlat_model=dy*(e_sn[0]-1)/2.0

cenlon[0], cenlat[0]=m(cenlon_model, cenlat_model, inverse=True)

#plt.plot(cenlon,cenlat,marker="o",ms=15)
#print cenlon, cenlat

#### draw nested domain rectangle
lon=range(4); lat=range(4)

if max_dom >= 2:
    ### domain 2
    # 4 corners
    ll_lon = dx*(i_start[1]-1)
    ll_lat = dy*(j_start[1]-1)
    ur_lon = ll_lon + dx/parent_grid_ratio[1] * (e_we[1]-1)
    ur_lat = ll_lat + dy/parent_grid_ratio[1] * (e_sn[1]-1)
    
    ## lower left (ll)
    lon[0],lat[0] = ll_lon, ll_lat
    ## lower right (lr)
    lon[1],lat[1] = ur_lon, ll_lat
    ## upper right (ur)
    lon[2],lat[2] = ur_lon, ur_lat
    ## upper left (ul)
    lon[3],lat[3] = ll_lon, ur_lat
    
    draw_screen_poly(lat, lon ,m)

    cenlon_model = ll_lon + (ur_lon-ll_lon)/2.0
    cenlat_model = ll_lat + (ur_lat-ll_lat)/2.0
#    plt.plot(cenlon,cenlat,marker="o",ms=15)
    #print m(cenlon, cenlat)cenlon, cenlat, ll_lon, ll_lat, ur_lon, ur_lat
    #print m(cenlon, cenlat,inverse=True)
    cenlon[1], cenlat[1]=m(cenlon_model, cenlat_model, inverse=True)


if max_dom >= 3:
    ### domain 3
    ## 4 corners
    ll_lon += dx/parent_grid_ratio[1]*(i_start[2]-1)
    ll_lat += dy/parent_grid_ratio[1]*(j_start[2]-1)
    ur_lon = ll_lon +dx/parent_grid_ratio[1]/parent_grid_ratio[2]*(e_we[2]-1)
    ur_lat =ll_lat+ dy/parent_grid_ratio[1]/parent_grid_ratio[2]*(e_sn[2]-1)
    
    ## ll
    lon[0],lat[0] = ll_lon, ll_lat
    ## lr
    lon[1],lat[1] = ur_lon, ll_lat
    ## ur
    lon[2],lat[2] = ur_lon, ur_lat
    ## ul
    lon[3],lat[3] = ll_lon, ur_lat
    
    draw_screen_poly(lat, lon ,m)
    #plt.plot(lon,lat,linestyle="",marker="o",ms=10)

    cenlon_model = ll_lon + (ur_lon-ll_lon)/2.0
    cenlat_model = ll_lat + (ur_lat-ll_lat)/2.0
#    plt.plot(cenlon,cenlat,marker="o",ms=15)
    #print m(cenlon, cenlat)cenlon, cenlat, ll_lon, ll_lat, ur_lon, ur_lat
    #print m(cenlon, cenlat,inverse=True)
    cenlon[2], cenlat[2]=m(cenlon_model, cenlat_model, inverse=True)


if max_dom >= 4:
    ### domain 3
    ## 4 corners
    ll_lon += dx/parent_grid_ratio[1]/parent_grid_ratio[2]*(i_start[3]-1)
    ll_lat += dy/parent_grid_ratio[1]/parent_grid_ratio[2]*(j_start[3]-1)
    ur_lon = ll_lon +dx/parent_grid_ratio[1]/parent_grid_ratio[2]/parent_grid_ratio[3]*(e_we[3]-1)
    ur_lat =ll_lat+ dy/parent_grid_ratio[1]/parent_grid_ratio[2]/parent_grid_ratio[3]*(e_sn[3]-1)
    
    ## ll
    lon[0],lat[0] = ll_lon, ll_lat
    ## lr
    lon[1],lat[1] = ur_lon, ll_lat
    ## ur
    lon[2],lat[2] = ur_lon, ur_lat
    ## ul
    lon[3],lat[3] = ll_lon, ur_lat
    
    draw_screen_poly(lat, lon ,m)
    #plt.plot(lon,lat,linestyle="",marker="o",ms=10)

    cenlon_model = ll_lon + (ur_lon-ll_lon)/2.0
    cenlat_model = ll_lat + (ur_lat-ll_lat)/2.0
#    plt.plot(cenlon,cenlat,marker="o",ms=15)
    #print m(cenlon, cenlat)cenlon, cenlat, ll_lon, ll_lat, ur_lon, ur_lat
    #print m(cenlon, cenlat,inverse=True)
    cenlon[3], cenlat[3]=m(cenlon_model, cenlat_model, inverse=True)

## save domain by pdf and png
plt.savefig("domain-test.pdf", bbox_inches="tight",edgecolor="none")
plt.savefig("domain-test.png", bbox_inches="tight", edgecolor="none")
plt.show()

# print each domain center lon lat
for i in range(max_dom):
    print cenlon[i], cenlat[i]

