class Dummy:
    def __init__(self):
        self.__privateAttribute = 1

    def __privateMethod(self):
        print("Dummy::__privateMethod(): "
        "This method should not be called outside.")

    def publicMethod(self):
        self.__privateMethod()
        print("__privateAttribute:", self.__privateAttribute)


d = Dummy()
d.publicMethod()
