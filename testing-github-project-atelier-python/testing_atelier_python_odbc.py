import pyodbc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from IPython.display import Image

cnxn=pyodbc.connect(("DSN=TRYCACHE;UID=Sergey;PWD=pAigu1y#"),autocommit=True)

Data=pd.read_sql("SELECT * FROM SQLUser.ENGINES",cnxn)
print(Data)
Data0=Data.drop(["LINE","PIINTTSTICKS","PIINTSHAPEID"],axis=1)
Data0["ID"].replace("Engine_","",inplace=True,regex=True)
Data0["ID"]=pd.to_numeric(Data0["ID"])
print(Data0.describe(percentiles=[0.25,0.5,0.75]))

Data1=Data0.drop(["SETTING3","S1","S10","S16","S18","S19","S5"],axis=1)
Data2=Data1.groupby("ID", as_index=False).CYCLE.max()
Data2.columns=["ID","ARRET"]
plt.scatter(Data2["ID"],Data2["ARRET"])
plt.title("Nuage de points ID/cycles avant arrêt d'un moteur")
plt.xlabel("ID d'un moteur")
plt.ylabel("Cycles avant arrêt")
plt.show()
plt.figure()
plt.hist(Data2["ARRET"],15)
plt.title("Histogramme des cycles avant arrêt d'un moteur")
plt.xlabel("Cycles avant arrêt")
plt.ylabel("Nombre de moteurs")
plt.show()
print(Data2.describe(percentiles=[0.25,0.5,0.75]))

Data3=Data1.merge(Data2,on=["ID","ID"],how="left")
Data3["RESTE"]=Data3["ARRET"]-Data3["CYCLE"]
print(Data3["RESTE"].describe(percentiles=[0.25,0.5,0.75]))

Data4=Data1.drop(["ID","CYCLE"],axis=1)
corrmat=Data4.corr()
plt.figure()
sns.heatmap(corrmat,xticklabels=corrmat.columns,yticklabels=corrmat.columns)
plt.title("Correlation entre les variables indépendantes")
plt.show()

Data5=Data1.loc[Data1["ID"]%2==1]
Data6=Data1.loc[Data1["ID"]%2==0]
Data5=Data5.drop(["ID","CYCLE"],axis=1)
Data6=Data6.drop(["ID","CYCLE"],axis=1)
scaler=StandardScaler()
scaler.fit(Data5)
Data5norm=scaler.transform(Data5)
pca=PCA(.95)
pca.fit(Data5norm)
print(pd.DataFrame(Data5norm))
print("Composantes retenues: ",pca.n_components_)
print("Coéfficients par composante par variable: \n",pd.DataFrame(pca.components_))

print("Variance expliquée par composante: \n",pca.explained_variance_)
print("Pourcentage de la variance expliquée: \n",pca.explained_variance_ratio_)

varexpcum=np.cumsum(pca.explained_variance_ratio_)
nbcomp=np.arange(1,13,1)

plt.figure()
plt.plot(nbcomp,varexpcum)
plt.title("Variance expliquée ~ # de composantes")
plt.xlabel("# de composantes")
plt.ylabel("Variance expliquée")
plt.plot((0,12),(0.9,0.9),"k--")
plt.plot((8,8),(0.4,1.0),"k--")
plt.show()

Data5pca=pca.fit_transform(Data5norm)
km=KMeans(n_clusters=3,init="random",n_init=1)
km.fit(Data5pca)
print(pd.DataFrame(Data5pca))
print("Centres des clusters: \n",km.cluster_centers_)

Data5pcakm=km.predict(Data5pca)
Data7=Data3.loc[Data1["ID"]%2==1]
Data7=Data7.reset_index()
Data7=Data7.drop(["index"],axis=1)
Data7clust=pd.concat([Data7,pd.DataFrame(Data5pcakm)],axis=1)
Data7moteur01=Data7clust.loc[Data7clust["ID"]==1]
Data7moteur47=Data7clust.loc[Data7clust["ID"]==47]
Data7moteur99=Data7clust.loc[Data7clust["ID"]==99]
plt.figure()
plt.scatter(Data7moteur01["CYCLE"],Data7moteur01["S2"],c=Data7moteur01[0])
plt.title("Обучающая выборка: датчик s2/двигатель 1")
plt.xlabel("Отработанные циклы")
plt.ylabel("Значения с датчика s2")
plt.show()
plt.figure()
plt.scatter(Data7moteur47["CYCLE"],Data7moteur47["S12"],c=Data7moteur47[0])
plt.title("Обучающая выборка: датчик s12/двигатель 47")
plt.xlabel("Отработанные циклы")
plt.ylabel("Значения с датчика s12")
plt.show()
plt.figure()
plt.scatter(Data7moteur99["CYCLE"],Data7moteur99["S13"],c=Data7moteur99[0])
plt.title("Обучающая выборка: датчик s13/двигатель 99")
plt.xlabel("Отработанные циклы")
plt.ylabel("Значения с датчика s13")
plt.show()
print(Data7moteur01)
print(Data7moteur47)
print(Data7moteur99)

scaler=StandardScaler()
scaler.fit(Data6)
Data6norm=scaler.transform(Data6)
Data6pca=pca.transform(Data6norm)
Data6pcakm=km.predict(Data6pca)
Data8=Data3.loc[Data1["ID"]%2==0]
Data8=Data8.reset_index()
Data8=Data8.drop(["index"],axis=1)
Data8clust=pd.concat([Data8,pd.DataFrame(Data6pcakm)],axis=1)
Data8moteur02=Data8clust.loc[Data8clust["ID"]==2]
Data8moteur50=Data8clust.loc[Data8clust["ID"]==50]
Data8moteur100=Data8clust.loc[Data8clust["ID"]==100]
plt.figure()
plt.scatter(Data8moteur02["CYCLE"],Data8moteur02["S2"],c=Data8moteur02[0])
plt.title("Прогнозная выборка: датчик s2/двигатель 2")
plt.xlabel("Отработанные циклы")
plt.ylabel("Значения с датчика s2")
plt.show()
plt.figure()
plt.scatter(Data8moteur50["CYCLE"],Data8moteur50["S12"],c=Data8moteur50[0])
plt.title("Прогнозная выборка: датчик s12/двигатель 50")
plt.xlabel("Отработанные циклы")
plt.ylabel("Значения с датчика s12")
plt.show()
plt.figure()
plt.scatter(Data8moteur100["CYCLE"],Data8moteur100["S13"],c=Data8moteur100[0])
plt.title("Прогнозная выборка: датчик s13/двигатель 100")
plt.xlabel("Отработанные циклы")
plt.ylabel("Значения с датчика s13")
plt.show()
print(Data8moteur02)
print(Data8moteur50)
print(Data8moteur100)

cnxn.close()