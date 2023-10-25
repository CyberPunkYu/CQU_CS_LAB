# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\pylearn\C15_BubbleSort\About.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(865, 393)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(About.sizePolicy().hasHeightForWidth())
        About.setSizePolicy(sizePolicy)
        About.setMinimumSize(QtCore.QSize(865, 393))
        About.setMaximumSize(QtCore.QSize(865, 393))
        About.setModal(False)
        self.textBrowser = QtWidgets.QTextBrowser(About)
        self.textBrowser.setGeometry(QtCore.QRect(160, 10, 681, 251))
        self.textBrowser.setObjectName("textBrowser")
        self.widget = QtWidgets.QWidget(About)
        self.widget.setGeometry(QtCore.QRect(20, 20, 111, 121))
        self.widget.setStyleSheet("background-image: url(:/Images/img/copy.png);")
        self.widget.setObjectName("widget")
        self.pbClose = QtWidgets.QPushButton(About)
        self.pbClose.setGeometry(QtCore.QRect(540, 277, 301, 101))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(16)
        self.pbClose.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/img/logout.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pbClose.setIcon(icon)
        self.pbClose.setIconSize(QtCore.QSize(64, 64))
        self.pbClose.setObjectName("pbClose")

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "About ... "))
        self.textBrowser.setHtml(_translate("About", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">ABOUT THIS SOFTWARE</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">The software was developped by Alex from Chongqing University.It was designed for educational purpose as an example for author\'s book. The licence is GPL.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">email: </span><span style=\" font-size:12pt; font-weight:600;\">chenbo@cqu.edu.cn   </span><span style=\" font-size:12pt;\">November, 2018</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pbClose.setText(_translate("About", "         CLOSE"))

import Images_rc
