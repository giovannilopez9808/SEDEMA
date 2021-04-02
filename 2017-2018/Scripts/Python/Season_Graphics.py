import numpy as np
import matplotlib.pyplot as plt
import os
colors = ["Blue",
          "Green",
          "black",
          "purple",
          "pink",
          "#f89edf",
          "orange",
          "Green",
          "cyan"]

dates = ["180420",
         "170623",
         "171113",
         "180202"]

titles = ["20 April 2018",
          "13 June 2017",
          "13 November 2017",
          "02 February 2018"]
dir_stations = "../../Stations/"
stations = sorted(os.listdir(dir_stations))
fig, axs = plt.subplots(2, 2,
                        figsize=(12, 9))
font_size = 13
axs = np.reshape(axs, 4)
for date, title, ax in zip(dates, titles, axs):
    if ax in [axs[0], axs[2]]:
        ax.set_ylabel("UV Index",
                      fontsize=font_size)
    if ax in [axs[2], axs[-1]]:
        ax.set_xlabel("CST (UTC - 6h)",
                      fontsize=font_size)
    ax.set_title(title,
                 fontsize=font_size)
    ax.set_ylim(0, 15)
    ax.set_yticks(np.arange(0, 15+3, 3))
    ax.set_xlim(6, 20)
    ax.set_xticks(np.arange(6, 19+2, 2))
    ax.tick_params(labelsize=font_size)
    for station, color in zip(stations, colors):
        car = dir_stations+station+"/Mediciones/"
        hour, data = np.loadtxt(car+date+"Ery.csv",
                                unpack=True,
                                delimiter=",")
        if(np.mean(data) != 0):
            data = data*40
            ax.plot(hour, data,
                    label=station,
                    c=color,
                    marker=".",
                    ls="none",
                    ms=3,
                    alpha=0.7)
    ax.legend(ncol=5,
              mode="expand",
              loc="upper center",
              markerscale=4,
              scatterpoints=1,
              frameon=False,
              fontsize=11)
plt.subplots_adjust(left=0.079,
                    bottom=0.09,
                    right=0.955,
                    top=0.921,
                    wspace=0.155,
                    hspace=0.2)
plt.savefig("../../Graficas/season.png", dpi=400)
