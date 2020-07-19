#                           Fecha de creacion
#                             06 enero 2019
#                               Creador
#                       Giovanni Gamaliel Lopez Padilla
#Este programa lee los archivos bajados de AERONET y crea un archivo en el cual
#recompila el AOD medido a diferentes horas y diferentes dias, el formato es
# 1 col - dia con el formato yymmdd
# 2 col - hora
# 3 col - AOD
import numpy as np
#Archivos obtenidos de aeronet
arc=["../Archivos/2017","../Archivos/2018"]
#Numero de columna donde se encuenta el dato de AOD 
#en el archivo .lev20
AODn=[25,18]
#Tipo de AOD
AODname=["340","500"]
for num in range(np.size(AODname)):
    print("Creando archivo AOD"+AODname[num]+"nm")
    #Archivo en donde se guardara el AOD
    AODfile=open("../Archivos/AOD"+AODname[num]+"Hora.txt","w")
    #Ciclo que varia el archivo de Aeronet
    for _j in range(2):
        #Matriz que guarda el AOD
        data=np.loadtxt(arc[_j]+".lev20",skiprows=7,usecols=AODn[num]
                        ,delimiter=",")
        #Matriz que guarda a que dia le corresponde el AOD
        date=np.loadtxt(arc[_j]+".lev20",skiprows=7,usecols=0
                        ,delimiter=",",dtype='str')
        #Matriz que guarda a que hora corresponde el AOD
        hora=np.loadtxt(arc[_j]+".lev20",skiprows=7,usecols=1
                        ,delimiter=",",dtype='str')
        #Matriz para guardar el dia
        day=np.zeros(np.size(date))
        #Matriz que guarda el mes
        month=np.zeros(np.size(date))
        #Matriz que guarda el año
        year=np.zeros(np.size(date))
        #Matrzi que guarda el dia con el formato yymmdd
        files=np.zeros(np.size(date))
        #Matriz que guarda la hora
        hour=np.zeros(np.size(hora))
        for _i in range(np.size(date)):
            #Obtencion del dia
            day[_i]=int(date[_i][0:2])
            #Obtencion del mes
            month[_i]=int(date[_i][3:5])
            #Obtencion del año
            year[_i]=int(date[_i][8:10])
            #Obtencion del dia con el formato yymmdd
            dia=year[_i]*10000+month[_i]*100+day[_i]
            #Guardado del dia con el formato yymmdd
            files[_i]=str(dia)
            #Guarado de la hora
            hour[_i]=hora[_i][0:2]
            #Corrección horaria
            hour[_i]=hour[_i]-6
            #Correccion del dia si es un numero negativo
            if hour[_i]<0:
                hour[_i]=24+hour[_i]
                files[_i]=files[_i]-1
        #Eliminacion de variables ya usadas
        del date,day,month,year,hora,dia
        #Inicialización de la variable
        n=1
        AOD=data[0]
        #Conteo de las horas
        for _i in range(1,np.size(hour)-1):
            #Funcion si para verificar si es la misma hora
            if(hour[_i]==hour[_i+1]):
            #Suma para el promedio
                AOD=AOD+data[_i+1]
                n=n+1
            #Si la funcion si resulta ser falta realiza el calculo del promedio 
            #de la suma e inicializa el valor de AOD
            else:
            #Funcion si para verificar que sí existio valores de AOD
                if(AOD/n>0):
                #Escritura el AOD
                    AODfile.write(str(int(files[_i]))+" "+str(int(hour[_i]))+" "
                                +str(round(AOD/n,4))+"\n")
                #Inicializacion del AOD
                AOD=data[_i+1]
                n=1
    #Cierre del archivo
    AODfile.close()
    #Eliminacion de las variables
    del data,hour,n,files