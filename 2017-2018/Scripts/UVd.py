import numpy as np
import matplotlib.pyplot as plt
from os import listdir
#<----------------Nombres de las estaciones y PATH donde esta------------------>
dir="../Stations/"
stations=listdir(dir)
#<------------------------Parametros de los datos------------------------------>
title,dates,color,phototype=["Winter","Summer"],["180202","180604"],["red","orange"],["Phototype III","Phototype IV"]
med=[300,450];t_i,t_f,t_lim=8,15,21
t=np.zeros([2,2,(t_f-t_i)*60,2])
#<-----------------------------Parametros de las graficas---------------------->
x=np.arange(8,15,1/60)
plt.xlabel("CST (UTC - 6h)",fontsize="large")
plt.ylabel("Exposure Time (min)",fontsize="large")
plt.ylim(0,175);plt.xlim(8,16)
#<-----------------------------Inicio del calculo------------------------------>
for n_med in range(2):
    print("Calculando "+phototype[n_med])
    for min in range((t_f-t_i)*60):
        for date in range(2):
            dosis=[]
            for j in range(np.size(stations)):
                car=dir+stations[j]+"/Mediciones/v0.0/"
                data=np.loadtxt(car+dates[date]+"Eryme.txt",skiprows=t_i*60+min,max_rows=(t_lim-t_i)*60-min)
                if data[:,1].mean()!=0:
                    tes,k=0,0
                    while tes<med[n_med] and k+min<(t_lim-t_i)*60:
                        tes+=data[k,1]*60
                        k+=1
                    dosis=np.append(dosis,k)
            #mean,sd=round(np.mean(dosis)),round(np.std(dosis,ddof=1),1)
            mean,sd=np.mean(dosis),np.std(dosis,ddof=1)
            t[n_med,date,min,0],t[n_med,date,min,1]=mean-sd,mean+sd
    #<--------------------------Grafica del maximo----------------------------->
    plt.fill_between(x,t[n_med,0,:,0],t[n_med,0,:,1],color=color[n_med])
    #<--------------------------Grafica del minimo----------------------------->
    plt.fill_between(x,t[n_med,1,:,0],t[n_med,1,:,1],color=color[n_med],label=phototype[n_med])
    print(np.min(t[n_med,1,:,0]),np.min(t[n_med,0,:,0]))
    #<------------------------Grafica del intermedio--------------------------->
    plt.fill_between(x,t[n_med,0,:,1],t[n_med,1,:,0],color=color[n_med],alpha=0.5)
plt.plot([15,15],[0,175],ls="--",color="black")
plt.legend(frameon=False,ncol=2,bbox_to_anchor=(0, 1,1,0.02),mode="expand")
plt.savefig("../Graficas/FillDosis2.png")
plt.show()
