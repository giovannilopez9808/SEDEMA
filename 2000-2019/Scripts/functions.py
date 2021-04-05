import datetime
import locale
import os


def mkdir(name, path=""):
    try:
        os.mkdir(path+name)
    except FileExistsError:
        pass


def obtain_month_names():
    names = []
    for i in range(1, 13):
        date = datetime.date(2000, i, 1)
        names.append(date.strftime("%B"))
    return names


def obtain_date_and_hour(date):
    hour = int(date[11:13])
    day = int(date[0:2])
    month = int(date[3:5])
    year = int(date[6:10])
    date = datetime.date(year, month, day)
    return date, hour


def obtain_day_consecutive(date):
    conseday = (date-datetime.date(date.year, 1, 1)).days
    if conseday > 364:
        conseday = 364
    return conseday


def conseday_to_date(conseday, year):
    date = datetime.date(year, 1, 1)+datetime.timedelta(days=conseday)
    return date


def date_formtat_mmdd(date):
    date = date.strftime("%m-%d")
    return date


def find_location(name, data_list):
    for loc, elements in enumerate(data_list):
        if name == elements:
            return loc


def date2yymmdd(date):
    year, month, day = str(date).split("-")
    year = year[2:4]
    return year+month+day


def obtain_date_from_filename(name):
    year = int("20"+name[0:2])
    month = int(name[2:4])
    day = int(name[4:6])
    date = datetime.date(year, month, day)
    return date


def forceAspect(ax, aspect):
    im = ax.get_images()
    extent = im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)
