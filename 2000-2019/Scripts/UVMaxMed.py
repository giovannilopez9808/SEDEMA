# <------Programa que calcula los maximos diarios anuales de la base de datos----->
import numpy as np
from os import listdir
import datetime
carp = "../Stations/"
# <-------Lista de estaciones en la base de datos------->
station = listdir(carp)
carplon = ["UVA", "Erythemal"]
lon = ["UVA", "Ery"]
# <----Ciclo que varia en eritemica y UVA---->
for i in range(np.size(lon)):
    print("Analizando "+carplon[i])
    annual = np.zeros([20, 365, 24])
    daily = np.zeros([24, 365])
    # <------Ciclo que varia las estaciones------->
    for namestation in station:
        if len(namestation) == 3:
            car = carp+namestation+"/"+carplon[i]+"/"
            # <----Lista de archivos que hay en la estacion----->
            files = listdir(car)
            # <----Ciclo que varia en los archivos---->
            for file in files:
                year, month, day = int(
                    "20"+file[0:2]), int(file[2:4]), int(file[4:6])
                day = (datetime.date(year, month, day) -
                       datetime.date(year, 1, 1)).days
                # <----------If que funciona para los dias bisiestos------------>
                if day > 364:
                    day = day-1
                year = year-2000
                # <--------Lectura de la información----------->
                data = np.loadtxt(car+file, usecols=1)
                # <--------Ciclo que varia en las horas--------->
                for hour in range(np.size(data)):
                    if data[hour] > 0:
                        # <----------If para obtener el mayor en la base de datos anual--------------->
                        if annual[year, day, hour] < data[hour]:
                            annual[year, day, hour] = data[hour]
    print("Calculando maximos diarios")
    # <----------Apertura del archivo resultante que contendra el maximo diario por hora------->
    file = open("../Archivos/MaxMe"+lon[i]+".txt", "w")
    # <-------Ciclo que varia en las horas--------->
    for hour in range(24):
        # <------------Ciclo que varia en los dias------------>
        for day in range(365):
            # <----------Ciclo que varia en los años------------->
            daily[hour, day] = annual[:, day, hour].max()
            # <-----Escritura del archivo-------->
            file.write(str(daily[hour, day])+" ")
        file.write("\n")
    file.close()
    UVmax = np.zeros([20, 12, 2])
    # <---------Apertura del archivo que contendra el maximo mensual-------->
    file = open("../Archivos/Max"+lon[i]+".txt", "w")
    n = 0
    UVdata = np.zeros([20, 365])
    prom_UV = np.zeros([20, 12, 2])
    std = np.zeros([20, 12, 2])
    prom_std = np.zeros(2)
    # <------------Proceso para calcular la desviacion estandar mensual--------------->
    # <-----------Ciclo que varia en los años------------>
    for year in range(20):
        # <---------Ciclo que varia en los dias------------>
        for day in range(365):
            max = 0
            for hour in range(11, 15):
                if max < annual[year, day, hour]:
                    max = annual[year, day, hour]
            # <-----------Calculo del mes------------->
            if max > 0:
                month = int(str(datetime.date(2000+year, 1, 1) +
                                datetime.timedelta(days=day))[5:7])-1
                UVdata[year, day] = max
                UVmax[year, month, 0] += max
                UVmax[year, month, 1] += 1
        # <---------Ciclo que varia en los dias------------>
        for day in range(365):
            # <----------Calculo del numero del mes------------->
            month = int(str(datetime.date(2000+year, 1, 1) +
                            datetime.timedelta(days=day))[5:7])-1
            if UVdata[year, day] > 0:
                prom_UV[year, month, 0] += UVdata[year, day]
                prom_UV[year, month, 1] += 1
        # <--------Ciclo que varia en el mes----------->
        for month in range(12):
            if prom_UV[year, month, 1] > 0:
                prom_UV[year, month, 0] = round(
                    prom_UV[year, month, 0]/prom_UV[year, month, 1], 2)
        # <-------Ciclo que varia en el dia----------->
        for day in range(365):
            # <---------Calculo del numero del mes------------>
            month = int(str(datetime.date(2000+year, 1, 1) +
                            datetime.timedelta(days=day))[5:7])-1
            if UVdata[year, day] > 0:
                std[year, month, 0] += (prom_UV[year,
                                                month, 0]-UVdata[year, day])**2
                std[year, month, 1] += 1
        # <--------Ciclo que varia en los meses----------->
        for month in range(12):
            if std[year, month, 1] > 0:
                std[year, month, 0] = np.sqrt(
                    std[year, month, 0]/std[year, month, 1])
                prom_std[0] += std[year, month, 0]
                prom_std[1] += 1
        prom_std[0] = round(prom_std[0]/prom_std[1], 2)
        # <-----------Ciclo que varia en el mes--------->
        for month in range(12):
            if std[year, month, 1] == 0:
                # <-------Si la SD en un mes es igual a cero, tomara el valor de la sd general------->
                std[year, month, 0] = prom_std[0]
        # <--------Ciclo que varia en el mes--------->
        for month in range(12):
            if UVmax[year, month, 1] != 0:
                UVmax[year, month, 0] = round(
                    UVmax[year, month, 0]/UVmax[year, month, 1], 2)
            if UVmax[year, month, 0] != 0:
                # <---------Escritura del archivo---------->
                file.write(
                    str(n)+" "+str(UVmax[year, month, 0])+" "+str(std[year, month, 0])+"\n")
            n += 1
    file.close()
