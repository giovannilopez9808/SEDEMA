#<-----------Libreria para leer el archivo xls---------------->
import xlrd
import numpy as np
#<-------------Librerias para leer archivos y crear carpetas------------>
from os import listdir
from os.path import isfile, join
import os
#<----------Libreria para ubicar los errores------------>
import errno
#<--------Funcion que lee los nombres de los archivos que hay en una carpeta--------->
def ls(ruta):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]
#<--------Localizacion de la carpeta--------->
dir="../xls/"
arc=ls(dir)
#<--------------Ciclo para analizar todos los archivos----------->
for i in range(np.size(arc)):
    print("Analizando archivo "+arc[i])
    year=arc[i][12:14]  #Año del archivo
    lon=arc[i][14:17]   #Longitud de medicion
    #Cambiar UVB a UVA
    if lon=="UVB":
        lon="Ery"
        carp="/Eritemica/"
    else:
        carp="/UVA/"  
    #Verficicacion si es año bisiesto o no
    if (int(year)%4==0): #Listado de fechas para año bisiesto
        date=np.loadtxt("../Archivos/si.txt",dtype=str)
    else: #Listado de fechas para año no bisiesto
        date=np.loadtxt("../Archivos/no.txt",dtype=str)
    #Apertura del archivo de excel
    data=xlrd.open_workbook(dir+arc[i])
    #Lectura del sheet
    sheet=data.sheet_by_index(0)
    #Ciclo para leer las columnas
    for j in range(sheet.ncols-2):
        #Lectura del nombre de la estacion
        station=str(sheet.cell_value(0,j+2))
        #Creacion de la carpeta
        try: #Direccion y nombre de la carpeta
            os.mkdir(dir+station)
        #Verificacion si la carpeta ya existe o no
        except OSError as e: #Si no se produce error realizar nada
            if e.errno!=errno.EEXIST:
                raise
        #Ciclo para variar los dias de las mediciones
        for k in range(int((sheet.nrows-1)/24)):
            #Apertura del archivo donde se guardara la medicion de un día
            file=open("../datos/"+station+carp+year+date[k,0]+date[k,1]+lon+".txt","w")
            #Ciclo que varia las horas
            for n in range(24):  #Lectura de la medicion
                me=sheet.cell_value(k*24+n+1,j+2)
                if me=="NA": med=0
                else:med=float(me)
                if med<0: #Si la medicion es menor a 0, dar el valor de 0
                    med=0 #Cambios de medicion a W/m^2
                if lon=="UVA": #Para UVA
                    med=med*10
                else: #Para Eritemica
                    med=med*0.05774715
                file.write(str(n+1)+" "+str(med)+"\n") #Escritura del archivo
            #Cierre del archivo
            file.close()