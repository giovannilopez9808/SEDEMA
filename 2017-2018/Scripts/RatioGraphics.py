#                           Fecha de creacion
#                             08 enero 2020
#                               Creador
#                       Giovanni Gamaliel López Padilla
#Este programa realiza la grafica de los ratios en la ruta estacion/AOD/Ratio/
import matplotlib.pyplot as plt
import numpy as np
#Nombre de las estaciones, esto sera usado para entrar a cada carpeta
#sta=["CHO","CUT","FAC","MER","MON","MPA","PED","SAG","SFE","TLA"]
sta=["CHO","CUT","MER","MON","MPA","PED","SAG","SFE","TLA"]
AOD="/AOD340nmv1/"
ver="v0.1/"
vermed="/Mediciones/"+ver
for _i in range(np.size(sta)):
    day=np.loadtxt("../"+sta[_i]+AOD+"datos340.txt",skiprows=1,usecols=0)
    ozono=np.loadtxt("../"+sta[_i]+AOD+"datos340.txt",skiprows=1,usecols=2)
    Rfile=open("../"+sta[_i]+AOD+ver+"Ratios Anual.txt","w")
    RDia=open("../"+sta[_i]+AOD+ver+"Ratios-Results.txt","w")
    Ranual=np.zeros([2,2,2])
    for _j in range(np.size(day)):
        Rdia=np.zeros([2,2])
        if ozono[_j]!=0:
            file=str(int(day[_j]))
            car="../"+sta[_i]
            print("Analizando el dia "+file+" de la estacion "+sta[_i])
            UVAme=np.loadtxt(car+vermed+file+"UVAme.txt",usecols=1,
                             skiprows=480,max_rows=660)
            Eryme=np.loadtxt(car+vermed+file+"Eryme.txt",usecols=1,
                             skiprows=480,max_rows=660)
            UVAmeh=np.loadtxt(car+vermed+file+"UVAme.txt",usecols=0,
                             skiprows=480,max_rows=660)
            Erymeh=np.loadtxt(car+vermed+file+"Eryme.txt",usecols=0,
                             skiprows=480,max_rows=660)
            Erymo=np.loadtxt(car+AOD+"Eritemica/"+file+"Erymo.txt",usecols=1,
                              skiprows=360)
            UVAmo=np.loadtxt(car+AOD+"UVA/"+file+"UVAmo.txt",usecols=1,
                             skiprows=360)
            Rery=open(car+AOD+ver+"Ratio/"+file+"Eryratio.txt","w")
            Ruva=open(car+AOD+ver+"Ratio/"+file+"UVAratio.txt","w")
            hora=10
            p=0
            pmeuva=(np.where(np.round(UVAmeh,1)==10)[0])[0]
            pmeery=(np.where(np.round(Erymeh,1)==10)[0])[0]
            for _k in range(6):
                for _n in range(60):
                    if(UVAme[pmeuva]!=0):
                        r=UVAme[pmeuva]/UVAmo[p]
                        Ruva.write(str(hora)+" "+str(r)+"\n")
                        if (hora>=12 and hora<=13):
                            Rdia[0,0]=Rdia[0,0]+r
                            Rdia[0,1]=Rdia[0,1]+1
                            if(int(day[_j]/10000)==17):
                                Ranual[0,0,0]=Ranual[0,0,0]+r
                                Ranual[0,0,1]=Ranual[0,0,1]+1
                            else:
                                Ranual[0,1,0]=Ranual[0,1,0]+r
                                Ranual[0,1,1]=Ranual[0,1,1]+1
                    if(Eryme[pmeery]!=0):
                        r=Eryme[pmeery]/Erymo[p]
                        Rery.write(str(hora)+" "+str(r)+"\n")
                        if (hora>=12 and hora<=13):
                            Rdia[1,0]=Rdia[1,0]+r
                            Rdia[1,1]=Rdia[1,1]+1
                            if(int(day[_j]/10000)==17):
                                Ranual[1,0,0]=Ranual[1,0,0]+r
                                Ranual[1,0,1]=Ranual[1,0,1]+1
                            else:
                                Ranual[1,1,0]=Ranual[1,1,0]+r
                                Ranual[1,1,1]=Ranual[1,1,1]+1
                    hora=hora+1/60
                    p=p+1
                    pmeery=pmeery+1
                    pmeuva=pmeuva+1
            if(Rdia[0,1]!=0):
                Rdia[0,0]=Rdia[0,0]/Rdia[0,1]
            if Rdia[1,1]!=0:
                Rdia[1,0]=Rdia[1,0]/Rdia[1,1]
            RDia.write(file+" "+str(round(Rdia[0,0],4))+" "
                        +str(round(Rdia[1,0],4))+"\n")
            Rery.close()
            Ruva.close()
            Ruva=np.loadtxt(car+AOD+ver+"Ratio/"+file+"UVAratio.txt")
            Rery=np.loadtxt(car+AOD+ver+"Ratio/"+file+"Eryratio.txt")
            if(np.size(Rery)!=0):
                plt.title(file+" "+sta[_i])
                plt.ylabel("Erythemal Ratio")
                plt.xlabel("Local time (h)")
                plt.xlim(10,16)
                plt.ylim(0.8,1.2)
                plt.plot([10,16],[1,1],c="black")
                plt.scatter(Rery[:,0],Rery[:,1])
                plt.savefig(car+AOD+ver+"Ratio/Graficas/"
                            +file+"-"+sta[_i]+"EryR.png")
                plt.clf()
            if (np.size(Ruva)!=0) :
                plt.title(file+" "+sta[_i])
                plt.ylabel("UVA Ratio")
                plt.xlabel("Local time (h)")
                plt.xlim(10,16)
                plt.ylim(0.8,1.2)
                plt.plot([10,16],[1,1],c="black")
                plt.scatter(Ruva[:,0],Ruva[:,1])
                plt.savefig(car+AOD+ver+"Ratio/Graficas/"
                            +file+"-"+sta[_i]+"UVAR.png")
                plt.clf()
    Ranual[0,0,0]=Ranual[0,0,0]/Ranual[0,0,1]
    Ranual[1,0,0]=Ranual[1,0,0]/Ranual[1,0,1]
    Ranual[0,1,0]=Ranual[0,1,0]/Ranual[0,1,1]
    Ranual[1,1,0]=Ranual[1,1,0]/Ranual[1,1,1]
    Rfile.write("Ratio ANUAL 2017 UVA "+str(round(Ranual[0,0,0],4))+"\n")
    Rfile.write("Ratio ANUAL 2017 Erythemal "+str(round(Ranual[1,0,0],4))+"\n")
    Rfile.write("Ratio ANUAL 2018 UVA "+str(round(Ranual[0,1,0],4))+"\n")
    Rfile.write("Ratio ANUAL 2018 Erythemal "+str(round(Ranual[1,1,0],4))+"\n")
    Rfile.close()
    RDia.close()
    Rdiario=np.loadtxt("../"+sta[_i]+AOD+ver+"Ratios-Results.txt")
    for _j in range(np.size(Rdiario[:,0])):
        prom1=0
        prom2=0
        n1=0
        n2=0
        if(Rdiario[_j,1]!=0):
            prom1=prom1+Rdiario[_j,1]
            n1=n1+1
        if Rdiario[_j,2]!=0:
            prom2=prom2+Rdiario[_j,2]
            n2=n2+1
    if n1!=0:
        prom1=prom1/n1
    if n2!=0:
        prom2=prom2/n2
    var1=0
    var2=0
    n1=0
    n2=0
    for _j in range(np.size(Rdiario[:,0])):
        if Rdiario[_j,1]!=0:
            var1=var1+(Rdiario[_j,1]-prom1)**2
            n1=n1+1
        if Rdiario[_j,1]!=0:
            var2=var2+(Rdiario[_j,2]-prom2)**2
            n2=n2+1
    num=np.arange(np.size(Rdiario[:,0]))
    if n1!=0:
        var1=pow(var1/n1,1/2)
        for _j in range(np.size(Rdiario[:,0])):
            if Rdiario[_j,1]!=0:
                plt.errorbar(_j,Rdiario[_j,1],yerr=var1,marker="o"
                         ,ls="none",alpha=0.6,color="b",capsize=5,markersize=5)
        plt.xlim(-1,max(num)+1)
        plt.ylabel("UVA Ratio") 
        plt.xlabel("Days")
        plt.title(sta[_i])  
        plt.plot([-10,100],[1,1],c="black")
        plt.savefig("../"+sta[_i]+AOD+"v0.0/RUVA.png")
        plt.clf()
    if n2!=0:
        var2=pow(var2/n2,1/2)
        for _j in range(np.size(Rdiario[:,0])):
            if Rdiario[_j,2]!=0:
                plt.errorbar(_j,Rdiario[_j,2],yerr=var1,marker="o"
                         ,ls="none",alpha=0.6,color="b",capsize=5,markersize=5)
        plt.xlim(-1,max(num)+1)
        plt.ylabel("Erythemal Ratio") 
        plt.xlabel("Days")
        plt.title(sta[_i])  
        plt.plot([-10,100],[1,1],c="black")
        plt.savefig("../"+sta[_i]+AOD+"v0.0/REry.png")
        plt.clf()   