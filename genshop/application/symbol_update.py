# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'symbol_update.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from genshop.logger import logging


class Ui_Form(object):
    def __init__(self, config, exchange_client, db_client):
        super(Ui_Form, self).__init__()
        self.logger = logging.getLogger()
        self.cfg = config
        self.exchange_client = exchange_client
        self.db_client = db_client

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(711, 493)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(230, 40, 271, 61))
        font = QtGui.QFont()
        font.setPointSize(25)

        self.label.setFont(font)
        self.label.setObjectName("label")

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(300, 130, 141, 25))
        self.lineEdit.setObjectName("lineEdit")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(240, 140, 67, 17))
        self.label_2.setObjectName("label_2")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(350, 200, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_symbol_request_click)

        self.StatusText = QtWidgets.QLabel(Form)
        self.StatusText.setGeometry(QtCore.QRect(300, 250, 331, 17))
        self.StatusText.setText("")
        self.StatusText.setObjectName("StatusText")
        self.StatusLabel = QtWidgets.QLabel(Form)
        self.StatusLabel.setGeometry(QtCore.QRect(250, 250, 67, 17))
        self.StatusLabel.setObjectName("StatusLabel")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "UPDATE DATA"))
        self.label_2.setText(_translate("Form", "Symbol:"))
        self.pushButton.setText(_translate("Form", "Update"))
        self.StatusLabel.setText(_translate("Form", "Status:"))

    def on_symbol_request_click(self):
        self.StatusText.setText("In progress")
        self.StatusText.repaint()

        requested_symbol = self.lineEdit.text()

        self.logger.info(f'on_symbol_request_click started for {requested_symbol}')

        symbol_is_valid = self.db_client.check_symbol(requested_symbol)
        if not symbol_is_valid:
            self.db_client.add_symbol(requested_symbol)

        try:
            if not requested_symbol:
                self.process_symbol_request_all()
            else:
                self.process_symbol_request(requested_symbol)
        except Exception as err:
            self.logger.info(f'on_symbol_request_click failed on {err}')
            self.StatusText.setText(f"Failed. Check Logs")
        else:
            self.StatusText.setText("Done")

    def process_symbol_request_all(self):
        self.logger.info(f'process_symbol_request_all started')

        symbols = self.db_client.get_symbols()
        for symbol in symbols:
            self.process_symbol_request(symbol)

    def process_symbol_request(self, requested_symbol):
        self.logger.info(f'process_symbol_request started for {requested_symbol}')

        symbol_is_valid = self.db_client.check_symbol(requested_symbol)
        if not symbol_is_valid:
            raise Exception(f'{requested_symbol} was not found in portfolio')

        last_timestamp = self.db_client.check_if_symbol_is_present(requested_symbol)
        if not last_timestamp:
            eod_data = self.exchange_client.get_ticker_eod_data_all(requested_symbol)
            data = self.exchange_client.get_ticker_daily_data_all(requested_symbol)
        else:
            eod_data = self.exchange_client.get_ticker_eod_data(last_timestamp, requested_symbol)
            data = self.exchange_client.get_ticker_daily_data(last_timestamp, requested_symbol)

        if data:
            self.db_client.store_minute_ticker_data(requested_symbol, data)
        else:
            msg_ = f'{requested_symbol} minute data was not received from ameritrade client'
            self.logger.info(msg_)
            raise Exception(msg_)

        if eod_data:
            self.db_client.store_eod_ticker_data(requested_symbol, eod_data)
        else:
            msg_ = f'{requested_symbol} eod data was not received from ameritrade client'
            self.logger.info(msg_)
            raise Exception(msg_)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
