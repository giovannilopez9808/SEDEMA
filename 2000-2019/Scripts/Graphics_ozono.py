#<----------------Programa que grafica el archivos datosozono.txt en una grafica------------->
import numpy as np
import matplotlib.pyplot as plt
import datetime
print("Leyendo datos de Ozono")
#<----------------Lectura de los archivos------------------>
date=np.loadtxt("../Archivos/datosozono.txt",skiprows=1,usecols=0,dtype=str)
o3=np.loadtxt("../Archivos/datosozono.txt",skiprows=1,usecols=1)
#<-------------Datos para las graficas y calculos--------------->
data,prom=np.zeros([20,365]),np.zeros([20,12,2])
Meses=["January","February","March","April","May","June","July","August"
       ,"September","October","November","December"]
numyear=["2000","","","","2004","","","","2008","",""
,"","2012","","","","2016","","","2019"]
#<------------Ciclo que varia los dias------------------>
for i in range(np.size(date)):
    #<-----------Recopilacion de los dias,mes y año------->
    day,month,year=int(date[i][4:6]),int(date[i][2:4]),int("20"+date[i][0:2])
    #<------------Calculo de los dias consecutivos----------->
    day=(datetime.date(year,month,day)-datetime.date(year,1,1)).days
    if day>=365:
        day=364
    month,year=month-1,year-2000
    data[year,day]=o3[i]
    prom[year,month,0]+=o3[i]
    prom[year,month,1]+=1
mean=o3.mean()
#<--------Ciclo de los años----------->
for year in range(20):
    #<-----------Ciclo de los dias------->
    for day in range(365):
        if data[year,day]==0:
            data[year,day]=mean
    #<------------Ciclo de los meses---------->
    for month in range(12):
        prom[year,month,0]=prom[year,month,0]/prom[year,month,1]
#<------Informacion para las graficas------------->
daysnum,year=np.arange(0,365,30.5),np.arange(0,20,1)
#numyear=year+2000
maxi=data.max()
mini=data.min()
#<-------Mapa de colores---------->
mapcolor="viridis"
plt.subplots_adjust(left=0.11,right=0.97,bottom=0.20,top=0.94)
plt.title("Period 2000-2019",fontsize="large")
numyear=["","2001","","","2004","","","","2008","","","","2012","","","","2016","","","2019"]
plt.yticks(year,numyear,fontsize="large")
plt.grid(linewidth=1,color="black",linestyle="--")
plt.xticks(daysnum,Meses,rotation=60,fontsize="large")
levels=np.arange(mini,maxi+20,20)
plt.contourf(data,cmap=mapcolor,levels=levels)
cbar=plt.colorbar()
cbar.ax.set_ylabel("Total Ozone Column (DU)",rotation=-90,va="bottom",fontsize="large")
#<---------Guardado de la grafica---------->
plt.savefig("../Graficas/OzonoDaily.png",dpi=200)
plt.clf()
#<-------Informacion para las graficas--------->
daysnum=np.arange(0,13,1)
plt.subplots_adjust(left=0.11,right=0.97,bottom=0.20,top=0.94)
plt.title("Annual Monthly Average - Period: 2000-2019",fontsize="large")
plt.yticks(year,numyear,fontsize="large")
plt.grid(linewidth=1,color="black",linestyle="--")
plt.xticks(daysnum,Meses,rotation=60,fontsize="large")
levels=np.arange(mini,maxi+20,20)
plt.contourf(prom[:,:,0],cmap=mapcolor,levels=levels)
cbar=plt.colorbar()
cbar.ax.set_ylabel("Total Ozone Column (DU)",rotation=-90,va="bottom",fontsize="large")
#<---------Guardado de las graficas---------->
plt.savefig("../Graficas/OzonoMonthly.png",dpi=200)
plt.clf()