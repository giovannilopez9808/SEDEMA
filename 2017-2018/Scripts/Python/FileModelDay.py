import numpy as np
import os


def mkdir(name, path=""):
    try:
        os.mkdir(path+name)
    except FileExistsError:
        print("Ya existe la carpeta "+path+name)


def read_tuv_results(path, file, hour_number=16):
    hour = []
    UVA_data = []
    Ery_data = []
    for _j in range(hour_number):
        k = 132+194*_j
        hora, UVA, Ery = np.loadtxt(path+file+".txt", skiprows=k,
                                    usecols=[0, 2, 3], max_rows=60,
                                    dtype=str, unpack=True)
        hour = np.append(hour, hora)
        UVA_data = np.append(UVA_data, UVA)
        Ery_data = np.append(Ery_data, Ery)
    return hour, UVA_data, Ery_data


dir_stations = "../../Stations/"
nm = "500"
dir_resultados = "ResultadosTUV/"
stations = os.listdir(dir_stations)
for station in stations:
    dir_aod = dir_stations+station+"/AOD"+nm+"DM/"
    mkdir(dir_resultados, path=dir_aod)
    dates = np.loadtxt(dir_aod+"datos.txt", usecols=0, skiprows=1, dtype=str)
    print("Escribiendo datos de la estacion "+station)
    for date in dates:
        file_UVA = open(dir_aod+dir_resultados+date+"UVA.txt", "w")
        file_Eri = open(dir_aod+dir_resultados+date+"Ery.txt", "w")
        hours, UVA_data, Ery_data = read_tuv_results(
            dir_aod+"Resultados/", date)
        for hour, UVA, Ery in zip(hours, UVA_data, Ery_data):
            file_UVA.write(hour+" "+UVA+"\n")
            file_Eri.write(hour+" "+Ery+"\n")
        file_UVA.close()
        file_Eri.close()
