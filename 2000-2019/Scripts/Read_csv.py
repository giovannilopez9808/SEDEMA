from functions import *
import pandas as pd
import os

inputs = {
    "path data": "../Archivos/SEDEMA_Data/Radiation/",
    "path stations": "../Stations/",
    "Wave": {
        "UVA": {
            "folder": "UVA",
            "name": "UVA",
            "change units": 10,
        },
        "UVB": {
            "folder": "Erythemal",
            "name": "Ery",
            "change units": 0.05774715,
        }
    }
}
files = sorted(os.listdir(inputs["path data"]))
# <--------------Ciclo para analizar todos los archivos----------->
for file in files:
    print("Analizando archivo {}".format(file))
    lon, year = file.split("_")
    year = year[0:4]
    folder = inputs["Wave"][lon]["folder"]
    name = inputs["Wave"][lon]["name"]
    resize = inputs["Wave"][lon]["change units"]
    data = pd.read_csv(inputs["path data"]+file).fillna(0)
    data["Date"] = pd.to_datetime(data["Date"])
    data_len = data["Date"].count()
    # Ciclo para leer las columnas
    for i in range(data_len):
        # Lectura del nombre de la estacion
        station = data["cve_station"][i]
        value = data["value"][i]
        hour = data["Date"][i].hour
        date = date2yymmdd(data["Date"][i].date())
        mkdir(station, path=inputs["path stations"])
        mkdir(folder, path=inputs["path stations"]+station+"/")
        path_station = inputs["path stations"]+station+"/"+folder+"/"
        file = open(path_station+date+".txt", "a")
        file.write("{} {:.5f}\n".format(hour, value*resize))
        file.close()
