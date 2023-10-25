import configparser
import os

class Stat:
    sFileName = os.path.expanduser('~') + os.sep + "stat.dat"
    def __init__(self):
        self.__load()

    def __load(self):
        data = configparser.ConfigParser()
        data.read(Stat.sFileName)
        if "Stats" not in data.keys():
            data["Stats"] = {}
        self.iCounter = 0
        self.iTotal = int(data["Stats"].get("iTotal",0))

    def __save(self):
        data = configparser.ConfigParser()
        data["Stats"] = {}
        data["Stats"]["iCounter"] = str(self.iCounter)
        data["Stats"]["iTotal"] = str(self.iTotal)

        with open(Stat.sFileName,"w") as f:
            data.write(f)

    def add(self):
        self.iCounter+=1
        self.iTotal+=1
        self.__save()

print(__name__,"module imported.")
stat = Stat()








