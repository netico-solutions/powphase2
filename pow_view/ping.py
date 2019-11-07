# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ping.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PingDialog(object):
    def setupUi(self, PingDialog):
        PingDialog.setObjectName("PingDialog")
        PingDialog.resize(622, 237)
        self.consoleOutTxt = QtWidgets.QTextBrowser(PingDialog)
        self.consoleOutTxt.setGeometry(QtCore.QRect(20, 20, 581, 192))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.consoleOutTxt.sizePolicy().hasHeightForWidth())
        self.consoleOutTxt.setSizePolicy(sizePolicy)
        self.consoleOutTxt.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.consoleOutTxt.setObjectName("consoleOutTxt")

        self.retranslateUi(PingDialog)
        QtCore.QMetaObject.connectSlotsByName(PingDialog)

    def retranslateUi(self, PingDialog):
        _translate = QtCore.QCoreApplication.translate
        PingDialog.setWindowTitle(_translate("PingDialog", "Ping"))
