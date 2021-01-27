#                           Fecha de creacion
#                             06 enero 2019
#                               Creador
#                       Giovanni Gamaliel Lopez Padilla
#Este programa realiza graficas en la carpeta DaysGraphic, busca en todas las estaciones
#los dias en los que hay medicion y grafica una imagen por dia
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
#Estaciones por graficar
dir="../Stations/"
stations=os.listdir(dir)
#Colores por estacion
stacol=["Blue","Red","Green","black","purple","pink","orange","brown","olive","cyan"]
names=np.transpose((stations,stacol))
#Dias en los cuales se graficara
dates,n=[],(datetime.date(2018,7,31)-datetime.date(2017,1,1)).days
for day in range(n):
    days=datetime.date(2017,1,1)+datetime.timedelta(days=day)
    year,month,date=str(days.year),days.month,days.day
    if month<10: 
        month="0"+str(month)
    else:
        month=str(month)
    if date<10:
        date="0"+str(date)
    else:
        date=str(date)
    year=year[2:4]
    dates=np.append(dates,year+month+date)
#Tipos de longitudes que se analizaran
lon=["Ery","UVA"];irra=["Erythemal","UVA"]
#Valores maximos para los dos tipos longitudes de onda
ylim=[0.45,90]
#Ciclo que corre para los dos tipos de onda
for k in range(2):
    #Ciclo que corre para los dias
    for date in dates:
        print("Graficando dia "+date+" con "+irra[k])
        #Leyenda del eje Y
        plt.ylabel(irra[k]+" Irradiance (W/m$^2$)")
        #Leyenda del eje X
        plt.xlabel("Local hour (h)")
        #Titulo de la grafica
        plt.title(date)
        #Limites de la grafica en el eje X
        plt.xlim(6,19)
        #Limites de la grafica en el eje Y
        plt.ylim(0,ylim[k])
        #Ciclo que corre para variar las estaciones
        for station,color in names:
            #Carpeta donde se encuenran las mediciones
            car="../Stations/"+station+"/Mediciones/v0.0/"
            #Lectura de las medicones
            data=np.loadtxt(car+date+lon[k]+"me.txt")
            #Condicion que verifica si existen datos validos
            if(data[:,1].mean()!=0):
                #Ploteo de los datos de medicion
                plt.plot(data[:,0],data[:,1],label=station,c=color
                ,marker=".",ls="none",ms=3,alpha=0.7)
        #Leyenda de las graficas
        plt.legend(ncol=5,mode="expand",loc="upper center",markerscale=4, scatterpoints=1,frameon=False)
        #Guardado de la grafica
        plt.savefig("../DaysGraphic/"+irra[k]+"/"+date+lon[k]+".png",dpi=600)
        #Borrado de la grafica
        plt.clf()
            