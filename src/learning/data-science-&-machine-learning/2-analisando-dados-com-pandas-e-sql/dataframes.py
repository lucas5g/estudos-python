import pandas as pd 
from numpy.random import randn

df = pd.DataFrame(randn(5,4), index=["A", "B", "C", "D", "E"], columns="W X Y Z".split())
df

df[['W']]

df["new"] = df['W'] + df['Y']

df.drop('new',axis=1)

df.drop('new', axis=1, inplace=True)
df

df.loc[['A', 'B']]

df.iloc[0,2]