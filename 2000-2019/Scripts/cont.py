import numpy as np
from os import listdir
import datetime
#<---------------------------------------------------------------------------------->
hour_i,hour_f=11,14
parameters=np.array(["CO","O3","NO2","PM10","SO2"],dtype=str)
dir,sta_dir,arc="../Contaminantes/","../Datos/","CDMX.csv"
stations,files=np.array(listdir(sta_dir),dtype=str),np.sort(listdir(dir))
n_sta,n_param=np.size(stations),np.size(parameters)
info=np.zeros([n_param,365,20,2])
for file in files:
    print("Leyendo "+file)
    dates,stations_name,parameters_name,data_list=np.loadtxt(dir+file,skiprows=11,usecols=[0,1,2,3],delimiter=",",dtype=str,unpack=True)
    print("Analizando "+file)
    for date,station_name,parameter_name,data in zip(dates,stations_name,parameters_name,data_list):
        hour,date=int(date[11:13]),date[0:10]
        #<---------------------------------Verificacion de la hora--------------------------->
        if hour_i<=hour<=hour_f:
            day,month,year=int(date[0:2]),int(date[3:5]),int(date[6:10])
            date=(datetime.date(year,month,day)-datetime.date(year,1,1)).days
            if date>364:
                date=364
            #<-----------------------------Verificacion del parametro---------------------->
            loc_parameter=np.where(parameter_name==parameters)
            if np.size(loc_parameter)!=0:
                #<-------------------------Verificacion de que el dato exista-------------->
                if data!="":
                    #<---------------------Verificacion de la estacion--------------------->
                    loc_station=np.where(station_name==stations)
                    if np.size(loc_station)!=0:
                        year+=-2000
                        info[loc_parameter[0],date,year,0]+=float(data)
                        info[loc_parameter[0],date,year,1]+=1
#<---------------------------------Escritura de los archivos---------------------------------->
print("Calculando promedios y escribiendo archivos")
n=0
for parameter in parameters:
    file=open("../Archivos/"+parameter+"_"+arc,"w")
    for day in range(365):
        for year in range(20):
            if info[n,day,year,1]!=0: info[n,day,year,0]=np.round(info[n,day,year,0]/info[n,day,year,1],3)
            else: info[n,day,year,0]=-99
            file.write(str(info[n,day,year,0]))
            if year!=19:
                file.write(",")
        file.write("\n")
    file.close()
    n+=1