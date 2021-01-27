#                           Fecha de creacion
#                           21 Diciembre 2019
#                               Creador
#                       Giovanni Gamaliel Lopez Padilla
#Este programa grafica las DR con barras de error con su desviaciones estandar 
import numpy as np
import matplotlib.pyplot as plt
#Lista de estaciones 
sta=["CHO","CUT","MER","MON","MPA","PED","SAG","SFE","TLA"]
#Lista de versiones
ver="/v0.0/"
#Lista de AOD
AO=["AOD500","AOD340"]
#Lista de carpetas de AOD
AOD=["/AOD500DM","/AOD340DM"]
nm=["500","340"]
#Ciclo que varia las estaciones
for i in range(np.size(sta)):
    #Ciclo que varia las versiones
    for j in range(np.size(AOD)):
        #Apertura de los archivos que se escribiran
        #Archivo para UVA
        carp="../"+sta[i]
        f1=open(carp+"/DRHora/"+AO[j]+"-UVADRHora.txt","w")
        #Archivo para Eritemica
        f2=open(carp+"/DRHora/"+AO[j]+"-EryDRHora.txt","w")
        #Carpeta donnde se encuentra la version
        car=carp+AOD[j]
        #Lista de los dias
        datos=np.loadtxt(car+"/datos"+nm[j]+".txt",skiprows=1,usecols=0)
        #Ciclo que correra para todos los dias
        for k in range(np.size(datos)):
            #Valor del dia
            file=str(int(datos[k]))
            #Valor de UVA de DR
            UVADR=np.loadtxt(car+ver+"DR/"+file+"UVADR.txt",usecols=1)
            #Valor de Eritemica de DR
            EryDR=np.loadtxt(car+ver+"DR/"+file+"EryDR.txt",usecols=1)
            #Escritura del promedio de las DR
            f1.write(file+" "+str(UVADR.mean())+"\n")
            f2.write(file+" "+str(EryDR.mean())+"\n")
        #Cierre de los archivos
        f1.close()
        f2.close()
    #Lectura de los promedios de UVA para los difentes AOD
    UVA500=np.loadtxt(carp+"/DRHora/"+AO[0]+"-UVADRHora.txt",usecols=1)
    UVA340=np.loadtxt(carp+"/DRHora/"+AO[1]+"-UVADRHora.txt",usecols=1)
    Ery500=np.loadtxt(carp+"/DRHora/"+AO[0]+"-EryDRHora.txt",usecols=1)
    Ery340=np.loadtxt(carp+"/DRHora/"+AO[1]+"-EryDRHora.txt",usecols=1)
    #Numero de dias totales
    num=np.arange(np.size(UVA500))
    plt.ylabel("%UVA Relative Difference")
    plt.xlabel("Days")
    plt.ylim(-40,40)
    plt.xlim(-1,np.size(UVA500))
    plt.title(sta[i])
    #Ploteo de las DR UVA de 550 con sus desviaciones estandar
    plt.errorbar(num,UVA500,yerr=np.nanstd(UVA500),
                 label="AOD 500nm",marker="o",ls="none",alpha=0.6,color="b",
                 capsize=5,markersize=5)
    #Ploteo de las DR UVA de 340 con sus desviaciones estandar
    plt.errorbar(num,UVA340,yerr=np.nanstd(UVA340),
                 label="AOD 340nm",marker="o",ls="none",alpha=0.6,color="r",
                 capsize=5,markersize=5)
    plt.plot([-1,100],[-20,-20],color="black")
    plt.plot([-1,100],[20,20],color="black")
    plt.legend(frameon=False)
    #Guardado del ploteo
    plt.savefig(carp+"/DRHora/UVADRHora.png")
    plt.clf()
    #Numero de dias
    num=np.arange(np.size(Ery340))
    plt.ylabel("%Erythemal Relative Difference")
    plt.xlabel("Days")
    plt.ylim(-40,40)
    plt.xlim(-1,np.size(Ery340))
    plt.title(sta[i])
    #Ploteo de las DR de Eritemica de 550 con sus desviaciones estandar
    plt.errorbar(num,Ery500,yerr=np.nanstd(Ery500),
                 label="AOD 500nm",marker="o",ls="none",alpha=0.6,color="b",
                 capsize=5,markersize=5)
    #Ploteo de las DR de Eritemica de 340 con sus desviaciones estandar
    plt.errorbar(num,Ery340,yerr=np.nanstd(Ery340),
                 label="AOD 340nm",marker="o",ls="none",alpha=0.6,color="r",
                 capsize=5,markersize=5)
    plt.plot([-1,100],[-20,-20],color="black")
    plt.plot([-1,100],[20,20],color="black")
    plt.legend(frameon=False)
    #Guardado de la grafica
    plt.savefig(carp+"/DRHora/EryDRHora.png")
    plt.clf()