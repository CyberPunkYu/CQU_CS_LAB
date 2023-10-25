#EnumConstants.py
from scipy import constants as C
for k,v in C.physical_constants.items():
    print(k,v)