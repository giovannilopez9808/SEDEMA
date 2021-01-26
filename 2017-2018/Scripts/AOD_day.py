# Este programa crea dos archivos los cuales contendran el AOD a 340nm y 500nm
# leyendo los archivos de la base de datos de Aeronet
import numpy as np


def Count_AOD(data, sum, n):
    if data > 0:
        sum += data
        n += 1
    return sum, n


def init_AOD(data):
    if data > 0:
        sum = data
        n = 1
    else:
        sum = 0
        n = 0
    return sum, n


def prom_AOD(sum, n):
    if n > 0:
        prom = sum/n
    else:
        prom = 0
    return str(round(prom, 4))


dir = "../Archivos/"
# Archivos de Aeronet
file_years = ["2017", "2018"]
# Numero de columnas que esta el AOD 340 y AOD 500 respectivamente
AOD_cols = [25, 18]
# Variacion de los archivos de salida
AOD_names = ["340", "500"]
# Apertura del archivo de salida
AOD_file = open(dir+"AOD_day.csv", "w")
AOD_file.write("Date,AOD 340,AOD 500\n")
for file_year in file_years:
    # Localizacion de los archivos
    dir_data = dir+file_year+"_lev20.csv"
    data_AOD_340 = np.loadtxt(dir_data, skiprows=7,
                              usecols=AOD_cols[0], delimiter=",")
    data_AOD_500 = np.loadtxt(dir_data, skiprows=7,
                              usecols=AOD_cols[1], delimiter=",")
    # Matriz que guarda el valor del dia
    dates = np.loadtxt(dir_data, skiprows=7, usecols=0,
                       delimiter=",", dtype='str')
    data_n = np.size(dates)
    AOD_sum_340 = data_AOD_340[0]
    AOD_sum_500 = data_AOD_500[0]
    n_340 = 1
    n_500 = 1
    for i in range(1, data_n):
        if dates[i-1] == dates[i]:
            AOD_sum_340, n_340 = Count_AOD(data_AOD_340[i], AOD_sum_340, n_340)
            AOD_sum_500, n_500 = Count_AOD(data_AOD_500[i], AOD_sum_500, n_500)
        else:
            AOD_file.write(dates[i-1]+","+prom_AOD(AOD_sum_340, n_340)
                           + ","+prom_AOD(AOD_sum_500, n_500)+"\n")
            AOD_sum_340, n_340 = init_AOD(data_AOD_340[i])
            AOD_sum_500, n_500 = init_AOD(data_AOD_500[i])
AOD_file.close()