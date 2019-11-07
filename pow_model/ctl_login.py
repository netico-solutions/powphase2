import time
import json
import platform
import subprocess
import paramiko

from pow_view import login
from . import ctl_ping
from PyQt5.QtWidgets import QDialog

class loginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = login.Ui_ConnectDialog()
        self.ui.setupUi(self)
        self.ui.Ping.clicked.connect(self.ping_button_clicked)
        self.ui.Connect.clicked.connect(self.connect_button_clicked)
        #self.setModal(True)
        self.show()
        self.exec()

    def ping_button_clicked(self):
        ip = self.ui.ip_adress.text()
        pw = ctl_ping.PingWindow(ip)

    def connect_button_clicked(self):
        ip = self.ui.ip_adress.text()
        user = self.ui.username.text()
        passw = self.ui.password.text()

        target_dict = {"ip":"",
                       "user":"",
                       "pass":""}

        target_dict["ip"] = ip
        target_dict["user"] = user
        target_dict["pass"] = passw

        with open('target.json', 'w') as outfile:
            json.dump(target_dict, outfile)

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.load_system_host_keys()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_client.connect(ip, username=user, password=passw)
        except:
            print("Connection Error!")
            #todo failed to connect dialog
            #todo handle reconnect


        self.hide()
