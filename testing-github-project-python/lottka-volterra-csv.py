'''
Created on 3 janv. 2018

@author: Sergey
'''
import csv
from math import *
import numpy as np
import pylab as pl
from matplotlib import pyplot

f=open("C:/Users/Sergey/workspace/Python Test/lynxhare.csv","r")
F=csv.reader(f,delimiter=";")
T=[]
B=[]
C=[]
for ligne in F:
    T.append(ligne[0])
    B.append(ligne[1])
    C.append(ligne[2])

temps=[int(a) for a in T[1::]]
lievres=[float(a) for a in B[1::]]
lynx=[float(a) for a in C[1::]]

f.close()

pl.plot(temps,lievres,"o-",color="orange",markersize=6,linewidth=2,label="$x(t)$ : Lievres")
pl.plot(temps,lynx,"o-",color="black",markerfacecolor="white",markersize=7,linewidth=1.5,label="$y(t)$ : Lynx")
labels=[1845+k for k in range(0,92,2)]
pl.xticks(temps[::2],labels,rotation=45,fontsize=8)
pl.legend(fontsize=14)
pl.title("Evolutions de $x$ et $y$ au cours du temps",fontsize=14)
pl.ylabel("Nombre d'animaux en milliers",fontsize=14)
pl.xlabel("Annees",fontsize=14)

ListMaxLynx=[]
ListTemps=[]
for k in range(len(lynx)-2):
    if lynx[k]<lynx[k+1] and lynx[k+1]>lynx[k+2]:
        ListMaxLynx.append(lynx[k+1])
        ListTemps.append(temps[k+1])
print(ListMaxLynx)

ListEcartTemps=[ListTemps[k+1]-ListTemps[k] for k in range(len(ListTemps)-1)]
T=np.mean(ListEcartTemps)
print("T=",T)