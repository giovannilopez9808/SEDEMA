import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


def select_files(files, type_name):
    files_type = []
    for file in files:
        if type_name in file:
            files_type.append(file)
    return files_type


def read_data(path, name):
    data = pd.read_csv("{}{}".format(path,
                                     name),
                       index_col=0)
    data = format_date_data(data)
    return data


def format_date_data(data):
    data.index = pd.to_datetime(data.index)
    data = data.drop(["parameter",
                      "unit", ],
                     1)
    return data


def clean_data(data, hour_i, hour_f):
    data = data[data.index.hour >= hour_i]
    data = data[data.index.hour <= hour_f]
    return data


def obtain_daily_maximum_per_stations(data):
    return data.groupby("cve_station").resample("D").max()


def format_data(data, resize):
    data["value"] = data["value"]*40*resize
    data = data.dropna()
    return data


def autolabel(rects):
    """Attach a text UV_list above each bar in *rects*, displaying its height."""
    for rect, i in zip(rects, range(len(rects))):
        height = rect.get_height()
        ax.annotate("{:.2f}".format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)


inputs = {
    "path data": "../Archivos/SEDEMA_Data/Radiation/",
    "path graphics": "../Graphics/",
    "wavelength": {  # "UVA": 10,
        "UVB": 0.0583, },
    "hour initial": 11,
    "hour final": 16,
    "UV minium": 1,
    "UV maximum": 16,
}
UV_count = np.zeros(inputs["UV maximum"]-inputs["UV minium"])
UV_list = np.arange(inputs["UV minium"],
                    inputs["UV maximum"])
X = UV_list-1
font_size = 13
files = sorted(os.listdir(inputs["path data"]))
n_total = 0
for wavelength in inputs["wavelength"]:
    resize = inputs["wavelength"][wavelength]
    files_type = select_files(files,
                              wavelength)
    for file in files_type:
        if not "2020" in file:
            print("Analizando archivo {}".format(file))
            data = read_data(inputs["path data"],
                             file)
            # data = clean_data(data,
            #                   inputs["hour initial"],
            #                   inputs["hour final"])
            data = obtain_daily_maximum_per_stations(data)
            data = format_data(data,
                               resize)
            for index in data.index:
                UV = data["value"][index]
                if inputs["UV maximum"] >= UV >= inputs["UV minium"]:
                    UV = int(UV-inputs["UV minium"])
                    UV_count[UV] += 1
                    n_total += 1
Y = np.arange(0, 20+2, 2)
UV_count = UV_count*100/n_total
fig, ax = plt.subplots(figsize=(9, 7))
plt.xticks(np.append(X, inputs["UV maximum"]-1)-0.5,
           np.append(UV_list, inputs["UV maximum"]),
           fontsize=font_size)
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
#plt.savefig(inputs["path graphics"]+"Histogram_UVI.png", dpi=400)
plt.show()
plt.clf()
