#                           Fecha de creacion
#                             06 enero 2019
#                               Creador
#                       Giovanni Gamaliel Lopez Padilla
import numpy as np
from os import listdir
car="../Stations/"
#Nanometros que se van a tomar
nm=500
#Factor de la ecuación de Angstrom
fac=nm/550
nm=str(nm)
aod_type="500"
carpaod="/AOD"+aod_type+"DM/"
#Datos de los dias en que existe valor de ozono
ozonoday=np.loadtxt("../OzonoCDMX.txt",usecols=0,dtype="str",skiprows=4290)
#Datos de ozono
ozono=np.loadtxt("../OzonoCDMX.txt",usecols=11,dtype="str",skiprows=4290)
#Estaciones que se analizaran
stations=listdir(car)
#Dias en los que existe datos de AOD
AODday=np.loadtxt("../AOD"+nm+"Dia.txt",usecols=0)
#Año y mes en los que hay datos de AOD de la forma yymm
AODmonth=np.loadtxt("../AOD"+nm+"Dia.txt",usecols=0)
#Datos de AOD
AOD=np.loadtxt("../AOD"+nm+"Dia.txt",usecols=1)
#Ciclo que corre para identificar el dia que esta el dato de ozono de la forma
#yymmdd
for _i in range(np.size(ozonoday)):
    ozonoday[_i]=ozonoday[_i][2:8]
#Ciclo el cual corre para obtener el dia en que existe una medicion de AOD
#de la forma yymm
for _i in range(np.size(AODmonth)):
    AODmonth[_i]=int(AODmonth[_i]/100)
#Ciclo el cual corre para analizar cada estacion
for station in stations:
    print("Analizando estacion "+station)
    #Carpeta en donde se encuentran las mediciones
    carmed=car+station+"/Mediciones/"
    carp=car+station+carpaod
    #Lee los dias escogidos como cielo despejado
    data=np.loadtxt(carmed+"datos.txt",skiprows=1,usecols=0)
#Abre el archivo en donde se guardaran los datos para el dia listo para
#el modelo
    datos=open(carp+"datos"+nm+".txt","w",dtype=str)
    n_days=np.size(data)
#Escribe cuantos dias hay para esa estacion
    datos.write(str(n_days)+"\n")
#Ciclo que corre para cada dia que fue escogido
    for _j in range(n_days):
        #Convierte el dia a string
        o3day=data[_j]
        #Checa las posiciones del dia de ozono
        posozono=(np.where(ozonoday==o3day)[0])
        if np.size(posozono)!=0:
            #Funcion si para verificar que exista el valor para el AOD
            #Encuentra la posicion para el AOD
            posaod=(np.where(AODday==data[_j])[0])
            #Guardado del dato de ozono
            o3=str(ozono[posozono[0]])
            #Verifica que exista para ese dia
            if np.size(posaod)!=0:
                #Guardado del AOD ya para 550nm
                aod=round(AOD[posaod[0]]*fac,4)
                #Si no existe valor de AOD para ese dia se realiza un promedio
                #de las mediciones que hay en el mes
            else:
                #Se crea la version yymm del dia que no existio valor de AOD
                day=data[0:4]
                #Guarda las posiciones que hay en el archivo que coincida con 
                #el mes y el año
                posi=(np.where(AODmonth==day)[0])
                aod=AOD[posi].mean()
                #Guardado del AOD ya como 550nm
                aod=str(round(aod*fac,4))
                #Guardado del dato de ozono
                #Formato del año
            year="20"+o3day[0:2]
            #Formato del mes
            month=o3day[2:4]
            #Formato de dia
            day=o3day[4:6]
            #Escritura en el archivo de datos
            datos.write(o3day+" "+aod+" "+o3+" "+year+" "+month+" "+day+"\n")
    datos.close()   