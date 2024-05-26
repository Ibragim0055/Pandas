import pandas as pd

list = {'a': [1, 2, 6, 4, 5], 'b': [6, 7, 8, 9, 0], 'c': [1, 3, 5, 6, 11]}

a = pd.DataFrame(list)

print(a[a['a'] == 2]["b"].head(4))

to = a[a['a'] == 2]

to.to_excel('pandas/lvl_7.xlsx')

print(a['a'].agg(['mean']))

print(a.info())

print(a.shape)

print(a.fillna)