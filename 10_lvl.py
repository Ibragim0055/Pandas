import pandas as pd

list = {'a': [10, 18, 3], 'b': [23, 10, 3]}

a = pd.DataFrame(list)

b = a.assign(c=lambda x: x['a'] + x['b'])

a = b.sort_values(['c'], ascending=True)

a = pd.DataFrame(a)

print(a)