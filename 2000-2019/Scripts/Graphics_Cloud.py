#<----------------Programa que realiza la graficas CloudDaily y CloudMonthly---------->
import numpy as np
import matplotlib.pyplot as plt
import datetime
print("Leyendo datos de Cloud Factor")
#<----------------Lectura de los archivos--------------------->
dates=np.loadtxt("../Archivos/DatosCloud.txt",skiprows=1,usecols=0,dtype=str)
cloud=np.loadtxt("../Archivos/DatosCloud.txt",skiprows=1,usecols=1)
data=np.zeros([16,365])
prom=np.zeros([16,12,2])
#<----------------Ciclo para varias los dias------------------>
i=0
for date in dates:
    #<---------------Calculo de los dias----------->
    day,month,year=int(date[4:6]),int(date[2:4]),int("20"+date[0:2])
    #<----------------Dias consecutivos---------->
    day=(datetime.date(year,month,day)-datetime.date(year,1,1)).days
    day,month,year=day-1,month-1,year-2004
    data[year,day]=cloud[i]
    prom[year,month,0]+=cloud[i]
    prom[year,month,1]+=1
    i+=1
mean=cloud.mean()
#<---------------Ciclo para variar los años--------------->
for year in range(16):
    #<----------------Ciclo para variar los meses----------->
    for month in range(12):
        if prom[year,month,1]!=0:
            prom[year,month,0]=prom[year,month,0]/prom[year,month,1]
maxi,mini=data.max(),data.min()
#<------------------------Constantes para las graficas----------------->
Meses=["January","February","March","April","May","June","July","August"
       ,"September","October","November","December"]
numyear=["2004","","","","2008","",""
,"","2012","","","","2016","","","2019"]
daysnum=np.arange(0,365,30.5)
year=np.arange(16)
#<------------Mapa de color------------>
mapcolor="coolwarm"
plt.subplots_adjust(left=0.11,right=0.97,bottom=0.20,top=0.94)
plt.title("Period 2004-2019",fontsize="large")
plt.yticks(year,numyear,fontsize="large")
plt.grid(linewidth=1,color="black",linestyle="--")
plt.xticks(daysnum,Meses,rotation=60,fontsize="large")
levels=np.arange(mini,maxi+0.2,0.2)
plt.contourf(data,cmap=mapcolor,levels=levels)
cbar=plt.colorbar()
cbar.ax.set_ylabel("Cloud Factor",rotation=-90,va="bottom",fontsize="large")
#<-----------Guardar la grafica---------->
plt.savefig("../Graficas/CloudDaily.png",dpi=200)
plt.clf()
daysnum=np.arange(0,13,1)
plt.subplots_adjust(left=0.11,right=0.97,bottom=0.20,top=0.94)
plt.title("Annual Monthly Average - Period: 2004-2019",fontsize="large")
plt.yticks(year,numyear,fontsize="large")
plt.grid(linewidth=1,color="black",linestyle="--")
plt.xticks(daysnum,Meses,rotation=60,fontsize="large")
levels=np.arange(mini,maxi+0.2,0.2)
plt.contourf(prom[:,:,0],cmap=mapcolor,levels=levels)
cbar=plt.colorbar()
cbar.ax.set_ylabel("Cloud Factor",rotation=-90,va="bottom",fontsize="large")
#<---------Guardar la grafica----------->
plt.savefig("../Graficas/CloudMonthly.png",dpi=200)
plt.clf()