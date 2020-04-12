# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_menu.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets

from genshop.application.strategy_window import Ui_Form as StrategyForm
from genshop.application.symbol_update import Ui_Form as SymbolUpdateForm


class Ui_MainWindow(object):
    def __init__(self, config, exchange_client, db_client):
        super(Ui_MainWindow, self).__init__()
        self.cfg = config
        self.exchange_client = exchange_client
        self.db_client = db_client

        self.symbol_form = None

        # self.process_symbol_request('GOOG')
        # self.process_symbol_request_all()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 801, 581))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.label_2 = QtWidgets.QLabel(self.tab_5)
        self.label_2.setGeometry(QtCore.QRect(210, 150, 391, 131))
        self.label_2.setObjectName("label_2")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 250, 241, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.on_symbol_update_clicked)

        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 214, 241, 21))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(240, 170, 241, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_hedger_strategy_clicked)

        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(240, 50, 331, 51))
        self.label.setObjectName("label")
        self.tabWidget.addTab(self.tab, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuGeneralShopper = QtWidgets.QMenu(self.menubar)
        self.menuGeneralShopper.setObjectName("menuGeneralShopper")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuGeneralShopper.addSeparator()
        self.menubar.addAction(self.menuGeneralShopper.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "TRADING STRATEGY BACKTESTER\n"
"© Copyright 2020 by GeneralShopper.com, LLC\n"
""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Main"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "File"))
        self.pushButton_3.setText(_translate("MainWindow", "Update Data"))
        self.pushButton_2.setText(_translate("MainWindow", "Moving Average"))
        self.pushButton.setText(_translate("MainWindow", "Hedge Strategy"))
        self.label.setText(_translate("MainWindow", "TRADING STRATEGY BACKTESTER"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Backtest"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Reports"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Setting"))
        self.menuGeneralShopper.setTitle(_translate("MainWindow", "&GeneralShopper"))

    def on_symbol_update_clicked(self):
        self.window = QtWidgets.QMainWindow()
        self.symbol_form = SymbolUpdateForm()
        self.symbol_form.setupUi(self.window)
        self.symbol_form.pushButton.clicked.connect(self.on_symbol_request_click)
        self.window.show()

    def on_hedger_strategy_clicked(self):
        self.window = QtWidgets.QMainWindow()
        ui = StrategyForm()
        ui.setupUi(self.window)
        self.window.show()

    def on_symbol_request_click(self):
        requested_symbol = self.symbol_form.lineEdit.text()

        self.symbol_form.StatusText.setText("In progress")

        try:
            if not requested_symbol:
                self.process_symbol_request_all()
            else:
                self.process_symbol_request(requested_symbol)
        except Exception as err:
            self.symbol_form.StatusText.setText(f"Failed on {err}")
        else:
            self.symbol_form.StatusText.setText("Done")

    def process_symbol_request_all(self):
        symbols = self.db_client.get_symbols()
        for symbol in symbols:
            self.process_symbol_request(symbol)

    def process_symbol_request(self, requested_symbol):
        symbol_is_valid = self.db_client.check_symbol(requested_symbol)
        if not symbol_is_valid:
            raise Exception(f'{requested_symbol} was not found in portfolio')

        last_timestamp = self.db_client.check_if_symbol_is_present(requested_symbol)
        if not last_timestamp:
            data = self.exchange_client.get_ticker_daily_data_all(requested_symbol)
        else:
            data = self.exchange_client.get_ticker_daily_data(last_timestamp, requested_symbol)

        if data:
            self.db_client.store_ticker_data(requested_symbol, data)
        else:
            raise Exception(f'{requested_symbol} data was not received from ameritrade client')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(None, None, None)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

