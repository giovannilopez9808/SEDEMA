import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from scipy.stats import sem 
from scipy.interpolate import interp1d
dir="../Stations/"
name=""
UV_ini=1
UV_fin=14
MED=[200,250,300,450,600,1000]
SED=["2.0","2.5","3.0","4.5","6.0","10.0"]
d_UV=UV_fin-UV_ini
stations=listdir(dir)
n_MED=np.size(MED)
time=np.zeros([d_UV,n_MED,2])
time_std=np.zeros([d_UV,n_MED])
skin_type=["I","II","III","IV","V","VI"]
UV=UV_ini
n_days=0
print("Contando los dias totales")
for station in stations:
    if station!=name:
        car=dir+station+"/datos.txt"
        dates=np.loadtxt(car,usecols=0,skiprows=1)
        n_days+=np.size(dates)
UV_std=np.zeros([n_days,d_UV,n_MED])
n_count=0
for station in stations:
    if station!=name:
        print("Analizando estacion "+station)
        carmod=dir+station+"/datos.txt"
        car=dir+station+"/Mediciones/v0.0/"
        dates=np.loadtxt(carmod,usecols=0,skiprows=1,dtype=str)
        for date in dates:
            data=np.loadtxt(car+date+"Eryme.txt")
            max_data=np.size(data[:,0])
            UVdata=data[:,1]*40
            for UV in range(d_UV):
                pos=np.where(UVdata>=UV+1)[0]
                if np.size(pos)!=0:
                    TEM=0
                    n=pos[0]
                    time_ini=data[n,0]
                    for type in range(n_MED):
                        yes=0
                        while yes!=1 and n<max_data:
                            TEM+=data[n,1]*60
                            if TEM>=MED[type]:
                                yes=1
                                dif=(data[n-1,0]-time_ini)*60
                                time[UV,type,0]+=dif
                                time[UV,type,1]+=1
                                UV_std[n_count,UV,type]=dif
                                n+=1
                            else: n+=1
            n_count+=1
print("Realizando las desviaciones estandar y normalizando los tiempos")
for UV in range(d_UV):
    for type in range(n_MED):
        time_std[UV,type]=np.std(UV_std[:,UV,type])
        if time[UV,type,1]!=0:
            time[UV,type,0]=time[UV,type,0]/time[UV,type,1]
print("Realizando graficas")
poly_n=3
x=np.arange(1,14)
x2=np.arange(UV_ini,UV_fin+1)
n=np.size(x)
for type in range(n_MED):
    y=time[:,type,0]
    fit=np.polyfit(x,y,poly_n)
    fit=np.poly1d(fit)
    pd=fit(x)
    #sd_pd=time_std[:,0]*1.96/np.sqrt(np.size(time_std[:,0]))
    sd_cf=1.96*time_std[:,0]
    plt.subplots_adjust(left=0.1,right=0.95,bottom=0.125,top= 0.95)
    plt.ylabel("Solar Exposure Time (minutes)")
    plt.title("Skin Phototype "+skin_type[type])
    plt.xticks(x)
    plt.xlim(UV_ini,UV_fin-1)
    plt.xlabel("UV Index")
    plt.ylim(0,200)
    #plt.errorbar(x[0],y[0],yerr=time_std[0,type],marker="o",linewidth=1
    #,ls="none",alpha=0.6,color="b",capsize=5,markersize=2,label="Monthly average")
    #for i in range(1,d_UV):
        #plt.errorbar(x[i],y[i],yerr=time_std[i,type],marker="o",linewidth=1
        #,ls="none",alpha=0.6,color="b",capsize=5,markersize=2)
    plt.plot(x,pd,label=" Solar Exposure Time to accumulate 1 MED ("+SED[type]+" SED)",color="aquamarine")
    plt.fill_between(x,y+time_std[:,type],y-time_std[:,type],color="green",label="Standar Desviation",alpha=0.5)
    #plt.fill_between(x,pd+sd_pd,pd-sd_pd,label="Prediction Bands",color="red")
    #plt.plot(x,pd-sd_pd,color="red")
    #plt.fill_between(x,pd+sd_cf,pd-sd_cf,label="Confidence Bands",color="green",alpha=0.5)
    #plt.plot(x,pd-sd_cf,color="green")
    plt.legend(ncol=2,frameon=False,loc=9,fontsize="small")
    plt.savefig("../Graficas/TEM"+skin_type[type]+".png")
    plt.clf()