from Disc import Disc
class Pole:
    def __init__(self,xPos):
        self.xPos = xPos
        self.discs = []   #disc 0 at bottom most

    def getDiscsTopPosition(self):
        return 481 - len(self.discs)*Disc.iDiscHeight

    def blit(self):
        for idx,disc in enumerate(self.discs):
            disc.rect.centerx = self.xPos
            disc.rect.bottom = 481 - Disc.iDiscHeight*idx
            disc.blit()

    def putDisc(self,disc):
        if self.discs:
            assert disc.iNo < self.discs[-1].iNo,"Rule violated."
        self.discs.append(disc)

    def popDisc(self):
        disc = self.discs.pop()
        assert disc != None, "No disc on pole."
        return disc


