import pygame

class Disc:
    "The said golden disc."
    iDiscHeight = 50
    def __init__(self,screen,number,imgFile):
        self.screen = screen
        self.iNo = number
        self.img = pygame.image.load(imgFile)
        self.rect = self.img.get_rect()

    def blit(self):
        self.screen.blit(self.img,self.rect)

class FlyingDisc:
    "The disc in moving..."
    verticalUpStage = 0
    horizontalMoveStage = 1
    verticalDownStage = 2

    def __init__(self,disc,poleFrom,poleTo):
        self.disc = disc
        self.poleFrom = poleFrom
        self.poleTo = poleTo

        self.xCurrent = poleFrom.xPos
        self.xTo = poleTo.xPos
        self.yCurrent = poleFrom.getDiscsTopPosition()
        self.yCeiling = Disc.iDiscHeight + 20
        self.yTo = poleTo.getDiscsTopPosition()
        self.xStep = (self.xTo - self.xCurrent)/50
        self.yUpStep = (self.yCeiling - self.yCurrent) / 50
        self.yDownStep = (self.yTo - self.yCeiling) / 50

        self.stageMove = self.verticalUpStage

    def blit(self):
        self.disc.rect.centerx = self.xCurrent
        self.disc.rect.bottom = self.yCurrent
        self.disc.blit()

    def flyMove(self):
        assert self.stageMove in (self.verticalDownStage,self.horizontalMoveStage,self.verticalUpStage)
        if self.stageMove == self.verticalUpStage:
            if abs(self.yCurrent-self.yCeiling) <= abs(self.yUpStep):
                self.yCurrent = self.yCeiling
                self.stageMove = self.horizontalMoveStage
            else:
                self.yCurrent += self.yUpStep
            return False

        if self.stageMove == self.horizontalMoveStage:
            if abs(self.xCurrent-self.xTo) <= abs(self.xStep):
                self.xCurrent = self.xTo
                self.stageMove = self.verticalDownStage
            else:
                self.xCurrent += self.xStep
            return False

        if self.stageMove == self.verticalDownStage:
            if abs(self.yCurrent-self.yTo) <= abs(self.yDownStep):
                self.yCurrent = self.yTo
                self.poleTo.putDisc(self.disc)
                return True
            else:
                self.yCurrent += self.yDownStep
            return False







