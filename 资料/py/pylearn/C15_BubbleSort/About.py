from PyQt5 import QtWidgets
from Ui_About import Ui_About

class About(QtWidgets.QDialog,Ui_About):
    def __init__(self,parent):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)

    def on_pbClose_released(self):
        self.close()
