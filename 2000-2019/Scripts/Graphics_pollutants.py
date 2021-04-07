import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

inputs = {
    "CO": {
        "tick": "CO",
        "color": "purple",
        "title": "CO (ppm)",
        "lim sup": 4,
        "lim inf": 0,
        "delta": 1
    },
    "PM10": {
        "tick": "PM$_{10}$",
        "color": "#A25715",
        "title": "PM$_{10}$ ($\mu g/m^3$)",
        "lim sup": 75,
        "lim inf": 0,
        "delta": 15
    },
    "NO2": {
        "tick": "NO$_2$",
        "color": "blue",
        "title": "NO$_2$, SO$_2$ (ppb)",
        "lim sup": 50,
        "lim inf": 0,
        "delta": 10
    },
    "O3": {
        "tick": "O$_3$",
        "color": "green",
        "title": "O$_3$ (ppb)",
        "lim sup": 90,
        "lim inf": 50,
        "delta": 10
    },
    "AOD": {
        "tick": "AOD$_{340}$",
        "color": "#CB258C",
        "title": "AERONET AOD$_{340}$",
        "lim sup": 0.8,
        "lim inf": 0,
        "delta": 0.15
    },
    "SO2": {
        "tick": "SO$_{2}$",
        "color": "black",
        "title": "NO$_2$, SO$_2$ (ppb)",
        "lim sup": 50,
        "lim inf": 0,
        "delta": 10
    },
}
parameters = {
    "path data": "../Archivos/",
    "file data": "CDMX.csv",
    "path graphics": "../Graphics/",
    "linewidth": 4,
    "fontsize": 12
}
plt.rc('font', size=parameters["fontsize"])
plt.rc('xtick', labelsize=parameters["fontsize"])
plt.rc('ytick', labelsize=parameters["fontsize"]-1)
fig, (ax1, ax3, ax4) = plt.subplots(3,
                                    figsize=(9, 9),
                                    sharex=True)
plt.subplots_adjust(top=0.97,
                    bottom=0.1,
                    left=0.09,
                    right=0.9,
                    hspace=0.15)
ax2 = ax1.twinx()
ax5 = ax4.twinx()
axs = np.array([ax2, ax1, ax3, ax4, ax5, ax3])
print("Pollutant\t Mean\t  e\t  m\t   b")
for input, ax in zip(inputs, axs):
    tick = inputs[input]["tick"]
    color = inputs[input]["color"]
    title = inputs[input]["title"]
    lim_inf = inputs[input]["lim inf"]
    lim_sup = inputs[input]["lim sup"]
    delta = inputs[input]["delta"]
    label = np.arange(2000, 2020)
    x = np.arange(20)
    file = parameters["path data"]+input+"_"+parameters["file data"]
    data = pd.read_csv(file)
    if ax != ax5:
        mean = list(data.mean())
    else:
        x = list(data["Year"]-2000)
        label = list(data["Year"])
        mean = list(data["AOD 340nm"])
    fit = np.polyfit(x, mean, 1)
    prom = round(np.mean(mean), 3)
    print("{}\t\t {:.1f}\t {:.1f}\t {:.2f}\t {:.2f}".format(
        input, prom, fit[0]*100/prom, fit[0], fit[1]))
    ax.plot(label, mean,
            ls="-",
            label=tick,
            color=color,
            linewidth=parameters["linewidth"])
    ax.set_xlim(2000, 2019)
    ax.set_ylim(lim_inf, lim_sup)
    yticks = np.arange(lim_inf, lim_sup+delta, delta)
    ax.set_yticks(yticks)
    ax.set_xticks(label)
    ax.set_xticklabels(label,
                       rotation=60)
    if ax in [ax2, ax5]:
        ax.set_ylabel(title,
                      rotation=-90,
                      va="bottom")
    else:
        ax.set_ylabel(title)
    if ax in [ax1, ax4]:
        ax.legend(frameon=False,
                  ncol=2, loc="best",
                  bbox_to_anchor=(0.84, 1))
    else:
        ax.legend(frameon=False,
                  ncol=2,
                  loc="upper right")
#plt.savefig(parameters["path graphics"]+"pollutants.png", dpi=400)
plt.show()
