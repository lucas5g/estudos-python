import pandas as pd 

# df = pd.read_csv("datasets/gdp.csv")
df = pd.read_csv("datasets/obesity_cleaned.csv")

df[["Sex"]]

df[["Sex"]].transpose()

df[["Year"]].shift()

df[["Year"]] - df[["Year"]].shift()

df["Year"].isin([1900, 1901, 1975])

df["Year"].values

df.columns

df.values

for idx, row in df.iterrows():
    print(idx, row)
    break


for idx, row in df.iterrows():
    print(idx, row["Country"])
    break

df.head()

df.set_index("Year").to_dict().keys()