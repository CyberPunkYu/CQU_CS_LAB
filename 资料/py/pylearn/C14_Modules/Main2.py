from Utils.Stat import stat
import random

for x in range(random.randint(1,16)):
    stat.add()

print("Stat: {}/{}.".format(stat.iCounter,stat.iTotal))

