import numpy as np
from os import listdir
import pandas as pd
import datetime
import math
#<--------------------Funcion para saber si tomar el lugar o no--------------------->
def loc(n_param,parameters,parameter):
    var=False
    pos=0
    for j in range(n_param):
        if parameter==parameters[j]:
            var=True
            pos=j
    return pos,var
#<---------------------------------------------------------------------------------->
hour_i,hour_f=11,14
parameters=["CO","O3","NO2","PM10"]
dir,sta_dir,arc="../Contaminantes/","../Datos/","CDMX.txt"
stations,files=listdir(sta_dir),listdir(dir)
n_sta,n_param=np.size(stations),np.size(parameters)
info=np.zeros([n_param,365,20,2])
for file in files:
    print("Analizando "+file)
    data=pd.read_csv(dir+file,skiprows=10)
    n=np.size(data["date"])
    for i in range(n):
        hour,date=int((data["date"][i])[11:13]),(data["date"][i])[0:10]
        #<---------------------------------Verificacion de la hora--------------------------->
        if (hour<=hour_f and hour>=hour_i):
            day,month,year=int(date[0:2]),int(date[3:5]),int(date[6:10])
            date=(datetime.date(year,month,day)-datetime.date(year,1,1)).days
            if date>364:
                date=364
            name,name2="cve_station","cve_parameter"    
            if year>2011:
                name,name2="id_station","id_parameter" 
            station,parameter=(data[name][i]),(data[name2][i])
            #<-----------------------------Verificacion del parametro---------------------->
            pos_para,var=loc(n_param,parameters,parameter)
            if var==True:
                value=(data["value"][i])
                #<-------------------------Verificacion de que el dato exista-------------->
                if math.isnan(value)==False:
                    #<---------------------Verificacion de la estacion--------------------->
                    pos_sta,var=loc(n_sta,stations,station)
                    if var==True:
                        year+=-2000
                        info[pos_para,date,year,0]+=value
                        info[pos_para,date,year,1]+=1
#<---------------------------------Escritura de los archivos---------------------------------->
print("Calculando promedios y escribiendo archivos")
for n in range(n_param):
    file=open("../Archivos/"+parameters[n]+arc,"w")
    for day in range(365):
        for year in range(20):
            if info[n,day,year,1]!=0: info[n,day,year,0]=info[n,day,year,0]/info[n,day,year,1]
            else: info[n,day,year,0]=-99
            file.write(str(info[n,day,year,0])+" ")
        file.write("\n")
    file.close()