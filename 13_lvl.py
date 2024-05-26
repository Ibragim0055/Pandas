import pandas as pd

list = {'a': [1, 3, 5, 6], 'b': [2, 4, 5, 3]}

a = pd.DataFrame(list)

b = {'a': 4, 'b': 7}

b = pd.DataFrame([b])

ab = pd.concat([b, a], ignore_index=True)

print(ab)

ab.drop([2, 3], inplace=True)

print(ab)