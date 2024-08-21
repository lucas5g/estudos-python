import pandas as pd 
import numpy as np
from numpy.random import randn


df = pd.DataFrame(randn(5,4), index=["A", "B", "C", "D", "E"], columns="W X Y Z".split())

df.index

df.columns

df.reset_index() 
df


novoind = "CA NY MY OR CO".split()

df['novo_index'] = novoind


df.reset_index().set_index("novo_index")


outside = ['G1', 'G1', 'G1', 'G2', 'G2', 'G2' ]
inside = [1,2,3,1,2,3]

hier_index = list(zip(outside, inside))
hier_index = pd.MultiIndex.from_tuples(hier_index)

hier_index

df = pd.DataFrame(np.random.randn(6,2), index=hier_index, columns=['A', 'B'])

df


df.loc['G1'].loc[1]

df.index.names = ['Grupo', 'Número']

df

df.xs(1, level='Número')