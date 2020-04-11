import sys

from PyQt5 import QtWidgets
from gui.main_menu import Ui_MainWindow


class PyQtClient:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(main_window)
        main_window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    cl = PyQtClient()
