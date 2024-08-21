import pandas as pd 
import numpy as np
from numpy.random import randn


df = pd.DataFrame(randn(5,4), index=["A", "B", "C", "D", "E"], columns="W X Y Z".split())


df 

df > 0

df[df > 0]

df['Y'] > 0

df[df['Y'] > 0]

df[(df['Y'] > 0) & (df['W'] > 0)]