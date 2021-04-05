from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from os import listdir
inputs = {
    "year initial": 2000,
    "year final": 2019,
    "path data": "../Archivos/",
    "file data": "Max_Monthly_Ery.csv",
}
years = np.arange(inputs["year initial"],
                  inputs["year final"]+1)
X = np.arange(0,
              (inputs["year final"]-inputs["year initial"]+1)*12,
              12)
X1 = np.arange(0,
               12*(inputs["year final"]-inputs["year initial"]+1))
maxi = np.zeros(12)
mini = np.zeros(12)+1000

data = pd.read_csv(inputs["path data"]+inputs["file data"])
data["Max Data"] = data["Max Data"]*40
data["std"] = data["std"]*40
# <-----------------Linear fit---------------------->
fit = np.polyfit(data.index, data["Max Data"], 1)
print(fit)
fit = np.poly1d(fit)
pd2 = fit(data.index)
# <------------Moving average para 6 meses------------->
data["SMA_6"] = data.iloc[:, 1].rolling(window=12).mean()
# <--------------------Inicio de la grafica UVyearlyError----------------------------------->
plt.xticks(X, years,
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
plt.plot(list(data["Date"]), list(data["SMA_6"]),
         label="Moving average",
         linewidth=3,
         color="grey")
# <-----------Ploteo de linear fit------------------>
plt.plot(list(data.index), pd2,
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
plt.show()
#plt.savefig("../Graficas/UVyearlyError.png", dpi=300)
plt.clf()
mean_y = np.zeros([20, 2])
# for i in data.index:
#     year = int(UVmax[i, 0]/12)
#     mean_y[year, 0] += UVmax[i, 1]
#     mean_y[year, 1] += 1
# for year in range(20):
#     mean_y[year, 0] = mean_y[year, 0]/mean_y[year, 1]
# fit = np.polyfit(np.arange(20), mean_y[:, 0], 1)
# print(fit)
