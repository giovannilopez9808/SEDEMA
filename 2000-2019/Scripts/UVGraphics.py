#<-------------Programa que realiza lo siguiente-------------->
#<----1)Del archivo MaxEry.txt realiza una interpolacion y el metodo---------->
#<---------moving average y los grafica en UVyearlyError---------------------->
#<----2)
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from os import listdir
from scipy.interpolate import interp1d
#<-------------------------------Datos constantes----------------------------->
Meses=["January","February","March","April","May","June","July","August"
            ,"September","October","November","December"]
years=np.arange(2000,2020,1)
X=np.arange(0,20*12,12)
X1=np.arange(0,12*20)
maxi=np.zeros(12);mini=np.zeros(12)+1000
#<-------------Lectura del archivo----------------->
UVmax=np.loadtxt("../Archivos/MaxEry.txt")
#<-----------Eritemica a UV Index---------------->
UVmax[:,1]=UVmax[:,1]*40
#<-----------Desviacion estandar----------------->
UVmax[:,2]=UVmax[:,2]*40
#<------------De Numpy a Pandas----------->
product={"Date":UVmax[:,0],"UVindex":UVmax[:,1],"std":UVmax[:,2]}
df=pd.DataFrame(product)
#<-----------------Linear fit---------------------->
fit=np.polyfit(UVmax[:,0],UVmax[:,1],1)
print(fit)
fit=np.poly1d(fit)
pd2=fit(UVmax[:,0])
#<------------Moving average para 6 meses------------->
df["SMA_6"]=df.iloc[:,1].rolling(window=3).mean()
#<--------------------Inicio de la grafica UVyearlyError----------------------------------->
plt.xticks(X,years,rotation=60,fontsize="large")
plt.yticks(fontsize="large")
plt.title("Period 2000-2019",fontsize="large")
plt.ylabel("UV Index",fontsize="large")
plt.xlim(0,20*12)
plt.ylim(0,16)
#<------------Barras de error--------------->
plt.errorbar(df["Date"],df["UVindex"],yerr=df["std"],marker="o",linewidth=1
,ls="--",alpha=0.6,color="black",capsize=5,markersize=2,label="Monthly average and SD")
#<--------Ploteo del moving average para 3 meses----------->
plt.plot(df["Date"],df["SMA_6"],label="Quarterly Moving average",linewidth=3,color="grey")
#<-----------Ploteo de linear fit------------------>
plt.plot(UVmax[:,0],pd2,label="Linear regression",color="red",linewidth=3)
plt.subplots_adjust(left=0.1,right=0.97,bottom=0.17,top=0.95)
plt.legend(ncol=3,mode="expand",frameon=False,fontsize="small")
#<---------------Guardado de la grafica-------------->
plt.savefig("../Graficas/UVyearlyError.png")
plt.clf()
mean_y=np.zeros([20,2])
for i in range(np.size(UVmax[:,0])):
    year=int(UVmax[i,0]/12)
    mean_y[year,0]+=UVmax[i,1]
    mean_y[year,1]+=1
for year in range(20):
    mean_y[year,0]=mean_y[year,0]/mean_y[year,1]
fit=np.polyfit(np.arange(20),mean_y[:,0],1)
print(fit)