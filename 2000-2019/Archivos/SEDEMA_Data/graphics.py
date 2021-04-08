import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import os


def format_data(data, resize):
    data.index = pd.to_datetime(data["Dates"])
    data = data.drop(["Dates", "parameter", "unit"], 1)
    data["value"] = data["value"]*resize*40
    return data


inputs = {
    "path data": "Radiation/",
    "path stations": "../../Stations/",
    "radiation": "UVB",
    "size": 0.0583,
    "year": "2019",
    "day initial": "2019-12-01",
    "day final": "2019-12-31"
}
colors = [(0, 0, 0),
          (152/255, 196/255, 8/255),
          (36/255, 113/255, 163/255),
          (1, 244/255, 0),
          #(1, 211/255, 0),
          (246/255, 174/255, 0),
          (239/255, 131/255, 0),
          (232/255, 97/255, 5/255),
          (255/255, 34/255, 34/255),
          (230/255, 42/255, 20/255),
          (165/255, 0/255, 0/255),
          (118/255, 8/255, 104/255),
          (118/255, 46/255, 159/255),
          (150/255, 53/255, 188/255),
          (156/255, 92/255, 188/255),
          (184/255, 150/255, 235/255),
          (198/255, 198/255, 248/255)]
file = inputs["radiation"]+"_"+inputs["year"]+".csv"
stations = sorted(os.listdir(inputs["path stations"]))
data = pd.read_csv(inputs["path data"]+file)
data = format_data(data,
                   inputs["size"])
index = data.resample("D").max()
daily_max = pd.DataFrame(columns=stations,
                         index=index.index)
for station in stations:
    data_max = data[data["cve_station"] == station]
    data_max = data_max.resample("D").max()
    daily_max[station] = data_max["value"]
data_max = daily_max[daily_max.index <= inputs["day final"]]
data_max = data_max[data_max.index >= inputs["day initial"]]
for station, color in zip(stations, colors):
    data = data_max[station]
    if data.count() != 0:
        plt.plot(data,
                 label=station,
                 ls="--",
                 marker="o",
                 color=color)
plt.legend(ncol=7,
           frameon=False,
           fontsize=9,
           bbox_to_anchor=(1.0, 1.05, 0.1, 0.1))
plt.ylim(2, 16)
plt.xlim(pd.to_datetime(inputs["day initial"]),
         pd.to_datetime(inputs["day final"]))
plt.yticks([i for i in range(2, 17)])
plt.grid(ls="--",
         color="#000000",
         alpha=0.5)
plt.xticks(rotation=60)
plt.subplots_adjust(top=0.881,
                    bottom=0.211,
                    left=0.066,
                    right=0.903,
                    hspace=0.2,
                    wspace=0.2)
plt.show()
