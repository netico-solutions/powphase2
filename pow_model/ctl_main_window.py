import sys
import time
import json
import threading
import paramiko

from pow_view import main_window
from . import ctl_login, ctl_save_csv
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main_window.Ui_PointOnWaveConfigurator()
        self.ui.setupUi(self)
        self.ui.push_read_json.clicked.connect(self.read_json_parameters)
        self.ui.push_write_json.clicked.connect(self.write_json_parameters)
        self.ui.push_open_files.clicked.connect(self.download_csv)
        self.ui.push_restart_svc.clicked.connect(self.restart_pow_service)
        self.ui.push_restart_fw.clicked.connect(self.restart_urtu_fw)
        self.ui.push_reboot.clicked.connect(self.reboot_urtu)
        self.show()
        self.loginfirst()
        self.run()


    def loginfirst(self):
        self.li = ctl_login.loginWindow()

    def run(self):
        while self.li.isVisible():
            time.sleep(1)
        else:
            pass

    def read_json_parameters(self):
        self.sftp_client = self.li.ssh_client.open_sftp()

        with self.sftp_client.open('/usr/local/src/pow-edge-app/config.json') as json_f:
            parameters = json_f.read()
            self.json_param = parameters.decode('utf-8')
            self.json_param = json.loads(self.json_param)

        self.sftp_client.close()

        #states[0] -> open, states[1] -> close
        self.ui.text_open_start_A.clear()
        self.ui.text_open_start_B.clear()
        self.ui.text_open_start_C.clear()
        self.ui.text_open_stop_A.clear()
        self.ui.text_open_stop_B.clear()
        self.ui.text_open_stop_C.clear()
        self.ui.text_close_start_A.clear()
        self.ui.text_close_start_B.clear()
        self.ui.text_close_start_C.clear()
        self.ui.text_close_stop_A.clear()
        self.ui.text_close_stop_B.clear()
        self.ui.text_close_stop_C.clear()
        self.ui.text_open_impulse.clear()
        self.ui.text_close_impulse.clear()
        self.ui.text_open_angle.clear()
        self.ui.text_close_angle.clear()
        self.ui.text_main_fq.clear()

        self.ui.text_open_start_A.insertPlainText(str(self.json_param['states'][0]['parameters'][3]))
        self.ui.text_open_start_B.insertPlainText(str(self.json_param['states'][0]['parameters'][4]))
        self.ui.text_open_start_C.insertPlainText(str(self.json_param['states'][0]['parameters'][5]))
        self.ui.text_open_stop_A.insertPlainText(str(self.json_param['states'][0]['parameters'][6]))
        self.ui.text_open_stop_B.insertPlainText(str(self.json_param['states'][0]['parameters'][7]))
        self.ui.text_open_stop_C.insertPlainText(str(self.json_param['states'][0]['parameters'][8]))
        self.ui.text_close_start_A.insertPlainText(str(self.json_param['states'][1]['parameters'][3]))
        self.ui.text_close_start_B.insertPlainText(str(self.json_param['states'][1]['parameters'][4]))
        self.ui.text_close_start_C.insertPlainText(str(self.json_param['states'][1]['parameters'][5]))
        self.ui.text_close_stop_A.insertPlainText(str(self.json_param['states'][1]['parameters'][6]))
        self.ui.text_close_stop_B.insertPlainText(str(self.json_param['states'][1]['parameters'][7]))
        self.ui.text_close_stop_C.insertPlainText(str(self.json_param['states'][1]['parameters'][8]))
        self.ui.text_open_impulse.insertPlainText(str(self.json_param['states'][0]['parameters'][10]))
        self.ui.text_close_impulse.insertPlainText(str(self.json_param['states'][0]['parameters'][11]))
        self.ui.text_open_angle.insertPlainText(str(self.json_param['states'][0]['angle']))
        self.ui.text_close_angle.insertPlainText(str(self.json_param['states'][1]['angle']))
        self.ui.text_main_fq.insertPlainText(str(self.json_param['states'][0]['parameters'][9]))

    def write_json_parameters(self):
        self.json_param['states'][0]['parameters'][3] = float(self.ui.text_open_start_A.toPlainText())
        self.json_param['states'][0]['parameters'][4] = float(self.ui.text_open_start_B.toPlainText())
        self.json_param['states'][0]['parameters'][5] = float(self.ui.text_open_start_C.toPlainText())
        self.json_param['states'][0]['parameters'][6] = float(self.ui.text_open_stop_A.toPlainText())
        self.json_param['states'][0]['parameters'][7] = float(self.ui.text_open_stop_B.toPlainText())
        self.json_param['states'][0]['parameters'][8] = float(self.ui.text_open_stop_C.toPlainText())
        self.json_param['states'][1]['parameters'][3] = float(self.ui.text_close_start_A.toPlainText())
        self.json_param['states'][1]['parameters'][4] = float(self.ui.text_close_start_B.toPlainText())
        self.json_param['states'][1]['parameters'][5] = float(self.ui.text_close_start_C.toPlainText())
        self.json_param['states'][1]['parameters'][6] = float(self.ui.text_close_stop_A.toPlainText())
        self.json_param['states'][1]['parameters'][7] = float(self.ui.text_close_stop_B.toPlainText())
        self.json_param['states'][1]['parameters'][8] = float(self.ui.text_close_stop_C.toPlainText())
        self.json_param['states'][0]['parameters'][10] = float(self.ui.text_open_impulse.toPlainText())
        self.json_param['states'][0]['parameters'][11] = float(self.ui.text_close_impulse.toPlainText())
        self.json_param['states'][1]['parameters'][10] = float(self.ui.text_open_impulse.toPlainText())
        self.json_param['states'][1]['parameters'][11] = float(self.ui.text_close_impulse.toPlainText())
        self.json_param['states'][0]['angle'] = float(self.ui.text_open_angle.toPlainText())
        self.json_param['states'][1]['angle'] = float(self.ui.text_close_angle.toPlainText())
        self.json_param['states'][0]['parameters'][9] = float(self.ui.text_main_fq.toPlainText())
        self.json_param['states'][1]['parameters'][9] = float(self.ui.text_main_fq.toPlainText())

        self.sftp_client = self.li.ssh_client.open_sftp()

        with self.sftp_client.file('/usr/local/src/pow-edge-app/config.json', "w") as json_f:
            json.dump(self.json_param, json_f)

        self.sftp_client.close()

    def restart_pow_service(self):
        (stdin, stdout, stderr) = self.li.ssh_client.exec_command('sh -l -c \'systemctl restart edge-pow\'')
        output = stdout.read()
        output = output.decode('utf-8')
        output = output.split()

    def restart_urtu_fw(self):
        (stdin, stdout, stderr) = self.li.ssh_client.exec_command('sh -l -c \'urtu_fw restart\'')
        output = stdout.read()
        output = output.decode('utf-8')
        output = output.split()

    def reboot_urtu(self):
        (stdin, stdout, stderr) = self.li.ssh_client.exec_command('sh -l -c \'reboot\'')
        output = stdout.read()
        output = output.decode('utf-8')
        output = output.split()

    def download_csv(self):
        self.sw = ctl_save_csv.saveCsvWindow()

