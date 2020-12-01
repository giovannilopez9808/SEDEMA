import numpy as np
import matplotlib.pyplot as plt
#<------------------------------Inicio de la grafica superior----------------------------->
parameters,tick=["PM10","CO"],["PM$_{10}$","CO"]
color,title=["#A25715","purple"],["$\mu g/m^3$","ppm"]
dir,arc="../Archivos/","CDMX.txt"
lw=4
font_size=11
#<-----Parametros para los limites de altura, los espacios y martriz de promedios--------->
label=np.arange(2000,2020);x=np.arange(20);lim=[75,4];delta=[15,1];mean=np.zeros([20,2])
for i in range(2):
    file=dir+parameters[i]+arc
    data=np.loadtxt(file)
    for year in range(20):
        mean[year,i]=np.mean(data[:,year])
    fit=np.polyfit(x,mean[:,i],1)
    prom=round(np.mean(mean[:,i]),3)
    print(parameters[i],prom,round(fit[0]*100/prom,3))
    print(fit)
#<------------------------------ax1 - PM10 y CO, ax3 - O3 y NO2------------------------------------->
fig,(ax1,ax3,ax4)=plt.subplots(3,figsize=(9,7))
plt.subplots_adjust(top=0.9,bottom=0.14,left=0.11,right=0.9)
ax2=ax1.twinx()
#<-----------------------------------Grafica del PM10------------------------------------->
ax1.plot(label,mean[:,0],ls="-",label=tick[0],color=color[0],linewidth=lw)
ax1.set_ylim(0,lim[0]);ax1.set_ylabel(title[0])
#<--------------------------------Eliminacion del eje x------------------------------------------>
ax1.set_xticks([])
#<-----------------------------------Grafica del CO------------------------------------->
ax2.plot(label,mean[:,1],ls="-",label=tick[1],color=color[1],linewidth=lw)
ax2.set_ylim(0,lim[1])
yticks1=np.arange(0,lim[0]+delta[0],delta[0])
yticks2=np.arange(0,lim[1]+delta[1],delta[1])
ax2.set_yticks(yticks2);ax2.set_ylabel(title[1],rotation=-90,va="bottom")
ax1.set_yticks(yticks1)
#<---------------------------Localizacion de las legendas de cada compuesto------------------------>
ax1.legend(frameon=False,ncol=2,loc="best",bbox_to_anchor=(0.895, 1));ax2.legend(frameon=False,ncol=2,loc="best")
#<-----------------------Inicio de la grafica inferior---------------------------->
parameters,title,color,tick=["NO2","O3"],"ppb",["blue","green"],["NO$_2$","O$_3$"]
label,x=np.arange(2000,2020),np.arange(20)
for i in range(np.size(parameters)):
    file=dir+parameters[i]+arc
    data=np.loadtxt(file)
    mean=np.zeros(20)
    for year in range(20):
        mean[year]=np.mean(data[:,year])
    fit=np.polyfit(x,mean,1)
    prom=round(np.mean(mean),3)
    print(parameters[i],prom,round(fit[0]*100/prom,3))
    print(fit)
    #<------------------------------------Graficas de O3 y NO2-------------------------------------->
    ax3.plot(label,mean,ls="-",label=tick[i],color=color[i],linewidth=lw)
ax3.set_ylim(0,80)
ax3.set_yticks(np.arange(0,90+15,15))
ax3.set_ylabel(title)
ax3.set_xticks([])
#<---------------------Leyendas de las graficas---------------------->
ax3.legend(frameon=False,ncol=2,loc="upper right")
label=np.arange(2000,2020);data=np.loadtxt("../Archivos/AOD.txt",skiprows=1)
fit=np.poly1d(fit);pd=fit(data[:,0])
ax4.plot(data[:,0],data[:,1],ls="-",label="AOD$_{340}$",color="#CB258C",linewidth=lw)
ax4.set_xticks(label)
ax4.set_xticklabels(label,rotation=60)
ax4.set_xlim(1999,2020)
ax4.set_yticks(np.arange(0,1+0.25,0.25))
ax4.set_ylim(0,1)  
ax4.set_ylabel("AERONET AOD") 
ax4.legend(frameon=False,loc="upper right")
plt.savefig("../Graficas/contCDMX.png",dpi=300)
plt.show()