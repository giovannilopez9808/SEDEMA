#                           Fecha de creacion
#                             06 enero 2019
#                               Creador
#                       Giovanni Gamaliel Lopez Padilla
#Este programa crea dos archivos los cuales contendran el AOD a 340nm y 500nm
#leyendo los archivos de la base de datos de Aeronet
import numpy as np
#Archivos de Aeronet
#arc=["2017","2018"]
arc=["2016"]
#Numero de columnas que esta el AOD 340 y AOD 500 respectivamente
col=[25,18]
#Variacion de los archivos de salida
AODn=["340","500"]
#Ciclo para varias el AOD 500 y AOD 340
for _m in range(np.size(AODn)):
    #Apertura del archivo de salida
    AODfile=open("../../2016/Archivos/AOD"+AODn[_m]+"Dia.txt","w")
    #AODfile=open("../AOD"+AODn[_m]+"Dia.txt","w")
    #Ciclo para variar los archivos de Aeronet
    for _j in range(np.size(arc)):
        #Localizacion de los archivos
        arcj="../../2016/Archivos/"+arc[_j]
        #arcj="../"+arc[_j]
        #Matriz que guarda el valor del AOD
        data=np.loadtxt(arcj+".lev20",skiprows=7,usecols=col[_m]
                        ,delimiter=",")
        #Matriz que guarda el valor del dia
        date=np.loadtxt(arcj+".lev20",skiprows=7,usecols=0
                        ,delimiter=",",dtype='str')
        #Matriz que guarda el dia
        day=np.zeros(np.size(date))
        #Matriz que guarda el mes
        month=np.zeros(np.size(date))
        #Matriz que guarda el año
        year=np.zeros(np.size(date))
        #Matriz que guarda el dia con el formato yymmdd
        files=np.zeros(np.size(date))
        #Ciclo que varia en las fechas
        for _i in range(np.size(date)):
            #Guardado del dia
            day[_i]=int(date[_i][0:2])
            #Guardado del mes
            month[_i]=int(date[_i][3:5])
            #Guardado del año
            year[_i]=int(date[_i][8:10])
            #Creacion del dia con el formato yymmdd
            dia=year[_i]*10000+month[_i]*100+day[_i]
            #Guardado del dia con el formato yymmdd
            files[_i]=str(dia)
        #Eliminacion de las variables usadas
        del date,day,month,year,dia
        #Inicializacion del conteo y del AOD
        n=1
        AOD=data[0]
        #Ciclo que encontrara los dias que son iguales
        for _i in range(1,np.size(files)-1):
            #Fucnion si para evaluar si se trata del mismo dia
           if(files[_i]==files[_i+1]):
               AOD=AOD+data[_i+1]
               n=n+1
           else:
               if(AOD/n>0):
                   #Escritura del AOD en el archivo
                   AODfile.write(str(int(files[_i]))+" "+str(round(AOD/n,4))+"\n")
                 #Inicializacion del AOD
               AOD=data[_i+1]
               n=1
    AODfile.close()