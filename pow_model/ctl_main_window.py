import sys
import ast
import time
import json
import threading
import paramiko

from pow_view import main_window
from . import ctl_login, ctl_save_csv, ctl_message
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main_window.Ui_PointOnWaveConfigurator()
        self.ui.setupUi(self)
        self.ui.actionClose.triggered.connect(self.closeMain)
        self.ui.push_read_json.clicked.connect(self.read_json_parameters)
        self.ui.push_write_json.clicked.connect(self.write_json_parameters)
        self.ui.push_open_files.clicked.connect(self.download_csv)
        self.ui.push_restart_svc.clicked.connect(self.restart_pow_service)
        self.ui.push_restart_fw.clicked.connect(self.restart_urtu_fw)
        self.ui.push_reboot.clicked.connect(self.reboot_urtu)
        self.ui.push_sync_time.clicked.connect(self.sync_urtu_time)
        self.ui.radio_voltage.setChecked(True)
        self.ui.push_write_json.setEnabled(False)
        self.show()
        self.loginfirst()
        self.run()

    def closeMain(self):
        sys.exit(0)

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
        self.ui.push_write_json.setEnabled(True)

        #states[0] -> open, states[1] -> close
        self.ui.text_open_point.clear()
        self.ui.text_close_point.clear()
        self.ui.text_open_impulse.clear()
        self.ui.text_close_impulse.clear()
        self.ui.text_open_angle.clear()
        self.ui.text_close_angle.clear()
        self.ui.text_main_fq.clear()
        self.ui.text_curr_1.clear()
        self.ui.text_curr_2.clear()
        self.ui.text_temp_1.clear()
        self.ui.text_temp_2.clear()
        self.ui.radio_voltage.setChecked(False)
        self.ui.radio_current.setChecked(False)

        self.ui.text_open_point.setText(str(self.json_param['states'][0]['time_temp']))
        self.ui.text_close_point.setText(str(self.json_param['states'][1]['time_temp']))
        self.ui.text_open_impulse.setText(str(self.json_param['states'][0]['impulse']))
        self.ui.text_close_impulse.setText(str(self.json_param['states'][1]['impulse']))
        self.ui.text_open_angle.setText(str(self.json_param['states'][0]['angle']))
        self.ui.text_close_angle.setText(str(self.json_param['states'][1]['angle']))
        self.ui.text_main_fq.setText(str(self.json_param['main_frequency']))
        self.ui.text_curr_1.setText(str(self.json_param['temp_calib']['current'][0]))
        self.ui.text_curr_2.setText(str(self.json_param['temp_calib']['current'][1]))
        self.ui.text_temp_1.setText(str(self.json_param['temp_calib']['temperature'][0]))
        self.ui.text_temp_2.setText(str(self.json_param['temp_calib']['temperature'][1]))

        if self.json_param['states'][0]['input_signal']:
            self.ui.radio_current.setChecked(True)
        else:
            self.ui.radio_voltage.setChecked(True)

    def write_json_parameters(self):

        try:
            open_point_text = ast.literal_eval(self.ui.text_open_point.text())
            close_point_text = ast.literal_eval(self.ui.text_close_point.text())

            assert isinstance(open_point_text,list), "Input parameter must be a list"
            assert isinstance(close_point_text,list), "Input parameter must be a list"
            assert len(open_point_text) > 1, "Insert at least two temp_time tuples"
            assert len(close_point_text) > 1, "Insert at least two temp_time tuples"

            for temp,times in open_point_text:
                assert isinstance(temp, int), "Temperature value must be an integer"
                assert isinstance(times, list), "Time values must be in a list"
                assert len(times) == 3, "You have to specify time values for all three phases"
                for time in times:
                    assert isinstance(time, float), "Time value must be a float"

            for temp,times in close_point_text:
                assert isinstance(temp, int), "Temperature value must be an integer"
                assert isinstance(times, list), "Time values must be in a list"
                assert len(times) == 3, "You have to specify time values for all three phases"
                for time in times:
                    assert isinstance(time, float), "Time value must be a float"

            self.json_param['states'][0]['time_temp'] = ast.literal_eval(self.ui.text_open_point.text())
            self.json_param['states'][1]['time_temp'] = ast.literal_eval(self.ui.text_close_point.text())
            self.json_param['states'][0]['impulse'] = float(self.ui.text_open_impulse.text())
            self.json_param['states'][1]['impulse'] = float(self.ui.text_close_impulse.text())
            self.json_param['states'][0]['angle'] = float(self.ui.text_open_angle.text())
            self.json_param['states'][1]['angle'] = float(self.ui.text_close_angle.text())
            self.json_param['temp_calib']['current'][0] = ast.literal_eval(self.ui.text_curr_1.text())
            self.json_param['temp_calib']['current'][1] = ast.literal_eval(self.ui.text_curr_2.text())
            self.json_param['temp_calib']['temperature'][0] = ast.literal_eval(self.ui.text_temp_1.text())
            self.json_param['temp_calib']['temperature'][1] = ast.literal_eval(self.ui.text_temp_2.text())

            if self.ui.radio_voltage.isChecked():
                self.json_param['states'][0]['input_signal'] = 0
                self.json_param['states'][1]['input_signal'] = 0

            elif self.ui.radio_current.isChecked():
                self.json_param['states'][0]['input_signal'] = 1
                self.json_param['states'][1]['input_signal'] = 0


            self.sftp_client = self.li.ssh_client.open_sftp()

            with self.sftp_client.file('/usr/local/src/pow-edge-app/config.json', "w") as json_f:
                json.dump(self.json_param, json_f)

            self.sftp_client.close()
            raise Exception("Configuration successfully writen!")

        except Exception as e:
            text = str(e)
            mw = ctl_message.Message(text)
            self.restart_pow_service()

    def restart_pow_service(self):
        try:
            (stdin, stdout, stderr) = self.li.ssh_client.exec_command('sh -l -c \'systemctl restart edge-pow\'')
            output = stdout.read()
            output = output.decode('utf-8')
            output = output.split()
            raise Exception("PoW service restart command sent!")


        except Exception as e:
            text = str(e)
            mw = ctl_message.Message(text)

    def restart_urtu_fw(self):
        try:
            (stdin, stdout, stderr) = self.li.ssh_client.exec_command('sh -l -c \'urtu_fw restart\'')
            output = stdout.read()
            output = output.decode('utf-8')
            output = output.split()
            raise Exception("Restart Real-time firmware command sent!")

        except Exception as e:
            text = str(e)
            mw = ctl_message.Message(text)

    def reboot_urtu(self):
        try:
            (stdin, stdout, stderr) = self.li.ssh_client.exec_command('sh -l -c \'reboot\'')
            output = stdout.read()
            output = output.decode('utf-8')
            output = output.split()
            raise Exception("Device restarted, please reconnect.")

        except Exception as e:
            text = str(e)
            mw = ctl_message.Message(text)


    def sync_urtu_time(self):
        try:
            ctime = time.strftime("%b %d %Y %H:%M:%S", time.gmtime())
            (stdin, stdout, stderr) = self.li.ssh_client.exec_command('sh -l -c \'date -s \"{}\"\''.format(ctime))
            raise Exception("Device time synchronized to:\n {} UTC".format(ctime))

        except Exception as e:
            text = str(e)
            mw = ctl_message.Message(text)

    def download_csv(self):
        self.sw = ctl_save_csv.saveCsvWindow()

