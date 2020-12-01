import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import datetime
Meses=["January","February","March","April","May","June","July","August"
            ,"September","October","November","December"]
numyear=["2005","","","2008","",""
,"","2012","","","","2016","","","2019"]
daysnum,resul,prom=np.arange(0,365,30.5),np.zeros([15,365]),np.zeros([12,2])
date,data=np.loadtxt("../Archivos/UVI-OMI.txt",usecols=0,dtype=str),np.loadtxt("../Archivos/UVI-OMI.txt",usecols=1)
n=np.size(data)
print("Calculando valores y promedios")
for i in range(n):
    year,month,day=int("20"+date[i][0:2]),int(date[i][2:4]),int(date[i][4:6])
    day=(datetime.date(year,month,day)-datetime.date(year,1,1)).days
    if day>364: day=364
    year+=-2005
    num=data[i]
    if num!=0:
        month+=-1
        prom[month,0]+=num;prom[month,1]+=1
for month in range(12):
    prom[month,0]=prom[month,0]/prom[month,1]
for i in range(n):
    year,month,day=int("20"+date[i][0:2]),int(date[i][2:4]),int(date[i][4:6])
    day=(datetime.date(year,month,day)-datetime.date(year,1,1)).days
    month+=-1
    year+=-2005
    if day>364: day=364
    if data[i]==0: data[i]=prom[month,0]
    resul[year,day]=data[i]
for year in range(15):
    for day in range(365):
        if resul[year,day]==0:
            n_year=2005+year
            month=(datetime.date(year,1,1)+datetime.timedelta(days=day)).month
            resul[year,day]=prom[month,0]
colors=[(58/255,156/255,43/255),(152/255,196/255,8/255),
(1,244/255,0),(1,211/255,0),(246/255,174/255,0),(239/255,131/255,0),
(232/255,97/255,5/255),(255/255,34/255,34/255),
(230/255,42/255,20/255),(165/255,0/255,0/255),
(118/255,46/255,159/255),(150/255,53/255,188/255),
(184/255,150/255,235/255),(198/255,198/255,248/255)]
n_bin=15
font_size=12
cmap_name="UV_Index"
cm=LinearSegmentedColormap.from_list(cmap_name,colors,N=n_bin)
print("Graficando UV Index")
plt.subplots_adjust(left=0.094,right=0.977,bottom=0.205,top=0.89)
plt.title("UV Index satellite-derived in Mexico City \n Period 2005-2019")
plt.yticks(np.arange(np.size(numyear)),numyear,fontsize=font_size)
plt.xticks(daysnum,Meses,rotation=60,fontsize=font_size)
levels=np.arange(1,16,1)
plt.contourf(resul,levels=levels,cmap=cm)
plt.grid(linewidth=1,color="black",linestyle="--")
cbar=plt.colorbar(ticks=np.arange(1,16,1))
cbar.ax.set_ylabel("UV Index",rotation=-90,va="bottom",fontsize=11)
plt.savefig("../Graficas/UVI-OMI.png",dpi=300)