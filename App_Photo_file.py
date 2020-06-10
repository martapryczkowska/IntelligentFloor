
from PyQt5 import QtCore, QtGui, QtWidgets
from App_Photo_correct import Ui_Form

class Ui_PickFile(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(798, 608)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(280, 210, 201, 51))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.textbox_filepicker = QtWidgets.QLineEdit(Form)
        self.textbox_filepicker.setReadOnly(True)
        self.textbox_filepicker.setText("Nie wybrano zdjęcia")
        self.textbox_filepicker.move(340, 300)
        self.textbox_filepicker.resize(300, 30)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(10)
        self.textbox_filepicker.setFont(font)

        self.button_filepicker = QtWidgets.QPushButton('Wybierz zdjęcie', Form)
        self.button_filepicker.move(200, 300)
        self.button_filepicker.resize(120, 30)
        self.Form = Form
        self.button_filepicker.clicked.connect(self.pickFile)
        self.button_filepicker.setFont(font)

        self.accept_file = QtWidgets.QPushButton('OK', Form)
        self.accept_file.move(530, 350),
        self.accept_file.clicked.connect(self.acceptFile)
        self.accept_file.setFont(font)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Wybierz zdjęcie stóp:"))
        self.button_filepicker.setText(_translate("Form", "Wybierz zdjęcie"))


    def pickFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.Form, "QFileDialog.getOpenFileName()", "",
                                                  "Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            self.textbox_filepicker.setText(fileName)

    def acceptFile(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        photo_path = self.textbox_filepicker.text()
        self.ui.setupUi(self.window, photo_path)
        self.window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_PickFile()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

