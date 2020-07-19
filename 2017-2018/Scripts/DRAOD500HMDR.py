#                           Fecha de creacion
#                             06 enero 2020
#                           Ultima modificacion
#                             17 junio 2020
#                               Creador
#                       Giovanni Gamaliel Lopez Padilla
#Este programa realiza las graficas de la medicion contra el modelo de la version
#500HMDR ademas de calcular la RD y graficarlas, todo esto para la irradiancia
#eritemica y UVA
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
#<-----------------------Funcion que grafica el modelo y las mediciones------------------->
def MedModGraph(name,UVAme,UVAmo,ylim,title,ylabel):
    plt.ylabel(ylabel);plt.xlabel("Local hour (h)")
    #<-----------------------Titulo y limites de las graficas------------------>
    plt.title(title);plt.xlim(10,16);plt.ylim(ylim[0],ylim[1])
    #Ploteo de los resultados del modelo
    plt.scatter(UVAmo[:,0],UVAmo[:,1],label="TUV model",c="red")
    #Ploteo de las mediciones
    plt.scatter(UVAme[:,0],UVAme[:,1],label="Measurement",c="blue")
    plt.legend(frameon=False,ncol=2,mode="expand")
    plt.savefig(name)
    plt.clf()
#<-------------------------------Funcion que grafica las DR------------------------------->
def DRplot(DRuva,name,title,ylabel):
    plt.title(title)
    plt.ylabel(ylabel);plt.xlabel("Local hour (h)")
    plt.ylim(-25,25);plt.xlim(10,16)
    plt.scatter(DRuva[:,0],DRuva[:,1])
    plt.plot([0,20],[10,10],c="black")
    plt.plot([0,20],[-10,-10],c="black")
    plt.savefig(name)
    plt.clf()
#<------------------------------Funcion que graficas las RD con el AOD------------------------>
def DRwAod(DRuva,AODx,AODy,name,title,ylabel):
    fig, ax_f = plt.subplots()
    ax2 = ax1.twinx()
    ax2.set_ylim(0,max(AODx)+0.3)
    ax1.set_ylim(-25,25)
    ax2.figure.canvas.draw()
    ax1.scatter(DRuva[:,0],DRuva[:,1],label="%DR",c="blue")
    ax1.plot([4,20],[10,10],c="black")
    ax1.plot([4,20],[-10,-10],c="black")
    ax1.set_xlim(9,16)
    ax1.set_title(title)
    ax1.set_ylabel(ylabel)
    ax1.set_xlabel("Local hour (h)")
    ax2.set_ylabel('AOD 500nm')
    ax2.scatter(AODx,AODy,label="AOD",c="red")
    fig.legend(loc="upper right",frameon=False,ncol=2)
    plt.savefig(name)
    plt.clf()
    del ax2,ax1,fig
#<------------------------------Funcion que escribe en los archivos------------------------------>
def escribir(UVAme,n,file):
    if(UVAme[n,1]!=0):
        #Calculo de la RD
        druva=100*(UVAmo[n,1]-UVAme[n,1])/UVAme[n,1]
        file.write(str(UVAmo[n,0])+" "+str(druva)+"\n")

    
dir="../Stations/";stations=listdir(dir)
lon=["UVA","Eritemica"]
#Ciclo que corre para todas las estaciones
for station in stations:
    print("Analizando la estacion "+station)
    #<------------------Carpeta donde se hara el calculo--------------------->
    car="../"+station+"/AOD500HMDR/"
    #<-----------------------Lectura de los dias----------------------------->
    dates=np.loadtxt("../"+station+"/AOD500DM/datos500.txt",skiprows=1,usecols=0,dtype=str)
    #<-----------------Ciclo que recorre todos los días---------------------->
    for date in dates:
        #<----------------Localizacion donde se encuentra la medicion-------------->
        medi=dir+station+"/Mediciones/v0.0/"+date
        title="Day"+date
        #<---------------------Lectura de los resultados del modelo ---------------->
        UVAmo=np.loadtxt(car+"UVA/"+date+"UVAmo.txt")
        Erymo=np.loadtxt(car+"Eritemica/"+date+"Erymo.txt")
        #Lectura de las mediciones
        UVAme=np.loadtxt(medi+"UVAme.txt",skiprows=600,max_rows=360)
        Eryme=np.loadtxt(medi+"Eryme.txt",skiprows=600,max_rows=360)
        #<-----------------------Grafica del UVA-------------------------------->
        ylabel="UVA Irradiance (W/m2)")
        ylim=[0,75]
        name=car+"v0.0/Graficas/"+date+"UVA.png"
        MedModGraph(name,UVAme,UVAmo,ylim,title,ylabel)
        #<-----------------------Grafica del eritemica------------------------>
        ylabel="Erythemal Irradiance (W/m2)"
        ylim=[0,0.45]
        name=car+"v0.0/Graficas/"+date+"Ery.png"
        MedModGraph(name,Eryme,Erymo,ylim,title,ylabel)
        #<------------------------Inicio del caldulo de RD--------------------->
        #Apertura de los archivos de Diferencias Relativas
        DRuva=open(car+"v0.0/DR/"+date+"DRUVA.txt","w");DRery=open(car+"v0.0/DR/"+date+"DREry.txt","w")
        #<-----------------------Ciclo para los minutos------------------------>
        for k in range(6*60):
            escribir(UVAme,k,DRuva);escribir(Eryme,k,DRery)
        #Cierre de los archivos
        DRuva.close();DRery.close()
        #Lectura de las diferencias relativas
        DRuva=np.loadtxt(car+"v0.0/DR/"+date+"DRUVA.txt")
        #Condicion para verificar la existencia de valores
        if np.size(DRuva)!=0:
            ylabel="%UVA Relative Difference";name=car+"v0.0/DR/Graficas/"+date+"DRUVA.png"
            DRplot(DRuva,name,title,ylabel):
        #Lectura de las diferencias relativas
        DRery=np.loadtxt(car+"v0.0/DR/"+date+"DRery.txt")
        #Condicion para verificar la existencia de los valores
        if np.size(DRery)!=0:
            ylabe=("%Erythemal Relative Difference";name=car+"v0.0/DR/Graficas/"+date+"DRery.png"
            DRplot(DRery,name,title,ylabel):
        #Localizacion de la carpeta donde se localiza el AOD 
        carp=car+"AODFound.txt"
        #Lectura del AOD 
        AOD=np.loadtxt(carp,usecols=[1,2,3],max_rows=6,skiprows=6*j)
        #Condicion para verificar la existencia de DR
        AODx=AOD[:,0]
        if np.size(DRuva)!=0:
            AODy=AOD[:,1]
            ylabel='%RD UVA Irradiance (W/m2)';name=car+"v0.0/DR/DRwAOD/"+date+"UVA.png"
            DRwAod(DRuva,AODx,AODy,name,title,ylabel)
        #Verificacion de la existenica de datos
        if np.size(DRery)!=0:
            AODy=AOD[:,2]
            ylabel='%RD Erythemal Irradiance (W/m2)';name=car+"v0.0/DR/DRwAOD/"+date+"Ery.png"
            DRwAod(DRuva,AODx,AODy,name,title,ylabel)