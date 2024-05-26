import pandas as pd

list = pd.read_csv('pandas/Students_Performance_132b1e1ff9.csv')


print(list.sort_values('writing score', ascending=False))
print(list.head())
print(list.tail())
print(list.dtypes)
print(list.describe())
print(list.dropna())

a = list.head()
a.to_csv('pandas/Students_Performance_132b1e1ff9.csv')