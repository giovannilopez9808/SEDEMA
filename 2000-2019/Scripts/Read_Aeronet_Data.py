import pandas as pd
import datetime
import os


def format_data(data, columns):
    data = clean_data(data,
                      inputs["columns"])
    data = date_formtat(data)
    data = drop_negative_values(data)
    return data


def clean_data(data, columns):
    for column in data:
        if not column in columns:
            data = data.drop(column, 1)
    return data


def date_formtat(data):
    data.index = pd.to_datetime(data["Date(dd:mm:yyyy)"],
                                format="%d:%m:%Y")
    data = data.drop("Date(dd:mm:yyyy)", 1)
    return data


def drop_negative_values(data):
    return data[data["AOD_340nm"] >= 0]


def obtain_daily_mean(data):
    return data.resample("D").mean()


def obtain_days_of_the_year(year):
    date_i = datetime.date(year, 1, 1)
    date_f = datetime.date(year, 12, 31)
    days = (date_f-date_i).days
    return days


def write_results(year, data):
    print("{}\t{:.2f}".format(year, data))


inputs = {
    "path data": "../Archivos/AERONET/",
    "columns": ["Date(dd:mm:yyyy)", "AOD_340nm"],
    "path results": "../Archivos/",
    "file results": "AOD_CDMX.csv",
    "year initial": 2000,
    "year final": 2019
}
files = sorted(os.listdir(inputs["path data"]))
file_result = open(inputs["path results"]+inputs["file results"], "w")
file_result.write("Year,AOD 340nm\n")
for file in files:
    year, _ = file.split(".")
    days = obtain_days_of_the_year(int(year))
    data = pd.read_csv(inputs["path data"]+file,
                       skiprows=6)
    data = format_data(data,
                       inputs["columns"])
    daily_mean = obtain_daily_mean(data)
    percentage = daily_mean["AOD_340nm"].count()*100/days
    write_results(year, percentage)
    year_mean = daily_mean.mean()
    file_result.write("{},{:.3f}\n".format(year, year_mean["AOD_340nm"]))
file_result.close()
