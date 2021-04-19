import matplotlib.pyplot as plt
import numpy as np
import datetime
import os


class stations_object:
    def __init__(self, date):
        self.date = date
        self.stations = []
        self.colors = {
            "CHO": "Blue",
            "CUA": "#03071e",
            "CUT": "#83c5be",
            "FAC":  "#d00000",
            "HAN": "#b07d62",
            "LAA": "#f72585",
            "MER": "black",
            "MON": "Purple",
            "MPA": "#0096c7",
            "PED": "#f89edf",
            "SAG": "orange",
            "SFE": "Green",
            "TLA": "cyan",
        }

    def append_station(self, station):
        self.stations.append(station)

    def obtain_mean(self):
        data = []
        for station in self.stations:
            data.append(station.data)
        self.mean = np.zeros_like(data[0])
        for i, values in enumerate(np.transpose(data)):
            sum = np.sum(values[values != 0])
            count = np.count_nonzero(values)
            if count != 0:
                self.mean[i] = sum/count

    def obtain_ratio_each_station(self):
        for station in self.stations:
            station.obtain_ratio(self.mean)

    def plot_ratios(self, path, name):
        for station in self.stations:
            plt.plot(station.hour, station.ratio,
                     label=station.name,
                     c=self.colors[station.name],
                     marker=".",
                     ls="none",
                     ms=3,
                     alpha=0.7)
        # Leyenda del eje X
        plt.xlabel("Local time (h)")
        plt.title(self.date)
        # # Leyenda de las graficas
        plt.legend(ncol=5,
                   frameon=False,
                   fontsize=9,
                   markerscale=4,
                   bbox_to_anchor=(0.9, 1.05, 0, 0.1)
                   )
        plt.plot([7, 19], [1, 1], color="red", ls="--", lw=3)
        # Limites de la grafica en el eje X
        plt.xlim(7, 18)
        plt.ylim(0.6, 1.4)
        plt.yticks(np.arange(0.6, 1.6, 0.1))
        plt.xticks(np.arange(7, 19))
        plt.grid(ls="--",
                 color="#000000",
                 alpha=0.5)
        #plt.savefig(path+name+".png", dpi=400)
        plt.show()
        plt.clf()
        # plt.close()

    def plot_data(self):
        for station in self.stations:
            plt.plot(station.hour, station.data*40,
                     label=station.name,
                     c=self.colors[station.name],
                     marker=".",
                     ls="none",
                     ms=3,
                     alpha=0.7)
        plt.plot(station.hour, self.mean*40,
                 label="Hourly mean",
                 c="red",
                 marker=".",
                 ls="none",
                 ms=3,
                 alpha=0.7)
        # Leyenda del eje X
        plt.xlabel("Local time (h)")
        plt.title(self.date)
        # # Leyenda de las graficas
        plt.legend(ncol=5,
                   frameon=False,
                   fontsize=9,
                   markerscale=4,
                   bbox_to_anchor=(0.9, 1.05, 0, 0.1)
                   )
        # Limites de la grafica en el eje X
        plt.xlim(7, 18)
        plt.ylim(0, 16)
        plt.yticks(np.arange(0, 17))
        plt.xticks(np.arange(7, 19))
        plt.grid(ls="--",
                 color="#000000",
                 alpha=0.5)
        #plt.savefig(path+name+".png", dpi=400)
        plt.show()
        plt.clf()


class station_object:
    def __init__(self, hour, data, name):
        self.hour = hour
        self.data = data
        self.name = name

    def obtain_ratio(self, mean):
        self.ratio = self.data[self.data != 0]/mean[self.data != 0]
        self.hour = self.hour[self.data != 0]


def yymmdd2date(date):
    year = int("20"+date[0:2])
    month = int(date[2:4])
    day = int(date[4:6])
    date = str(datetime.date(year, month, day))
    return date


inputs = {
    "path stations": "../../Stations/",
    "path data days": "../../Stations/MON/",
    "path measurements": "/Mediciones/",
    "path graphics": "../../Graphics/Days/",
    "file data days": "days_select.txt",
    "wavelength": "Ery",
}
stations = sorted(os.listdir(inputs["path stations"]))
# dates = np.loadtxt(inputs["path data days"] +
#                    inputs["file data days"],
#                    dtype=str)
dates = [
    "170123",
    "171113",
    "171127",
    "180107",
]
for date in dates:
    date_title = yymmdd2date(date)
    stations_list = stations_object(date_title)
    for station in stations:
        path = inputs["path stations"]+station+inputs["path measurements"]
        hour, data = np.loadtxt(path+date+inputs["wavelength"]+".csv",
                                delimiter=",",
                                unpack=True)
        if(data.mean() != 0):
            station_data = station_object(hour,
                                          data,
                                          station,
                                          )
            stations_list.append_station(station_data)
    stations_list.obtain_mean()
    stations_list.plot_data()
    stations_list.obtain_ratio_each_station()
    stations_list.plot_ratios(inputs["path graphics"],
                              date_title)
