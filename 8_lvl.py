import pandas as pd

list = {'a': [1, 2, 3, 4, 5], 'b': [6, 20, 15, 9, 0], 'c': [1, 103, 5, 45, 11]}

a = pd.DataFrame(list)

b = a.iloc[2:]
print(b)
c = a.loc[3:, 'b':]
print(c)
c.to_excel('pandas/lvl_7.xlsx')

print(a.iat[3, 1])
print(a.at[3, 'b'])