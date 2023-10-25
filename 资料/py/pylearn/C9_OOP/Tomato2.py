class Tomato:
    objectCount = 0

    def __init__(self):
        self.objectCount += 1
        Tomato.objectCount += 1

t1 = Tomato()
t2 = Tomato()
print("Tomato.objectCount:", Tomato.objectCount)
print("t1.objectCount:",t1.objectCount)
print(Tomato.__bases__)