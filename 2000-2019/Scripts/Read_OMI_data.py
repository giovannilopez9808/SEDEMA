import matplotlib.pyplot as plt
import pandas as pd


def date_format(data):
    data["Date"] = data["Datetime"].str[0:4]+"-" + \
        data["Datetime"].str[4:6]+"-"+data["Datetime"].str[6:8]
    data["Date"] = pd.to_datetime(data["Date"])
    data.index = data["Date"]
    data = data.drop(["Date", "Datetime"], 1)
    return data


def clean_data(data, columns):
    for column in data.columns:
        if not column in columns:
            data = data.drop(column, 1)
    return data


def obtain_data_in_period(data, date_i, date_f):
    data = data[data.index >= date_i]
    data = data[data.index <= date_f]
    return data


def drop_data_useless(data, columns, limit):
    for column in columns:
        data = data[data[column] < limit]
    return data


def plot_data(data, column, date_initial, date_final):
    plt.subplots(figsize=(10, 4))
    plt.ylabel(column)
    dates, xtick = obtain_xticks(date_initial,
                                 date_final)
    plt.xlim(pd.to_datetime(date_initial),
             pd.to_datetime(date_final))
    plt.xticks(dates, xtick)
    plt.ylim(7, 18)
    plt.yticks([ytick for ytick in range(7, 19)])
    plt.scatter(data.index, data)
    plt.grid(ls="--",
             color="#000000",
             alpha=0.5)
    plt.show()


def obtain_xticks(date_initial, date_final):
    year_i = int(date_initial[0:4])
    year_f = int(date_final[0:4])
    xtick = []
    dates = []
    for year in range(year_i, year_f+2):
        xtick.append(year)
        dates.append(pd.to_datetime("{}-01-01".format(year)))
    return dates, xtick


inputs = {
    "path data": "../Archivos/",
    "file data": "Data_OMI_",
    "product": "OMUVB",
    "skiprows": 50,
    "UVI limit": 18,
    "UVIcolumns": ["CSUVindex", "UVindex"],
    "file results": "UVI_",
    "day initial": "2005-01-01",
    "day final": "2019-12-31",
}
data = pd.read_fwf(inputs["path data"]+inputs["file data"]+inputs["product"]+".dat",
                   skiprows=inputs["skiprows"])
data = date_format(data)
data = clean_data(data,
                  inputs["UVIcolumns"])
data = obtain_data_in_period(data,
                             inputs["day initial"],
                             inputs["day final"])
data = drop_data_useless(data,
                         inputs["UVIcolumns"],
                         inputs["UVI limit"])
for uvicolumn in inputs["UVIcolumns"]:
    print("Creando archivo {}".format(uvicolumn))
    data_UVI = data[uvicolumn]
    plot_data(data_UVI,
              uvicolumn,
              inputs["day initial"],
              inputs["day final"])
    data_UVI.to_csv("{}{}{}.csv".format(inputs["path data"],
                                        inputs["file results"],
                                        uvicolumn),
                    float_format='%.4f')
