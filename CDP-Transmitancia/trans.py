import numpy as np
import matplotlib.pyplot as plt

def calc(arc,col,pos,text,title):
    min,max=436,488
    data=np.loadtxt(arc+".txt",usecols=col,skiprows=min,max_rows=max)
    lon=np.loadtxt(arc+".txt",usecols=0,skiprows=min,max_rows=max)
    p=[data[:,pos[0]]/data[:,pos[1]],data[:,pos[2]]/data[:,pos[3]]]
    dp,f,b,dfx=np.zeros(2),np.zeros([2,2]),np.zeros(2),np.zeros([max-1,2])
    for j in range(2):
        dp[j]=(p[j][max-1]-p[j][0])/(lon[max-1]-lon[0])
        for i in range(max-1):
            dfx[i,1]=(p[j][i+1]-p[j][i])/(lon[i+1]-lon[i])
            dfx[i,0]=lon[i]
        for i in range(max):
            if f[j,1]<p[j][i] and abs(lon[i]-365)<=5:
                f[j,1]=p[j][i]
                f[j,0]=lon[i]
        b[j]=f[j,1]-dp[j]*f[j,0]
    print(f[:,1])
    print(round(f[:,1].mean(),3))
    plt.subplots_adjust(left=0.073,right=0.957,bottom=0.155,top=0.926)
    plt.ylim(0,1)
    plt.grid(ls="--",color="black")
    plt.title(title)
    plt.xlabel("Wavelength (nm)")
    plt.yticks(np.arange(0,1+0.1,0.1))
    plt.xticks(np.arange(320,400+5,5),rotation=60)
    plt.xlim(320,400)
    plt.scatter(lon,p[0][:],marker=".",label=text[0])
    plt.scatter(lon,p[1][:],marker=".",label=text[1])
    plt.legend(ncol=4,frameon=False)
    plt.savefig(title+".png")
    plt.clf()

calc("Cabina1",[1,2,3,4,5,6],[3,1,5,1],["12:12/12:09","12:19/12:09"],"Cabina A")
calc("Cabina2",[1,2,3,4,5],[3,0,4,0],["11:58/11:53","12:04/11:53"],"Cabina B")
calc("Cabina3",[1,2,3,4,5,6],[0,3,1,5],["11:27/11:24","11:38/11:36"],"Cabina C")
calc("Cabina4",[1,2,3,4,5,6],[0,3,1,4],["10:43/10:40","10:48/10:46"],"Cabina D")