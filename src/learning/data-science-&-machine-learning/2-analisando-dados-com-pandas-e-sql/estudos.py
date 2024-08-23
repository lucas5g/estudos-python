import pandas as pd 

numero_de_dias = 100

#Series temporais
datas = pd.date_range(start='1/1/2024', periods=numero_de_dias)

datas


df = pd.DataFrame(range(numero_de_dias), columns=["number"], index=datas)
df

df.index
df.index[0]

df.index[0].day
df.index[0].month
df.index[0].year 
df.index[0].hour
df[df.index.month == 1]

df["Month"] = df.index.month
import datetime

df[df.index > datetime.datetime(2024,1,10)]


#Entrada e saída de dados
df1 = pd.read_csv("exemplo.csv", sep=",", decimal=".")
df1.info()

df1

df1.to_csv("exemplo2.csv", sep=";", decimal=",")



df = pd.read_html("https://tvglobo.fandom.com/pt-br/wiki/Tabela_de_filmes_exibidos_na_Sess%C3%A3o_da_Tarde")

df2 = df[0]

df_filter = df2[df2['Data da transmissão'] != "Content"]
df_filter['Data da transmissão'] = pd.to_datetime(df_filter["Data da transmissão"], dayfirst=True)

df_filter[df_filter['Data da transmissão'].dt.year == 1979]

