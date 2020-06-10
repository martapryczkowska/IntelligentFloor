
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
import cv2
from image import Photo_Legit
from App_Photo_measurement import Ui_PhotoMsrmnt
from foot_parameters import Foot

class Ui_Form(object):
    def setupUi(self, Form,  photo_path):
        Form.setObjectName("Form")
        Form.resize(798, 608)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(240, 10, 240, 360))
        self.label.setObjectName("label")
        self.slider1 = QtWidgets.QSlider(Form)
        self.slider1.setGeometry(QtCore.QRect(160, 410, 451, 22))
        self.slider1.setOrientation(QtCore.Qt.Horizontal)
        self.slider1.setObjectName("slider1")
        self.slider1.setValue(52)
        self.slider1.setTickInterval(10)
        self.slider1.setMaximum(255)
        self.slider1.valueChanged[int].connect(lambda sv, attribute='min_h': self.changeSliderValue(sv, attribute))


        self.slider2 = QtWidgets.QSlider(Form)
        self.slider2.setGeometry(QtCore.QRect(160, 460, 451, 22))
        self.slider2.setOrientation(QtCore.Qt.Horizontal)
        self.slider2.setObjectName("slider2")
        self.slider2.setValue(0)
        self.slider2.setTickInterval(10)
        self.slider2.setMaximum(255)
        self.slider2.valueChanged[int].connect(lambda sv, attribute='min_s': self.changeSliderValue(sv, attribute))

        self.slider3 = QtWidgets.QSlider(Form)
        self.slider3.setGeometry(QtCore.QRect(160, 520, 451, 22))
        self.slider3.setOrientation(QtCore.Qt.Horizontal)
        self.slider3.setObjectName("slider3")
        self.slider3.setValue(13)
        self.slider3.setTickInterval(10)
        self.slider3.setMaximum(255)
        self.slider3.valueChanged[int].connect(lambda sv, attribute='min_v': self.changeSliderValue(sv, attribute))


        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(160, 370, 351, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(500, 560, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.divide_Photo)

        self.photo = Photo_Legit(path=photo_path)
        self.pixmap1 = QPixmap(photo_path)
        self.pixmap1 = self.pixmap1.scaled(288, 432)
        self.label.setPixmap(self.pixmap1)

        self.photo.filterImage()
        self.displayImage(self.photo.mask, mask=True)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Użyj suwaków aby poprawić kontury:"))
        self.pushButton.setText(_translate("Form", "OK"))

    def displayImage(self, imageIN, mask=False):
        if not mask:
            image = cv2.resize(imageIN, (288, 432), interpolation=cv2.INTER_AREA)
            height, width, _ = image.shape
            image = QImage(image.data, width, height, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap(image))
        if mask:
            image = cv2.resize(imageIN, (288, 432))
            height, width = image.shape
            image = QImage(image.data, width, height, QImage.Format_Grayscale8)
            self.label.setPixmap(QPixmap(image))

    def changeSliderValue(self, value, attribute):
        new_value = int(value/255 * 255)
        if attribute == 'min_h':
            self.photo.h_min = new_value
        elif attribute == 'min_s':
            self.photo.s_min = new_value
        elif attribute == 'min_v':
            self.photo.v_min = new_value

        self.photo.filterImage()
        self.displayImage(self.photo.mask, mask=True)

    def divide_Photo(self):
        try:
            self.photo.findContour()
            self.photo.findExtremePoints()

            self.imageCentered = Photo_Legit(in_image=self.photo.centerMatrix(), desc='centered Foot image')
            self.imageCentered.inheritFilter(self.photo)
            self.imageCentered.filterImage()
            self.imageCentered.findContour()
            self.imageCentered.findExtremePoints()
            self.imageCentered.divideImage()

            self.rightFoot = Foot(in_image=self.imageCentered.rightFoot, desc='right foot', right=True)
            self.rightFoot.inheritFilter(self.imageCentered)
            self.rightFoot.filterImage()
            self.rightFoot.findContour()
            self.rightFoot.findExtremePoints()
            self.rightFoot.centerImage()

            self.leftFoot = Foot(in_image=self.imageCentered.leftFoot, desc='left foot', left=True)
            self.leftFoot.inheritFilter(self.imageCentered)
            self.leftFoot.filterImage()
            self.leftFoot.findContour()
            self.leftFoot.findExtremePoints()
            self.leftFoot.centerImage()

            self.rightFootCenteredImage = Foot(in_image=self.rightFoot.centered, desc='centered image', right=True)
            self.rightFootCenteredImage.inheritFilter(self.rightFoot)
            self.rightFootCenteredImage.filterImage()

            self.leftFootCenterImage = Foot(in_image=self.leftFoot.centered, desc='centered image', left=True)
            self.leftFootCenterImage.inheritFilter(self.leftFoot)
            self.leftFootCenterImage.filterImage()

            self.openWindowPhotodivided(self.rightFootCenteredImage, self.leftFootCenterImage)

        except:
            self.open_message_box("Nie udało się podzielić zdjecia, wybierz nowe lub popraw kontury")

    def openWindowPhotodivided(self, rightFoot, leftFoot):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_PhotoMsrmnt()
        self.ui.setupUi(self.window, rightFoot, leftFoot)
        self.window.show()

    def open_message_box(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(text)
        returnValue = msg.exec()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form, 'C:\\Users\MARTA\PycharmProjects\intelligent_floor\PI\example6.jpg')
    Form.show()
    sys.exit(app.exec_())

