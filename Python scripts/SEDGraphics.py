import numpy as np
import matplotlib.pyplot as plt
from os import listdir
import datetime
#<-----------------Carpetas donde se localizan lo datos------------------->
carp=["../2016","../2017-2018"]
#<---------------------Paramatros para variar------------------->
hour_i,hour_f=12,15
max,month_max,data_f=np.zeros(365),np.zeros([12,2]),np.zeros([12,5])
# graf-> median,mean,percentil 25,percentil 75,SD
for i in range(2):
    print("Analizando "+carp[i])
    if i==0:
        car=carp[i]
        stations=["/"]
    else:
        car=carp[i]+"/Stations/"
        stations=listdir(car)
    for station in stations:
        dir=car+station
        dates=np.loadtxt(dir+"/AOD500DM/datos500.txt",skiprows=1,usecols=0,dtype=str)
        dir+="/Mediciones/v0.0/"
        for date in dates:
            arc=dir+date+"Eryme.txt"
            year,month,day=int(date[0:2]),int(date[2:4]),int(date[4:6])
            days=(datetime.date(year,month,day)-datetime.date(year,1,1)).days
            if days>364:
                days=364
            month+=-1
            data=np.loadtxt(arc,skiprows=hour_i*60,usecols=1,max_rows=60*(hour_f-hour_i))
            data=data.max()
            if data!=0:
                month_max[month,0]+=data
                month_max[month,1]+=1
                if max[days]<data:
                    max[days]=data
for month in range(12):
    if month_max[month,1]!=0:
        month_max[month,0]=month_max[month,0]/month_max[month,1]*40
file=open("year.txt","w")
for month in range(12):
    file.write("a\n")
    data=[]
    for day in range(365):
        n_month=(datetime.timedelta(days=day)+datetime.date(year,1,1)).month-1
        if n_month==month:
            if max[day]!=0:
                data=np.append(data,max[day])
                file.write(str(max[day])+"\n")
    data_f[month,0]=round(np.median(data)*40,3)
    data_f[month,1]=round(np.mean(data)*40,3)
    data_f[month,2]=round(np.percentile(data,25)*40,3)
    data_f[month,3]=round(np.percentile(data,75)*40,3)
    data_f[month,4]=round(np.std(data,ddof=0)*40,3)
n_month=np.arange(12)
file.close()
Meses=["January","February","March","April","May","June","July","August"
       ,"September","October","November","December"]
fig,ax1=plt.subplots()
plt.subplots_adjust(left=0.11,right=0.88,bottom=0.20,top=0.95)
plt.xticks(np.arange(12),Meses,rotation=60)
ax2=ax1.twinx()
ax1.set_ylabel("Erythemal irradiance (W/m$^2$)")
ax1.set_ylim(0,15)
ax2.set_ylim(0,15*0.9)
ax2.set_ylabel("SED/hr")
ax1.scatter(n_month,data_f[:,0],label="Median")
ax1.plot(n_month,data_f[:,1],label="Mean")
ax1.grid()
for month in n_month:
    ax1.plot([month,month],[data_f[month,2],data_f[month,3]],color="black")
ax1.fill_between(n_month,data_f[:,0]-data_f[:,4],data_f[:,0]+data_f[:,4],label="SD",color="orange",alpha=0.5)
ax1.legend(frameon=False,ncol=3,loc=3)
plt.show()
arc=open("data.txt","w")
for i in range(12):
    for j in range(5):
        arc.write(str(data_f[i,j])+" ")
    arc.write("\n")
arc.close()