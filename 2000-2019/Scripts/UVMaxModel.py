import numpy as np
import matplotlib.pyplot as plt
from os import listdir 
import datetime
carp=["UVA","Eritemica"]
AODver="0.16"
lon=["UVA","Ery"]
for i in range(np.size(carp)):
    print("Analizando "+carp[i])
    daily=np.zeros([1440,365])
    dir="../"+carp[i]+"/"+AODver+"/"
    files=listdir(dir)
    for file in files:
        year=2000+int(file[0:2])
        day=int(file[4:6])
        month=int(file[2:4])
        date=file[2:6]
        date=(datetime.date(year,month,day)-datetime.date(year,1,1)).days
        if date>364:
            date=364
        data=np.loadtxt(dir+file,usecols=1)
        for hour in range(np.size(data)):
            if data[hour]>0:
                if daily[hour,date]<data[hour]:
                    daily[hour,date]=data[hour]
    arc=open("../Archivos/UVdaily"+lon[i]+".txt","w")
    for j in range(365):
        for k in range(1440):
            arc.write(str(daily[k,j])+" ")
        arc.write("\n")
    arc.close()