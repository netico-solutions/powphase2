import time
import sys
import platform
import subprocess
import json
import paramiko
import fnmatch
from pow_view import save_csv
from pow_model import ctl_main_window, ctl_message
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5 import QtGui

class saveCsvWindow(QDialog):
    def __init__(self):
        super().__init__()


        with open('target.json', 'r') as outfile:
            self.ssh_target = json.load(outfile)

        self.ui = save_csv.Ui_SaveFile()
        self.ui.setupUi(self)
        self.list_entry_model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(self.list_entry_model)
        self.ui.push_list_files.clicked.connect(self.list_remote_directory)
        self.ui.push_save_file.clicked.connect(self.save_file_to_local)
        self.ui.push_save_file.setEnabled(False)

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.load_system_host_keys()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.ssh_client.connect(self.ssh_target["ip"], username=self.ssh_target["user"],
                                    password=self.ssh_target["pass"], timeout=3)
        except Exception as e:
            text = "Connection Error: " + str(e)
            mw = ctl_message.Message(text)
            print(e)
            print("Connection Error!")

        self.setModal(True)
        self.show()
        self.exec_()

    def save_file_to_local(self):
        try:
            remote_files = []
            selected_items = self.ui.listView.selectedIndexes()

            for sel in selected_items:
                remote_files.append(sel.data())

            if not remote_files:
                raise Exception("Please select a file.")

            remote_csv_filename = '/usr/local/src/pow-edge-app/' + remote_files[0]

            ftp = self.ssh_client.open_sftp()
            remote_csv_file = ftp.file(remote_csv_filename, "r")
            remote_file_data = remote_csv_file.read()
            remote_file_data = remote_file_data.decode('utf-8')
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", "","CSV Files (*.csv)", options=options)

            if not fileName:
                raise Exception("File not saved.")
            with open(fileName, "w") as file:
                file.write(remote_file_data)

            ftp.close()
            raise Exception("File saved.")
            self.close()

        except Exception as e:
            text = str(e)
            mw = ctl_message.Message(text)

            print(e)


    def list_remote_directory(self):
        try:
            ftp = self.ssh_client.open_sftp()
            csv_files = []

            for filename in ftp.listdir('/usr/local/src/pow-edge-app/'):
                if fnmatch.fnmatch(filename, "*.csv"):
                    csv_files.append(filename)

            csv_files.sort()

            for i in csv_files:
                item = QtGui.QStandardItem(i)
                self.list_entry_model.appendRow(item)

            self.ui.push_save_file.setEnabled(True)

        except Exception as e:
            text = "Error: " + str(e)
            mw = ctl_message.Message(text)
            print(e)
            ftp.close()
            self.close()

    def closeEvent(self, event):
        self.ssh_client.close()




