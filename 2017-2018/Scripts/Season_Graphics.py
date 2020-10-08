import numpy as np
import matplotlib.pyplot as plt
import os
colors=["Blue","Red","Green","black","purple","pink","brown","orange","Green","cyan"]
dates=["180420","180604","171113","180202"]
titles=["Spring","Summer","Autumn","Winter"]
dir="../Stations/"
stations=os.listdir(dir)
stations=np.sort(stations)
fig,axs=plt.subplots(2,2,figsize=(10,9))
axs=np.reshape(axs,4)
for date,title,ax in zip(dates,titles,axs):
    ax.set_ylabel("UV Index")
    ax.set_xlabel("CST (UTC - 6h)")
    ax.set_title(title)
    ax.set_ylim(0,14)
    ax.set_xlim(6,19)
    for station,color in zip(stations,colors):
        car=dir+station+"/Mediciones/v0.0/"
        hour,data=np.loadtxt(car+date+"Eryme.txt",unpack=True)
        if(np.mean(data)!=0):
            data=data*40
            ax.plot(hour,data,label=station,c=color,marker=".",ls="none",ms=3,alpha=0.7)  
    ax.legend(ncol=5,mode="expand",loc="upper center",markerscale=3, scatterpoints=1,frameon=False)
plt.subplots_adjust(left=0.079,bottom=0.09,right=0.955,top=0.921,wspace=0.183,hspace=0.348)
plt.savefig("../SeasonGraphic/season.png")