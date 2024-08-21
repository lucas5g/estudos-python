import pandas as pd 
import numpy as np
from numpy.random import randn


df = pd.DataFrame(randn(5,4), index=["A", "B", "C", "D", "E"], columns="W X Y Z".split())

df.loc[['A', 'B'], ['W']]

df.iloc[0,2]

df.iloc[:-1, :]

df.iloc[1:4, 1:3]

df + df