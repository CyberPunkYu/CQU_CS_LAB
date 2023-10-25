#Special.py
from scipy import special as S
import pprint
pprint.pprint([x for x in dir(S) if not x.startswith("_")])
