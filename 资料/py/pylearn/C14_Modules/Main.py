from Stat import stat
print("------------华丽的分界线----------------")
import Stat
import Stat
import random


print("id(stat):",id(stat), "id(Stat.stat):",id(Stat.stat))
print("Stat.Stat:",Stat.Stat)

for x in range(random.randint(1,16)):
    stat.add()

print("Stat: {}/{}.".format(stat.iCounter,stat.iTotal))


