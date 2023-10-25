"""
The idea comes from internet.
The code is written by Alex@ChongQing university:  chenbo@cqu.edu.cn   Nov,2018
"""

import tkinter
import random, math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TreeNode:
    maxDepth = 8
    nBranches = 3
    def __init__(self, bottom, top, depth=0):
        self.bottom = bottom
        self.top = top
        self.drawingTop = top
        self.depth = depth
        self.children = []
        self.__generateDescendents()

    def bfs(self):  #breadth first search
        nodesQueue = [self]
        while True:
            if len(nodesQueue)==0:
                break
            x = nodesQueue.pop(0)
            yield x
            nodesQueue.extend(x.children)

    def __generateDescendents(self):
        "Recursively build sub-tree of the current node."
        n = random.randint(TreeNode.nBranches//2,\
                           round(TreeNode.nBranches*1.5))
        n = n if n >=1 else 1

        r = 0.20 + random.random() * 0.2
        x = self.bottom.x + (self.top.x - self.bottom.x) * r
        y = self.bottom.y + (self.top.y - self.bottom.y) * r
        self.drawingTop = Point(x, y)

        if self.depth < self.maxDepth:
            a = math.pi * 0.5 / n
            for i in range(n):
                angleOffset =  a * (n-1) / 2 - a * i + math.pi
                angleOffset *= (0.9 + random.random() * 0.2)
                son = self.__bornSon(self.drawingTop, self.top, angleOffset)
                self.children.append(son)

    def __bornSon(self, bottom, top, angleOffset):
        "Born a son of current node, with designated offset angle."
        xWidth = top.x - bottom.x    #Width of sub-tree
        yHeight = top.y - bottom.y   #Height of sub-tree

        angleSubTree = math.atan(yHeight / xWidth) if xWidth !=0 else math.pi/2
        if (angleSubTree < 0 and bottom.y > top.y) or \
                (angleSubTree > 0 and bottom.y < top.y):
            angleSubTree += math.pi

        angleSon = angleSubTree + angleOffset

        r = 0.9 + random.random() * 0.2
        c = math.sqrt(xWidth ** 2 + yHeight ** 2) * r
        xOffset = c * math.cos(angleSon)
        yOffset = c * math.sin(angleSon)
        topNew = Point(xOffset + bottom.x, yOffset + bottom.y)
        return TreeNode(bottom, topNew, self.depth + 1)


class RenderHelper:
    canvas = None
    def showTree(tree):
        "Render a tree on canvas."
        assert RenderHelper.canvas != None, "Please set canvas first."
        RenderHelper.tree = tree
        for x in RenderHelper.canvas.find_all():
            RenderHelper.canvas.delete(x)
        for x in tree.bfs():
            RenderHelper.__renderNode(x)
        RenderHelper.canvas.update()

    def __renderNode(node):
        "Render a TreeNode."
        colorFill = "#{0:0>2x}{0:0>2x}{0:0>2x}".\
            format(int(0x60 * node.depth / node.maxDepth))
        RenderHelper.__drawLine(node.bottom,node.drawingTop,
            colorFill=colorFill,width=1.5 ** (node.maxDepth - node.depth))

        if not node.children: #draw leaf if it is a leaf
            red = 0xff * node.drawingTop.y / RenderHelper.tree.drawingTop.y
            red = int(red * (0.8 + random.random() * 0.4))
            red = red if red <= 0xff else 0xff
            colorFill = "#{0:0>2x}9000".format(red)
            RenderHelper.canvas.create_oval(
                node.drawingTop.x - 3,node.drawingTop.y - 3,
                node.drawingTop.x + 3,node.drawingTop.y + 3,
                fill=colorFill)

        RenderHelper.canvas.update()     #This sentence for contruction show


    def __drawLine(pt0, pt1, width, colorFill, minDist=10):
        dots = RenderHelper.__generateDotsSequence(pt0,pt1,minDist)
        RenderHelper.canvas.create_line(dots,fill=colorFill,width=width,
            smooth=True)

    def __generateDotsSequence(pt0,pt1,minDist):
        dots = []
        dx, dy = pt1.x - pt0.x, pt1.y - pt0.y
        c = math.sqrt(dx ** 2 + dy ** 2)
        n = int(c / minDist) + 1

        xPrev,yPrev = pt0.x,pt0.y
        for i in range(n):
            xOffset = dx * i / n
            yOffset = dy * i / n
            if i > 0:
                xOffset += minDist * (0.5 - random.random()) * 0.25
                yOffset += minDist * (0.5 - random.random()) * 0.25
            x,y = pt0.x + xOffset,pt0.y + yOffset
            dots.extend([xPrev,yPrev,x,y])
            xPrev,yPrev = x,y
        dots.extend([xPrev,yPrev,pt1.x,pt1.y])
        return dots


class TreeBuilder:
    def setPara(bottom,top,nBranches=3,maxDepth=8):
        TreeBuilder.bottom = bottom
        TreeBuilder.top = top
        TreeBuilder.nBranches = nBranches
        TreeBuilder.maxDepth = maxDepth

    def buildTree(depthOffset=0):
        TreeBuilder.maxDepth += depthOffset
        TreeBuilder.maxDepth = TreeBuilder.maxDepth \
            if TreeBuilder.maxDepth <=10 else 10
        TreeBuilder.maxDepth = TreeBuilder.maxDepth \
            if TreeBuilder.maxDepth >=2 else 2

        print("Build a tree, branches:{},depth:{}.".
              format(TreeBuilder.nBranches,TreeBuilder.maxDepth))
        TreeNode.maxDepth = TreeBuilder.maxDepth
        TreeNode.nBranches = TreeBuilder.nBranches
        t = TreeNode(TreeBuilder.bottom,TreeBuilder.top)
        RenderHelper.showTree(t)



if __name__ == "__main__":
    tk = tkinter.Tk()
    tk.title("Build Tree")
    canvas = tkinter.Canvas(tk,width=1024,height=768,bg="#ffffff")
    canvas.pack()

    RenderHelper.canvas = canvas
    TreeBuilder.setPara(bottom=Point(1024/2,768-20),
                        top=Point(1024/2,768*0.1))
    TreeBuilder.buildTree()

    tk.bind("n", lambda evt: TreeBuilder.buildTree())
    tk.bind("=", lambda evt: TreeBuilder.buildTree(depthOffset=1))
    tk.bind("+", lambda evt: TreeBuilder.buildTree(depthOffset=1))
    tk.bind("-", lambda evt: TreeBuilder.buildTree(depthOffset=-1))
    tk.mainloop()
