names = ['jack','mary','tom','dorothy','peter']
names.sort()
print(names)
names.sort(key=len)
print("sort by len:", names)

scores = [82, 66, 66, 93, 24, 15, 77.8]
scores.sort(reverse=True)
print(scores)