#                           Fecha de creacion
#                           21 Diciembre 2019
#                               Creador
#                       Giovanni Gamaliel Lopez Padilla
#Este programa revisa los valores de AOD para cada estacion y las plotea en
#una misma grafica y sera guardada e la ruta estacion/AOD
import numpy as np
import matplotlib.pyplot as plt
#Lista de las estaciones
sta=["CHO","CUT","FAC","MER","MON","MPA","PED","SAG","SFE","TLA"]
#Carpeta donde se guardara
for i in range(np.size(sta)):
    print("Analizando la estacion "+sta[i])
    #Lectura del AOD 500
    aod500=np.loadtxt("../"+sta[i]+"/AOD500DM/datos500.txt"
                      ,skiprows=1,usecols=1)
    #Lectura del AOD 340
    aod340=np.loadtxt("../"+sta[i]+"/AOD340DM/datos340.txt"
                      ,skiprows=1,usecols=1)
    #Lectura de los dias
    dias=np.loadtxt("../"+sta[i]+"/AOD500DM/datos500.txt",skiprows=1,usecols=0)
    #Dias del a�o con su correspondencia al d�a consecutivo
    num=np.loadtxt("../Days.txt")
    #Reinicio de la busqueda
    #Ciclo que hace la correspondencia
    for j in range(np.size(dias)):
        a=(np.where(num==dias[j])[0])[0]
        dias[j]=a
    #Ploteo de la grafica
    plt.xlabel("Consecutive Days 2017-2018")
    plt.ylabel("Daily mean AOD from AERONET")
    plt.title(sta[i])
    plt.ylim(0,0.8)
    #Ploteo de AOD 550
    plt.scatter(dias,aod500,label="AOD 500nm",c="r",alpha=0.6)
    #Ploteo de AOD 340
    plt.scatter(dias,aod340,label="AOD 340nm",c="b",alpha=0.6)
    plt.legend(frameon=False,ncol=2,loc="upper right",mode="expand",
           borderaxespad=0.,bbox_to_anchor=(0., 1, 1., .1))
    #Guardar el archivo
    plt.savefig("../"+sta[i]+"/AOD.png")
    plt.clf()