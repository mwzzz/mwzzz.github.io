# https://pandas.ac.cn/docs/user_guide/10min.html

import numpy as np
import pandas as pd

a = np.nan
print(type(a), a)

s = pd.Series([1, 2, 3, '1', 1.1, [144, 'aa']])
print(s)

df = pd.DataFrame(
    {
        'key1': ['value1', 'value4'],
        'key2': ['value2', None],
        'key3': ['value3', None]
    }
)

print(df)
print(df.head())
print('\n')
print(df.tail())

print(df.index)
print(df.columns)

print(df.to_numpy())
df2 = pd.DataFrame(df.to_numpy())
print(df2)
print(df2.describe())

df3 = pd.DataFrame(
    {
        'col1': [1, 2, 3],
        'col2': [4, 11, 6],
        'col3': [7, 8, 9],
    }
)
print(df3)
# df3.sort_index()
df3 = df3.sort_values(by="col2")
print(df3)
