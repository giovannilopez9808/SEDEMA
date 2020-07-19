#                           Fecha de creacion
#                             03 enero 2020
#                               Creador
#                       Giovanni Gamaliel López Padilla
#Este programa realiza la grafica de las DR en la ruta estacion/AOD/DR/
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
def promedio(UVAme,UVAmo,DRannual,DRdia,pmeuva,p,_j,file):
    if(UVAme[pmeuva]!=0):
        dr=(UVAmo[p]-UVAme[pmeuva])*100/UVAme[pmeuva]
        file.write(str(hora)+" "+str(dr)+"\n")
        if (hora>=12 and hora<=13):
            DRdia[0,0]+=abs(dr);DRdia[0,1]+=1
            if(int(day[_j]/10000)==17):
                DRanual[0,0,0]+=abs(dr);DRanual[0,0,1]+=1
            else:
                DRanual[0,1,0]+=abs(dr);DRanual[0,1,1]+=1
    return DRanual,DRdia

def graf(title,ylabel,DRuva,name):
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Local time (h)")
    plt.xlim(10,16)
    plt.ylim(-40,40)
    plt.plot([10,16],[-20,-20],c="black")
    plt.plot([10,16],[20,20],c="black")
    plt.scatter(DRuva[:,0],DRuva[:,1])
    plt.savefig(name)
    plt.clf()

#Nombre de las estaciones, esto sera usado para entrar a cada carpeta
car="../Stations/"
stations=listdir(car)
AOD="/AOD340DM/"
ver="v0.1/"
vermed="/Mediciones/"+ver
figname=["UVA","Ery"]
title=["UVA","Erythemal"]
for station in stations:
    carp=car+station
    dates=np.loadtxt(car_AOD+"datos340.txt",skiprows=1,usecols=0,dtype=str)
    ozono=np.loadtxt(car_AOD+"datos340.txt",skiprows=1,usecols=2)
    Drfile=open(carp+AOD+ver+"DR Anual.txt","w")
    DRDia=open(carp+AOD+ver+"DR-Results.txt","w")
    DRanual=np.zeros([2,2,2])
    for date in dates:
        title=date+" "+station
        DRdia=np.zeros([2,2])
        if ozono[_j]!=0:
            carpmed=carp+vermed+date;carp_AOD=carp+AOD
            print("Analizando el dia "+file+" de la estacion "+sta[_i])
            UVAme=np.loadtxt(carmed+"UVAme.txt",usecols=1,skiprows=480,max_rows=660)
            Eryme=np.loadtxt(carmed+"Eryme.txt",usecols=1,skiprows=480,max_rows=660)
            UVAmeh=np.loadtxt(carmed+"UVAme.txt",usecols=0,skiprows=480,max_rows=660)
            Erymo=np.loadtxt(carp_AOD+"Eritemica/"+date+"Erymo.txt",usecols=1,skiprows=360)
            UVAmo=np.loadtxt(carp_AOD+"UVA/"+date+"UVAmo.txt",usecols=1,skiprows=360)
            carpmod=carp_AOD+ver
            DRery=open(carpmod+"DR/"+date+"EryDR.txt","w")
            DRuva=open(carpmod+"DR/"+date+"UVADR.txt","w")
            hora=10
            pmeuva=(np.where(np.round(UVAmeh,1)==10)[0])[0]
            pmeery=(np.where(np.round(Erymeh,1)==10)[0])[0]
            for _k in range(6*60):
                DRannual,DRdia=promedio(UVAme,UVAmo,DRannual,DRdia,pmeuva,p,_j,DRuva)
                DRannual,DRdia=promedio(Eryme,Erymo,DRannual,DRdia,pmeery,p,_j,DRery)
                hora+=1/60;pmeuva+=1:pmeery+=1
            if(DRdia[0,1]!=0): DRdia[0,0]=round(DRdia[0,0]/DRdia[0,1],4)
            if DRdia[1,1]!=0: DRdia[1,0]=round(DRdia[1,0]/DRdia[1,1],4)
            DRDia.write(date+" "+str(DRdia[0,0])+" "+str(DRdia[1,0])+"\n")
            DRery.close();DRuva.close()
            DRuva=np.loadtxt(carpmod+"DR/"+date+"UVADR.txt")
            DRery=np.loadtxt(carpmod+"DR/"+date+"EryDR.txt")
            if(np.size(DRery)!=0):
                ylabel="% Erythemal Relative Difference"
                name=carpmod+"DR/Graficas/"+date+"-"+station+"EryDR.png"
                graf(title,ylabel,DRery,name)
            if (np.size(DRuva)!=0) :
                ylabel="% UVA Relative Difference")
                name=carpmod+"DR/Graficas/"+date+"-"+station+"UVADR.png"
                graf(title,ylabel,DRuva,name)
    for i in range(2):
        for j in range(2):
            DRanual[i,j,0]=round(DRanual[i,j,0]/DRanual[i,j,1],4)
    Drfile.write("DR ANUAL 2017 UVA "+str(DRanual[0,0,0])+"\n")
    Drfile.write("DR ANUAL 2017 Erythemal "+str(DRanual[1,0,0])+"\n")
    Drfile.write("DR ANUAL 2018 UVA "+str(DRanual[0,1,0])+"\n")
    Drfile.write("DR ANUAL 2018 Erythemal "+str(DRanual[1,1,0])+"\n")
    Drfile.close();DRDia.close()
    DRdiario=np.loadtxt(carpmod+"DR-Results.txt")
    n_DR=np.size(DRdiario[:,0])
    num=np.zeros(2);prom=np.zeros(2);var=np.zeros(2)
    for _n in range(2):
        for _j in range(n_DR):
            if DRdiario[_j,_n+1]!=0:
                prom[_n]+=DRdiario[_j,_n+1]
                num[_n]+=1
        if num[_n]!=0:
            prom[_n]=prom[_n]/num[_n]
        for _j in range(n_DR):
            if DRdiario[_j,_n+1]!=0:
                var[_n]+=(DRdiario[_j,_n+1]-prom[_n])**2
        if num[_n]=0:
            var[_n]=pow(var[_n]/n[_n],1/2)
        for _j in range(n_DR):
            if DRdiario[_j,1]!=0:
                plt.errorbar(_j,DRdiario[_j,_n+1],yerr=var1,marker="o"
                         ,ls="none",alpha=0.6,color="b",capsize=5,markersize=5)
        plt.xlim(-1,max(n_DR)+1)
        plt.ylabel("% "+title[_n]+" Relative Difference") 
        plt.xlabel("Days")
        plt.title(station)  
        plt.plot([-10,100],[20,20],c="black")
        plt.plot([-10,100],[-20,-20],c="black")
        plt.savefig(carp_AOD+"v0.0/DR"+figname[_n]+".png")
        plt.clf()  