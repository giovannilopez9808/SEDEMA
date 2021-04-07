from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from os import listdir
import pandas as pd
import numpy as np
import datetime
inputs = {
    "year initial": 2000,
    "year final": 2019,
    "path data": "../Archivos/",
    "path graphics": "../Graphics/",
    "file data": "Max_Monthly_Ery.csv",
}
years = np.arange(inputs["year initial"],
                  inputs["year final"]+1)
X = years-inputs["year initial"]
# <-------------Lectura de los datos------------------>
data = pd.read_csv(inputs["path data"]+inputs["file data"])
# <---------Erythemal a UVI-------------->
data["Max Data"] = data["Max Data"]*40
data["std"] = data["std"]*40
# <------------Moving average------------->
data["SMA"] = data.iloc[:, 1].rolling(window=3).mean()
# <--------------Tendencia----------------->
data.index = pd.to_datetime(data["Date"])
yearly_mean = data["Max Data"].resample("YS").mean()
mean_data = yearly_mean.mean()
fit = np.polyfit(X,
                 list(yearly_mean), 1)

print("Parameter\tm\tMean\tTendency")
print("UVI:\t   \t{:.2f}\t{:.1f}\t{:.1f}".format(
    fit[0], mean_data, fit[0]*100/mean_data))

fit = np.poly1d(fit)
pd2 = fit(np.append(X, 20))
# <--------------------Inicio de la grafica UVyearlyError----------------------------------->
plt.xticks(X*12, years,
           rotation=60,
           fontsize=12)
plt.yticks(fontsize=12)
plt.title("Period 2000-2019",
          fontsize="large")
plt.ylabel("UV Index",
           fontsize="large")
plt.xlim(0, 20*12)
plt.ylim(0, 16)
# <------------Barras de error--------------->
plt.errorbar(list(data["Date"]), list(data["Max Data"]),
             yerr=data["std"],
             marker="o",
             linewidth=1,
             ls="--",
             alpha=0.6,
             color="black",
             capsize=5,
             markersize=2,
             label="Monthly average and SD")
# <--------Ploteo del moving average para 3 meses----------->
plt.plot(list(data["Date"]), list(data["SMA"]),
         label="Moving average",
         linewidth=3,
         color="grey")
# <-----------Ploteo de linear fit------------------>
plt.plot(np.append(X, 20)*12, pd2,
         label="Linear fit",
         color="red",
         linewidth=3)
plt.subplots_adjust(left=0.102,
                    right=0.979,
                    bottom=0.16,
                    top=0.917)
plt.legend(ncol=3,
           mode="expand",
           frameon=False,
           fontsize="small")
# <---------------Guardado de la grafica-------------->
plt.savefig(inputs["path graphics"]+"UV_Moving_Average.png",
            dpi=400)
