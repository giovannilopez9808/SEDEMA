
import matplotlib.pyplot as pyplot
from functions import *
import numpy as np
import datetime


def read_data(path, name):
    data = np.loadtxt(inputs["path data"]+inputs["file data"],
                      usecols=np.arange(1, 21),
                      delimiter=",",
                      skiprows=1,
                      )
    data = np.transpose(data)
    return data


def define_yticks(ax, year_initial, year_final):
    years_number, years = obtain_yticks(year_initial, year_final)
    ax.set_yticks(years_number)
    ax.set_yticklabels(years)


def obtain_yticks(year_initial, year_final):
    years = np.arange(year_initial, year_final+1)
    years_number = years-year_initial-0.5
    return years_number, years


def define_xticks(ax):
    month_days, month_names = obtain_xticks()
    ax.set_xticks(month_days)
    ax.set_xticklabels(month_names)


def obtain_xticks():
    month_names = obtain_month_names()
    month_days = obtain_month_days()
    return month_days, month_names


def obtain_month_days():
    month_days = []
    for month in range(1, 13):
        day = (datetime.date(2019, month, 1) -
               datetime.date(2019, 1, 1)).days
        month_days.append(day)
    return month_days


inputs = {
    "path data": "../Archivos/",
    "file data": "O3_CDMX.csv",
    "path graphics": "../Graphics/",
    "graphic name": "O3",
    "map color": "viridis",
    "year initial": 2000,
    "year final": 2019
}
data = read_data(inputs["path data"],
                 inputs["file data"])
fig, ax = plt.subplots()
plt.subplots_adjust(top=0.922,
                    bottom=0.081,
                    left=0.023,
                    right=0.977,
                    hspace=0.2,
                    wspace=0.2)
plt.title("Period 2000-2019",
          fontsize="large")
define_xticks(ax)
define_yticks(ax,
              inputs["year initial"],
              inputs["year final"],)
ax.grid(linewidth=1,
        color="#000000",
        linestyle="--")
levels = np.arange(0,
                   150,
                   15)
map_data = ax.imshow(data,
                     cmap=inputs["map color"],
                     origin="lower",
                     vmin=0,
                     vmax=135
                     )
cbar = fig.colorbar(map_data,
                    values=np.delete(levels+7.5, -1),
                    ticks=levels,
                    )
cbar.ax.set_ylabel("O$_3$ (ppb)",
                   rotation=-90,
                   va="bottom",
                   fontsize="large")
cbar.set_ticklabels(np.array(levels, dtype=str))
forceAspect(ax,
            1)
# <---------Guardado de la grafica---------->
plt.savefig(inputs["path graphics"]+inputs["graphic name"],
            dpi=400)
