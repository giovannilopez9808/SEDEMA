import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
UV_min=1
UV_max=12
color=["green","lime","aquamarine","cyan","skyblue","royalblue","indigo"
,"violet","lightcoral","maroon","red"]
d_UV=UV_max-UV_min
day=["2017-01-04","2018-05-27"]
def Dosis(d_UV,inv,d,day):
    MED=200
    t=inv[:,0]
    y=inv[:,1]
    UVData=inv[:,1]*40
    for i in range(d_UV):
        n=np.where(UVData>=i+1)[0]
        if np.size(n)!=0:
            TEM,yes=0,0
            n1=n2=n[0]
            while yes==0:
                TEM+=y[n2]*60
                if TEM>=MED:
                    n2+=-1
                    yes=1
                else: n2+=1
            plt.fill_between(t[n1:n2],y[n1:n2],label="UV="+str(i+1),alpha=0.4,color=mcolors.to_rgb(color[i]))
            TEM,yes=0,0
            n2=n1=n[np.size(n)-1]
            while yes==0:
                TEM+=y[n2]*60
                if TEM>=MED:
                    yes=1
                    n2+=1
                else: n2+=-1
            plt.fill_between(t[n2:n1],y[n2:n1],alpha=0.4,color=mcolors.to_rgb(color[i]))
    plt.legend(ncol=7,loc=9,frameon=False,fontsize="xx-small")
    plt.ylim(0,0.35)
    plt.ylabel("Solar Erythemal irradince (W/m$^2$)")
    plt.xlabel("Local time (h)")
    plt.title("Day "+day[d])
    plt.xlim(6,20)
    plt.savefig("../fig"+str(d)+".png")
    plt.clf()
inv=np.loadtxt("170104Eryme.txt")
ver=np.loadtxt("180527Eryme.txt")
Dosis(d_UV,inv,0,day)
Dosis(d_UV,ver,1,day)