#swapaxes.py
import numpy as np
a = np.array([[1,2],[3,4]])
print("a=\n",a)
print("a.swapaxes(0,1):\n",a.swapaxes(0,1))

b = np.array([[1,2,3,4],[5,6,7,8]])
print("b=\n",b)
print("b.reshape(2,2,2)=\n",b.reshape(2,2,2))
print("b.reshape(2,2,2).swapaxes(1,2))=\n",b.reshape(2,2,2).swapaxes(1,2))
