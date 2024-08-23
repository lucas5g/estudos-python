import sqlite3
import pandas as pd

conn = sqlite3.connect("web.db")

df = pd.read_csv("bd_data.csv", index_col=0)
df.index.name = "id"
df.to_sql("data", conn, index_label="id")

db = conn.cursor()
db.execute("create table products (id, name, price )")

db.execute("drop table products")
db.execute("drop table data")

db.execute("create table products ([id] integer primary key, [name] text, price )")

db.execute(
    """insert into products (id, name, price)
    values
    (1, "Computador", 800),
    (2, "Printer", 200),
    (3, "Tablet", 300)
"""
)

conn.commit()

df2 = df.iloc[::-2]
df2.to_sql('data', conn, if_exists='append')

# select 
db.execute("select * from data")
db.fetchone()
db.fetchall()

df = pd.DataFrame(db.fetchall())

db.execute("select * from data where A > 200 and B > 100")
db.fetchall()

query = "select * from data"
df = pd.read_sql(query, con=conn, index_col='id')
df
