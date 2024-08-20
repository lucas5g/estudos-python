import pandas as pd 
import numpy as np

labels = ['a', 'b', 'c']

minha_lista = [10, 20, 30]

arr = np.array([10,20,30])
arr

d = {'a': 10, 'b': 20, 'c': 30}

pd.Series(labels)

pd.Series(data=labels, index=minha_lista)

pd.Series(d)

ser1 = pd.Series([1,2,3,4], index=['EUA', 'Alemanha', 'Rússia', 'Japão'])
ser1

ser2 = pd.Series([1,2,3,4], index=['EUA', 'Alemanha', 'Itália', 'Japão'])

ser2, ser1['Alemanha']

ser1 + ser2

pd.Series(labels)

pd.Series(data=labels, index=minha_lista)