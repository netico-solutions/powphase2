# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!

import json
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConnectDialog(object):

    def init_json_param(self):
        try:
            with open("target.json", "r") as init_json:
                self.init_json_file = json.load(init_json)
        except:
            self.init_json_file = {"ip" : "192.168.2.50",
                                   "user": "root",
                                   "pass": "invalid_password"
                                   }

    def setupUi(self, ConnectDialog):
        self.init_json_param()
        ConnectDialog.setObjectName("ConnectDialog")
        ConnectDialog.setFixedSize(676, 302)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ConnectDialog.sizePolicy().hasHeightForWidth())
        ConnectDialog.setSizePolicy(sizePolicy)
        self.label = QtWidgets.QLabel(ConnectDialog)
        self.label.setGeometry(QtCore.QRect(40, 20, 191, 20))
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(ConnectDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(100, 60, 471, 141))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")


        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.ip_adress = QtWidgets.QLineEdit(self.layoutWidget)
        self.ip_adress.setInputMethodHints(QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhPreferNumbers|QtCore.Qt.ImhUrlCharactersOnly)
        self.ip_adress.setMaxLength(40)
        self.ip_adress.setObjectName("ip_adress")
        self.ip_adress.setText(self.init_json_file["ip"])
        self.username = QtWidgets.QLineEdit(self.layoutWidget)
        self.username.setInputMethodHints(QtCore.Qt.ImhLowercaseOnly|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhPreferLowercase)
        self.username.setMaxLength(7)
        self.username.setObjectName("username")
        self.username.setText(self.init_json_file["user"])
        self.gridLayout.addWidget(self.username, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.ip_adress, 0, 1, 1, 1)
        self.password = QtWidgets.QLineEdit(self.layoutWidget)
        self.password.setMaxLength(20)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.password.setText(self.init_json_file["pass"])
        self.gridLayout.addWidget(self.password, 2, 1, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(ConnectDialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(100, 220, 471, 30))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Ping = QtWidgets.QPushButton(self.layoutWidget1)
        self.Ping.setObjectName("Ping")
        self.horizontalLayout.addWidget(self.Ping)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.Connect = QtWidgets.QPushButton(self.layoutWidget1)
        self.Connect.setObjectName("Connect")
        self.horizontalLayout.addWidget(self.Connect)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)

        self.retranslateUi(ConnectDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectDialog)

    def retranslateUi(self, ConnectDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectDialog.setWindowTitle(_translate("ConnectDialog", "Login"))
        self.label.setText(_translate("ConnectDialog", "Please connect to the device"))
        self.label_2.setText(_translate("ConnectDialog", "username"))
        self.label_4.setText(_translate("ConnectDialog", "IP address"))
        self.label_3.setText(_translate("ConnectDialog", "password"))
        self.Ping.setText(_translate("ConnectDialog", "Ping!"))
        self.Connect.setText(_translate("ConnectDialog", "Connect"))
