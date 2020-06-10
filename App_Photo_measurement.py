from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtGui import QImage, QPixmap
from foot_parameters import Foot
from svm_classifier import svm_classifier
import numpy as np



class Ui_PhotoMsrmnt(object):
    def setupUi(self, Form,  righFoot, leftFoot):
        self.rightFoot = righFoot
        self.leftFoot = leftFoot

        Form.setObjectName("Form")
        Form.resize(926, 862)
        self.labelImage1 = QtWidgets.QLabel(Form)
        self.labelImage1.setGeometry(QtCore.QRect(180, 20, 241, 361))
        self.labelImage1.setObjectName("labelImage1")
        self.labelImage2 = QtWidgets.QLabel(Form)
        self.labelImage2.setGeometry(QtCore.QRect(540, 20, 241, 361))
        self.labelImage2.setObjectName("labelImage2")

        self.slider1_1 = QtWidgets.QSlider(Form)
        self.slider1_1.setGeometry(QtCore.QRect(40, 420, 381, 22))
        self.slider1_1.setOrientation(QtCore.Qt.Horizontal)
        self.slider1_1.setObjectName("slider1_1")
        self.slider1_1.setValue(self.leftFoot.h_min)
        self.slider1_1.setMaximum(255)
        self.slider1_1.valueChanged[int].connect(lambda sv, attribute='min_h', foot=self.leftFoot: self.changeSliderValue2(sv, attribute, foot))

        self.slider1_2 = QtWidgets.QSlider(Form)
        self.slider1_2.setGeometry(QtCore.QRect(40, 470, 381, 22))
        self.slider1_2.setOrientation(QtCore.Qt.Horizontal)
        self.slider1_2.setObjectName("slider1_2")
        self.slider1_2.setValue(self.leftFoot.s_min)
        self.slider1_2.setMaximum(255)
        self.slider1_2.valueChanged[int].connect(lambda sv, attribute='min_s', foot=self.leftFoot: self.changeSliderValue2(sv, attribute, foot))

        self.slider1_3 = QtWidgets.QSlider(Form)
        self.slider1_3.setGeometry(QtCore.QRect(40, 530, 381, 22))
        self.slider1_3.setOrientation(QtCore.Qt.Horizontal)
        self.slider1_3.setObjectName("slider1_3")
        self.slider1_3.setValue(self.leftFoot.v_min)
        self.slider1_3.setMaximum(255)
        self.slider1_3.valueChanged[int].connect(lambda sv, attribute='min_v', foot=self.leftFoot: self.changeSliderValue2(sv, attribute, foot))

        self.slider2_1 = QtWidgets.QSlider(Form)
        self.slider2_1.setGeometry(QtCore.QRect(480, 420, 381, 22))
        self.slider2_1.setOrientation(QtCore.Qt.Horizontal)
        self.slider2_1.setObjectName("slider2_1")
        self.slider2_1.setValue(self.rightFoot.h_min)
        self.slider2_1.setMaximum(255)
        self.slider2_1.valueChanged[int].connect(lambda sv, attribute='min_h', foot=self.rightFoot: self.changeSliderValue2(sv, attribute, foot))

        self.slider2_2 = QtWidgets.QSlider(Form)
        self.slider2_2.setGeometry(QtCore.QRect(480, 470, 381, 22))
        self.slider2_2.setOrientation(QtCore.Qt.Horizontal)
        self.slider2_2.setObjectName("slider2_2")
        self.slider2_2.setValue(self.leftFoot.s_min)
        self.slider2_2.setMaximum(255)
        self.slider2_2.valueChanged[int].connect(lambda sv, attribute='min_s', foot=self.rightFoot: self.changeSliderValue2(sv, attribute, foot))

        self.slider2_3 = QtWidgets.QSlider(Form)
        self.slider2_3.setGeometry(QtCore.QRect(480, 530, 381, 22))
        self.slider2_3.setOrientation(QtCore.Qt.Horizontal)
        self.slider2_3.setObjectName("slider2_3")
        self.slider2_3.setValue(self.leftFoot.v_min)
        self.slider2_3.setMaximum(255)
        self.slider2_3.valueChanged[int].connect(lambda sv, attribute='min_v', foot=self.rightFoot: self.changeSliderValue2(sv, attribute, foot))


        self.buttonPomiar1 = QtWidgets.QPushButton(Form)
        self.buttonPomiar1.setGeometry(QtCore.QRect(170, 570, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        self.buttonPomiar1.setFont(font)
        self.buttonPomiar1.setObjectName("buttonPomiar1")
        self.buttonPomiar1.clicked.connect(lambda: self.pomiar(self.leftFoot))
        self.buttonPomiar2 = QtWidgets.QPushButton(Form)
        self.buttonPomiar2.setGeometry(QtCore.QRect(600, 570, 111, 41))
        self.buttonPomiar2.clicked.connect(lambda: self.pomiar(self.rightFoot))

        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        self.buttonPomiar2.setFont(font)
        self.buttonPomiar2.setObjectName("buttonPomiar2")
        self.label_AI_1 = QtWidgets.QLabel(Form)
        self.label_AI_1.setGeometry(QtCore.QRect(40, 620, 91, 16))
        self.label_AI_1.setObjectName("label_AI_1")

        self.label_AI_1_result = QtWidgets.QLabel(Form)
        self.label_AI_1_result.setGeometry(QtCore.QRect(135, 620, 91, 16))
        self.label_AI_1_result.setObjectName("label_AI_1_result")

        self.label_KY_1 = QtWidgets.QLabel(Form)
        self.label_KY_1.setGeometry(QtCore.QRect(40, 650, 81, 16))
        self.label_KY_1.setObjectName("label_KY_1")

        self.label_KY_1_result = QtWidgets.QLabel(Form)
        self.label_KY_1_result.setGeometry(QtCore.QRect(135, 650, 81, 16))
        self.label_KY_1_result.setObjectName("label_AI_1_result")


        self.label_Clarke_1 = QtWidgets.QLabel(Form)
        self.label_Clarke_1.setGeometry(QtCore.QRect(40, 680, 81, 16))
        self.label_Clarke_1.setObjectName("label_Clarke_1")

        self.label_Clarke_1_result = QtWidgets.QLabel(Form)
        self.label_Clarke_1_result.setGeometry(QtCore.QRect(135, 680, 81, 16))
        self.label_Clarke_1_result.setObjectName("label_AI_1_result")

        self.label_Alfa_1 = QtWidgets.QLabel(Form)
        self.label_Alfa_1.setGeometry(QtCore.QRect(40, 710, 71, 16))
        self.label_Alfa_1.setObjectName("label_Alfa_1")

        self.label_Alfa_1_result = QtWidgets.QLabel(Form)
        self.label_Alfa_1_result.setGeometry(QtCore.QRect(135, 710, 71, 16))
        self.label_Alfa_1_result.setObjectName("label_Alfa_1")

        self.label_gamma_1 = QtWidgets.QLabel(Form)
        self.label_gamma_1.setGeometry(QtCore.QRect(40, 740, 71, 16))
        self.label_gamma_1.setObjectName("label_gamma_1")

        self.label_gamma_1_result = QtWidgets.QLabel(Form)
        self.label_gamma_1_result.setGeometry(QtCore.QRect(135, 740, 71, 16))
        self.label_gamma_1_result.setObjectName("label_gamma_1")

        self.label_Alfa_2 = QtWidgets.QLabel(Form)
        self.label_Alfa_2.setGeometry(QtCore.QRect(500, 710, 71, 16))
        self.label_Alfa_2.setObjectName("label_Alfa_2")

        self.label_Alfa_2_result = QtWidgets.QLabel(Form)
        self.label_Alfa_2_result.setGeometry(QtCore.QRect(600, 710, 71, 16))
        self.label_Alfa_2_result.setObjectName("label_Alfa_2")

        self.label_KY_2 = QtWidgets.QLabel(Form)
        self.label_KY_2.setGeometry(QtCore.QRect(500, 650, 81, 16))
        self.label_KY_2.setObjectName("label_KY_2")

        self.label_KY_2_result = QtWidgets.QLabel(Form)
        self.label_KY_2_result.setGeometry(QtCore.QRect(600, 650, 81, 16))

        self.label_Clarke_2 = QtWidgets.QLabel(Form)
        self.label_Clarke_2.setGeometry(QtCore.QRect(500, 680, 81, 16))
        self.label_Clarke_2.setObjectName("label_Clarke_2")

        self.label_Clarke_2_result = QtWidgets.QLabel(Form)
        self.label_Clarke_2_result.setGeometry(QtCore.QRect(600, 680, 81, 16))

        self.label_AI_2 = QtWidgets.QLabel(Form)
        self.label_AI_2.setGeometry(QtCore.QRect(500, 620, 91, 16))
        self.label_AI_2.setObjectName("label_AI_2")

        self.label_AI_2_result = QtWidgets.QLabel(Form)
        self.label_AI_2_result.setGeometry(QtCore.QRect(600, 620, 91, 16))

        self.label_gamma_2 = QtWidgets.QLabel(Form)
        self.label_gamma_2.setGeometry(QtCore.QRect(500, 740, 71, 16))
        self.label_gamma_2.setObjectName("label_gamma_2")

        self.label_gamma_2_result = QtWidgets.QLabel(Form)
        self.label_gamma_2_result.setGeometry(QtCore.QRect(600, 740, 71, 16))

        self.buttonSVM1 = QtWidgets.QPushButton(Form)
        self.buttonSVM1.setGeometry(QtCore.QRect(290, 810, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        self.buttonSVM1.setFont(font)
        self.buttonSVM1.setObjectName("buttonSVM1")
        self.buttonSVM1.clicked.connect(lambda: self.SVM_classify(False))

        self.SVM_result_1 = QtWidgets.QLabel(Form)
        self.SVM_result_1.setGeometry(QtCore.QRect(50, 810, 211, 41))
        self.SVM_result_1.setFont(font)


        self.button_SVM2 = QtWidgets.QPushButton(Form)
        self.button_SVM2.setGeometry(QtCore.QRect(760, 810, 111, 41))

        self.SVM_result_2 = QtWidgets.QLabel(Form)
        self.SVM_result_2.setGeometry(QtCore.QRect(500, 810, 211, 41))
        self.SVM_result_2.setFont(font)



        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        self.button_SVM2.setFont(font)
        self.button_SVM2.setObjectName("button_SVM2")
        self.button_SVM2.clicked.connect(lambda: self.SVM_classify(True))


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


        self.displayImage(self.leftFoot.mask, label=self.labelImage1)
        self.displayImage(self.rightFoot.mask, label=self.labelImage2)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.buttonPomiar1.setText(_translate("Form", "Pomiar"))
        self.buttonPomiar2.setText(_translate("Form", "Pomiar"))
        self.label_AI_1.setText(_translate("Form", "Wskaźnik AI:"))

        self.label_KY_1.setText(_translate("Form", "Wskaźnik KY:"))

        self.label_Clarke_1.setText(_translate("Form", "Kąt Clarke\'a:"))

        self.label_Alfa_1.setText(_translate("Form", "Kąt alfa:"))

        self.label_gamma_1.setText(_translate("Form", "Kąt gamma:"))


        self.label_Alfa_2.setText(_translate("Form", "Kąt alfa:"))

        self.label_KY_2.setText(_translate("Form", "Wskaźnik KY:"))

        self.label_Clarke_2.setText(_translate("Form", "Kąt Clarke\'a:"))

        self.label_AI_2.setText(_translate("Form", "Wskaźnik AI:"))

        self.label_gamma_2.setText(_translate("Form", "Kąt gamma:"))

        self.buttonSVM1.setText(_translate("Form", "Wynik SVM"))
        self.button_SVM2.setText(_translate("Form", "Wynik SVM"))

    def displayImage(self, imageIN, label):
        image = cv2.resize(imageIN, (288, 432))
        height, width = image.shape
        image = QImage(image.data, width, height, QImage.Format_Grayscale8)
        label.setPixmap(QPixmap(image))



    def pomiar(self, Foot1):
        #Foot1 = Foot cenetered
        #AI parameter
        try:
            Foot1.findContour()
            Foot1.assingContour()
            Foot1.rotate(Foot1.toe2.extTop, Foot1.middle.extBot, secToe=True)
            Foot1.FootRotatedSecToeImage = Foot(in_image=Foot1.rotatedSecToe, desc='Image rotated second Toe', right=Foot1.right, left=Foot1.left)

            Foot1.FootRotatedSecToeImage.inheritFilter(Foot1)
            Foot1.FootRotatedSecToeImage.filterImage()
            Foot1.FootRotatedSecToeImage.findContour()
            Foot1.FootRotatedSecToeImage.assingContour()
            Foot1.FootRotatedSecToeImage.calculateLengthAndDivide(Foot1.FootRotatedSecToeImage.middle.extTop,
                                                                  Foot1.FootRotatedSecToeImage.middle.extBot)
            Foot1.FootRotatedSecToeImage.findContour()

            Foot1.FootRotatedSecToeImage.assignMiddleFootParts()
            Foot1.FootRotatedSecToeImage.AIclassify()

        except:
            pass
        finally:

            if Foot1.FootRotatedSecToeImage.right:
                if Foot1.FootRotatedSecToeImage.AI:
                    self.label_AI_2_result.setText(str(round(Foot1.FootRotatedSecToeImage.AI, 3)))
                else:
                    self.label_AI_2_result.setText("Nie udało się wyznaczyć tego parametru")

            else:
                if Foot1.FootRotatedSecToeImage.AI:
                    self.label_AI_1_result.setText(str(round(Foot1.FootRotatedSecToeImage.AI, 3)))
                else:
                    self.label_AI_1_result.setText("Nie udało się wyznaczyć tego parametru")

        try:
            Foot1.FootRotatedSecToeImage.midFoot.innerPoint(Foot1.FootRotatedSecToeImage.right,
                                                               Foot1.FootRotatedSecToeImage.left,
                                                               Foot1.FootRotatedSecToeImage.image)
            Foot1.FootRotatedSecToeImage.ClarkeAngle(Foot1.FootRotatedSecToeImage.image)

        except:
            pass
        finally:
            if Foot1.FootRotatedSecToeImage.right:
                if Foot1.FootRotatedSecToeImage.Clarke:
                    self.label_Clarke_2_result.setText(str(round(Foot1.FootRotatedSecToeImage.Clarke, 3)))
                else:
                    self.label_Clarke_2_result.setText("Nie udało się wyznaczyć tego parametru")

            else:
                if Foot1.FootRotatedSecToeImage.Clarke:
                    self.label_Clarke_1_result.setText(str(round(Foot1.FootRotatedSecToeImage.Clarke, 3)))
                else:
                    self.label_Clarke_1_result.setText("Nie udało się wyznaczyć tego parametru")

        try:
            if Foot1.FootRotatedSecToeImage.left:
                point1 = Foot1.FootRotatedSecToeImage.hindFoot.extRight
                point2 = Foot1.FootRotatedSecToeImage.foreFoot.extRight
            else:
                point1 = Foot1.FootRotatedSecToeImage.hindFoot.extLeft
                point2 = Foot1.FootRotatedSecToeImage.foreFoot.extLeft
            Foot1.FootRotatedSecToeImage.rotate(point1, point2, otrLine=True)

            Foot1.FootRotatedOtrLine = Foot(in_image=Foot1.FootRotatedSecToeImage.rotatedOtrLine,
                                               desc='image rotated line between outer points', left=Foot1.FootRotatedSecToeImage.left,
                                                right=Foot1.FootRotatedSecToeImage.right)
            Foot1.FootRotatedOtrLine.inheritFilter(Foot1.FootRotatedSecToeImage)
            Foot1.FootRotatedOtrLine.filterImage()
            Foot1.FootRotatedOtrLine.findContour()
            Foot1.FootRotatedOtrLine.assingContour()
            Foot1.FootRotatedOtrLine.calculateLengthAndDivide(Foot1.FootRotatedOtrLine.middle.extTop,
                                                                 Foot1.FootRotatedOtrLine.middle.extBot)
            Foot1.FootRotatedOtrLine.findContour()
            Foot1.FootRotatedOtrLine.assignMiddleFootParts()
            Foot1.FootRotatedOtrLine.midFoot.innerPoint(Foot1.FootRotatedOtrLine.right,
                                                           Foot1.FootRotatedOtrLine.left,
                                                           Foot1.FootRotatedOtrLine.image)
            Foot1.FootRotatedOtrLine.archWidth(Foot1.FootRotatedOtrLine.right, Foot1.FootRotatedOtrLine.left)
        except:
            pass
        finally:
            if Foot1.FootRotatedOtrLine.right:
                if Foot1.FootRotatedOtrLine.KY:
                    self.label_KY_2_result.setText(str(round(Foot1.FootRotatedOtrLine.KY, 3)))
                else:
                    self.label_KY_2_result.setText("Nie udało się wyznaczyć tego parametru")

            else:
                if Foot1.FootRotatedOtrLine.KY:
                    self.label_KY_1_result.setText(str(round(Foot1.FootRotatedOtrLine.KY, 3)))
                else:
                    self.label_KY_1_result.setText("Nie udało się wyznaczyć tego parametru")

        try:
            Foot1.FootRotatedOtrLine.fingerAngle(Foot1.FootRotatedOtrLine.right, Foot1.FootRotatedOtrLine.left)
        except:
            pass
        finally:
            if Foot1.FootRotatedOtrLine.right:
                if Foot1.FootRotatedOtrLine.alpha:
                    self.label_Alfa_2_result.setText(str(round(Foot1.FootRotatedOtrLine.alpha, 3)))
                else:
                    self.label_Alfa_2_result.setText("Nie udało się wyznaczyć tego parametru")

            else:
                if Foot1.FootRotatedOtrLine.alpha:
                    self.label_Alfa_1_result.setText(str(round(Foot1.FootRotatedOtrLine.alpha, 3)))
                else:
                    self.label_Alfa_1_result.setText("Nie udało się wyznaczyć tego parametru")
        try:
            Foot1.FootRotatedOtrLine.hindFoot.innerPoint(Foot1.FootRotatedOtrLine.right, Foot1.FootRotatedOtrLine.left, Foot1.FootRotatedOtrLine.image)
            Foot1.FootRotatedOtrLine.gamma()
        except:
            pass
        finally:
            if Foot1.FootRotatedOtrLine.right:
                if Foot1.FootRotatedOtrLine.gammaA:
                    self.label_gamma_2_result.setText(str(round(Foot1.FootRotatedOtrLine.gammaA, 3)))
                else:
                    self.label_gamma_2_result.setText("Nie udało się wyznaczyć tego parametru")

            else:
                if Foot1.FootRotatedOtrLine.gammaA:
                    self.label_gamma_1_result.setText(str(round(Foot1.FootRotatedOtrLine.gammaA, 3)))
                else:
                    self.label_gamma_1_result.setText("Nie udało się wyznaczyć tego parametru")

    def changeSliderValue2(self, value, attribute, Foot):
        new_value = int(value/255 * 255)
        if attribute == 'min_h':
            Foot.h_min = new_value
        elif attribute == 'min_s':
            Foot.s_min = new_value
        elif attribute == 'min_v':
            Foot.v_min = new_value

        Foot.filterImage()
        if Foot.right:
            label = self.labelImage2
        else:
            label = self.labelImage1
        self.displayImage(Foot.mask, label)

    def SVM_classify(self, right):
        if right:
            AI_result = self.label_AI_2_result.text()
            KY_result = self.label_KY_2_result.text()
        else:
            AI_result = self.label_AI_1_result.text()
            KY_result = self.label_KY_1_result.text()

        if AI_result !="Nie udało się wyznaczyć tego parametru" or KY_result !="Nie udało się wyznaczyć tego parametru":
            SVM_result = svm_classifier(AI_result, KY_result)

        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(12)
        self.SVM_result_1.setStyleSheet("color: red;")
        self.SVM_result_1.setFont(font)
        self.SVM_result_2.setStyleSheet("color: red;")
        self.SVM_result_2.setFont(font)




        if len(SVM_result) != 0:
            if SVM_result[0] == 0:
                if right:
                    self.SVM_result_2.setText("stopa wydrążona")
                else:
                    self.SVM_result_1.setText("stopa wydrążona")
            elif SVM_result[0] == 1:
                if right:
                    self.SVM_result_2.setText("stopa prawidłowa")
                else:
                    self.SVM_result_1.setText("stopa prawidłowa")
            elif SVM_result[0] == 2:
                if right:
                    self.SVM_result_2.setText("płaskostopie")
                else:
                    self.SVM_result_1.setText("płaskostoie")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_PhotoMsrmnt()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

