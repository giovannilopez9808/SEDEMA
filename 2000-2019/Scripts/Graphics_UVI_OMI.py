from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime


def forceAspect(ax, aspect):
    im = ax.get_images()
    extent = im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)


def obtain_month_names():
    names = []
    for i in range(1, 13):
        date = datetime.date(2000, i, 1)
        names.append(date.strftime("%B"))
    return names


numyear = ["2005",
           "",
           "",
           "2008",
           "",
           "",
           "",
           "2012",
           "",
           "",
           "",
           "2016",
           "",
           "",
           "2019"]
inputs = {
    "path data": "../Archivos/",
    "column": "CSUVindex",
    "year initial": 2005,
    "year final": 2019,
}
month_days = np.arange(0, 365, 30.2)
month_names = obtain_month_names()
UVI_map = np.zeros((inputs["year final"]-inputs["year initial"]+1,
                    365))
data = pd.read_csv(inputs["path data"]+"UVI_"+inputs["column"]+"_clean.csv",
                   index_col=0)
data.index = pd.to_datetime(data.index)
data_mean = data.resample("MS").mean()
for year in range(inputs["year initial"], inputs["year final"]+1):
    year_i = year-inputs["year initial"]
    for day in range(365):
        date = datetime.date(year, 1, 1)+datetime.timedelta(days=day)
        try:
            value = (data[inputs["column"]][str(date)]).mean()
            UVI_map[year_i, day] = value
        except:
            month = date.month
            date = datetime.date(year, month, 1)
            value = data_mean[inputs["column"]][str(date)]
            #UVI_map[year_i, day] = value
colors = [(1, 1, 1),
          (58/255, 156/255, 43/255),
          (152/255, 196/255, 8/255),
          (1, 244/255, 0),
          (1, 211/255, 0),
          (246 / 255, 174/255, 0),
          (239/255, 131/255, 0),
          (232/255, 97/255, 5/255),
          (255/255, 34/255, 34/255),
          (230/255, 42/255, 20/255),
          (165/255, 0/255, 0/255),
          (118/255, 46/255, 159/255),
          (150/255, 53/255, 188/255),
          (184/255, 150/255, 235/255),
          (198/255, 198/255, 248/255)]
n_bin = 16
font_size = 12
cmap_name = "UV_Index"
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
print("Graficando UV Index")
fig, ax = plt.subplots(1, 1)
plt.subplots_adjust(left=0.094,
                    right=0.977,
                    bottom=0.205,
                    top=0.89)
ax.set_ylim(0, 14)
ax.set_yticks(np.arange(np.size(numyear)))
ax.set_yticklabels(numyear,
                   fontsize=font_size)
ax.set_xticks(month_days)
ax.set_xticklabels(month_names,
                   rotation=60,
                   fontsize=font_size)
map = ax.imshow(UVI_map,
                cmap=cm,
                vmin=0,
                vmax=15,
                origin="lower")
ax.grid(linewidth=1,
        color="black",
        linestyle="--")
forceAspect(ax, 1.5)
cbar = fig.colorbar(map, ticks=np.arange(0, 16, 1))
cbar.ax.set_ylabel("UV Index",
                   rotation=-90,
                   va="bottom",
                   fontsize=11)
ax.set_title("UV Index satellite-derived in Mexico City \n Period 2005-2019")
plt.show()
#plt.savefig("../Graficas/UVI-OMI.png", dpi=300)
