"""
The program was originally writen by JinPeng, 20184374@cqu.edu.cn.
Refractored by Alex CHEN  chenbo@cqu.edu.cn
Nov 2018 @ChongQing University

The audio file was downloaded from https://audionautix.com/, it is free under author's license.
"""

import os,sys
import pygame.locals
from Button import *
from Disc import *
from Pole import *
import HanoiGenerator
from enum import Enum

class AppState(Enum):
    idle = 0
    running = 1
    finished = 2

class HanoiTower:
    instance = None
    userEventDiscMoveInterval = pygame.USEREVENT + 1
    userEventFlyDiscMove = pygame.USEREVENT + 2
    def __init__(self):
        assert HanoiTower.instance == None, "Only one HanoiTower object allowed."
        HanoiTower.instance = self
        self.hanoiGenerator = None
        self.initGame()

    def createButtons(self):
        self.btnReset = Button(self.screen,120,535,
                               self.sResourcePath+"resetNormal.png",
                               self.sResourcePath+"resetFocused.png",
                               self.sResourcePath+"resetPushed.png",
                               self.sResourcePath+"resetDisabled.png")
        self.btnRun = Button(self.screen,360,535,
                               self.sResourcePath+"runNormal.png",
                               self.sResourcePath+"runFocused.png",
                               self.sResourcePath+"runPushed.png",
                               self.sResourcePath+"runDisabled.png")
        self.btnStep = Button(self.screen,600,535,
                               self.sResourcePath+"stepNormal.png",
                               self.sResourcePath+"stepFocused.png",
                               self.sResourcePath+"stepPushed.png",
                               self.sResourcePath+"stepDisabled.png")
        self.btnPause = Button(self.screen,840,535,
                               self.sResourcePath+"pauseNormal.png",
                               self.sResourcePath+"pauseFocused.png",
                               self.sResourcePath+"pausePushed.png",
                               self.sResourcePath+"pauseDisabled.png")
        self.buttons = [self.btnStep,self.btnRun,self.btnPause,self.btnReset]

    def createPolesDiscs(self):
        self.flyingDisc = None
        self.poles = []
        pole0 = Pole(150)
        pole0.putDisc(Disc(self.screen,4,self.sResourcePath + "gray.png"))
        pole0.putDisc(Disc(self.screen,3,self.sResourcePath + "orange.png"))
        pole0.putDisc(Disc(self.screen,2,self.sResourcePath + "yellow.png"))
        pole0.putDisc(Disc(self.screen,1,self.sResourcePath + "green.png"))
        pole0.putDisc(Disc(self.screen,0,self.sResourcePath + "blue.png"))

        self.poles.append(pole0)
        self.poles.append(Pole(480))
        self.poles.append(Pole(810))

    def syncState(self, state):
        if state == AppState.idle:
            self.btnReset.setEnabled(True)
            self.btnRun.setEnabled(True)
            self.btnStep.setEnabled(True)
            self.btnPause.setEnabled(False)
        elif state == AppState.running:
            self.btnReset.setEnabled(False)
            self.btnRun.setEnabled(False)
            self.btnStep.setEnabled(False)
            self.btnPause.setEnabled(True)
        elif state == AppState.finished:
            self.btnReset.setEnabled(True)
            self.btnRun.setEnabled(False)
            self.btnStep.setEnabled(False)
            self.btnPause.setEnabled(False)
        else:
            assert False, "syncState():Unrecognized state parameter."
        self.appState = state

    def initGame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((960, 540), 0, 32)
        pygame.display.set_caption("Tower of Hanoi")

        self.sResourcePath = "resource" + os.sep
        self.imgBackground = pygame.image.load(self.sResourcePath + "background.png").convert()

        self.bgm = pygame.mixer.music.load(self.sResourcePath+"Serenity.mp3")
        pygame.mixer.music.play(loops = int(1e9), start = 0.0)

        self.createPolesDiscs()
        self.createButtons()
        self.syncState(AppState.idle)

    def render(self):
        self.screen.blit(self.imgBackground, (0, 0))

        for x in self.buttons + self.poles:
            x.blit()

        if self.flyingDisc:
            self.flyingDisc.blit()

        pygame.display.update()

    def moveDiscStart(self,iPoleFrom,iPoleTo):
        disc = self.poles[iPoleFrom].popDisc()
        assert self.flyingDisc == None
        self.flyingDisc = FlyingDisc(disc,self.poles[iPoleFrom],self.poles[iPoleTo])
        self.flyTimerStart()

    def moveDiscEnd(self):
        self.flyingDisc = None
        self.flyTimerStop()
        if self.appState == AppState.running:
            self.intervalTimerStart()

    def run(self):
        if not self.hanoiGenerator:
            self.reset()
            self.hanoiGenerator = HanoiGenerator.hanoi(5, 0, 1, 2)
        self.syncState(AppState.running)
        if not self.flyingDisc:
            self.runNextMove()

    def reset(self):
        if self.flyingDisc:
            print("One disc still in moving...")
            return

        self.hanoiGenerator = None
        self.createPolesDiscs()
        self.syncState(AppState.idle)

    def pause(self):
        self.intervalTimerStop()
        self.syncState(AppState.idle)

    def step(self):
        if self.flyingDisc:
            print("One disc still in moving...")
            return

        if not self.hanoiGenerator:
            self.createPolesDiscs()
            self.hanoiGenerator = HanoiGenerator.hanoi(5, 0, 1, 2)

        self.runNextMove()

    def mouseEvent(self,event):
        for b in self.buttons:
            r = b.mouseEvent(event)
            if r:
                break

        if r == None:
            return None

        if r == self.btnRun:
            self.run()
        elif r == self.btnStep:
            self.step()
        elif r == self.btnPause:
            self.pause()
        elif r == self.btnReset:
            self.reset()
        else:
            assert False, "Wrong return value from Button.mouseEvent()."

    def intervalTimerStart(self):
        pygame.time.set_timer(HanoiTower.userEventDiscMoveInterval, 100)

    def intervalTimerStop(self):
        pygame.time.set_timer(HanoiTower.userEventDiscMoveInterval, 0)

    def flyTimerStart(self):
        pygame.time.set_timer(HanoiTower.userEventFlyDiscMove, 10)

    def flyTimerStop(self):
        pygame.time.set_timer(HanoiTower.userEventFlyDiscMove, 0)

    def flyMove(self):
        if not self.flyingDisc:
            self.flyTimerStop()
            return

        if self.flyingDisc.flyMove():
            self.moveDiscEnd()

    def runNextMove(self):
        assert self.hanoiGenerator != None
        self.intervalTimerStop()
        try:
            nextAction = next(self.hanoiGenerator)
        except (StopIteration, Exception) as e:
            self.hanoiGenerator = None
            self.intervalTimerStop()
            self.syncState(AppState.finished)
            print("Iteration over, not more actions.")
        else:
            poleFrom, poleTo = nextAction
            self.moveDiscStart(poleFrom, poleTo)

    def mainLoop(self):
        while (True):
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    sys.exit()

                elif event.type == HanoiTower.userEventFlyDiscMove:
                    self.flyMove()

                elif event.type == HanoiTower.userEventDiscMoveInterval:
                     self.runNextMove()

                elif event.type in (pygame.MOUSEBUTTONDOWN,
                                  pygame.MOUSEBUTTONUP,pygame.MOUSEMOTION):
                    self.mouseEvent(event)

            self.render()

if __name__ == '__main__':
    t = HanoiTower()
    t.mainLoop()


