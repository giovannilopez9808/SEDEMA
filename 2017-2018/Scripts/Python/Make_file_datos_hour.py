import numpy as np
from os import listdir


def obtain_factor(nm):
    fac = nm/550
    nm = str(nm)
    return fac, nm


def folder_name_AOD(nm):
    return "AOD"+nm+"HM/"


def search_values(date_list, data_list, date):
    value = data_list[date_list == date]
    if np.size(value) == 0:
        value = [-1]
    return value


def format_date(date):
    year = str(int("20"+date[0:2]))
    month = str(int(date[2:4]))
    day = str(int(date[4:6]))
    return year, month, day


def format_to_tuv(file, date, aod, ozono, year, month, day, hour_i, hour_f):
    file.write(date+" "+aod+" "+ozono+" "+year
               + " "+month+" "+day+" "+hour_i+" "+hour_f+"\n")


def write_aod(file, date, aod, ozono, year, month, day, hour):
    if float(aod) > 0:
        hour_i = str(int(hour))
        hour_f = str(int(hour_i)+1)
        format_to_tuv(file, date, aod, ozono,
                      year, month, day, hour_i, hour_f)


def number_of_days(data1, data2):
    size = np.intersect1d(data1, data2)
    size = np.size(size)
    return size


def size_data_select(data_ozono, dates_aod, data_aod, data_select):
    size_ozono = np.intersect1d(data_ozono, data_select)
    data_list = np.array(data_aod, dtype=float)
    date_aod = dates_aod[data_list > 0]
    size = number_of_days(size_ozono, date_aod)
    return str(size)


def multiply_factor(data, factor):
    data_factor = np.round(np.array(data, dtype=float)*factor, 3)
    data_factor = np.array(data_factor, dtype=str)
    return data_factor


def write_data(file, date, aod, ozono, hour):
    if float(ozono) > 0:
        year, month, day = format_date(date)
        write_aod(file, date, aod,
                  ozono, year, month, day, hour)


def write_hours_number(file, n):
    if n == 1:
        if aod_values != [-1]:
            n = str(n)
            file.write(n+"\n")
    else:
        n = str(n)
        file.write(n+"\n")


nm_list = [340, 500]
nm_col_list = [2, 3]
dir_stations = "../../Stations/"
dir_data = "../../Archivos/"
ozono_dates, ozono_data = np.loadtxt(
    dir_data+"Ozono.csv", delimiter=",", skiprows=1, unpack=True, dtype=str)
for nm, nm_col in zip(nm_list, nm_col_list):
    fac, nm = obtain_factor(nm)
    dir_aod = folder_name_AOD(nm)
    aod_dates, hours, aod_list = np.loadtxt(
        dir_data+"AOD_hour.csv", delimiter=",",
        skiprows=1, unpack=True, dtype=str, usecols=[0, 1, nm_col])
    aod_list = multiply_factor(aod_list, fac)
    stations = listdir(dir_stations)
    for station in stations:
        dir_station = dir_stations+station+"/"
        days_select = np.loadtxt(dir_station+"days_select.txt", dtype=str)
        size = size_data_select(
            ozono_dates, aod_dates, aod_list, days_select)
        file = open(dir_station+dir_aod+"datos.txt", "w")
        file.write(size+"\n")
        for day_select in days_select:
            ozono = search_values(ozono_dates, ozono_data, day_select)
            ozono = ozono[0]
            aod_values = search_values(aod_dates, aod_list, day_select)
            hour_values = search_values(aod_dates, hours, day_select)
            n = np.size(aod_values)
            write_hours_number(file, n)
            for hour, aod in zip(hour_values, aod_values):
                write_data(file, day_select, aod, ozono, hour)
        file.close()
