from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def getSize(self):
        pass


class Triangle(Shape):
    def __init__(self):
        self.point0 = (0,0)
        self.point1 = (0,0)
        self.point2 = (0,0)

    def draw(self):
        print("Triangle::draw")

    def getSize(self):
        pass       #detail omitted

    def getArea(self):
        return 0   #it should be w * h / 2

class Circle(Shape):
    def __init__(self):
        self.ptCenter = (0,0)
        self.iRadius = 0

    def draw(self):
        print("Circle::draw")

    def getSize(self):
        pass

    def getArea(self):
        return 0

class Paragraph(Shape):
    def __init__(self):
        self.sContent = ""

    def draw(self):
        print("Paragraph::draw")

    def getSize(self):
        pass

    def setFont(self,fontName,fontSize):
        pass


t1 = Triangle()
t2 = Triangle()
c1 = Circle()
c2 = Circle()
p1 = Paragraph()

#doc模拟一个文档，将界面元素组织在列表中
doc = [p1,c2,t2,c1,t1]

#遍历全部界面元素，将它们全部画出来
def renderDocument(doc):
    for x in doc:
        x.draw()

renderDocument(doc)




