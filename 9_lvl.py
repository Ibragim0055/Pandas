import pandas as pd

list = {'a': [10, 18, 3], 'b': [23, 10, 3]}

a = pd.DataFrame(list)

summ = a['a'] + a['b']

s = pd.DataFrame(summ)

s.columns = ['list']

print(s.sort_values(['list'], ascending=True).head(2))