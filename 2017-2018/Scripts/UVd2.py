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
fig,ax1=plt.subplots()
plt.xlabel("Local Time (h)",fontsize="large")
ax2=ax1.twinx()
ax1.set_ylabel("Exposure Time to Phototype III (min)",fontsize="large")
ax2.set_ylabel("Exposure Time to Phototype IV (min)",fontsize="large")
plt.xlim(8,16)#;plt.ylim(0,175)
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
n_med=0
#<--------------------------Grafica del maximo----------------------------->
ax1.fill_between(x,t[n_med,0,:,0],t[n_med,0,:,1],color=color[n_med])
#<--------------------------Grafica del minimo----------------------------->
ax1.fill_between(x,t[n_med,1,:,0],t[n_med,1,:,1],color=color[n_med],label=phototype[n_med])
#<------------------------Grafica del intermedio--------------------------->
ax1.fill_between(x,t[n_med,0,:,1],t[n_med,1,:,0],color=color[n_med],alpha=0.5)
n_med=1
#<--------------------------Grafica del maximo----------------------------->
ax2.fill_between(x,t[n_med,0,:,0],t[n_med,0,:,1],color=color[n_med])
#<--------------------------Grafica del minimo----------------------------->
ax2.fill_between(x,t[n_med,1,:,0],t[n_med,1,:,1],color=color[n_med],label=phototype[n_med])
#<------------------------Grafica del intermedio--------------------------->
ax2.fill_between(x,t[n_med,0,:,1],t[n_med,1,:,0],color=color[n_med],alpha=0.5)
ax1.plot([15,15],[0,175],ls="--",color="black")
ax1.set_ylim(0,400)
ax2.set_ylim(0,175)
ax1.legend(frameon=False,loc=2)
ax2.legend(frameon=False,loc=1)
#plt.savefig("../Graficas/FillDosis.png")
plt.show()
