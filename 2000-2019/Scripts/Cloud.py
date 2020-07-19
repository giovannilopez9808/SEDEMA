#<-----------Programa que obtiene la informacion del archivo OzonoCDMX.txt--------->
#<-------------------------y crea el archivo DatosCloud.txt------------------------>
import numpy as np
from os import listdir
#<------------Llama al archivos de los datos--------------->
dates=np.loadtxt("../Archivos/OzonoCDMX.txt",skiprows=1,usecols=0,dtype=str)
data=np.loadtxt("../Archivos/OzonoCDMX.txt",skiprows=1,usecols=15)
cloud=np.ones([20,12,31,2])*2
cloudprom=np.zeros([20,12,2])
clouddate=np.zeros([20,12,31],dtype=int)
#<-----------Ciclo que varia en las fechas-------------->
for date in dates:
    year=int(date[0:4])
    if year<2020:
        year=int(date[2:4])
        month=int(date[4:6])-1
        day=int(date[6:8])-1
        clouddate[year,month,day]=int(date[0:8])
        cloud[year,month,day,0]=cloud[year,month,day,0]+data[i]
        cloud[year,month,day,1]=cloud[year,month,day,1]+1
#<----------Ciclo que varia en los años------------>
for year in range(20):
    #<-----------Ciclo que varia en los meses-------->
    for month in range(12):
        #<----------Ciclo que varia en los dias------>
        for day in range(31):
            if cloud[year,month,day,1]>2:
                cloud[year,month,day,0]=(cloud[year,month,day,0]-2)/(cloud[year,month,day,1]-2)
                cloudprom[year,month,0]=cloudprom[year,month,0]+cloud[year,month,day,0]
                cloudprom[year,month,1]=cloudprom[year,month,1]+1
#<-----Archivo que guardara los datos-------->
arc=open("../Archivos/DatosCloud.txt","w")
#<---------------Calculo del promedio memsual anual--------------->
#<----------Ciclo que varia los años--------->
for year in range(20):
    #<-----------Ciclo que varia los meses---->
    for month in range(12):
        if cloudprom[year,month,1]!=0:
            cloudprom[year,month,0]=cloudprom[year,month,0]/cloudprom[year,month,1]
        #<------------Ciclo que varia los dias---------->
        for day in range(31):
            if clouddate[year,month,day]!=0:
                if cloud[year,month,day,1]>2:
                    cd=cloud[year,month,day,0]
                else:
                    cd=cloudprom[year,month,0]
                files=str(clouddate[year,month,day])
                yearn=files[2:8]
                day=str(int(files[6:8]))
                month=str(int(files[4:6]))
                year=str(int(files[0:4]))
                #<-----------Escritura del archivo----------->
                arc.write(str(yearn)+" "+str(round(cd,3))+" "+year+" "+month+" "+day+"\n")
arc.close()