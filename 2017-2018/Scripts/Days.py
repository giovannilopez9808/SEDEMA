import numpy as np
import matplotlib.pyplot as plt
from os import listdir
stacol=["Blue","Red","Green","black","purple","pink","pink","orange","green","cyan"]
dir="../Stations/"
stations=listdir(dir)
title=["Winter","Spring","Summer","Autumn"]
dates=["180202","180420","180604","171113"]
i=0
for date in dates:
    plt.ylabel("UV Index",fontsize="large")
    plt.xlabel("Local Time (h)",fontsize="large")
    plt.title(title[i],fontsize="large")
    plt.xticks(fontsize="large")
    plt.yticks(fontsize="large")
    plt.ylim(0,14)
    plt.xlim(6,19)
    for j in range(np.size(stations)):
        car=dir+stations[j]+"/Mediciones/v0.0/"
        data=np.loadtxt(car+date+"Eryme.txt")
        if data[:,1].mean()!=0:
            data[:,1]=data[:,1]*40
            plt.plot(data[:,0],data[:,1],label=stations[j],c=stacol[j],marker=".",ls="none",ms=3,alpha=0.7)
    plt.legend(frameon=False,ncol=5,mode="expand",loc="upper center",markerscale=4, scatterpoints=1)
    plt.savefig(date+".png")
    plt.clf()
    i+=1