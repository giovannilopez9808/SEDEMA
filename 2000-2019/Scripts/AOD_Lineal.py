import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
#<------------------------Funcion de la radiacion de cuerpo negro------------------>
def f(x,m):
    return m*x
year,aod=np.loadtxt("../Archivos/AOD.txt",skiprows=1,unpack=True)
print(np.mean(aod))
#pars,cov=curve_fit(f=f,xdata=year,ydata=aod,p0=[0])
pars=np.polyfit(np.arange(np.size(aod)),aod,1)
print(pars[0])
fit=f(year,pars[0])
plt.ylim(0,1)
plt.plot(year,aod)
plt.plot(year,fit)
plt.show()