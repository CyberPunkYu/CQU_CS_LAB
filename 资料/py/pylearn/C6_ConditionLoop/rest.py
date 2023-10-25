*x,y = [1,2,3]
print(x,y)
x,y,*rest = [1,2,3,4,5]
print(x,y,rest)

first,*middle,last = "Leonardo di ser Piero Da Vinci".split()
print(first, "-", middle, "-", last)
