import os
print(type(os))
print([x for x in dir(os) if not x.startswith("_")])