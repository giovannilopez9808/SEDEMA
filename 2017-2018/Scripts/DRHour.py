import numpy as np
import matplotlib.pyplot as plt
period=np.zeros([2,2])
period[0,0],period[0,1]=6,10
period[1,0],period[1,1]=4,5
sta=["CHO","CUT","MER","MON","MPA","PED","SFE","TLA"]
#1 Numero de estacion
#2 Numero de minutos
#3 Periodo
#4 UVA y Eritemica
horas=np.arange(1440)
hora=np.arange(0,1440,120)
hour=np.arange(0,24,2)
prom=np.zeros([1440,3,2])
nprom=np.zeros([3,2])
ylimi=[70,0.45]
lon=["UVA","Ery"]
title=["UVA","Erythemal"]
label=["june-october","november-march","april-may"]
for i in range(np.size(sta)):
    data=np.zeros([1440,3,2])
    num=np.zeros([3,2])
    files=np.loadtxt("../"+sta[i]+"/AOD500DM/datos500.txt",skiprows=1,usecols=0)
    print("Escribiendo la estacion "+sta[i])
    for j in range(np.size(files)):
        day=str(int(files[j]))
        month=int(day[2:4])
        for k in range(2):
            me=np.loadtxt("../"+sta[i]+"/Mediciones/v0.0/"+day+lon[k]+"me.txt",usecols=1) 
            if me.mean()!=0:
                if  month>=period[0,0] and month<=period[0,1]:
                    n=0
                else:
                    if month>=period[1,0] and month<=period[1,1]:
                        n=2
                    else:
                        n=1
                num[n,k]=num[n,k]+1
                nprom[n,k]=nprom[n,k]+1
                for m in range(1440):
                    data[m,n,k]=data[m,n,k]+me[m]
                    prom[m,n,k]=prom[m,n,k]+me[m]
    ndays=0
    for k in range(2):
        for n in range(3):
            if num[n,k]!=0:
                ndays=ndays+num[n,k]
                for m in range(1440):
                    data[m,n,k]=data[m,n,k]/num[n,k]
                if data[:,n,k].mean()!=0:
                    plt.scatter(horas,data[:,n,k],label=label[n])
        plt.legend(frameon=False,ncol=3)
        plt.ylim(0,ylimi[k])
        plt.ylabel(title[k]+" Irradiance (W/m$^2$)")
        plt.xticks(hora,hour)
        plt.xlim(6*60,19*60)
        plt.xlabel("Local time (h)")
        plt.title("Station "+sta[i]+" Days counted:"+str(int(ndays)))
        plt.savefig("../SeasonGraphic/"+sta[i]+lon[k]+".png")
        plt.clf()
ndays=0
for k in range(2):
    for n in range(3):
        if num[n,k]!=0:
            ndays=ndays+num[n,k]
            for m in range(1440):
                prom[m,n,k]=prom[m,n,k]/nprom[n,k]
            if data[:,n,k].mean()!=0:
                plt.scatter(horas,data[:,n,k],label=label[n])
    plt.legend(frameon=False,ncol=3)
    plt.ylim(0,ylimi[k])
    plt.ylabel(title[k]+" Irradiance (W/m$^2$)")
    plt.xticks(hora,hour)
    plt.xlim(6*60,19*60)
    plt.xlabel("Local time (h)")
    plt.title("Days counted:"+str(int(ndays)))
    plt.savefig("../SeasonGraphic/Year"+lon[k]+".png")
    plt.clf()