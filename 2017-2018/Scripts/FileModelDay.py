import numpy as np
from os import listdir
carp="../Stations/"
stations=listdir(carp)
for station in stations:
    car=carp+station+"/AOD340DM/"
    dates=np.loadtxt(car+"datos340.txt",usecols=0,skiprows=1,dtype=str)
    for date in dates:
        print("Escribiendo el dia ",date," en la estacion ",station)
        UVA=open(car+"UVA/"+date+"UVAmo.txt","w")
        Eri=open(car+"Eritemica/"+date+"Erymo.txt","w")
        for _j in range(15):
            carpm=car+"ResultadosTUV/"
            k=132+194*_j
            hora=np.loadtxt(carpm+files+".txt",skiprows=k,usecols=0,max_rows=60,dtype=str)
            UVAme=np.loadtxt(carpm+files+".txt",skiprows=k,usecols=2,max_rows=60)
            Eryme=np.loadtxt(carpm+files+".txt",skiprows=k,usecols=3,max_rows=60)
            for _k in range(np.size(hora)):
                UVA.write(hora[_k]+" "+str(UVAme[_k])+"\n")
                Eri.write(hora[_k]+" "+str(Eryme[_k])+"\n")
        UVA.close()
        Eri.close()