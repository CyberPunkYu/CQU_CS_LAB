import sys
from PyQt5 import QtWidgets
import MainWidget

app = QtWidgets.QApplication(sys.argv)

mw = MainWidget.MainWidget()
mw.show()

exit(app.exec_())

