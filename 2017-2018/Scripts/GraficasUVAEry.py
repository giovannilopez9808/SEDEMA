#                           Fecha de creacion
#                           21 Diciembre 2019
#                               Creador
#                       Giovanni Gamaliel López Padilla
#Este codigo toma los archivos de medicion y modelo y los grafica en un mismo
#archivo
import matplotlib.pyplot as plt
import numpy as np
#Estaciones usadas para entrar a la carpeta
#sta=["CHO","CUT","MER","MON","MPA","PED","SAG","SFE","TLA"]
sta=["FAC"]
#Ciclo que cambia de estación en estación
for i in range(np.size(sta)):
    AOD="/AOD340HM/"
    #Carpeta para entrar en el AOD
    car="../"+sta[i]+AOD
    #Version de la medicon
    ver="/v0.0/"
    #Días que contiene cada estacion
    files=np.loadtxt("../"+sta[i]+"/AOD500DM/datos500.txt",skiprows=1,usecols=0)
    #Ciclo para variar los días
    for j in range(np.size(files)):
        #Dia por graficar
        file=str(int(files[j]))
        #Identificador donde va el programa
        print("Graficando dia "+file+" de la estacion "+sta[i])
        #Datos de UVA del modelo
        uvamod=np.loadtxt(car+"UVA/"+file+"UVAmo.txt")
        #Datos de Eritemica del modelo
        erymod=np.loadtxt(car+"Eritemica/"+file+"Erymo.txt")
        #Datos de UVA de la medicion
        uvamed=np.loadtxt("../"+sta[i]+"/Mediciones"+ver+file+"UVAme.txt")
        #Datos de Eritemica de la medición
        erymed=np.loadtxt("../"+sta[i]+"/Mediciones"+ver+file+"Eryme.txt")
        #Inicio del ploteo
        plt.ylabel("Solar UVA Irradiance (W/m2)")
        plt.xlabel("Local Time (h)")
        plt.title(sta[i]+" "+file)
        plt.ylim(0,70)
        plt.xlim(6,19)
        #Ploteo de la medicion
        plt.scatter(uvamed[:,0],uvamed[:,1],label="Measurement")
        #Ploteo del modelo
        plt.scatter(uvamod[:,0],uvamod[:,1],label="TUV model")
        plt.legend(frameon=False,ncol=2)
        #Guardar el archivo
        plt.savefig(car+ver+"Graficas/"+file+"-"+sta[i]+"UVA.png")
        plt.clf()
        plt.ylabel("Solar Erythemal Irradiance (W/m2)")
        plt.xlabel("Local Time (h)")
        plt.title(sta[i]+" "+file)
        plt.ylim(0,0.45)
        plt.xlim(6,19)
        #Ploteo de la medición
        plt.scatter(erymed[:,0],erymed[:,1],label="Measurement")
        #Ploteo del modelo
        plt.scatter(erymod[:,0],erymod[:,1],label="TUV model")
        plt.legend(frameon=False,ncol=2)
        #Guardar el archivo
        plt.savefig(car+ver+"Graficas/"+file+"-"+sta[i]+"Ery.png")
        plt.clf()
del car,erymed,erymod,file,files,i,j,sta,uvamed,uvamod,ver