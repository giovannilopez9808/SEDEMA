import numpy as np
import os


def read_tuv_results(file, type, hour_number=16, path=""):
    if type == "UVA":
        col = 2
    else:
        col = 3
    hour = []
    data_list = []
    for _j in range(hour_number):
        k = 132+194*_j
        hora, data = np.loadtxt(path+file+".txt", skiprows=k,
                                usecols=[0, col], max_rows=60,
                                unpack=True)
        hour = np.append(hour, hora)
        data_list = np.append(data_list, data)
    return hour, data_list


def RD_calculation(data1, data2, aod, delta):
    values_to_count = data1 != 0
    data1 = data1[values_to_count]
    data2 = data2[values_to_count]
    n = np.size(data1)
    if n > 0:
        dif_relative = (data2-data1)/data1
        RD_abs = round(np.mean(np.abs(dif_relative))*100, 2)
        dif_relative = round(np.mean(dif_relative)*100, 2)
        if dif_relative < 0 or RD_abs < 10 or aod >= 0.8:
            decision = True
        else:
            decision = False
            aod += delta
            aod = round(aod, 3)
    else:
        aod = 0
        RD_abs = -1
        dif_relative = -1
        decision = True
    return decision, aod, str(RD_abs), str(dif_relative)

def write_aod(file, date, rd, dif):
    if rd != "-1":
        file.write(date+","+str(aod)+","+rd+","+dif+"\n")

dir_stations = "../../Stations/"
ver = "Ery"
hour_i = 11
hour_f = 16
aod_delta = 0.01
hour_total = hour_f-hour_i
stations = sorted(os.listdir(dir_stations))
for station in stations:
    dir_station = dir_stations+station+"/"
    dir_mediciones = dir_station+"Mediciones/"
    dir_resultados = dir_station+"AOD_DR_"+ver+"/"
    file_aod = open(dir_resultados+"AOD_found.csv", "w")
    file_aod.write("Date,AOD,RD, Difference\n")
    dates, ozono_list, years, months, days = np.loadtxt(
        dir_resultados+"datos.txt", skiprows=1, usecols=[0, 2, 3, 4, 5], unpack=True, dtype=str)
    for date, ozono, year, month, day in zip(dates, ozono_list, years, months, days):
        print("Analizando estación "+station +
              " en el día "+day+" "+month+" "+year)
        hour_med, data_med = np.loadtxt(
            dir_mediciones+date+ver+".csv", unpack=True,
            skiprows=hour_i*60, max_rows=hour_total*60, delimiter=",")
        aod = 0.025
        isaodfine = False
        while not(isaodfine):
            file_data = open("datos.txt", "w")
            file_data.write(station+"\n")
            line = date+" "+str(aod)+" "+ozono+" "+year+" "+month+" "+day+"\n"
            file_data.write(line)
            file_data.close()
            os.system("./tuvDR.out")
            hour, data_model = read_tuv_results(
                date, type=ver, hour_number=hour_total)
            isaodfine, aod, RD_abs, dif_relative = RD_calculation(
                data_med, data_model, aod, aod_delta)
        write_aod(file_aod, date, RD_abs, dif_relative)
        os.system("rm "+date+".txt")
    file_aod.close()
