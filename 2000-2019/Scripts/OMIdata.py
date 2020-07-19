import h5py 
from os import listdir
import numpy as np
car="../Data/"
lon=83
alt=[109,110]
files=listdir(car)
yy="00"
f=open("../Archivos/UVI-OMI.txt","w")
for file in files:
    c=car+file
    year=file[21:23]
    if year!=yy:
        print("Calculando año 20"+year)
        yy=year
    date=year+file[24:28]
    HD5=h5py.File(c,"r")
    data=list(HD5["HDFEOS/GRIDS/OMI UVB Product/Data Fields/CSUVindex"])
    UVI=0
    n=0
    for i in alt:
        OMI=data[i][lon]
        if  OMI>0:
            UVI+=data[i][lon]
            n+=1
    if n!=0:
        UVI=UVI/n
    f.write(date+" "+str(round(UVI,2))+"\n")
f.close()