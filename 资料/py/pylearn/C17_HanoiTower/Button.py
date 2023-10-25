from enum import Enum
import pygame

class ButtonState(Enum):
    normal = 0      #正常
    focused = 1     #高亮
    pushed = 2      #按下
    disabled = 3    #禁用

class Button:
    def __init__(self,screen,xCenter,yBottom,
                 fileNormal,fileFocused,filePushed,fileDisabled):
        self.screen = screen
        self.imgNormal = pygame.image.load(fileNormal)
        self.imgFocused = pygame.image.load(fileFocused)
        self.imgPushed = pygame.image.load(filePushed)
        self.imgDisabled = pygame.image.load(fileDisabled)
        self.state = ButtonState.normal

        self.rect = self.imgNormal.get_rect()
        self.rect.centerx = xCenter
        self.rect.bottom = yBottom

    def setEnabled(self,bEnabled):
        self.state = ButtonState.normal if bEnabled \
            else ButtonState.disabled

    def mouseEvent(self,e):
        x,y = pygame.mouse.get_pos()
        if e.type == pygame.MOUSEMOTION:
            return self.__mouseMotionEvent(x,y)

        if not self.rect.collidepoint(x,y):
            return

        if e.type == pygame.MOUSEBUTTONDOWN:
            return self.__mouseDownEvent()

        if e.type == pygame.MOUSEBUTTONUP:
            return self.__mouseUpEvent()

    def __mouseUpEvent(self):
        if self.state not in (ButtonState.disabled,):
            self.state = ButtonState.focused
            return self
        return None

    def __mouseDownEvent(self):
        if self.state in (ButtonState.normal,ButtonState.focused):
            self.state = ButtonState.pushed
        return

    def __mouseMotionEvent(self,x,y):
        if self.rect.collidepoint(x,y):
            if self.state == ButtonState.normal:
                self.state = ButtonState.focused
        else:
            if self.state == ButtonState.focused:
                self.state = ButtonState.normal

    def blit(self):
        img = None
        if self.state == ButtonState.normal:
            img = self.imgNormal
        elif self.state == ButtonState.focused:
            img = self.imgFocused
        elif self.state == ButtonState.disabled:
            img = self.imgDisabled
        elif self.state == ButtonState.pushed:
            img = self.imgPushed
        self.screen.blit(img,self.rect)
