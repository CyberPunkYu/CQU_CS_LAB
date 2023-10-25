avgScore = 77.2323423
classNo = 3
sText = "The average score of class {no} is {score:.3f}." \
        .format(score=avgScore, no=classNo)
print(sText)

print(f'The average score of class {classNo} is {avgScore:.2f}.')
