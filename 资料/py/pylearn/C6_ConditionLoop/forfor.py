matrix = [[x+1+y+1 for x in range(5)] for y in range(6)]
for r in range(6):
    for c in range(5):
        matrix[r][c] *= 2

for r in matrix:
    print(r)