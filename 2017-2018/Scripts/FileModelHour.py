import numpy as np
from os import listdir
car="../Stations/"
stations=listdir(car)
for station in stations:
    carp=car+station+"/AOD340HM/"
    num=int(np.loadtxt(carp+"datoswhora.txt",usecols=0,max_rows=1))
    p=1
    for m in range(num):
        n=int(np.loadtxt(carp+"datoswhora.txt",skiprows=p,usecols=0,max_rows=1))
        file=np.loadtxt(carp+"/datoswhora.txt",skiprows=p+1,usecols=0,max_rows=1,dtype=str)
        p=p+n+1
        print("Escribiendo el dia ",file," en la estacion ",station)
        UVA=open(carp+"UVA/"+file+"UVAmo.txt","w")
        Eri=open(carp+"Eritemica/"+file+"Erymo.txt","w")
        for _j in range(n):
            k=int(194*_j+132)
            carpm=carp+"ResultadosTUV/"
            hora=np.around(np.loadtxt(carpm+file+".txt",skiprows=k,usecols=0,max_rows=60),4)
            Uva=np.loadtxt(carpm+file+".txt",skiprows=k,usecols=2,max_rows=60)
            Ery=np.loadtxt(carpm+file+".txt",skiprows=k,usecols=3,max_rows=60)
            for ii in range(np.size(hora)):
                UVA.write(str(hora[ii])+"  "+str(Uva[ii])+"\n")
                Eri.write(str(hora[ii])+"  "+str(Ery[ii])+"\n")
        UVA.close()
        Eri.close()
del k,n,hora,file,Ery,sta,car,m,num,p,UVA,ii