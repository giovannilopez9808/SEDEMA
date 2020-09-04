import numpy as np
import matplotlib.pyplot as plt
x=np.arange(0,10,0.1)
y=x**2
y2=x**3
plt.plot(x,y,label="fffff")
plt.plot(x,y2,label="yyyyy")
plt.legend(frameon=False,ncol=2,loc=2,bbox_to_anchor=(0., 1.05,1,0.02),borderaxespad=0,mode="expand")
plt.show()