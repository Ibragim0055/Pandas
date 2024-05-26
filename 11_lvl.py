import pandas as pd

data = {'a': [10, 18, 3, 10], 'b': [23, 10, 3, 23]}

df = pd.DataFrame(data)

df['c'] = df['a'] + df['b']

df = df.sort_values('c', ascending=True)

print(df)

grouped = df.groupby(['c']).size().to_frame('size').count()

print(grouped)


print(df.groupby(['c']))