import numpy as np


dir_data = "../../Archivos/"
ver = "UVB"
file = ver+".csv"
file_final = ver+"_clean.csv"
data_list = np.loadtxt(dir_data+file, delimiter=",", dtype=str)
file_clean = open(dir_data+file_final, "w")
n, m = np.shape(data_list)
for data in data_list:
    for j in range(m):
        if data[j] == "":
            data[j] = "0.0"
        if j != m-1:
            file_clean.write(data[j]+",")
        else:
            file_clean.write(data[j]+"\n")
file_clean.close()
