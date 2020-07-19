import numpy as np
import matplotlib.pyplot as plt
#<------------------------Funcion de las graficas individuales con el objeto ax--------------------->
def graf(ax,n_MED,day):
    data=np.loadtxt(day+"Eryme.txt");UVindex=data[:,1]*40
    #<-----------------------Limites de la grafica--------------------------->
    ax.set_xlim(7,18);ax.set_xticks([]);ax.set_ylim(0,16);ax.set_ylabel("UV Index")
    #<----------------------------Titulo------------------------------------->
    ax.set(title="Determination of "+SED[n_MED]+" SED for Phototype "+p[n_MED]+" \n from UV Index measurements")
    for UV in range(UV_i,UV_f+1):
        i=np.where(UVindex>=UV)[0]
        if np.size(i)!=0:
            dosis=0;n_f=n_i=i[0]
            while dosis<MED[n_MED]:    
                dosis+=data[n_f,1]*60;n_f+=1
            #<-------------------Limites de X y Y------------------->
            x,y=data[n_i:n_f,0],UVindex[n_i:n_f]
            #<-----------------------------Grafica para  la leyenda---------------------->
            ax.fill_between(x,y,color=color[UV-1],label="UVI="+str(UV),alpha=0.5);dosis=0;n_f=n_i=i[np.size(i)-1]
            while dosis<MED[n_MED]:
                dosis+=data[n_f,1]*60;n_f+=-1
            #<-----------------------------Grafica sin leyenda------------------------>
            ax.fill_between(data[n_f:n_i,0],UVindex[n_f:n_i],color=color[UV-1],alpha=0.5)
    #<---------------------Leyendas de la grafica---------------------------->
    ax.legend(ncol=5,fontsize="xx-small",frameon=False,loc=2)
#<--------------------------Parametros de los dias, titulos de las graficas y dosis--------------------------->
days,p,SED,MED=["170102","180527"],["III","IV"],["3.0","4.5"],[300,450]
#<--------------------------------Inicio del UV---------------------------->
UV_i,UV_f=1,13;d_UV=UV_f-UV_i
#<---------------------------------Colores-------------------------------------->
color=["lightcoral","salmon","chocolate","darkorange","gold","yellowgreen","lawngreen","limegreen","turquoise"
,"teal","steelblue","royalblue","plum"]
#<--------------------------Subplots----------------------------->
fig,((ax1,ax2),(ax3,ax4))=plt.subplots(2,2,figsize=(9,7))
plt.subplots_adjust(left=0.1,right=0.94,bottom=0.09,top= 0.90)
i=0
for n_MED in range(2):
    for day in days:
        if n_MED==0:
            if day=="170102": graf(ax1,n_MED,day) #<---------------Grafica de la izquiera superior------------------>
            else: graf(ax3,n_MED,day) #<---------------Grafica de la izquiera inferior------------------>
        else:
            if day=="170102": graf(ax2,n_MED,day)#<---------------Grafica de la derecha superior------------------>
            else: graf(ax4,n_MED,day) #<---------------Grafica de la derecha inferior------------------>
plt.savefig("../Graficas/FillDosis.png")