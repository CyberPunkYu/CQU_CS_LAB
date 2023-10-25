scores = [78,99,22,12,15,67]

def compAvergageScore(scores):
    assert len(scores) > 0
    assert max(scores) <= 100
    assert min(scores) >= 0
    return sum(scores) / len(scores)

print(compAvergageScore(scores))