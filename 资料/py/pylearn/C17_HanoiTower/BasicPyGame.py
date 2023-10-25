#BasicPyGame.py
import sys,os
import pygame.locals
class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((960, 540))
        pygame.display.set_caption("Tower of Hanoi")

        self.sResourcePath = "resource" + os.sep
        self.imgBackground = pygame.image.load(\
            self.sResourcePath + "background.png").convert()

        self.bgm = pygame.mixer.music.load(self.sResourcePath+"Serenity.mp3")
        pygame.mixer.music.play(loops = int(1e9), start = 0.0)

    def render(self):
        self.screen.blit(self.imgBackground, (0, 0))
        #...
        pygame.display.update()

    def mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    sys.exit()

                elif event.type in (pygame.MOUSEBUTTONDOWN,\
                    pygame.MOUSEBUTTONUP,pygame.MOUSEMOTION):
                    print("Mouse event:",event)
                else:
                    print("Non-mouse event:",event)

            self.render()

if __name__ == '__main__':
    a = App()
    a.mainLoop()