import numpy as np
def weekday(i):
    return (i+6) % 7  #假设1号为周六
print(np.fromfunction(weekday,(31,)).astype(np.int))
