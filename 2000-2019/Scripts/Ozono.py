#<---------------Programa que recopila la informacion del ozono------------>
from os import listdir
import numpy as np
car="../Ozono/"
#<------------Nombre de los archivos-------------->
files=listdir(car)
ozonodate=ozonodata=np.zeros([5,12,31])
ozonoprom=np.zeros([5,12,2])
#<---------------Ciclo que varia en los dias----------->
for file in files:
    data=np.loadtxt(car+file,skiprows=71,max_rows=1,usecols=65,delimiter=",")
    day,month,year=file[27:29],file[25:27],file[22:24]
    date="20"+year+month+day
    year,month,day=int(year),int(month)-1,int(day)-1
    ozonodata[year,month,day],ozonodate[year,month,day]=data,int(date)
    if data>0:
        ozonoprom[year,month,0]+=data
        ozonoprom[year,month,1]+=1
#<----------Archivo donde seran guardados todos los datos--------------->
arc=open("../Archivos/datosozono.txt","w")
#<-----------Calculo de los promedios mensuales anuales------------->
#<--------Ciclo para las horas----------->
for year in range(5):
    #<----------Ciclo para los meses------------>
    for month in range(12):
        if ozonodata[year,month,1]!=0:
            ozonoprom[year,month,0]=round(ozonoprom[year,month,0]/ozonoprom[year,month,1])
        else:
            ozonoprom[year,month,0]=250
        #<------------Ciclo que varia los dias------------->
        for day in range(31):
            if ozonodate[year,month,day]!=0:
                if ozonodata[year,month,day]!=0:
                    ozono=ozonodata[year,month,day]
                else:
                    ozono=ozonoprom[year,month,0] 
                ozono=str(ozono)
                date=" 200"+str(year)+" "+str(month+1)+" "+str(day+1)
                file=str(int(ozonodate[year,month,day]))
                file=file[2:8]
                #<-----------Escritura en el archivo------------>
                arc.write(file+" "+ozono+date+"\n")
#<---------------Lectura de los archivos------------->
dates=np.loadtxt("../Archivos/OzonoCDMX.txt",skiprows=1,usecols=0,dtype=str)
data=np.loadtxt("../Archivos/OzonoCDMX.txt",skiprows=1,usecols=11)
ozono=np.zeros([20,12,31])
ozonoprom=np.zeros([20,12,2])
ozonodate=np.zeros([20,12,31],dtype=int)
#<-----------Ciclo para variar en los dias----------------->
for i in range(np.size(dates)):
    year=int(dates[i][0:4])
    if year<2020:
        #<------------Guardado de las fechas------------->
        year,month,day=int(dates[i][2:4]),int(dates[i][4:6])-1,int(dates[i][6:8])-1
        ozonodate[year,month,day]=int(dates[i][0:8])
        if data[i]>0:
            if ozono[year,month,day]==0:
                ozono[year,month,day]=data[i]
            else:
                ozono[year,month,day]=(ozono[year,month,day]+data[i])/2
#<------------Ciclo para variar a los años------------>
for year in range(20):
    #<--------Ciclo para varias los meses------------->
    for month in range(12):
        #<------Ciclo para variar los dias------------>
        for day in range(31):
            if ozono[year,month,day]!=0:
                ozonoprom[year,month,0]+=ozono[year,month,day]
                ozonoprom[year,month,1]+=1
#<--------Ciclo para variar los años------------->
for year in range(20):
    #<----------Ciclo para variar los meses---------->
    for month in range(12):
        if ozonoprom[year,month,1]!=0:
            ozonoprom[year,month,0]=ozonoprom[year,month,0]/ozonoprom[year,month,1]
        else:
            ozonoprom[year,month,0]=250
        #<---------Ciclo para variar los dias------------>
        for day in range(31):
            if ozonodate[year,month,day]!=0:
                if ozono[year,month,day]!=0:
                    o3=ozono[year,month,day]
                else:
                    o3=ozonoprom[year,month,day]
                files=str(ozonodate[year,month,day])
                yymmdd=files[2:8]
                #<-------------Escritura del archivo--------------->
                arc.write(str(yymmdd)+" "+str(round(o3))+"\n")
arc.close()
