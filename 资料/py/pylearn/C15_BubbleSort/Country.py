#Country.py
from enum import Enum

class CompareState(Enum):
    prev = 0   #the item in comparation as prev item
    next = 1   #the item in comparation as next item
    idle = 2   #the item is not in comparation
    fixed = 3  #the item's position have been settled by sort algorithm

class Country:
    def __init__(self,name,gdp,logofile):
        self.sName = name
        self.fGdp = gdp
        self.sLogoFile = logofile
        self.compareState = CompareState.idle
