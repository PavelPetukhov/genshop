import sys

from PyQt5 import QtWidgets
from genshop.application.main_menu import Ui_MainWindow

from genshop.database.db_client import DBClient
from genshop.ameritrade.ameritrade_client import AmeritradeClient


class App:
    def __init__(self, config):
        self.cfg = config
        self.db_client = DBClient(self.cfg.database)
        self.exchange_client = AmeritradeClient(self.cfg.ameritrade)

        if self.cfg.application and self.cfg.application.validate_schema_on_start:
            self.db_client.validate_db_schema()

        app = QtWidgets.QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()

        ui = Ui_MainWindow(config, self.exchange_client, self.db_client)
        ui.setupUi(main_window)
        main_window.show()
        sys.exit(app.exec_())

