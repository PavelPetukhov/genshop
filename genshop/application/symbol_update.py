# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'symbol_update.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def __init__(self):
        super(Ui_Form, self).__init__()

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
        # self.pushButton.clicked.connect(self.button_click)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "UPDATE DATA"))
        self.label_2.setText(_translate("Form", "Symbol:"))
        self.pushButton.setText(_translate("Form", "Update"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
