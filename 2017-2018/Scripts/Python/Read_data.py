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


def clean_data(data):
    n_data = np.size(data)
    data_clean = np.zeros(n_data)
    for i in range(n_data):
        if data[i] != '':
            data_clean[i] = float(data[i])
    return data_clean


def clean_date(date):
    month = date[0:2]
    day = date[3:5]
    year = date[6:10]
    date = year+month+day
    return date


def format_data(date, data):
    data = clean_data(data)
    date = clean_date(date)
    return date, data


dir = "../Archivos/"
dir_mediciones = "/Mediciones/"
dir_stations = "../Stations/"
minutes_per_day = int(60*24)
files_data = ["UVA.csv", "UVB.csv"]
files_types = ["UVA", "Ery"]
hours = np.round(np.linspace(0, 24, 1440), 6)
for file_data, files_type in zip(files_data, files_types):
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
                          usecols=col, skiprows=1, dtype=str)
        for i_day in range(n_days):
            min_i = minutes_per_day*i_day
            min_f = minutes_per_day*(i_day+1)
            data_day = data[min_i:min_f]
            date_day = dates[min_i:min_i+1][0]
            date_day, data_day = format_data(date_day, data_day)
            file_day = open(dir_stations+station +
                            dir_mediciones+date_day+files_type+".txt", "w")
            for hour, data_i in zip(hours, data_day):
                file_day.write(str(hour)+" "+str(data_i)+"\n")
            file_day.close()
