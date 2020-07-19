import numpy as np
import matplotlib.pyplot as plt
import datetime
from os import listdir
car="../Stations/"
AOD="/AOD500DM/"
ver="v0.0/"
lon=["UVA","Ery"]
Meses=["January","February","March","April","May","June","July","August"
       ,"September","October","November","December"]
stations=listdir(car)
#ratiog=(month,hour,UVA/Erythemal)
ratiog=np.zeros([365,360,2,2])
DRg=np.zeros([365,360,2,2])
def prom(x,y,day,_k):
    if np.size(x)!=0:
        for _n in range(np.size(x[:,0])):
            if x[_n,1]!=0:
                y[day,_n,_k,0]+=x[_n,1]
                y[day,_n,_k,1]+=1
    return y[day,_n,_k,0],y[day,_n,_k,1]
def plotcontour(title,daysnum,Meses,x,hour,y):
    levels=np.arange(0.600,1.400,0.1)
    plt.title(title)
    plt.xticks(x,hour)
    plt.ylabel("Month")
    plt.xlabel("Local time (h)")
    plt.yticks(daysnum,Meses)
    plt.contourf(y[:,:,0],levels)
    plt.colorbar()
    plt.show()
    plt.clf()
for station in stations:
    print("Analizando la estacion "+station)
    carR=car+station+AOD+ver+"Ratio/"
    carDR=car+station+AOD+ver+"DR/"
    data=np.loadtxt(car+station+AOD+"datos500.txt",skiprows=1,usecols=0,dtype=str)
    for file in data:
        month=int(file[2:4])
        day=int(file[4:6])
        year=int(20+file[0:2])
        day=(datetime.date(year,month,day)-datetime.date(year,1,1)).days
        if day>364:
            day=day-1
        for _k in range(2):
            Ratios=np.loadtxt(carR+file+lon[_k]+"ratio.txt")
            DR=np.loadtxt(carDR+file+lon[_k]+"DR.txt")
            ratiog[day,_n,_k,0],ratiog[day,_n,_k,1]=prom(Ratios,ratiog,day,_k)
            DRg[day,_n,_k,0],DRg[day,_n,_k,1]=prom(DR,DRg,day,_k)
for _i in range(365):
    for _j in range(360):
        for _k in range(2):
            if ratiog[_i,_j,_k,1]!=0:
                ratiog[_i,_j,_k,0]=ratiog[_i,_j,_k,0]/ratiog[_i,_j,_k,1]
            if DRg[_i,_j,_k,1]!=0:
                DRg[_i,_j,_k,0]=DRg[_i,_j,_k,0]/DRg[_i,_j,_k,1]    
daysnum=np.arange(0,365,30.5)
hour=np.arange(10,17,1)
x=np.arange(0,400,60)
plotcontour("Mensual Ratios",daysnum,Meses,x,hour,ratiog)
plotcontour("Mensual RD",daysnum,Meses,x,hour,DRg)