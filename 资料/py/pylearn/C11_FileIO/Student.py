import configparser

class Score:
    def __init__(self,name,score):
        self.sLessonName = name
        self.score = score

class Student:
    def __init__(self, no="", name="",age=0):
        self.sNo = no
        self.sName = name
        self.iAge = age
        self.scores = []

    def addScore(self,lessonName,lessonScore):
        self.scores.append(Score(lessonName,lessonScore))

    def save(self,filename):
        data = configparser.ConfigParser()
        sSection = "Basic"
        data[sSection] = {}
        data[sSection]["sNo"] = self.sNo
        data[sSection]["sName"] = self.sName
        data[sSection]["iAge"] = str(self.iAge)

        sSection = "Scores"
        data[sSection] = {}
        data[sSection]["scores.size"] = str(len(self.scores))
        for idx,v in enumerate(self.scores):
            data[sSection]["sLessonName[{}]".format(idx)] = v.sLessonName
            data[sSection]["score[{}]".format(idx)] = str(v.score)

        with open(filename,"w") as file:
            data.write(file)

    def load(self,filename):
        data = configparser.ConfigParser()
        data.read(filename)

        sSection = "Basic"
        self.sNo = data[sSection]["sNo"]
        self.sName = data[sSection]["sName"]
        self.iAge = int(data[sSection]["iAge"])

        sSection = "Scores"
        iSize = int(data[sSection].get("scores.size",0))
        for idx in range(iSize):
            sLessonName = data[sSection].get("sLessonName[{}]".format(idx),
                                            "UNKNOWN")
            score = float(data[sSection].get("score[{}]".format(idx),"0"))
            self.scores.append(Score(sLessonName,score))

s = Student("2018197","Dora Henry",17)
s.addScore("C++",78)
s.addScore("Data Structure", 82.5)
s.addScore("Algorithm Design", 90)
s.save("dora.ini")


t = Student()
t.load("dora.ini")
print(t.sNo, t.sName, t.iAge)
for x in t.scores:
    print(x.sLessonName, "\t", x.score)

