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


def plot_grid(UV_max, percentage_limit):
    even = np.arange(0, percentage_limit+2, 2)
    odd = even-1
    for i in range(np.size(even)):
        plt.plot([-4,  UV_max+1],
                 [even[i], even[i]],
                 color="black",
                 ls="--",
                 alpha=0.5)
        plt.plot([-4, UV_max+1],
                 [odd[i], odd[i]],
                 color="gray",
                 ls="--",
                 alpha=0.3)


def obtain_xticks(UV_values):
    return np.append(UV_values, UV_values[-1]+1)


def obtain_yticks(percentage_limit):
    return np.arange(0, percentage_limit+2, 2)


def autolabel(rects):
    """Attach a text UV_values above each bar in *rects*, displaying its height."""
    for i, rect in enumerate(rects):
        height = rect.get_height()
        ax.annotate("{:.2f}".format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center',
                    va='bottom',
                    fontsize=9)


inputs = {
    "path data": "../Archivos/SEDEMA_Data/Radiation/",
    "path graphics": "../Graphics/",
    "wavelength": {  # "UVA": 10,
        "UVB": 0.0583, },
    "hour initial": 11,
    "hour final": 16,
    "UV minium": 1,
    "UV maximum": 16,
    "Percentage limit": 20,
}
UV_count = np.zeros(inputs["UV maximum"]-inputs["UV minium"])
UV_values = np.arange(inputs["UV minium"],
                      inputs["UV maximum"])
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
UV_count = UV_count*100/n_total
fig, ax = plt.subplots(figsize=(9, 7))
plt.ylim(0, 20)
plt.xlim(-1, inputs["UV maximum"]+1)
plt.xlabel("Daily maximums UV Index", fontsize=font_size)
plt.ylabel("Frequency (%) of Days", fontsize=font_size)
plt.title("Period 2000-2019", fontsize=font_size)
rects = ax.bar(UV_values, UV_count,
               color="#00838a",
               width=1,
               edgecolor="black")
autolabel(rects)
plot_grid(inputs["UV maximum"],
          inputs["Percentage limit"])
xticks = obtain_xticks(UV_values)
yticks = obtain_yticks(inputs["Percentage limit"])
plt.xticks(xticks-0.5,
           xticks,
           fontsize=font_size)
plt.yticks(yticks,
           fontsize=font_size)
# <--------Guardado de la grafica-------------->
plt.subplots_adjust(left=0.102,
                    bottom=0.093,
                    right=0.962,
                    top=0.936)
plt.savefig("{}Histogram.png".format(inputs["path graphics"]),
            dpi=400)
plt.show()
