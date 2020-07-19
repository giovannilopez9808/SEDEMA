#                           Fecha de creacion
#                           27 Diciembre 2019
#                               Creador
#                       Giovanni Gamaliel López Padilla
#Localiza los valores maximos y minimos de los maximos solares y guarda su 
#ubicación para graficarlos junto con los resultados de modelo TUV para ese dia.
#Los maximos solares de cada dia lo guarda en un archivo llamado "maximos.txt",
#en seguida checa que otras estaciones tienen ese mismo día de medición y
#las grafica.
import numpy as np
import matplotlib.pyplot as plt
sta=["MON","CHO","CUT","MER","SAG","SFE","TLA"]
styme=["UVAme.txt","Eryme.txt"]
stymo=["UVAmo.txt","Erymo.txt"]
ymax=[75,0.5]
car=["UVA/","Eritemica/"]
lon=["UVA","Erythemal"]
ver="/v0.0/"
maxd=np.zeros(2)
mind=np.zeros(2)
locmod=["","","",""]
stationmax=["","","",""]
locmed=["","","",""]
days=["","","",""]
daysloc=np.zeros(4)
maximos=open("./Maximos.txt","w")
for i in range(np.size(sta)):
    carp="../"+sta[i]
    datos=np.loadtxt(carp+"/AOD500nm/datos.txt",skiprows=1,usecols=0)
    for k in range(np.size(datos)):
        file=str(int(datos[k]))
        UVA=np.loadtxt(carp+"/Mediciones/"+ver+file+"UVAme.txt")
        Eritemica=np.loadtxt(carp+"/Mediciones/"+ver+file+"Eryme.txt")
        maximos.write(sta[i]+" "+file+" "+str(np.max(UVA))+" "
                      +str(np.max(Eritemica))+"\n")
maximos.close()
maxi=np.loadtxt("./maximos.txt",usecols=[2,3])
station=np.loadtxt("./Maximos.txt",usecols=0,dtype='str')
day=np.loadtxt("./Maximos.txt",usecols=1)
n=0
for i in range(2):
    maxd[i]=np.max(maxi[:,i])
    mind[i]=np.min(maxi[:,i])
    var=np.where(maxi[:,i]==maxd[i])[0]
    k=var[0]            
    locmed[n]="../"+station[k]+"/Mediciones"+ver+str(int(day[k]))+styme[i]
    locmod[n]="../"+station[k]+"/AOD340nmv1/"+car[i]+str(int(day[k]))+stymo[i]
    stationmax[n]=station[k]
    days[n]=station[k]+" "+str(int(day[k]))
    daysloc[n]=int(day[k])
    var=np.where(maxi[:,i]==mind[i])[0]
    k=var[0]
    locmed[n+1]="../"+station[k]+"/Mediciones"+ver+str(int(day[k]))+styme[i]
    locmod[n+1]="../"+station[k]+"/AOD340nmv1/"+car[i]
    locmod[n+1]=locmod[n+1]+str(int(day[k]))+stymo[i]
    stationmax[n+1]=station[k]
    days[n+1]=station[k]+" "+str(int(day[k]))
    daysloc[n+1]=int(day[k])
    maxme=np.loadtxt(locmed[n])
    minme=np.loadtxt(locmed[n+1])
    maxmo=np.loadtxt(locmod[n])
    minmo=np.loadtxt(locmod[n+1])
    plt.ylabel(lon[i]+" Irradiance (W/m2)")
    plt.xlabel("Local hour (h)")
    plt.title(days[n])
    plt.xlim(5,20)
    plt.ylim(0,ymax[i])
    plt.scatter(maxme[:,0],maxme[:,1],c="blue",label="Measurement")
    plt.scatter(maxmo[:,0],maxmo[:,1],c="red",label="TUV Model")
    plt.legend(frameon=False,ncol=2)
    plt.show()
    plt.clf()
    plt.ylabel(lon[i]+" Irradiance (W/m2)")
    plt.xlabel("Local hour (h)")
    plt.title(days[n+1])
    plt.xlim(5,20)
    plt.ylim(0,ymax[i])
    plt.scatter(minme[:,0],minme[:,1],c="blue",label="Measurement")
    plt.scatter(minmo[:,0],minmo[:,1],c="red",label="TUV Model")
    plt.legend(frameon=False,ncol=2)
    plt.show()
    plt.clf()
    n=n+2
daysequal=["","","","","","",""]
staequal=["","","","","","",""]
p=0
for n in range(np.size(daysloc)):
    if(daysloc[n]!=0):
        k=0
        for i in range(np.size(sta)):
            carp="../"+sta[i]
            datos=np.loadtxt(carp+"/AOD500nm/datos.txt",skiprows=1,usecols=0)
            j=0
            si=0
            while si==0:
                if daysloc[n]==datos[j]:
                    daysequal[k]=sta[i]+"/Mediciones/"+ver+str(int(daysloc[n]))
                    staequal[k]=sta[i]
                    k=k+1
                    si=1
                j=j+1
                if j==np.size(datos):
                    si=1
        for j in range(2):
            plt.title("Day "+str(int(daysloc[n])))
            plt.xlabel("Local hour (h)")
            plt.ylabel(lon[j]+" Irradiance (W/m2)")
            plt.ylim(0,ymax[j])
            plt.xlim(5,20)
            data=np.loadtxt("../"+stationmax[n]+"/AOD340nmv1/"
                            +car[j]+str(int(daysloc[n]))+stymo[j])
            plt.scatter(data[:,0],data[:,1],label="TUV Model of station "
                        +stationmax[n],c="red")
            for i in range(k):
                data=np.loadtxt("../"+daysequal[i]+styme[j])
                plt.scatter(data[:,0],data[:,1],label=staequal[i])
                plt.legend(loc="upper right")
            plt.legend(loc="upper right",frameon=False,ncol=3)
            plt.show()
            plt.clf()