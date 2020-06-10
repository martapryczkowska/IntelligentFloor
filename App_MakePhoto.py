from PyQt5 import QtCore, QtGui, QtWidgets
from rasp_communicate import RaspberryCommunication
import datetime
from App_Photo_correct import Ui_Form
from  time import sleep

class Ui_MakePhoto(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(771, 618)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        Form.setFont(font)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(270, 190, 231, 91))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.make_photo)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(210, 340, 391, 71))
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 400, 231, 91))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.acceptFile)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Zrób zdjęcie stóp"))
        self.pushButton_2.setText(_translate("Form", "OK"))

    def acceptFile(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        photo_path = self.label.text()
        self.ui.setupUi(self.window, photo_path)
        self.window.show()


    def make_photo(self):
        try:
            rspCmn = RaspberryCommunication()
            myssh = rspCmn.Connect(ip='192.168.43.137', pw='kamil')
            rspCmn.SendCommand(myssh, command='cd /home/pi/')
            file_name = str(datetime.datetime.now().time()).replace(".", "_").replace(':', '_')
            rspCmn.SendCommand(myssh, command='python camera.py ' + file_name + '.jpg')
            sleep(2)
            self.label.setText("Y:/shared/"+file_name+".jpg")
        except:
            self.label.setText("Nie udało sie wykonać zdjęcia")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_MakePhoto()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

