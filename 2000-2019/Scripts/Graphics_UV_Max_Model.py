import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from os import listdir 
AODver="0.061"
lon=["UVA","Ery"]
Meses=["January","February","March","April","May","June","July","August"
            ,"September","October","November","December"]
title=["UVA irradiance","Erythemal irradiance"]
numyear=["2000","","","","2004","","","","2008","",""
,"","2012","","","","2016","","","2019"]
years=np.arange(0,20,1)
daysnum=np.arange(0,365,30.5)
hours=np.arange(0,24+2,2)
hoursnum=np.arange(0,1440,60*2)
delta=[5,0.035/2]
for i in range(np.size(lon)):
    daily=np.loadtxt("../Archivos/UVdaily"+lon[i]+".txt")
    daily=np.transpose(daily)
    plt.subplots_adjust(left=0.10,right=0.96,bottom=0.20,top=0.93)
    plt.ylabel("Local Time (h)")
    plt.title("Mexico City - TUV Model")
    plt.xticks(daysnum,Meses,rotation=60)
    plt.yticks(hoursnum,hours)
    plt.ylim(60*4,60*20)
    maxi=daily.max()
    levels=np.arange(0,maxi+delta[i],delta[i])
    plt.contourf(daily,levels=levels,cmap="inferno")
    plt.colorbar(label=title[i]+" (W/m$^2$)")
    plt.savefig("../Graficas/MaxMod"+lon[i]+".png",dpi=200)
    plt.clf()
colors=[(58/255,156/255,43/255),(152/255,196/255,8/255),
(1,244/255,0),(1,211/255,0),(246/255,174/255,0),(239/255,131/255,0),
(232/255,97/255,5/255),(230/255,42/255,20/255),(228/255,34/255,130/255),
(175/255,94/255,153/255),(118/255,116/255,180/255),
(102/255,47/255,149/255),(102/255,47/255,149/255),(102/255,47/255,149/255),
(102/255,47/255,149/255),(102/255,47/255,149/255),(102/255,47/255,149/255)]
n_bin=18
cmap_name="UV_Index"
cm=LinearSegmentedColormap.from_list(cmap_name,colors,N=n_bin)
daily=daily*40
plt.subplots_adjust(left=0.10,right=0.96,bottom=0.20,top=0.93)
plt.ylabel("Local Time (h)")
plt.title("Mexico City - TUV Model")
plt.xticks(daysnum,Meses,rotation=60)
plt.yticks(hoursnum,hours)
plt.ylim(60*4,60*20)
maxi=daily.max()
levels=np.arange(1,19,1)
plt.contourf(daily,levels=levels,cmap=cm)
cbar=plt.colorbar()
cbar.ax.set_ylabel("UV Index",rotation=-90,va="bottom")
plt.savefig("../Graficas/MaxModUVindex.png",dpi=200)
plt.clf()