from PyQt5 import QtCore, QtGui, QtWidgets

class UI_Display_DataBase(object):

    def setupUi(self, Form, result):
        Form.setObjectName("Form")
        Form.resize(600, 500)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Imię", "Nazwisko", "Wiek", "Wada stóp"])
        for i, record in enumerate(result):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(record[1]))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(record[2]))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(record[3])))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(record[4]))
        self.tableWidget.resizeColumnsToContents()
        layoutGrid = QtWidgets.QGridLayout()
        Form.setLayout(layoutGrid)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.tableWidget.setGeometry(QtCore.QRect(50, 120, 500, 300))
        self.tableWidget.setSizePolicy(sizePolicy)
        positions=(0,0)
        layoutGrid.addWidget(self.tableWidget, *positions)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "DataBase"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = UI_Display_DataBase()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

