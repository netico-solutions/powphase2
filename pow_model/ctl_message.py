import time
import sys
import platform
import subprocess
from pow_view import message
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui

class Message(QDialog):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.setModal(True)
        self.ui = message.Ui_message()
        self.ui.setupUi(self)
        self.ui.push_ok.clicked.connect(self.closeEvent)
        self.update_text(self.text)
        self.show()
        self.exec()

    def closeEvent(self, event):
        self.close()

    def update_text(self, text):
        self.ui.label_message.setText(text)



