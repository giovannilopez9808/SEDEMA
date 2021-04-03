from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from functions import *
import numpy as np
# <------------------------Funcion para hacer la grafica----------------------->


def graf(result, levels, title, name, label, month_days, months_name, cm="inferno"):
    plt.subplots_adjust(left=0.097, right=0.977, bottom=0.205, top=0.890)
    plt.title(title)
    plt.ylabel("CST (UTC - 6h)")
    plt.xticks(month_days, months_name, rotation=60)
    plt.ylim(6, 18)
    plt.contourf(result, levels=levels, cmap=cm)
    cbar = plt.colorbar(ticks=levels)
    cbar.ax.set_ylabel(label, rotation=-90, va="bottom")
    plt.show()
    #plt.savefig(name, dpi=200)
    plt.clf()


# <----------------------Carpetas dy titulos de las graficas------------------->
folder_names = {
    "path graphics": "../Graficas/",
    "path data": "../Archivos/",
}
inputs = {
    "UVA": {
        "folder": "UVA",
        "title": "UVA irradince",
        "delta": 5
    },
    "Ery": {
        "folder": "Eritemica",
        "title": "Erythemal irradiance",
        "delta": 0.035/2
    }
}
months_name = obtain_month_names()
# <---------------------Dias de los months_name y delta de cada grafica-------------->
month_days = np.arange(0, 365, 30.5)
delta = [5, 0.035/2]
# <-------------------------Graficas de UVA y Eritemica------------------------>
for input in inputs:
    print("Graficando "+inputs[input]["folder"])
    result = np.loadtxt(folder_names["path data"]+"MaxMe"+input+".txt")
    print(np.shape(result))
    maxi = result.max()
    title = "Mexico City - Period: 2000-2019"
    levels = np.arange(0, maxi+inputs[input]["delta"], inputs[input]["delta"])
    name = folder_names["path graphics"]+"Max"+input+".png"
    label = inputs[input]["title"]+" (W/m$^2$)"
    graf(result, levels, title, name, label, month_days, months_name)
# <-------------------------Definicion de los colres--------------------------->
# colors = [(58/255, 156/255, 43/255),
#           (152/255, 196/255, 8/255),
#           (1, 244/255, 0),
#           (1, 211/255, 0),
#           (246/255, 174/255, 0),
#           (239/255, 131/255, 0),
#           (232/255, 97/255, 5/255),
#           (255/255, 34/255, 34/255),
#           (230/255, 42/255, 20/255),
#           (165/255, 0/255, 0/255),
#           (118/255, 46/255, 159/255),
#           (150/255, 53/255, 188/255),
#           (184/255, 150/255, 235/255),
#           (198/255, 198/255, 248/255)]
# n_bin = 15
# cmap_name = "UV_Index"
# cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
# # <--------------------------Graficas de UV Index------------------------------>
# result = result*40
# min = 1000
# for i in range(np.size(result[:, 0])):
#     for j in range(np.size(result[0, :])):
#         if min > round(result[i, j])-1 and round(result[i, j])-1 > 0:
#             min = result[i, j]
# print(min)
# print("Graficando UV Index")
# title = "UV Index measured in Mexico City \n Period 2000 - 2019"
# label = "UV Index"
# name = folder_names["path graphics"]+"MaxUVindex.png"
# levels = np.arange(1, 16, 1)
# graf(result, levels, title, name, label, month_days, months_name)
