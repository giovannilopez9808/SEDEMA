#<------Programa que genera histogramas a partir de la base de datos------>
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from os import listdir 
#<-------Funcion para señalar los valores arriba de los histogramas---------->
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
#<-------Valores predefinidos-------->
UV_min,UV_max,d_UV=1,15,1
#<------Direccion de los datos------>
carp="../Datos/"
#<-------Nombres de estaciones------>
stations=listdir(carp)
label,d_UV,X=np.arange(UV_min,UV_max+d_UV,d_UV),int((UV_max-UV_min)/d_UV),np.arange(d_UV)
UV_count_t,n_total=np.zeros(d_UV),0
#<----Numeros pares------>
even=np.arange(2,24+2,2)
#<----Numeros impares----->
odd=np.arange(1,24+2+1,2)
#<-------Ciclo para variar las estaciones---------->
for station in stations:
    #<-----------n_ind: variable que guarda la cantidad de dias----------------->
    UV_count,n_ind=np.zeros(d_UV),0
    print("Analizando estacion "+station)
    car=carp+station+"/Eritemica/"
    data=listdir(car)
    #<--------Ciclo para varias las fechas----------->
    for date in data:
        med=np.loadtxt(car+date,usecols=1)
        UV=med.max()*40
        #<-----------Conteo de los UV----------->
        if UV_max>=UV>=UV_min:
            n_total+=1
            n_ind+=1
            UV=int(UV-UV_min)
            UV_count[UV]+=1
            UV_count_t[UV]+=1
    if n_ind!=0:
        UV_count=np.around(UV_count*100/n_ind,2)
#<------------Inicio del ploteo del histograma general---------------->
Y=np.arange(0,20+2,2)
UV_count_t=np.around(UV_count_t*100/n_total,2)
fig, ax = plt.subplots(figsize=(9,7))
plt.xticks(X,label,fontsize="large");plt.yticks(Y,fontsize="large")
plt.ylim(0,20);plt.xlim(-1,X.max()+1)
plt.xlabel("UV Index daily maximum",fontsize="large");plt.ylabel("Frequency (%) of Days",fontsize="large")
plt.title("Period 2000-2019",fontsize="large")
#<--------Grafica de las grillas---------->
for i in range(np.size(even)):
    plt.plot([-4,UV_max+1],[even[i],even[i]],color="black",ls="--",alpha=0.5)
    plt.plot([-4,UV_max+1],[odd[i],odd[i]],color="gray",ls="--",alpha=0.3)
rect=ax.bar(X,UV_count_t,color="#00838a");autolabel(rect)
#<--------Guardado de la grafica-------------->
plt.savefig("../Graficas/HistTotal.png")
plt.clf()