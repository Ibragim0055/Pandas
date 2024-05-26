import pandas as pd
import numpy as np

s = pd.Series(np.arange(5), index=["a", "b", "c", "d", "e"])
s.name = "Данные"
s.index.name = "Индекс"
print(s)