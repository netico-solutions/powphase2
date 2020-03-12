# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_message(object):
    def setupUi(self, message):
        message.setObjectName("message")
        # enable custom window hint
        message.setWindowFlags(message.windowFlags() | QtCore.Qt.CustomizeWindowHint)

        # disable (but not hide) close button
        message.setWindowFlags(message.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        message.setWindowModality(QtCore.Qt.ApplicationModal)
        message.setFixedSize(667, 201)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(message.sizePolicy().hasHeightForWidth())
        message.setSizePolicy(sizePolicy)
        message.setFocusPolicy(QtCore.Qt.StrongFocus)
        message.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.push_ok = QtWidgets.QPushButton(message)
        self.push_ok.setGeometry(QtCore.QRect(290, 150, 83, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_ok.sizePolicy().hasHeightForWidth())
        self.push_ok.setSizePolicy(sizePolicy)
        self.push_ok.setObjectName("push_ok")
        self.label_message = QtWidgets.QLabel(message)
        self.label_message.setGeometry(QtCore.QRect(30, 20, 601, 61))
        self.label_message.setAlignment(QtCore.Qt.AlignCenter)
        self.label_message.setObjectName("label_message")

        self.retranslateUi(message)
        QtCore.QMetaObject.connectSlotsByName(message)

    def retranslateUi(self, message):
        _translate = QtCore.QCoreApplication.translate
        message.setWindowTitle(_translate("message", "Message"))
        self.push_ok.setText(_translate("message", "Ok"))
        self.label_message.setText(_translate("message", "TextLabel"))
