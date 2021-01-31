from os import listdir
import numpy as np
ver = "Ery"
dir_stations = "../../Stations/"
stations = sorted(listdir(dir_stations))
for station in stations:
    if not(station in []):
        dir_aod_results = dir_stations+station+"/AODDR"+ver+"/"
        dates_data, ozono, year, month, day = np.loadtxt(
            dir_aod_results+"datos.txt", skiprows=1, unpack=True, usecols=[0, 2, 3, 4, 5], dtype=str)
        dates_aod, aod_list = np.loadtxt(
            dir_aod_results+"AOD_found.csv", delimiter=",", unpack=True, usecols=[0, 1], skiprows=1, dtype=str)
        file_data = open(dir_aod_results+"datos_w_aod.txt", "w")
        n_data = np.size(dates_data)
        n_aod = np.size(dates_aod)
        file_data.write(str(n_aod)+"\n")
        i_aod = 0
        i_data = 0
        while i_aod < n_aod:
            if dates_data[i_data] == dates_aod[i_aod]:
                line = dates_aod[i_aod]+" "+aod_list[i_aod]+" "+ozono[i_data] + \
                    " "+year[i_data]+" "+month[i_data]+" "+day[i_data]+"\n"
                file_data.write(line)
                i_aod += 1
                print(i_aod, n_aod, station)
            i_data += 1
        file_data.close()
