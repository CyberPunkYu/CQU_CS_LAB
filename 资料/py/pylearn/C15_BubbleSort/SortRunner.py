#SortRunner.py
from PyQt5 import QtCore
from Country import CompareState
import time

class SortRunner(QtCore.QThread):
    updateInformer = QtCore.pyqtSignal()
    def __init__(self, countries, parent):
        super().__init__(parent)
        self.countries = countries

    def run(self):
        for x in self.countries:
            x.compareState = CompareState.idle
        self.updateInformer.emit()
        time.sleep(0.1)
        for i in range(len(self.countries)-1,0,-1):
            for j in range(0,i):
                self.countries[j].compareState = CompareState.prev
                self.countries[j+1].compareState = CompareState.next
                self.updateInformer.emit()
                time.sleep(0.1)
                if self.countries[j].fGdp < self.countries[j+1].fGdp:
                    self.countries[j],self.countries[j+1] = \
                        self.countries[j+1],self.countries[j]
                    self.updateInformer.emit()
                    time.sleep(0.2)
                self.countries[j].compareState = CompareState.idle
                self.countries[j+1].compareState = CompareState.idle
            self.countries[i].compareState = CompareState.fixed

        self.countries[0].compareState = CompareState.fixed
        self.updateInformer.emit()
        return
