import numpy as np
import datetime
import os


class TES:
    def __init__(self,
                 hour_i,
                 hour_f,
                 hour_lim,
                 dosis,
                 med,
                 cloud_factor,
                 filenames_dosis,
                 phototype_names,
                 tes_names,
                 data_folder):
        self.hour_i = hour_i
        self.hour_f = hour_f
        self.hour_lim = hour_lim
        self.dosis = dosis
        self.MED = med
        self.cloud_factor = cloud_factor
        self.filenames_dosis = filenames_dosis
        self.phototype_names = phototype_names
        self.tes_names = tes_names
        self.data_folder = data_folder
        self.init_system()

    def init_system(self):
        self.n_dosis = np.size(self.dosis)
        self.n_cloud = np.size(self.cloud_factor)
        self.n_MED = np.size(self.MED)
        self.hours = 60*(self.hour_f-self.hour_i)
        self.hour_max = 60*(self.hour_lim-self.hour_i)
        self.time_uva_mean_hourly = np.zeros(
            [self.hours, self.n_dosis, self.n_cloud, 2])
        self.time_uvb_mean_hourly = np.zeros(
            [self.hours, self.n_MED, self.n_cloud, 2])
        self.time_uva = np.zeros(
            [self.hours, 365, self.n_dosis, self.n_cloud, 2])
        self.time_uvb = np.zeros(
            [self.hours, 365, self.n_MED, self.n_cloud, 2])
        self.time_uvb_mean_monthly = np.zeros(
            [self.hours, 12, self.n_MED, self.n_cloud, 2])
        self.time_uva_mean_monthly = np.zeros(
            [self.hours, 12, self.n_dosis, self.n_cloud, 2])

    def calc_TES(self):
        for folder in self.data_folder:
            print("Analizando {}".format(folder))
            self.obtain_stations(folder)
            for station in self.stations:
                self.obtain_path_measurements(station)
                self.obtain_dates_from_data()
                for date in self.dates:
                    self.obtain_measurements_from_date(date)
                    self.obtain_date_from_name(date)
                    self.conse_day = date2consecutive_day(self.year,
                                                          self.month,
                                                          self.day)
                    for cloud, cloud_i in zip(self.cloud_factor, range(self.n_cloud)):
                        self.calc_TES_for_each_type(self.n_dosis,
                                                    self.dosis,
                                                    cloud_i,
                                                    cloud,
                                                    self.data_uva,
                                                    self.time_uva)
                        self.calc_TES_for_each_type(self.n_MED,
                                                    self.MED,
                                                    cloud_i,
                                                    cloud,
                                                    self.data_uvb,
                                                    self.time_uvb)
        for cloud_i in range(self.n_cloud):
            for hour in range(self.hours):
                for day in range(365):
                    self.obtain_mean_for_each_type(self.n_dosis,
                                                   cloud_i,
                                                   hour, day,
                                                   self.time_uva)
                    self.obtain_mean_for_each_type(self.n_MED,
                                                   cloud_i,
                                                   hour, day,
                                                   self.time_uvb)
        for cloud_i in range(self.n_cloud):
            self.obtain_monthly_mean_for_each_type(cloud_i,
                                                   self.n_dosis,
                                                   self.time_uva,
                                                   self.time_uva_mean_monthly)
            self.obtain_monthly_mean_for_each_type(cloud_i,
                                                   self.n_MED,
                                                   self.time_uvb,
                                                   self.time_uvb_mean_monthly)
            self.obtain_hourly_mean_for_each_type(cloud_i,
                                                  self.n_dosis,
                                                  self.time_uva,
                                                  self.time_uva_mean_hourly)
            self.obtain_hourly_mean_for_each_type(cloud_i,
                                                  self.n_MED,
                                                  self.time_uvb,
                                                  self.time_uvb_mean_hourly)
        for cloud_i in range(self.n_cloud):
            self.fill_data_from_lost_days(cloud_i,
                                          self.n_dosis,
                                          self.time_uva,
                                          self.time_uva_mean_monthly,
                                          self.time_uva_mean_hourly)
            self.fill_data_from_lost_days(cloud_i,
                                          self.n_MED,
                                          self.time_uvb,
                                          self.time_uvb_mean_monthly,
                                          self.time_uvb_mean_hourly)

    def obtain_stations(self, folder):
        if folder == "2016":
            self.dirstations = "../"+folder
            self.stations = [""]
        else:
            self.dirstations = "../"+folder+"/Stations/"
            self.stations = os.listdir(self.dirstations)

    def obtain_path_measurements(self, station):
        self.dir_data = self.dirstations+station+"/AOD500DM/"
        self.dir_med = self.dirstations+station+"/ResultadosTUV/"

    def obtain_dates_from_data(self):
        self.dates = np.loadtxt(self.dir_data+"datos.txt",
                                skiprows=1,
                                usecols=0,
                                dtype=str)

    def obtain_measurements_from_date(self, date):
        self.data_uva = np.loadtxt(self.dir_med+date+"UVAmo.txt",
                                   usecols=1,
                                   skiprows=self.hour_i*60, max_rows=self.hour_max)
        self.data_uvb = np.loadtxt(self.dir_med+date+"Erymo.txt",
                                   usecols=1,
                                   skiprows=self.hour_i*60, max_rows=self.hour_max)

    def obtain_date_from_name(self, name):
        self.day = int(name[4:6])
        self.month = int(name[2:4])
        self.year = int(name[0:2])

    def calc_TES_for_each_type(self, types, type_values, cloud_i, cloud_value, data, time):
        for type_i, type_value in zip(range(types), type_values):
            for hour in range(self.hours):
                self.calc_integral(type_i, type_value, hour,
                                   cloud_i, cloud_value, data, time)

    def calc_integral(self, type_i, type_value, hour, cloud_i, cloud_value, data, time):
        dosis_uva = 0
        i = hour
        while dosis_uva < type_value and i < self.hour_max-1:
            if data[i] != 0:
                dosis_uva += data[i]*60*cloud_value
            i += +1
        if dosis_uva != 0:
            if i < self.hour_max-1:
                min = i+1-hour
            else:
                min = self.hour_max-hour
            time[hour, self.conse_day, type_i, cloud_i, 0] += min
            time[hour, self.conse_day, type_i, cloud_i, 1] += 1

    def obtain_mean_for_each_type(self, type_n, cloud_i, hour, day, time):
        for type_i in range(type_n):
            data_count = time[hour, day, type_i, cloud_i, 1]
            if data_count != 0:
                data_sum = time[hour, day, type_i, cloud_i, 0]
                time[hour, day, type_i, cloud_i,
                     0] = data_sum // data_count + 1

    def obtain_monthly_mean_for_each_type(self, cloud_i, type_n, time, time_mean):
        for type_i in range(type_n):
            for hour in range(self.hours):
                for day in range(365):
                    month = obtain_month_from_consecutive_day(day)
                    time_day = time[hour, day, type_i, cloud_i, 0]
                    if time_day != 0:
                        time_mean[hour, month, type_i, cloud_i, 0] += time_day
                        time_mean[hour, month, type_i, cloud_i, 1] += 1
                for month in range(12):
                    data_sum = time_mean[hour, month, type_i, cloud_i, 0]
                    data_count = time_mean[hour, month, type_i, cloud_i, 1]
                    if data_count != 0:
                        time_mean[hour, month, type_i, cloud_i,
                                  0] = data_sum//data_count+1

    def obtain_hourly_mean_for_each_type(self, cloud_i, type_n, time, time_hourly):
        for type_i in range(type_n):
            for hour in range(self.hours):
                for day in range(365):
                    time_day = time[hour, day, type_i, cloud_i, 0]
                    if time_day != 0:
                        time_hourly[hour, type_i, cloud_i, 0] += time_day
                        time_hourly[hour, type_i, cloud_i, 1] += 1
                data_count = time_hourly[hour, type_i, cloud_i, 1]
                data_sum = time_hourly[hour, type_i, cloud_i, 0]
                time_hourly[hour, type_i, cloud_i, 0] = data_sum//data_count+1

    def fill_data_from_lost_days(self, cloud_i, type_n, time, time_mean, time_hourly):
        for type_i in range(type_n):
            for hour in range(self.hours):
                for day in range(365):
                    if time[hour, day, type_i, cloud_i, 0] == 0:
                        month = obtain_month_from_consecutive_day(day)
                        if time_mean[hour, month, type_i, cloud_i, 0] != 0:
                            time[hour, day, type_i, cloud_i,
                                 0] = time_mean[hour, month, type_i, cloud_i, 0]
                        else:
                            time[hour, day, type_i, cloud_i,
                                 0] = time_hourly[hour, type_i, cloud_i, 0]

    def write_results(self, path):
        self.write_results_for_each_type(path,
                                         self.tes_names[0],
                                         self.filenames_dosis,
                                         self.n_dosis,
                                         self.time_uva)
        self.write_results_for_each_type(path,
                                         self.tes_names[1],
                                         self.phototype_names,
                                         self.n_MED,
                                         self.time_uvb)

    def write_results_for_each_type(self, path, name, type_names, type_n, time):
        for type_i, type_name in zip(range(type_n), type_names):
            for cloud_i in range(self.n_cloud):
                cloud_name = str(cloud_i)
                file = open(path+name+"_"+type_name+"_"+cloud_name+".csv", "w")
                file.write("Hour")
                for day in range(365):
                    date = consecutive_day2date(day)
                    header = self.mm_dd_format(date)
                    file.write(","+header)
                file.write("\n")
                for hour in range(self.hours):
                    hour_index = self.hh_mm_format(hour)
                    file.write(hour_index)
                    for day in range(365):
                        time_day_hour = time[hour, day, type_i, cloud_i, 0]
                        file.write(",{:.2f}".format(time_day_hour))
                    file.write("\n")
                file.close()

    def hh_mm_format(self, minute):
        hour = self.hour_i+minute//60
        minute = minute-(minute//60)*60
        hour = self.header_file_format(hour)
        minute = self.header_file_format(minute)
        return hour+":"+minute

    def mm_dd_format(self, date):
        month = self.header_file_format(date.month)
        day = self.header_file_format(date.day)
        return month+"-"+day

    def header_file_format(self, number):
        number = str(number).zfill(2)
        return number


def date2consecutive_day(year, month, day):
    """
    Funcion para obtener el dia consecutivo a partir de una fecha
    """
    num = (datetime.date(year, month, day)-datetime.date(year, 1, 1)).days
    if num > 364:
        num = num-1
    return num


def obtain_month_from_consecutive_day(day):
    """
    Funcion para obtener el numero de mes de una fecha en dias consecutivos
    """
    date = consecutive_day2date(day)
    month = date.month-1
    return month


def consecutive_day2date(day):
    """
    Funcion para obtener la fecha a partir del dia consecutivo
    """
    date = datetime.date(2019, 1, 1)+datetime.timedelta(day)
    return date
