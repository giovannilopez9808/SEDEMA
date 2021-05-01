import matplotlib.pyplot as plt
import pandas as pd
import datetime


def obtain_index(year_i, year_f):
    index = []
    days = (datetime.date(year_f, 12, 31)-datetime.date(year_i, 1, 1)).days
    for day in range(days+1):
        date = datetime.date(year_i, 1, 1)+datetime.timedelta(days=day)
        index.append(str(date))
    return index


def obtain_xticks(year_i, year_f):
    dates = []
    years = []
    for year in range(year_i, year_f+1):
        years.append(year)
        date = datetime.date(year, 1, 1)
        dates.append(str(date))
    return dates, years


inputs = {
    "path data": "../Archivos/",
    "file data": "AOD_CDMX.csv",
    "year initial": 2000,
    "year final": 2019,
}
data = pd.read_csv(inputs["path data"]+inputs["file data"],
                   index_col=0)
index = obtain_index(inputs["year initial"],
                     inputs["year final"])
data_plain = pd.DataFrame(index=index,
                          columns=["Data"],)
for year in data.columns:
    for date in data.index:
        index = str(year)+"-"+date
        value = data[year][date]
        data_plain["Data"][index] = value
plt.subplots(figsize=(8, 5))
plt.scatter(data_plain.index,
            list(data_plain["Data"]),
            alpha=0.5,
            label="AOD$_{500nm}$")
dates, years = obtain_xticks(inputs["year initial"],
                             inputs["year final"])
plt.xticks(dates, years,
           rotation=60,)
plt.xlim(dates[0],
         str(datetime.date(inputs["year final"], 12, 31)))
plt.ylim(0,)
plt.grid(ls="--",
         color="#000000",
         alpha=0.5)
plt.subplots_adjust(top=0.97,
                    bottom=0.124,
                    left=0.086,
                    right=0.981,
                    hspace=0.2,
                    wspace=0.2
                    )
plt.ylabel("AOD$_{500nm}$")
plt.show()
