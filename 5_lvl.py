import pandas as pd
import numpy as np

list = {'a': ['rr',2], 'b': ['hello', 'world']}

a = pd.DataFrame(list)

print(a)

a.index = ['BMW', 'MERS'] # Изменение индексов на по указанному название индексов

print()

print(a)

print()

print(a.loc['MERS'])
print()

print(a.index)
print(a.columns)
print(a.axes) # Вывод index и columns вместе
print(a.dtypes) # Типы данных
print(type(a["a"])) # Убеждения столбцы что у DataFrame являются объектами класса Series