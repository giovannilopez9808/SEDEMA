from functions import *
import pandas as pd
import datetime
import os


def create_index_yearly_hour(hour_initial, hour_final):
    index_hourly = []
    index_daily = []
    for day in range(365):
        date = conseday_to_date(day, 2001)
        index_daily.append(date)
        day = date.day
        month = date.month
        for hour in range(hour_initial, hour_final+1):
            date = datetime.datetime(2001, month, day, hour)
            index_hourly.append(date)
    return index_daily, index_hourly


def ls(path, wavelenght):
    return [file for file in sorted(os.listdir(path)) if wavelenght in file]


inputs = {
    "path data": "../Archivos/SEDEMA_Data/Radiation/",
    "path results": "../Archivos/",
    "path stations": "../Stations/",
    "year initial": 2000,
    "year final": 2018,
    "hour initial": 6,
    "hour final": 18,
    "wavelenght": {
        "UVA": {
            "name": "UVA",
            "scale": 10,
        },
        "UVB": {
            "name": "UVB",
            "scale": 0.05774715
        }
    },
}
lon = "UVA"
pd.set_option('mode.chained_assignment', None)
stations = sorted(os.listdir(inputs["path stations"]))
hours = [hour for hour in range(inputs["hour initial"],
                                inputs["hour final"]+1)]
files = ls(inputs["path data"],
           inputs["wavelenght"][lon]["name"])
index_daily, index_hourly = create_index_yearly_hour(inputs["hour initial"],
                                                     inputs["hour final"])
data_max_station = pd.DataFrame(columns=stations,
                                index=index_hourly).fillna(0.0)
data_max = pd.DataFrame(columns=hours,
                        index=index_daily).fillna(0.0)
for file in files:
    print("Analizando archivo {}".format(file))
    data = pd.read_csv(inputs["path data"]+file,
                       index_col=0)
    data.index = pd.to_datetime(data.index)
    for station in stations:
        data_station = data[data["cve_station"] == station]
        for hour in range(inputs["hour initial"],
                          inputs["hour final"]+1):
            data_hour = data_station[data_station.index.hour == hour]
            for data_i in data_hour.index:
                month = data_i.month
                day = data_i.day
                if month == 2 and day == 29:
                    day = 28
                value = data_hour["value"][data_i]
                index = datetime.datetime(2001, month, day, hour)
                if data_max_station[station][index] <= value:
                    data_max_station[station][index] = value
data_max_station.to_csv(inputs["path results"]+"data_hour.csv",
                        float_format='%.4f')
for index in data_max_station.index:
    index_date = index.date()
    hour = index.hour
    for station in stations:
        value = data_max_station[station][index]
        if data_max[hour][index_date] <= value:
            data_max[hour][index_date] = value * \
                inputs["wavelenght"][lon]["scale"]
data_max.to_csv(inputs["path results"]+"data.csv",
                float_format='%.4f')
