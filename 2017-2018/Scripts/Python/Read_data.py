import numpy as np
import os


def mkdir(name, path=""):
    try:
        os.mkdir(path+name)
    except FileExistsError:
        print("Ya existe la carpeta "+path+name)


def total_days(dates, minutes_per_day):
    size = np.size(dates)
    n = int(size/minutes_per_day)
    n += size-minutes_per_day*n
    return int(n)


def format_date(date):
    month = date[0:2]
    day = date[3:5]
    year = date[8:10]
    date = year+month+day
    return date


dir = "../../Archivos/"
dir_mediciones = "/Mediciones/"
dir_stations = "../../Stations/"
minutes_per_day = int(60*24)
files_data = ["UVA_clean.csv", "UVB_clean.csv"]
files_types = ["UVA", "Ery"]
factors=[10,0.05774715]
hours = np.round(np.linspace(0, 24, 1440), 6)
for file_data, files_type,factor in zip(files_data, files_types,factors):
    stations = np.loadtxt(dir+file_data, delimiter=",",
                          max_rows=1, dtype=str, usecols=np.arange(2, 17))
    dates = np.loadtxt(dir+file_data, delimiter=",",
                       dtype=str, usecols=0, skiprows=1)
    n_days = total_days(dates, minutes_per_day)
    for station, col in zip(stations, range(2, 17)):
        station = station.upper()
        mkdir(station, path=dir_stations)
        mkdir("Mediciones", path=dir_stations+station+"/")
        data = np.loadtxt(dir+file_data, delimiter=",",
                            usecols=col, skiprows=1)
        for i_day in range(n_days):
            min_i = minutes_per_day*i_day
            min_f = minutes_per_day*(i_day+1)
            data_day = data[min_i:min_f]
            date_day = dates[min_i:min_i+1][0]
            date_day = format_date(date_day)
            file_day = open(dir_stations+station +
                            dir_mediciones+date_day+files_type+".csv", "w")
            for hour, data_i in zip(hours, data_day):
                file_day.write(str(hour)+","+str(data_i)+"\n")
            file_day.close()
