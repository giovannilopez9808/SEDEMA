#                           Fecha de creacion
#                             06 enero 2019
#                               Creador
#                       Giovanni Gamaliel Lopez Padilla
# Este programa realiza graficas en la carpeta DaysGraphic, busca en todas las estaciones
# los dias en los que hay medicion y grafica una imagen por dia
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os


def yymmdd2date(date):
    year = int("20"+date[0:2])
    month = int(date[2:4])
    day = int(date[4:6])
    date = str(datetime.date(year, month, day))
    return date


inputs = {
    "path stations": "../../Stations/",
    "path data days": "../../Stations/MON/",
    "path measurements": "/Mediciones/",
    "file data days": "days_select.txt",
    "wavelength": "Ery",
}
colors = {
    "CHO": "Blue",
    "CUA": "#03071e",
    "CUT": "#83c5be",
    "FAC":  "#d00000",
    "HAN": "#b07d62",
    "LAA": "#f72585",
    "MER": "black",
    "MON": "Purple",
    "MPA": "#0096c7",
    "PED": "#f89edf",
    "SAG": "orange",
    "SFE": "Green",
    "TLA": "#52b788",
}
stations = sorted(os.listdir(inputs["path stations"]))
dates = np.loadtxt(inputs["path data days"] +
                   inputs["file data days"],
                   dtype=str)
for date in dates:
    for station in stations:
        path = inputs["path stations"]+station+inputs["path measurements"]
        hour, data = np.loadtxt(path+date+inputs["wavelength"]+".csv",
                                delimiter=",",
                                unpack=True)
        if(data.mean() != 0):
            # Ploteo de los datos de medicion
            plt.plot(hour, data*40,
                     label=station,
                     c=colors[station],
                     marker=".",
                     ls="none",
                     ms=3,
                     alpha=0.7)
    date = yymmdd2date(date)
    # Leyenda del eje Y
    plt.ylabel("UV Index")
    # Leyenda del eje X
    plt.xlabel("Local time (h)")
    # Titulo de la grafica
    plt.title(date)
    # Limites de la grafica en el eje X
    plt.xlim(5, 20)
    # Limites de la grafica en el eje Y
    plt.ylim(0, 16)
    # Leyenda de las graficas
    plt.legend(ncol=5,
               frameon=False,
               fontsize=9,
               bbox_to_anchor=(0.9, 1.05, 0, 0.1))
    # Borrado de la grafica
    plt.show()
    plt.clf()
