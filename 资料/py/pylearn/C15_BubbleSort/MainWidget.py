import os,random
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QSizePolicy
from Country import Country,CompareState
from SortRunner import SortRunner
import Ui_MainWidget
import About


class MainWidget(QtWidgets.QMainWindow,Ui_MainWidget.Ui_MainWidget):
    def __init__(self,parent=None):
        super(MainWidget,self).__init__(parent)
        self.setupUi(self)
        self.sortRunner = None
        self.panelCountries = []
        self.initCountries()
        self.setToIdleState()
        self.displayCountries()

    def setToRunningState(self):
        self.pbStart.setEnabled(False)
        self.pbStop.setEnabled(True)
        self.pbShuffle.setEnabled(False)
        self.pbAbout.setEnabled(False)
        self.pbExit.setEnabled(False)

    def setToIdleState(self):
        self.pbStart.setEnabled(True)
        self.pbStop.setEnabled(False)
        self.pbShuffle.setEnabled(True)
        self.pbAbout.setEnabled(True)
        self.pbExit.setEnabled(True)

    def handlerUpdateInformer(self):
        self.displayCountries()

    def initCountries(self):
        self.countries = []

        import configparser
        data = configparser.ConfigParser()
        data.read("countries.ini")
        data = data["Countries"]
        iSize = int(data.get("countries.size",0))
        for i in range(iSize):
            name = data.get("countries[{}].sName".format(i),"ERROR").strip()
            gdp = float(data.get("countries[{}].fGdp".format(i),"0"))
            logofile = data.get("countries[{}].sLogoFile".format(i),"ERROR").strip()
            self.countries.append(Country(name,gdp,logofile))

    def createPanelCountries(self):
        for i in range(len(self.countries)):
            panel = QtWidgets.QToolButton(self.centralwidget)
            panel.setFixedHeight(52)
            panel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
            panel.setFont(QtGui.QFont("Cambria",16))
            panel.setIconSize(QtCore.QSize(64,48))
            panel.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            self.verticalLayoutCountries.addWidget(panel)
            self.panelCountries.append(panel)

    def displayCountries(self):
        if len(self.panelCountries) == 0:
            self.createPanelCountries()
        assert len(self.panelCountries) == len(self.countries)

        for x, y in zip(self.panelCountries,self.countries):
            x.setText(" " * 10 + "${:<30,.2f}{}".format(y.fGdp,y.sName))
            x.setIcon(QtGui.QIcon("img{}{}".format(os.sep,y.sLogoFile)))
            if y.compareState == CompareState.prev:
                x.setStyleSheet("background-color: rgb(255, 255, 0);")
            elif y.compareState == CompareState.next:
                x.setStyleSheet("background-color: rgb(255, 0, 0);")
            elif y.compareState == CompareState.fixed:
                x.setStyleSheet("background-color: rgb(0, 255, 0);")
            else:
                x.setStyleSheet("")


    def on_pbShuffle_released(self):
        random.shuffle(self.countries)
        for x in self.countries:
            x.compareState = CompareState.idle
        self.displayCountries()

    def on_pbExit_released(self):
        self.close()

    def on_pbAbout_released(self):
        dlg = About.About(self)
        dlg.exec()

    def on_pbStop_released(self):
        assert self.sortRunner != None
        self.sortRunner.terminate()

    def on_pbStart_released(self):
        if self.sortRunner != None:
            if not self.sortRunner.isFinished():
                self.sortRunner.terminate()
                assert self.sortRunner.wait(2000)

        self.setToRunningState()

        self.sortRunner = SortRunner(self.countries,self)
        self.sortRunner.updateInformer.connect(self.handlerUpdateInformer)
        self.sortRunner.finished.connect(self.setToIdleState)
        self.sortRunner.start()







