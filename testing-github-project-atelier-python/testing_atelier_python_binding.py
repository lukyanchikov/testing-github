import codecs, sys
import intersys.pythonbind3

# Connect to the Cache' database
url = "localhost[1972]:User"
user = "Sergey"
password = "pAigu1y#"
conn = intersys.pythonbind3.connection()
conn.connect_now(url,user,password, None)
database = intersys.pythonbind3.database(conn)
   
import numpy as np
import pandas as pd
# import matplotlib
# import matplotlib.pyplot as plt
# import seaborn as sns

sqlstring ="SELECT * FROM SQLUSER.ENGINES"
query=intersys.pythonbind3.query(database)
query.prepare(sqlstring)
query.execute()
Data_liste=[]
Data=pd.DataFrame()
cols=query.fetch([None])
Data_liste.append(cols)
Data=pd.DataFrame(data=Data_liste)
Data_liste=[]
Data_df=()
flag=1
while flag:
    cols=query.fetch([None])
    if len(cols)==0: break
    Data_liste.append(cols)
    Data_df=pd.DataFrame(data=Data_liste)
    Data=pd.concat([Data,Data_df])
    Data_liste=[]
    Data_df=()