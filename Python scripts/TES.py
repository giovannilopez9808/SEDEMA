#                           Fecha de creación
#                           08 abril 2020
#                               Creador
#                     Giovanni Gamaliel LÃopez Padilla
import numpy as np
from os import listdir
import math
import datetime
# <------Valores para interactuar------->
hour_i=8                            #Hora inicial
hour_f=18                           #Hora final
hour_lim=21                         #Hora limite
Dosis=[10000,15000,20000,30000]     #Dosis
MED=[200,250,300,450,600,1000]      #MED eritemal
cloud=[1,0.9,0.6]                   #Cloud Factor
medication=["Pso1","Pso1_5","Pso2","Pso3"]          #Tratamiento
# <-----Funcion para obtener el dia consecutivo a partir de una fecha-------------->
def consecutive_days(year,month,day):
    num=(datetime.date(year,month,day)-datetime.date(year,1,1)).days
    if num>364:
        num=num-x1
    return num
#<---Funcion para obtener el numero de mes de una fecha en dias consecutivos------->
def n_month(day):
    month=(datetime.date(2000,1,1)+datetime.timedelta(day)).month-1
    return month
# <--------Funcion para llevar el conteo de los minutos y el promedio------------->
def cont(type_d,n_dosis,hour,num,Dosis,n_uva,cloud,time_uva,type_c,data_uva):
    dosis_uva=0
    i=hour
    while dosis_uva<Dosis[type_d] and i<n_uva-1:
        if data_uva[i]!=0:
            dosis_uva+=data_uva[i]*60*cloud[type_c]
        i+=+1
    if dosis_uva!=0:
        if i<n_uva-1:
            min=i+1-hour
            time_uva[hour,num,type_d,type_c,0]+=min
            time_uva[hour,num,type_d,type_c,1]+=1
        else:
            min=n_uva-hour
            time_uva[hour,num,type_d,type_c,0]+=min
            time_uva[hour,num,type_d,type_c,1]+=1
    return time_uva[hour,num,type_d,type_c,0],time_uva[hour,num,type_d,type_c,1]
#<-----Funcion que calcula el promedio de los TES y los asigna a donde hay ceros----->
def prom(type_c,n_dosis,time_uva,time_uva_mean,car,i,medication,hour_i,hour_f):
    for type_d in range(n_dosis):
        file=open(car+name[i]+"-"+medication[type_d]+"-"+str(type_c)+".csv","w");file.write(",")
        for day in range(365):
            date_name=datetime.date(2019,1,1)+datetime.timedelta(days=day)
            date_num=str(date_name.day);date_name=date_name.strftime("%b")
            file.write(date_num+"-"+date_name+",")
        file.write("\n")
        for hour in range(n_hour):
            hour_name=str(round(hour_i+hour/60,4))
            file.write(hour_name+",")
            for day in range(365):
                month=n_month(day)
                if time_uva[hour,day,type_d,type_c,0]!=0:
                    time_uva_mean[hour,month,type_d,type_c,0]+=time_uva[hour,day,type_d,type_c,0]
                    time_uva_mean[hour,month,type_d,type_c,1]+=1
            for month in range(12):
                time_uva_mean[hour,month,type_d,type_c,0]=math.ceil(time_uva_mean[hour,month,type_d,type_c,0]/time_uva_mean[hour,month,type_d,type_c,1])
            for day in range(365):
                if time_uva[hour,day,type_d,type_c,0]==0:
                    month=n_month(day)
                    time_uva[hour,day,type_d,type_c,0]=time_uva_mean[hour,month,type_d,type_c,0]
                file.write(str(round(time_uva[hour,day,type_d,type_c,0],2))+",")
            file.write("\n")
        file.close()
#<---------------------------------------------------------------------------------->
carp=["../2016","../2017-2018"]
n_rom=["I","II","III","IV","V","VI"]
name=["dosis","Max"]
n_dosis=np.size(Dosis)
n_cloud=np.size(cloud)
n_MED=np.size(MED)
n_hour=60*(hour_f-hour_i)
#<-------------hour,day,type dosis, type cloud , count---------------->
time_uva=np.zeros([60*(hour_f-hour_i),365,n_dosis,n_cloud,2])
time_uvb=np.zeros([60*(hour_f-hour_i),365,n_MED,n_cloud,2])
time_uvb_mean=np.zeros([60*(hour_f-hour_i),12,n_MED,n_cloud,2])
time_uva_mean=np.zeros([60*(hour_f-hour_i),12,n_dosis,n_cloud,2])
#<----Ciclo para variar las carpetar---->
for car in carp:
    if car=="../2016":
        dirstations=car
        stations=[""]
        print("Analizando 2016")
    else:
        dirstations=car+"/Stations/"
        stations=listdir(dirstations)
        print("Analizando 2017-2018")
    #<----Cilco para variar entre estaciones---->
    for station in stations:
        #<-----Carpeta donde se localizan los dias------>
        dir_med=dirstations+station+"/Resultados/"
        dir_data=dirstations+station+"/AOD500DM/"
        #<-----Lectura de los dias----->
        dates=np.loadtxt(dir_data+"datos500.txt",skiprows=1,usecols=0,dtype=str)
        #<-----Ciclo para variar los dias---->
        for date in dates:
            #<-----Lectura de los resultados del modelo---->
            n_uv=(hour_lim-hour_i)*60
            data_uva=np.loadtxt(dir_med+date+"UVAmo.txt",usecols=1,skiprows=hour_i*60,max_rows=n_uv)
            data_uvb=np.loadtxt(dir_med+date+"Erymo.txt",usecols=1,skiprows=hour_i*60,max_rows=n_uv)
            day,month,year=int(date[4:6]),int(date[2:4]),int(date[0:2])
            num=consecutive_days(year,month,day)
            for type_c in range(n_cloud):
                for type_d in range(n_dosis):
                    for hour in range(n_hour):
                        time_uva[hour,num,type_d,type_c,0],time_uva[hour,num,type_d,type_c,1]=cont(type_d,n_dosis,hour,num,Dosis,n_uv,cloud,time_uva,type_c,data_uva)
                for type_d in range(n_MED):
                    for hour in range(n_hour):
                        time_uvb[hour,num,type_d,type_c,0],time_uvb[hour,num,type_d,type_c,1]=cont(type_d,n_MED,hour,num,MED,n_uv,cloud,time_uvb,type_c,data_uvb)
    for type_c in range(n_cloud):
        for hour in range(n_hour):
            for day in range(365):
                for type_d in range(n_dosis):
                    if time_uva[hour,day,type_d,type_c,1]!=0:
                        time_uva[hour,day,type_d,type_c,0]=math.ceil(time_uva[hour,day,type_d,type_c,0]/time_uva[hour,day,type_d,type_c,1])
                for type_d in range(n_MED):
                    if time_uvb[hour,day,type_d,type_c,1]!=0:
                        time_uvb[hour,day,type_d,type_c,0]=math.ceil(time_uvb[hour,day,type_d,type_c,0]/time_uvb[hour,day,type_d,type_c,1])
car="Data/"
print("Escribiendo archivos")
for type_c in range(n_cloud):
    prom(type_c,n_dosis,time_uva,time_uva_mean,car,0,medication,hour_i,hour_f)
    prom(type_c,n_MED,time_uvb,time_uvb_mean,car,1,n_rom,hour_i,hour_f)