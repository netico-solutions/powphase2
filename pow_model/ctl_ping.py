import time
import sys
import platform
import subprocess
from pow_view import ping
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui

class PingWindow(QDialog):
    def __init__(self, ip):
        super().__init__()
        self.setModal(True)
        self.ip = ip
        self.ui = ping.Ui_PingDialog()
        self.ui.setupUi(self)
        self.run()
        self.show()
        self.exec_()

    def ping_device(self):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '2', self.ip]
        ping_response = subprocess.Popen(command, stdout=subprocess.PIPE).stdout.read()
        return str(ping_response, 'utf-8')

    def stdout_to_textbox(self):
        text = self.ping_device()
        self.ui.consoleOutTxt.setText(text)
        self.show()


    def run(self):
        self.stdout_to_textbox()
        self.close()




