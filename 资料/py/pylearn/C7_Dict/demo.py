from PyQt5 import QtCore

print(QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd"))
print(QtCore.QDateTime.currentDateTime().toString("yyyy/MM/dd"))
print(QtCore.QDateTime.currentDateTime().toString("MM-dd,yyyy"))
print(QtCore.QDateTime.currentDateTime().toString("dd/MM/yyyy"))
print(QtCore.QDateTime.currentDateTime().toString("MMM-dd,yyyy"))
print(QtCore.QDateTime.currentDateTime().toString("yyyy-MMM-dd"))

