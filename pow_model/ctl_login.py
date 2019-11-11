import time
import sys
import json
import platform
import subprocess
import paramiko
import threading

from pow_view import login
from . import ctl_ping, ctl_message
from PyQt5.QtWidgets import QDialog

class loginWindow(QDialog):
    def __init__(self):
        self.conn_active_flag = False
        super().__init__()
        self.ui = login.Ui_ConnectDialog()
        self.ui.setupUi(self)
        self.ui.Ping.clicked.connect(self.ping_button_clicked)
        self.ui.Connect.clicked.connect(self.connect_button_clicked)
        self.is_alive_thread = threading.Thread(target=self.is_active, args=())
        self.is_alive_thread.setDaemon(True)
        self.is_alive_thread.start()
        self.setModal(True)
        self.show()
        self.exec()

    def closeEvent(self, event):
        sys.exit(0)

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
            self.ssh_client.connect(ip, username=user, password=passw, timeout=2)
            self.conn_active_flag = True
            self.hide()

        except Exception as e:
            text = "Connection Error: " + str(e)
            mw = ctl_message.Message(text)
            print("Connection Error!")
            time.sleep(1)

    def is_active(self):
        while True:
            while self.conn_active_flag:
                try:
                    self.ssh_client.exec_command('ls', timeout=3)
                    print("Connected.")
                    time.sleep(3)
                except Exception as e:
                    print("Connection Error!")
                    self.ssh_client.close()
                    self.conn_active_flag = False
                    time.sleep(1)
                    text = "Connection Error: " + str(e)
                    mw = ctl_message.Message(text)
                    self.show()
                    break

            else:
                time.sleep(2)
                print("No active connection.")



