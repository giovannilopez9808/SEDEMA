import numpy as np
import matplotlib.pyplot as plt
UVdata = np.loadtxt("../Archivos/MaxEry.2txt", usecols=[0, 1])
UVdata[:, 1] = UVdata[:, 1]*40
prom = np.zeros([20, 2])
x = np.arange(20)
for i in range(np.size(UVdata[:, 0])):
    year = int(UVdata[i, 0]/12)
    prom[year, 0] += UVdata[i, 1]
    prom[year, 1] += 1
for year in range(20):
    prom[year, 0] = prom[year, 0]/prom[year, 1]
fit = np.polyfit(x, prom[:, 0], 1)
fit = np.poly1d(fit)
print(fit)
pd = fit(x)
plt.subplots_adjust(left=0.097, right=0.977, bottom=0.171, top=0.957)
plt.ylim(6, 12)
plt.xlabel("Year")
plt.ylabel("UV Index")
plt.plot(x, prom[:, 0], label="Data", ls="--", color="black")
plt.scatter(x, prom[:, 0], c="black")
plt.plot(x, pd, label="Fit", color="red")
plt.xticks(x, x+2000, rotation="60")
plt.legend(frameon=False, ncol=2)
print(prom[:, 0].mean())
plt.show()
