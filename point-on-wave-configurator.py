import sys

from PyQt5.QtWidgets import QApplication
from pow_model import ctl_main_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ctl_main_window.MainWindow()
    sys.exit(app.exec())

        
