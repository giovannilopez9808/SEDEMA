# <------Programa que calcula los maximos diarios anuales de la base de datos----->
from functions import *
from os import listdir
import numpy as np
import datetime


def obtain_month_number(year, year_i, day):
    month = (datetime.date(year_i+year, 1, 1) +
             datetime.timedelta(days=day)).month
    return month


inputs = {
    "path stations": "../Stations/",
    "path data": "../Archivos/",
    "wavelength": {
        "UVA": {
            "filename": "UVA"
        },
        "Erythemal": {
            "filename": "Ery"
        },
    },
    "year initial": 2000,
    "year final": 2019,
    "hour initial": 11,
    "hour final": 15
}
# <-------Lista de estaciones en la base de datos------->
stations = sorted(listdir(inputs["path stations"]))
d_year = inputs["year final"]-inputs["year initial"]+1
# <----Ciclo que varia en eritemica y UVA---->
for wavelength in inputs["wavelength"]:
    print("Analizando {}".format(wavelength))
    max_annual = np.zeros([d_year, 365, 24])
    max_daily = np.zeros([24, 365])
    # <------Ciclo que varia las estaciones------->
    for station in stations:
        dir_station = inputs["path stations"]+station+"/"+wavelength+"/"
        # <----Lista de archivos que hay en la estacion----->
        files = sorted(listdir(dir_station))
        # <----Ciclo que varia en los archivos---->
        for file in files:
            date = obtain_date_from_filename(file)
            day = obtain_day_consecutive(date)
            year = date.year-inputs["year initial"]
            # <--------Lectura de la información----------->
            data = np.loadtxt(dir_station+file, usecols=1)
            # <--------Ciclo que varia en las horas--------->
            for hour in range(np.size(data)):
                if data[hour] > 0:
                    # <----------If para obtener el mayor en la base de datos anual--------------->
                    if max_annual[year, day, hour] < data[hour]:
                        max_annual[year, day, hour] = data[hour]
    print("Calculando maximos diarios")
    # <----------Apertura del archivo resultante que contendra el maximo diario por hora------->
    file = open(inputs["path data"]+"Max_daily_" +
                inputs["wavelength"][wavelength]["filename"]+".csv", "w")

    # <-------Ciclo que varia en las horas--------->
    file.write("Hour")
    for day in range(365):
        date = conseday_to_date(day, 2001)
        date = date_formtat_mmdd(date)
        file.write(",{}".format(date))
    file.write("\n")
    for hour in range(24):
        file.write("{}".format(hour))
        # <------------Ciclo que varia en los dias------------>
        for day in range(365):
            # <----------Ciclo que varia en los años------------->
            max_daily[hour, day] = max_annual[:, day, hour].max()
            # <-----Escritura del archivo-------->
            file.write(",{:.4f}".format(max_daily[hour, day]))
        file.write("\n")
    file.close()
    UVmax = np.zeros([d_year, 12, 2])
    # <---------Apertura del archivo que contendra el maximo mensual-------->
    file = open(inputs["path data"]+"Max_Monthly_" +
                inputs["wavelength"][wavelength]["filename"]+".csv", "w")
    file.write("Date,Max Data,std\n")
    UVdata = np.zeros([d_year, 365])
    prom_UV = np.zeros([d_year, 12, 2])
    std = np.zeros([d_year, 12, 2])
    prom_std = np.zeros(2)
    # <------------Proceso para calcular la desviacion estandar mensual--------------->
    # <-----------Ciclo que varia en los años------------>
    for year in range(d_year):
        # <---------Ciclo que varia en los dias------------>
        for day in range(365):
            max = 0
            for hour in range(inputs["hour initial"], inputs["hour final"]+1):
                if max < max_annual[year, day, hour]:
                    max = max_annual[year, day, hour]
            # <-----------Calculo del mes------------->
            if max > 0:
                month = obtain_month_number(year,
                                            inputs["year initial"],
                                            day)-1
                UVdata[year, day] = max
                UVmax[year, month, 0] += max
                UVmax[year, month, 1] += 1
        # <---------Ciclo que varia en los dias------------>
        for day in range(365):
            # <----------Calculo del numero del mes------------->
            month = obtain_month_number(year,
                                        inputs["year initial"],
                                        day)-1
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
            month = obtain_month_number(year,
                                        inputs["year initial"],
                                        day)-1
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
            date = datetime.date(year+inputs["year initial"],
                                 month+1,
                                 1)
            if UVmax[year, month, 1] != 0:
                UVmax[year, month, 0] = round(
                    UVmax[year, month, 0]/UVmax[year, month, 1], 2)
            if UVmax[year, month, 0] != 0:
                # <---------Escritura del archivo---------->
                file.write("{},{:.4f},{:.4f}\n".format(
                    date, UVmax[year, month, 0], std[year, month, 0]))
    file.close()
