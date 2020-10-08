import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
#<------------------------Funcion para hacer la grafica----------------------->
def graf(resul,levels,cm,title,name,label,daysnum,Meses):
    plt.subplots_adjust(left=0.097,right=0.977,bottom=0.205,top=0.890)
    plt.title(title)
    plt.ylabel("CST (UTC - 6h)")
    plt.xticks(daysnum,Meses,rotation=60)
    plt.ylim(6,18)
    plt.contourf(resul,levels=levels,cmap=cm)
    cbar=plt.colorbar(ticks=levels)
    cbar.ax.set_ylabel(label,rotation=-90,va="bottom")
    plt.savefig(name,dpi=200)
    plt.clf()
#<----------------------Carpetas dy titulos de las graficas------------------->
lon=["UVA","Ery"];carp=["UVA","Eritemica"];title=["UVA irradiance","Erythemal irradiance"]
Meses=["January","February","March","April","May","June","July","August"
            ,"September","October","November","December"]
#<---------------------Dias de los meses y delta de cada grafica-------------->
daysnum=np.arange(0,365,30.5);delta=[5,0.035/2]
#<-------------------------Graficas de UVA y Eritemica------------------------>
for i in range(np.size(lon)):
    print("Graficando "+carp[i])
    resul=np.loadtxt("../Archivos/MaxMe"+lon[i]+".txt");maxi=resul.max()
    title="Mexico City - Period: 2000-2019";levels=np.arange(0,maxi+delta[i],delta[i])
    name="../Graficas/Max"+lon[i]+".png";label=title[i]+" (W/m$^2$)";cm="inferno"
    graf(resul,levels,cm,title,name,label,daysnum,Meses)
#<-------------------------Definicion de los colres--------------------------->
colors=[(58/255,156/255,43/255),(152/255,196/255,8/255),
(1,244/255,0),(1,211/255,0),(246/255,174/255,0),(239/255,131/255,0),
(232/255,97/255,5/255),(255/255,34/255,34/255),
(230/255,42/255,20/255),(165/255,0/255,0/255),
(118/255,46/255,159/255),(150/255,53/255,188/255),
(184/255,150/255,235/255),(198/255,198/255,248/255)]
n_bin=15
cmap_name="UV_Index"
cm=LinearSegmentedColormap.from_list(cmap_name,colors,N=n_bin)
#<--------------------------Graficas de UV Index------------------------------>
resul=resul*40
min=1000
for i in range(np.size(resul[:,0])):
    for j in range(np.size(resul[0,:])):
        if min>round(resul[i,j])-1 and round(resul[i,j])-1>0:
            min=resul[i,j]
print(min)
print("Graficando UV Index")
title="UV Index measured in Mexico City \n Period 2000 - 2019"
label="UV Index";name="../Graficas/MaxUVindex.png"
levels=np.arange(1,16,1)
graf(resul,levels,cm,title,name,label,daysnum,Meses)