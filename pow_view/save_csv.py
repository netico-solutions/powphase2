# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'save_csv.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SaveFile(object):
    def setupUi(self, SaveFile):
        SaveFile.setObjectName("SaveFile")
        SaveFile.setWindowModality(QtCore.Qt.ApplicationModal)
        SaveFile.resize(790, 479)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SaveFile.sizePolicy().hasHeightForWidth())
        SaveFile.setSizePolicy(sizePolicy)
        SaveFile.setModal(True)
        self.listView = QtWidgets.QListView(SaveFile)
        self.listView.setGeometry(QtCore.QRect(110, 60, 661, 381))
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView.setProperty("showDropIndicator", False)
        self.listView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listView.setObjectName("listView")
        self.layoutWidget = QtWidgets.QWidget(SaveFile)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 60, 91, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.push_list_files = QtWidgets.QPushButton(self.layoutWidget)
        self.push_list_files.setObjectName("push_list_files")
        self.verticalLayout.addWidget(self.push_list_files)
        self.push_save_file = QtWidgets.QPushButton(self.layoutWidget)
        self.push_save_file.setObjectName("push_save_file")
        self.verticalLayout.addWidget(self.push_save_file)
        self.label = QtWidgets.QLabel(SaveFile)
        self.label.setGeometry(QtCore.QRect(110, 40, 62, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(SaveFile)
        self.label_2.setGeometry(QtCore.QRect(510, 40, 62, 20))
        self.label_2.setObjectName("label_2")
        self.push_delete_file = QtWidgets.QPushButton(SaveFile)
        self.push_delete_file.setGeometry(QtCore.QRect(10, 410, 89, 28))
        self.push_delete_file.setObjectName("push_delete_file")

        self.retranslateUi(SaveFile)
        QtCore.QMetaObject.connectSlotsByName(SaveFile)

    def retranslateUi(self, SaveFile):
        _translate = QtCore.QCoreApplication.translate
        SaveFile.setWindowTitle(_translate("SaveFile", "Save file"))
        self.push_list_files.setText(_translate("SaveFile", "List Files"))
        self.push_save_file.setText(_translate("SaveFile", "Save File"))
        self.label.setText(_translate("SaveFile", "Name:"))
        self.label_2.setText(_translate("SaveFile", "Size:"))
        self.push_delete_file.setText(_translate("SaveFile", "Delete Files"))
