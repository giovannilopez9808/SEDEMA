import numpy as np
import datetime


def obtain_month_int(date):
    return int(date[4:6])


def obtain_day_int(date):
    return int(date[6:8])


def obtain_date(date):
    return date[0:8]


def conseday2date(days, year):
    date = datetime.date(year, 1, 1)+datetime.timedelta(days=days)
    return date


def obtain_year_int(date):
    return int(date[0:4])


def date_yymmdd(day, year):
    date = conseday2date(day, year)
    year = str(date.year)
    month = format_number(date.month)
    day = format_number(date.day)
    date = year+month+day
    return date


def format_number(number):
    number_str = str(number)
    number_str = "0"*(2-len(number_str))+number_str
    return number_str


def obtain_days_of_month(month):
    month_f = month+1
    first_day = datetime.date(2019, 1, 1)
    day_i = datetime.date(2019, month, 1)
    if month_f > 12:
        day_f = datetime.date(2019, 12, 31)
    else:
        day_f = datetime.date(2019, month+1, 1)
    day_i = (day_i-first_day).days
    day_f = (day_f-first_day).days+1
    return day_i, day_f


def date2conseday(year, month, day):
    day_conse = (datetime.date(year, month, day) -
                 datetime.date(year, 1, 1)).days
    if day_conse > 364:
        day_conse = 364
    return day_conse


def obtain_data(dates, dataset, year_i, year_f, data_list):
    for date, data in zip(dates, dataset):
        year = obtain_year_int(date)
        if year_f > year >= year_i:
            month, day = obtain_month_int(date), obtain_day_int(date)
            day = date2conseday(year, month, day)
            if data > 0:
                data_list[year-year_i, day] = data


def mean_data(data_list):
    data_mean = np.zeros((4, 12))
    for year in range(4):
        for month in range(12):
            day_i, day_f = obtain_days_of_month(month+1)
            data_select, n = without_zeros(data_list,day_i,day_f,year)
            mean = fill_mean(n, data_select)
            data_mean[year, month] = mean
    return np.round(data_mean, 2)


def without_zeros(data_list, i, f,year):
    data_select = data_list[year, i:f]
    data_select = data_select[data_select > 0]
    size = np.size(data_select)
    return data_select, size


def fill_mean(n, data):
    if n != 0:
        mean = np.mean(data)
    else:
        mean = 0
    return mean


def fill_data(data, data_mean, year_i):
    for year in range(4):
        for day in range(365):
            if data[year, day] == 0:
                month = conseday2date(day, year+year_i).month-1
                data[year, day] = data_mean[year, month]
    data = np.round(data, 2)


def write_data(file, data, year_i):
    for year in range(4):
        for day in range(365):
            date = date_yymmdd(day, year+year_i)
            file_ozono.write(date+","+str(data[year, day])+"\n")


dir = "../Archivos/"
dates = np.loadtxt(dir+"OzonoCDMX.txt", usecols=0, skiprows=28, dtype=str)
data_ozono = np.loadtxt(dir+"OzonoCDMX.txt", usecols=11, skiprows=28)
file_ozono = open(dir+"Ozono.csv", "w")
file_ozono.write("Date,Ozono\n")
year_f, year_i = 2021, 2017
ozono_final = np.zeros((4, 365))
obtain_data(dates, data_ozono, year_i, year_f, ozono_final)
ozono_mean = mean_data(ozono_final)
fill_data(ozono_final, ozono_mean, year_i)
ozono_final = np.round(ozono_final, 2)
write_data(file_ozono, ozono_final, year_i)
file_ozono.close()
