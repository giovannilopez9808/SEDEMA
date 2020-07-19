#<----------Este programa lee los archivos del modelo TUV---------->
#<------------y los separa en diferentes archivos------------------>
import numpy as np
from os import listdir 
tauver="0.16"
car="../ResultadosTUV/"+tauver+"/"
#<---------Archivos que se procesaran---------->
file=listdir(car)
#<--------Ciclo que varia los dias----------->
for files in file:
    year=int(files[0:2])
    if year>16:
        date=files[0:6]
        print("Escribiendo el dia ",files)
        #<----------Apertura del archivo de escritura--------->
        UVA=open("../UVA/"+tauver+"/"+date+"UVAmo.txt","w")
        Eri=open("../Eritemica/"+tauver+"/"+date+"Erymo.txt","w")
        #<-------Ciclo que varia para leer el formato---------->
        for _j in range(24):
            k=132+194*_j
            hora=np.loadtxt(car+files,skiprows=k,usecols=0,max_rows=60)
            UVAme=np.loadtxt(car+files,skiprows=k,usecols=2,max_rows=60)
            Eryme=np.loadtxt(car+files,skiprows=k,usecols=3,max_rows=60)
            #<--------Ciclo que varia las horas------------>
            for _k in range(60):
                UVA.write(str(hora[_k])+" "+str(UVAme[_k])+"\n")
                Eri.write(str(hora[_k])+" "+str(Eryme[_k])+"\n")
        UVA.close()
        Eri.close()
        del date,hora,UVAme,Eryme,k