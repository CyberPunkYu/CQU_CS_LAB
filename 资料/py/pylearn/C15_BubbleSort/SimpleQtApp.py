#SimpleQtApp.py
import sys
from PyQt5 import QtWidgets,QtCore

app = QtWidgets.QApplication(sys.argv)
wdMain = QtWidgets.QWidget()
wdMain.setGeometry(200,200,800,600)
wdMain.setWindowTitle("GUI, Let's embrace the world!")

btnExit = QtWidgets.QPushButton('EXIT',wdMain)
btnExit.resize(200,80)
btnExit.move(300,300)
btnExit.clicked.connect(QtCore.QCoreApplication.quit)

wdMain.show()
r = app.exec_()
print("message loop ended.")
exit(r)