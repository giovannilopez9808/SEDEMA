import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from PIL import Image
#<-------------------Parametros de las carpetas de datos, titulos de graficas y colores--------------------->
carp=["2016","2017-2018"];title=["Warm dry","Rainy","Cold dry"];color=["orange","#0061FF","green"]
#<-----------------------Meses de las temporadas------------------>
n_season=np.array([[3,5],[6,10]])
#<-------------Hora de final e inicial, total de datos, matriz para los promedios------------->
hour_f,hour_i=20,7;n=(hour_f-hour_i)*60;data=np.zeros([3,n,2])
for i in range(2):
    print("Analizando "+carp[i]);car="../"
    #<------------Localizacion para el año 2016------------------>
    if i==0: car+=carp[i];stations=[""]
    #<------------Localizacion para el año 2017-2018------------->
    else: car+=carp[i]+"/Stations/";stations=listdir(car)  
    for station in stations:
        dir=car+station
        #<------------------------Archivos de los dias----------------------->
        dates=np.loadtxt(dir+"/AOD500DM/datos500.txt",skiprows=1,usecols=0,dtype=str)
        dir+="/Mediciones/v0.0/"  
        for date in dates:
            #<------------------Localización del archivos de datos--------------------->
            arc=dir+date;month=int(date[2:4]);season=2
            for j in range(2):
                #<----------------Localización de la temporada-------------------->
                if n_season[j,0]<=month<=n_season[j,1]: season=j
            #<-----------------------Lectura de datos---------------------------->
            med=np.loadtxt(arc+"Eryme.txt",skiprows=hour_i*60,usecols=1,max_rows=n)
            for hour in range(n):
                var=med[hour]
                if var!=0: data[season,hour,0]+=var;data[season,hour,1]+=1
print("calculando promedios")
n_data=np.copy(data[:,:,1])
for season in range(3):
    for hour in range(n):
        #<-------------------------------------Calculo de los promedios por temporada------------------------->
        if data[season,hour,1]!=0: data[season,hour,0]=data[season,hour,0]/data[season,hour,1]
print("creando graficas")
#<-----------------------------Subplots para tener dos ejes Y---------------------------->
fig,ax1=plt.subplots()
#<-----------------------------Labels del eje X------------------------>
plt.xticks(np.arange(0,n,60),np.arange(hour_i,hour_f))
plt.subplots_adjust(left=0.08,right=0.88,bottom=0.14,top= 0.95)
ax2=ax1.twinx();ax1.set_xlabel("CST (UTC - 6h)",fontsize="large")
ax2.set_ylabel("SED/hr",fontsize="large",rotation=-90,va="bottom");ax1.set_yticks([]);ax2.set_ylim(0,13)
x=np.arange(n)
data=data*40*0.9
for season in range(3):
    #<------------------Decision para el tamaño de la grafica------------------->
    a=4
    if season==1:a=2
    ax2.plot(x,data[season,:,0],label=title[season]+" season",color=color[season],linewidth=a)
ax2.legend(frameon=False,ncol=5,mode="expand",loc="upper center")
tick=np.arange(0,14,1);ax2.set_yticks(tick);ax2.set_yticklabels(tick,fontsize="large")
plt.savefig("a.png")
plt.clf()
im=Image.open("plot.png")
plot=Image.open("a.png")
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(7,3))
ax1.imshow(im)
ax2.imshow(plot)
for ax in [ax1,ax2]:
    ax.axis("off")
plt.subplots_adjust(left=0.033,bottom=0,right=1,top=1,wspace=0)
plt.savefig("climate.png")