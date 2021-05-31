import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def read_data(path, file):
    # <-------------Lectura de los datos------------------>
    data = pd.read_csv("{}{}".format(path,
                                     file),
                       index_col=0)
    # <---------Erythemal a UVI-------------->
    data["Max"] = data["Max"]*40
    data["std"] = data["std"]*40
    data.index = pd.to_datetime(data.index)
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
    "path graphics": "../Graphics/",
    "path data": "../Archivos/",
    "file data": "Max_Monthly_UVB.csv",
    "Months moving Average": 3,
    "year initial": 2000,
    "year final": 2019,

}
data = read_data(inputs["path data"],
                 inputs["file data"])
# <------------Moving average------------->
moving_average_data = obtain_moving_average_monthly(data["Max"],
                                                    inputs["Months moving Average"])
data = cut_data(data,
                "2000-01-01",
                "2019-12-01",)
# <--------------Tendencia----------------->
yearly_mean = obtain_yearly_mean(data)
mean_data = yearly_mean.mean()
fit = np.polyfit(list(yearly_mean.index.year),
                 list(yearly_mean["Max"]), 1)

print("Parameter\tm\tMean\tTendency")
print("UVI:\t\t{:.2f}\t{:.1f}\t{:.1f}".format(fit[0],
                                              mean_data["Max"],
                                              fit[0]*100/mean_data["Max"]))

fit = np.poly1d(fit)
years = list(yearly_mean.index.year)
years.append(2020)
years = np.array(years)
Fit_line = fit(years)
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
plt.xlim(0,
         (inputs["year final"]-inputs["year initial"]+1)*12)
plt.ylim(0,
         16)
# # <------------Barras de error--------------->
plt.errorbar(range(len(data["Max"])),
             list(data["Max"]),
             yerr=data["std"],
             marker="o",
             linewidth=1,
             ls="None",
             alpha=0.8,
             color="black",
             capsize=5,
             markersize=2,
             label="Monthly average and SD")
# # <--------Ploteo del moving average para 3 meses----------->
plt.plot(range(len(moving_average_data)),
         list(moving_average_data),
         label="Moving average",
         linewidth=3,
         color="grey",
         alpha=0.9)
# # <-----------Ploteo de linear fit------------------>
plt.plot((years-inputs["year initial"])*12,
         Fit_line,
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
