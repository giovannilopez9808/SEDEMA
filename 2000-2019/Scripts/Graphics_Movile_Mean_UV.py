from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from os import listdir
import pandas as pd
import numpy as np
import datetime


def read_data(path, file):
    # <-------------Lectura de los datos------------------>
    data = pd.read_csv("{}{}".format(path,
                                     file))
    # <---------Erythemal a UVI-------------->
    data["Max Data"] = data["Max Data"]*40
    data["std"] = data["std"]*40
    data.index = pd.to_datetime(data["Date"])
    data = data.drop("Date", 1)
    return data


def obtain_moving_average_monthly(data, month):
    return data.rolling(window=month).mean()


def cut_data(data, date_i, date_f):
    data = data[data.index >= date_i]
    data = data[data.index <= date_f]
    return data


def obtain_yearly_mean(data):
    return data.resample("Y").mean()


inputs = {
    "year initial": 2000,
    "year final": 2019,
    "path data": "../Archivos/",
    "path graphics": "../Graphics/",
    "file data": "Max_Monthly_Ery.csv",
}
data = read_data(inputs["path data"],
                 inputs["file data"])
# <------------Moving average------------->
moving_average_data = obtain_moving_average_monthly(data["Max Data"], 3)
print(data[data.index >= "2020-01-01"])
data = cut_data(data,
                "2000-01-01",
                "2019-12-01",)
print(data)
# <--------------Tendencia----------------->
yearly_mean = obtain_yearly_mean(data)
mean_data = yearly_mean.mean()
fit = np.polyfit(list(yearly_mean.index.year),
                 list(yearly_mean["Max Data"]), 1)

print("Parameter\tm\tMean\tTendency")
print("UVI:\t   \t{:.2f}\t{:.1f}\t{:.1f}".format(fit[0],
                                                 mean_data["Max Data"],
                                                 fit[0]*100/mean_data["Max Data"]))

fit = np.poly1d(fit)
years = list(yearly_mean.index.year)
years.append(2020)
years = np.array(years)
pd2 = fit(years)
# <-------Inicio de la grafica UVyearlyError-------->
plt.xticks((years-inputs["year initial"])*12,
           years,
           rotation=60,
           fontsize=12)
plt.yticks(fontsize=12)
plt.title("Period 2000-2019",
          fontsize="large")
plt.ylabel("UV Index",
           fontsize="large")
plt.xlim(0, 20*12)
plt.ylim(0, 16)
# # <------------Barras de error--------------->
plt.errorbar(range(data["Max Data"].count()), list(data["Max Data"]),
             yerr=data["std"],
             marker="o",
             linewidth=1,
             ls="--",
             alpha=0.6,
             color="black",
             capsize=5,
             markersize=2,
             label="Monthly average and SD")
# # <--------Ploteo del moving average para 3 meses----------->
plt.plot(range(moving_average_data.count()+2),
         list(moving_average_data),
         label="Moving average",
         linewidth=3,
         color="grey")
# # <-----------Ploteo de linear fit------------------>
plt.plot([i*12 for i in range(21)], pd2,
         label="Linear fit",
         color="red",
         linewidth=3)
plt.subplots_adjust(top=0.922,
                    bottom=0.147,
                    left=0.109,
                    right=0.948,
                    hspace=0.2,
                    wspace=0.2
                    )
plt.legend(ncol=3,
           mode="expand",
           frameon=False,
           fontsize="small")
# # <---------------Guardado de la grafica-------------->
plt.savefig("{}UV_Moving_Average.png".format(inputs["path graphics"]),
            dpi=400)
plt.show()
