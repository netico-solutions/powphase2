import sys
import ast
import time
import json
import threading
import paramiko
import jsonschema
import copy

from config_schema.config_json_schema import valid_schema
from pow_view import main_window
from . import ctl_login, ctl_save_csv, ctl_message
from PyQt5.QtWidgets import QMainWindow, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main_window.Ui_PointOnWaveConfigurator()
        self.ui.setupUi(self)
        self.ui.actionClose.triggered.connect(self.closeMain)
        self.ui.push_read_json.clicked.connect(self.read_json_parameters)

        self.ui.push_save_config.clicked.connect(self.save_json_from_config_tool)
        self.ui.push_load_config.clicked.connect(self.load_json_to_config_tool)

        self.ui.push_write_json.clicked.connect(self.write_json_parameters)
        self.ui.push_open_files.clicked.connect(self.download_csv)
        self.ui.push_restart_svc.clicked.connect(self.restart_pow_service)
        self.ui.push_restart_fw.clicked.connect(self.restart_urtu_fw)
        self.ui.push_reboot.clicked.connect(self.reboot_urtu)
        self.ui.push_sync_time.clicked.connect(self.sync_urtu_time)
        self.ui.radio_voltage.setChecked(True)
        self.disable_buttons_before_login()
        self.show()
        self.ui.push_login.clicked.connect(self.login)
        self.ui.push_logout.clicked.connect(self.logout)
        self.li = ctl_login.loginWindow()
        with open('./config_schema/default_config.json',
                  'r') as default_config_file:
            self.json_param = json.load(default_config_file)
            self.dj = copy.deepcopy(self.json_param)
        self.populate_config_fields()
        # self.json_param = {}
        # self.loginfirst()
        # self.run()

    def closeMain(self):
        sys.exit(0)

    def login(self):
        self.li.show_me()

        while self.li.isVisible():
            time.sleep(1)
        else:
            if self.li.conn_active_flag:
                self.enable_buttons_after_login()

    def loginfirst(self):
        self.li = ctl_login.loginWindow()

    def run(self):
        while self.li.isVisible():
            time.sleep(1)
        else:
            if self.li.conn_active_flag:
                self.enable_buttons_after_login()

    def logout(self):
        self.li.ssh_client.close()
        self.li.conn_active_flag = False
        self.disable_buttons_before_login()

    def save_json_from_config_tool(self):

        try:

            json_param = self.construct_config_params_dict()

            jsonschema.validate(json_param, schema=valid_schema)

            self.json_param = copy.deepcopy(json_param)

            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(
                self,
                "QFileDialog.getSaveFileName()",
                "",
                "JSON Files (*.json)",
                options=options)

            if not fileName:
                raise Exception("File not saved.")
            with open(fileName, "w") as file:
                json.dump(self.json_param, file)

            raise Exception("File saved.")

        except jsonschema.exceptions.ValidationError as e:
            mw = ctl_message.Message('JSON file not in valid format!\n\n'
                                     + e.message)
        except Exception as e:
            text = str(e)
            if text in ['File not saved.']:
                pass
            else:
                if text in ['File saved.']:
                    prepended_text = ''
                else:
                    prepended_text = 'Invalid config parameters!\n\n'
                mw = ctl_message.Message(prepended_text + text)

    def load_json_to_config_tool(self):

        try:

            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(
                self,
                "QFileDialog.getOpenFileName()",
                "",
                "JSON Files (*.json)",
                options=options)

            if not fileName:
                raise Exception("File not loaded.")

            with open(fileName, 'r') as json_file:
                read_json_file = json.load(json_file)

            # Check JSON file here
            jsonschema.validate(read_json_file, schema=valid_schema)

            self.json_param = copy.deepcopy(read_json_file)

            self.populate_config_fields()

            if self.li.conn_active_flag:
                self.ui.push_write_json.setEnabled(True)

            raise Exception("Configuration successfully loaded!")

        except jsonschema.exceptions.ValidationError as e:
            mw = ctl_message.Message('JSON file not in valid format!\n\n'
                            + e.message)
        except Exception as e:
            text = str(e)
            if text in ['File not loaded.']:
                pass
            else:
                mw = ctl_message.Message(text)

    def read_json_parameters(self):

        try:

            sftp_client = self.li.ssh_client.open_sftp()
            with sftp_client.open('/usr/local/src/pow-edge-app/config.json') as json_f:
                parameters = json_f.read()
                read_json_file = parameters.decode('utf-8')
                read_json_file = json.loads(read_json_file)
            sftp_client.close()

            jsonschema.validate(read_json_file, schema=valid_schema)

            self.json_param = copy.deepcopy(read_json_file)
            self.populate_config_fields()

            self.ui.push_write_json.setEnabled(True)

        except jsonschema.exceptions.ValidationError as e:
            raise Exception('JSON file not in valid format!\n\n'
                            + e.message)
        except Exception as e:
            text = str(e)
            mw = ctl_message.Message(text)

    def write_json_parameters(self):

        try:
            json_param = self.construct_config_params_dict()
            jsonschema.validate(json_param, schema=valid_schema)
            self.json_param = copy.deepcopy(json_param)
            sftp_client = self.li.ssh_client.open_sftp()

            with sftp_client.open('/usr/local/src/pow-edge-app/config.json') as json_f:
                parameters = json_f.read()
                read_json_file = parameters.decode('utf-8')
                read_json_file = json.loads(read_json_file)

            if (read_json_file["main_frequency"] != self.json_param["main_frequency"]):
                self.total_reconfigure()

            with sftp_client.file('/usr/local/src/pow-edge-app/config.json', "w") as json_f:
                json.dump(self.json_param, json_f)

            sftp_client.close()

            raise Exception("Configuration successfully writen!")

        except jsonschema.exceptions.ValidationError as e:
            raise Exception('JSON file not in valid format!\n\n'
                            + e.message)
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
            self.logout()
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

    def disable_buttons_before_login(self):
        self.ui.push_read_json.setEnabled(False)
        self.ui.push_write_json.setEnabled(False)
        self.ui.push_open_files.setEnabled(False)
        self.ui.push_reboot.setEnabled(False)
        self.ui.push_restart_fw.setEnabled(False)
        self.ui.push_restart_svc.setEnabled(False)
        self.ui.push_sync_time.setEnabled(False)
        self.ui.push_logout.setEnabled(False)
        self.ui.push_login.setEnabled(True)

    def enable_buttons_after_login(self):
        self.ui.push_read_json.setEnabled(True)
        if self.json_param:
            self.ui.push_write_json.setEnabled(True)
        self.ui.push_open_files.setEnabled(True)
        self.ui.push_reboot.setEnabled(True)
        self.ui.push_restart_fw.setEnabled(True)
        self.ui.push_restart_svc.setEnabled(True)
        self.ui.push_sync_time.setEnabled(True)
        self.ui.push_logout.setEnabled(True)
        self.ui.push_login.setEnabled(False)

    def populate_config_fields(self):
        # states[0] -> open, states[1] -> close
        self.ui.text_open_point.clear()
        self.ui.text_close_point.clear()
        self.ui.text_open_impulse.clear()
        self.ui.text_close_impulse.clear()
        self.ui.text_open_angle.clear()
        self.ui.text_close_angle.clear()
        # self.ui.text_main_fq.clear()
        self.ui.text_curr_1.clear()
        self.ui.text_curr_2.clear()
        self.ui.text_temp_1.clear()
        self.ui.text_temp_2.clear()
        self.ui.radio_voltage.setChecked(False)
        self.ui.radio_current.setChecked(False)

        self.ui.text_open_point.setText(
            str(self.json_param['states'][0]['time_temp']))
        self.ui.text_close_point.setText(
            str(self.json_param['states'][1]['time_temp']))
        self.ui.text_open_impulse.setText(
            str(self.json_param['states'][0]['impulse']))
        self.ui.text_close_impulse.setText(
            str(self.json_param['states'][1]['impulse']))
        self.ui.text_open_angle.setText(
            str(self.json_param['states'][0]['angle']))
        self.ui.text_close_angle.setText(
            str(self.json_param['states'][1]['angle']))
        # self.ui.text_main_fq.setText(str(self.json_param['main_frequency']))
        self.ui.text_curr_1.setText(
            str(self.json_param['temp_calib']['current'][0]))
        self.ui.text_curr_2.setText(
            str(self.json_param['temp_calib']['current'][1]))
        self.ui.text_temp_1.setText(
            str(self.json_param['temp_calib']['temperature'][0]))
        self.ui.text_temp_2.setText(
            str(self.json_param['temp_calib']['temperature'][1]))

        self.ui.dropdown_fq.setCurrentIndex(
            self.ui.dict_of_avaliable_freqs[
                str(self.json_param['main_frequency'])])

        if self.json_param['states'][0]['input_signal']:
            self.ui.radio_current.setChecked(True)
        else:
            self.ui.radio_voltage.setChecked(True)

    def construct_config_params_dict(self):
        params = copy.deepcopy(self.dj)
        params['states'][0]['time_temp'] = ast.literal_eval(
            self.ui.text_open_point.text())
        params['states'][1]['time_temp'] = ast.literal_eval(
            self.ui.text_close_point.text())
        params['states'][0]['impulse'] = float(
            self.ui.text_open_impulse.text())
        params['states'][1]['impulse'] = float(
            self.ui.text_close_impulse.text())
        params['states'][0]['angle'] = float(
            self.ui.text_open_angle.text())
        params['states'][1]['angle'] = float(
            self.ui.text_close_angle.text())
        params['temp_calib']['current'][0] = ast.literal_eval(
            self.ui.text_curr_1.text())
        params['temp_calib']['current'][1] = ast.literal_eval(
            self.ui.text_curr_2.text())
        params['temp_calib']['temperature'][0] = ast.literal_eval(
            self.ui.text_temp_1.text())
        params['temp_calib']['temperature'][1] = ast.literal_eval(
            self.ui.text_temp_2.text())
        params['main_frequency'] = float(str(self.ui.dropdown_fq.currentText()))

        if self.ui.radio_voltage.isChecked():
            params['states'][0]['input_signal'] = 0
            params['states'][1]['input_signal'] = 0

        elif self.ui.radio_current.isChecked():
            params['states'][0]['input_signal'] = 1
            params['states'][1][
                'input_signal'] = 0

        return params

    def total_reconfigure(self):
        text = "Device reconfiguration:" \
               "\nPress OK button and please wait for the heartBeat pattern on the status LED (~2 minutes)"
        mw = ctl_message.Message(text)
        time.sleep(0.1)

        if (self.json_param["main_frequency"] == 50.0):
            (stdin, stdout, stderr) = self.li.ssh_client.exec_command \
                ('sh -l -c \'cd /usr/local/src/urtu-base-sys-root-bin/; git checkout remotes/origin/pow-50hz; ./install.sh\'')
            output = stdout.read()
            output = output.decode('utf-8')
            errora = stderr.read()
            errora = errora.decode('utf-8')
            print(errora)
            output = output.split()
            print(output)

        elif (self.json_param["main_frequency"] == 60.0):
            (stdin, stdout, stderr) = self.li.ssh_client.exec_command \
                ('sh -l -c \'cd /usr/local/src/urtu-base-sys-root-bin/; git checkout remotes/origin/pow-60hz; ./install.shqq\'')
            output = stdout.read()
            output = output.decode('utf-8')
            errora = stderr.read()
            errora = errora.decode('utf-8')
            print(errora)
            print(output)
            output = output.split()\

