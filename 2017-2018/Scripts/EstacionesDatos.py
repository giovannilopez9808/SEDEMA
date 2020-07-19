#                           Fecha de creacion
#                             03 enero 2020
#                               Creador
#                       Giovanni Gamaliel López Padilla
#Este programa separa los datos de UVA y UVB en archivos distintos para cada estacion
import numpy as np
import matplotlib.pyplot as plt
#Estaciones por analizar
sta=np.loadtxt("../UVA.txt",max_rows=1,dtype="str")
#Lectura de los dias
day=np.loadtxt("../Days.txt",dtype="str")
#Ciclo que corre para variar las estaciones leidas
for i in range(np.size(sta)):
    print("Leyendo información de la estación "+sta[i])
    #Lectura de los datos de UVA y eritemica
    UVAdata=np.loadtxt("../Archivos/UVA.txt",usecols=i,skiprows=1)
    Erydata=np.loadtxt("../Archivos/UVB.txt",usecols=i,skiprows=1)
    #Inicializacion del contador
    n=0
    #Ciclo que varia los dias
    for j in range(np.size(day)):
        #Inicializacion de la hora
        hora=0
        #Lectura de las mediciones
        UVAme=open("../"+sta[i]+"/Mediciones/v0.0/"+day[j]+"UVAme.txt","w")
        Eryme=open("../"+sta[i]+"/Mediciones/v0.0/"+day[j]+"Eryme.txt","w")
        #Ciclo que varia las horas
        for k in range(24):
            #Ciclo que varia los minutos
            for m in range(60):
                #Normalizacon de los valores a W/m^2
                UVAdata[n]=UVAdata[n]*10
                Erydata[n]=Erydata[n]*0.05774715
                #Escritura de los datos
                UVAme.write(str(hora)+" "+str(UVAdata[n])+"\n")
                Eryme.write(str(hora)+" "+str(Erydata[n])+"\n")
                hora=hora+1/60
                n=n+1
        #Cierre de los archivos
        UVAme.close()
        Eryme.close()
        #Lectura de las mediciones
        UVAme=np.loadtxt("../"+sta[i]+"/Mediciones/v0.0/"+day[j]+"UVAme.txt")
        Eryme=np.loadtxt("../"+sta[i]+"/Mediciones/v0.0/"+day[j]+"Eryme.txt")
        #Limite del eje Y
        plt.ylim(0,75)
        #Titulo
        plt.title(day[j])
        #Ploteo de la medicion UVA
        plt.scatter(UVAme[:,0],UVAme[:,1])
        #Guardado de la grafica
        plt.savefig("../"+sta[i]+"/Mediciones/"+day[j]+"UVAme.png")
        #Limpieza del grafico
        plt.clf()
        #Limite en el eje Y
        plt.ylim(0,0.45)
        #Titulo
        plt.title(day[j])
        #Ploteo de la medicion eritemica
        plt.scatter(Eryme[:,0],Eryme[:,1])
        #Guardado de la grafica
        plt.savefig("../"+sta[i]+"/Mediciones/"+day[j]+"Eryme.png")
        #Limpieza del grafico
        plt.clf()
    del UVAdata,Erydata