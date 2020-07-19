#                           Fecha de creacion
#                           21 Diciembre 2019
#                               Creador
#                       Giovanni Gamaliel López Padilla
#Este programa realiza los archivos datoswhora para cada estacion
import numpy as np
from os import listdir
#Tipo de AOD
typeAOD=["340"]
for ntype in range(np.size(typeAOD)):
    print("Creando AOD"+typeAOD[ntype]+"nm")
    #Lectura de los datos de AOD
    data=np.loadtxt("../AOD"+typeAOD[ntype]+"Hora.txt")
    #Calculo del promedio por horas cada dia del AOD
    # 1er columna - Horas del dia
    # 2da columna - Mes
    # 3er columna - 0 - Valor - 1 - Conteo 
    aodprom=np.zeros([24,12,2])
    #Ciclo para calcular el AOD por hora y guardarlo en aodprom
    for _i in range(np.size(data[:,0])):
        #Valor de la posicion del mes
        mes=int(str(int(data[_i,0]))[2:4])
        #Valor en posicion de la matriz para el mes
        mes=mes-1
        #Valor de la posicion de la hora
        hora=int(data[_i,1])
        #Valor de la posicion en la matriz para la hora
        hora=hora-1
        #Guardado de l valor
        aodprom[hora,mes,0]+=data[_i,2]
        #Conteo
        aodprom[hora,mes,1]+=1
    #Ciclo para realizar el promedio del AOD
    for _i in range(np.size(aodprom[:,0,0])):
        for _j in range(np.size(aodprom[0,:,0])):
            #Condicional para verificar si existe un valor de AOD
            if aodprom[_i,_j,1]!=0:
                aodprom[_i,_j,0]=aodprom[_i,_j,0]/aodprom[_i,_j,1]
    del mes,hora
    #Nombre de las estaciones
    car="../Stations/"
    stations=listdir(car)
    #Ciclo para correr en todas las estaciones
    for station in stations:
        carp=car+station
        datos=np.loadtxt(carp+"/AOD"+typeAOD[ntype]+"DM/datos"+typeAOD[ntype]+".txt",skiprows=1)
        arc=open(carp+"/AOD"+typeAOD[ntype]+"HM/datos"+typeAOD[ntype]+"Hora.txt","w")
        num=np.size(datos[:,0])
        arc.write(str(num)+"\n")
        for _i in range(num):
            sea=np.where(data==datos[_i,0])[0]
            n_sea=np.size(sea)
            if n_sea!=0:
                arc.write(str(n_sea)+"\n")
                for _j in range(n_sea):
                    p=sea[_j]
                    ini=data[p,1]
                    fin=ini+1
                    arc.write(str(int(datos[_i,0]))+" "+str(data[p,2])+" "
                            +str(datos[_i,2])+" "+str(int(datos[_i,3]))
                            +" "+str(int(datos[_i,4]))+" "+str(int(datos[_i,5]))
                            +" "+str(int(ini))+" "+str(int(fin))+"\n")
            else:
                mes=int(str(datos[_i,0])[2:4])
                mes=mes-1
                n=np.size(np.where(aodprom[:,mes,1]!=0)[0])
                arc.write(str(n)+"\n")
                for _j in range(np.size(aodprom[:,mes,0])):
                    if aodprom[_j,mes,0]!=0:
                        arc.write(str(int(datos[_i,0]))+" "
                                +str(round(aodprom[_j,mes,0],4))
                                +" "+str(datos[_i,2])
                                +" "+str(int(datos[_i,3]))
                                +" "+str(int(datos[_i,4]))
                                +" "+str(int(datos[_i,5]))+" "+str(int(_j))
                                +" "+str(int(_j+1))+"\n")
        arc.close()