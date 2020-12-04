import numpy as np
import matplotlib.pyplot as plt
def promedio(data):
    mean=np.zeros(20)
    for year in range(20):
        mean[year]=np.mean(data[:,year])
    return mean
parameters=["PM10","CO","NO2","O3","AOD","SO2"]
ticks=["PM$_{10}$","CO","NO$_2$","O$_3$","AOD$_{340}$","SO$_2$"]
colors=["#A25715","purple","blue","green","#CB258C","black"]
titles=["$\mu g/m^3$","ppm","ppb","ppb","AERONET AOD","ppb"]
lim_list_sup=[75,4,50,90,0.8,50]
lim_list_inf=[0,0,0,50,0,0]
delta_list=[15,1,10,10,0.15,10]
#lim_list_sup=[75,4,90,90,1,25]
#delta_list=[15,1,15,15,0.25,5]
dir,arc="../Archivos/","CDMX.csv"
lw=4;font_size=12
plt.rc('font', size=font_size) 
plt.rc('xtick', labelsize=font_size)  
plt.rc('ytick', labelsize=font_size-1) 
fig,(ax1,ax3,ax4)=plt.subplots(3,figsize=(9,9))
plt.subplots_adjust(top=0.97,bottom=0.1,left=0.09,right=0.9,hspace=0.15)
ax2=ax1.twinx()
ax5=ax4.twinx()
axs=np.array([ax1,ax2,ax3,ax4,ax5,ax3])
for parameter,ax,tick,color,title,lim_inf,lim_sup,delta in zip(parameters,axs,ticks,colors,titles,lim_list_inf,lim_list_sup,delta_list):
    label=np.arange(2000,2020);x=np.arange(20)
    if ax!=ax5:
        file=dir+parameter+"_"+arc
        data=np.loadtxt(file,delimiter=",")
        mean=promedio(data)
    else:
        year_list,data=np.loadtxt(dir+parameter+".txt",skiprows=1,unpack=True)
        x=year_list-2000
        label=year_list
        mean=data
    fit=np.polyfit(x,mean,1)
    prom=round(np.mean(mean),3)
    print(parameter,round(prom,1),round(fit[0]*100/prom,1),np.round(fit,2))
    ax.plot(label,mean,ls="-",label=tick,color=color,linewidth=lw)
    ax.set_xlim(2000,2019)
    ax.set_ylim(lim_inf,lim_sup)
    yticks=np.arange(lim_inf,lim_sup+delta,delta)
    ax.set_yticks(yticks)
    if not(ax in [ax4,ax5]):
        ax.set_xticks([])
    else:
        if ax==ax4:
            ax.set_xticks(label)
            ax.set_xticklabels(label,rotation=60)
    if ax in [ax2,ax5]:
        ax.set_ylabel(title,rotation=-90,va="bottom")
    else:
        ax.set_ylabel(title)
    if ax in [ax2,ax4]:
        ax.legend(frameon=False,ncol=2,loc="best",bbox_to_anchor=(0.84, 1))
    else:
        ax.legend(frameon=False,ncol=2,loc="upper right")
plt.savefig("../Graficas/contCDMX.png",dpi=300)
#plt.show()