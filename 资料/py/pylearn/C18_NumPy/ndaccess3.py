import numpy as np

a = [[x+y for x in range(5)] for y in range(6)]
a = np.array(a).astype(int)
idx = slice(0,None,3),slice(None,None,2)
print(a[idx])

