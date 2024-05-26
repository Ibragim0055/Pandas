import pandas as pd
import numpy as np

s = pd.Series(np.arange(3, 8), index=["a", "b", "c", "d", "e"])

print(s)
print(s[2:5])

print(s+s)