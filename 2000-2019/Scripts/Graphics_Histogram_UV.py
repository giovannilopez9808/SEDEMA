# <------Programa que genera histogramas a partir de la base de datos------>
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
# <-------Funcion para señalar los valores arriba de los histogramas---------->


def autolabel(rects):
    """Attach a text UV_list above each bar in *rects*, displaying its height."""
    for rect, i in zip(rects, range(len(rects))):
        height = rect.get_height()
        ax.annotate("{:.2f}".format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)


# <-------Valores predefinidos-------->
inputs = {
    "path stations": "../Stations/",
    "folder erythemal": "/Erythemal/",
    "path graphics": "../Graphics/",
    "UV minium": 1,
    "UV maximum": 16,
}
# <-------Nombres de estaciones------>
stations = sorted(listdir(inputs["path stations"]))
UV_list = np.arange(inputs["UV minium"],
                    inputs["UV maximum"])
X = UV_list-1
UV_count = np.zeros(inputs["UV maximum"]-inputs["UV minium"])
n_total = 0
font_size = 13
# <-------Ciclo para variar las estaciones---------->
for station in stations:
    # <-----------n_ind: variable que guarda la cantidad de dias----------------->
    print("Analizando estacion "+station)
    path_station = inputs["path stations"]+station+inputs["folder erythemal"]
    files = listdir(path_station)
    # <--------Ciclo para varias las fechas----------->
    for file in files:
        med = np.loadtxt(path_station+file,
                         usecols=1)
        UV = med.max()*40
        # <-----------Conteo de los UV----------->
        if inputs["UV maximum"] >= UV >= inputs["UV minium"]:
            if UV != 0:
                n_total += 1
                UV = int(UV-inputs["UV minium"])
                UV_count[UV] += 1
# <------------Inicio del ploteo del histograma general---------------->
Y = np.arange(0, 20+2, 2)
UV_count = UV_count*100/n_total
fig, ax = plt.subplots(figsize=(9, 7))
plt.xticks(X-0.5, UV_list, fontsize=font_size)
plt.yticks(Y, fontsize=font_size)
plt.ylim(0, 20)
plt.xlim(-1, X.max()+1)
plt.xlabel("UV Index daily maximum", fontsize=font_size)
plt.ylabel("Frequency (%) of Days", fontsize=font_size)
plt.title("Period 2000-2019", fontsize=font_size)
# <--------Grafica de las grillas---------->
# <----Numeros pares------>
even = np.arange(2, 24+2, 2)
# <----Numeros impares----->
odd = np.arange(1, 24+2+1, 2)
for i in range(np.size(even)):
    plt.plot([-4, inputs["UV maximum"]+1], [even[i], even[i]],
             color="black", ls="--", alpha=0.5)
    plt.plot([-4, inputs["UV maximum"]+1], [odd[i], odd[i]],
             color="gray", ls="--", alpha=0.3)
rect = ax.bar(X, UV_count,
              color="#00838a", width=1, edgecolor="black")
autolabel(rect)
# <--------Guardado de la grafica-------------->
plt.subplots_adjust(left=0.102, bottom=0.093, right=0.962, top=0.936)
plt.savefig(inputs["path graphics"]+"Histogram_UVI.png", dpi=400)
plt.show()
plt.clf()
