from PyQt5 import QtCore, QtGui, QtWidgets
from App_DataBaseWindow import UI_DataBase
from App_Photo_file import Ui_PickFile
from App_MakePhoto import Ui_MakePhoto

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 90, 371, 91))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openWindowPickFile)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 210, 371, 91))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.openWindowMakePhoto)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 330, 371, 91))
        self.pushButton_3.clicked.connect(self.openWindowDataBase)

        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FooTApp"))
        self.pushButton.setText(_translate("MainWindow", "Wczytaj zdjęcie z pliku"))
        self.pushButton_2.setText(_translate("MainWindow", "Zrób zdjęcie"))
        self.pushButton_3.setText(_translate("MainWindow", "Otwórz bazę danych"))

    def openWindowDataBase(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = UI_DataBase()
        self.ui.setupUi(self.window)
        self.window.show()

    def openWindowPickFile(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_PickFile()
        self.ui.setupUi(self.window)
        self.window.show()

    def openWindowMakePhoto(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MakePhoto()
        self.ui.setupUi(self.window)
        self.window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

