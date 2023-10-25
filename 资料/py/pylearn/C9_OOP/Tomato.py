class Tomato:
    objectCount = 0
    def smile():
        print("Tomato.smile(): without self parameter.")

    def __init__(self):
        Tomato.objectCount += 1

Tomato.smile()
t1 = Tomato()
t2 = Tomato()
t3 = Tomato()
print("Tomato.objectCount:", Tomato.objectCount)
print("t1.objectCount:",t1.objectCount)
print("id of Tomato.objectCount:",id(Tomato.objectCount))
print("id of t1.objectCount:",id(t1.objectCount))
