import pandas as pd
import matplotlib.pyplot as plt

list = {'a': [10, 18, 3], 'b': [23, 10, 3]}

a = pd.DataFrame(list)

summ = a['a'] + a['b']

s = pd.DataFrame(summ)

s.columns = ['list']

print(s.sort_values(['list'], ascending=True))

plt.hist(s["list"], label="Тест по математике")
plt.xlabel("Баллы за тест")
plt.ylabel("Количество студентов")
plt.legend()
plt.show()