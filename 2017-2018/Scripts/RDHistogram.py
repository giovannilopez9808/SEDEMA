import numpy as np
import matplotlib.pyplot as plt
sta=["CHO","CUT","MER","MON","MPA","PED","SAG","SFE","TLA"]
lon=["UVA","Erythemal"]
AOD=["/AOD500DM/","/AOD340DM/"]
aodtitle=["AOD 500nm","AOD 340nm"]
n=["500","340"]
irra=["UVA","Ery"]
for _j in range(2):
    DR=np.zeros([4,np.size(sta)])
    Ratio=np.zeros([4,np.size(sta)])
    for _i in range(np.size(sta)):
        car="../"+sta[_i]+AOD[_j]+"v0.0/"
        DR[:,_i]=np.loadtxt(car+"DR Anual.txt",usecols=4)
        Ratio[:,_i]=np.loadtxt(car+"Ratios Anual.txt",usecols=4)
    num=np.arange(9)
    for _i in range(2):
        fig, ax = plt.subplots(figsize=(9,7))
        x = np.arange(len(sta))  # the label locations
        width =0.5  # the width of the bars
        plt.ylabel("Annual mean "+lon[_i]+" (%)RD")
        rects1=ax.bar(x-width/2,DR[_i,:],width,label='2017'
                      ,facecolor="purple")
        rects2=ax.bar(x+width/2,DR[_i+2,:],width,label='2018'
                      ,facecolor="green")
        plt.legend(fontsize=15,frameon=False)
        plt.title(aodtitle[_j])
        plt.ylim(0,40)
        plt.xlabel("Station")
        plt.xticks(num,sta)
        def autolabel(rects):
            for rect in rects:
                height =round(rect.get_height(),2)
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0,3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom',)
        
        
        autolabel(rects1)
        autolabel(rects2)
        plt.savefig("../BarGraphics/"+irra[_i]+n[_j]+"DR.png")
        plt.clf()
    for _i in range(2):
        fig, ax = plt.subplots(figsize=(9,7))
        x = np.arange(len(sta))  # the label locations
        width =0.5  # the width of the bars
        plt.ylabel("Annual mean "+lon[_i]+" Ratio")
        rects1=ax.bar(x-width/2,Ratio[_i,:],width,label='2017',facecolor="purple")
        rects2=ax.bar(x+width/2,Ratio[_i+2,:],width,label='2018',facecolor="green")
        plt.legend(fontsize=15,frameon=False)
        plt.title(aodtitle[_j])
        plt.ylim(0.8,1.4)
        plt.xlabel("Station")
        plt.xticks(num,sta)
        def autolabel(rects):
            for rect in rects:
                height =round(rect.get_height(),2)
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0,3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom',)
        
        
        autolabel(rects1)
        autolabel(rects2)
        plt.savefig("../BarGraphics/"+irra[_i]+n[_j]+"Ratio.png")
        plt.clf()