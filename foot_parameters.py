import math

import cv2
import numpy as np

from image import Photo_Legit


class PartFoot():
    def __init__(self, dsc, contours):
        self.dsc = dsc
        self.contours = contours
        self.extBot = None
        self.extTop = None
        self.extLeft = None
        self.extRight = None
        self.innerPt = None
        self.findExtremePoint()

    def findExtremePoint(self):
        self.extLeft = tuple(self.contours[self.contours[:, :, 0].argmin()][0])
        self.extRight = tuple(self.contours[self.contours[:, :, 0].argmax()][0])
        self.extTop = tuple(self.contours[self.contours[:, :, 1].argmin()][0])
        self.extBot = tuple(self.contours[self.contours[:, :, 1].argmax()][0])

    def draw(self, image):
        cv2.drawContours(image, self.contours, -1, (0, 255, 255), 2)


    def drawExtreme(self, image, left=True, right=True, top=True, bot=True):
        if(right):
            cv2.circle(image, self.extLeft, 5, (255, 255, 255), -1)
        if(left):
            cv2.circle(image, self.extRight, 5, (255, 255, 255), -1)
        if(bot):
            cv2.circle(image, self.extBot, 5, (255, 255, 255), -1)
        if(top):
            cv2.circle(image, self.extTop, 5, (255, 255, 255), -1)

    def innerPoint(self, right, left, image):

        if right == True:
            global_x = (0,0)
            for i in range(self.extTop[1], self.extBot[1]):
                index = np.where(self.contours[:,:, 1] == i)
                local_max = (1000,0)
                for x in index[0]:
                    if self.contours[x][0][0] < local_max[0]:
                        local_max = (self.contours[x][0][0], self.contours[x][0][1])
                if local_max[0] > global_x[0]:
                    global_x = local_max

        if left == True:
            global_x = (1000,0)
            for i in range(self.extTop[1], self.extBot[1]):
                index = np.where(self.contours[:,:, 1] == i)
                local_max = (0,0)
                for x in index[0]:
                    if self.contours[x][0][0] > local_max[0]:
                        local_max = (self.contours[x][0][0], self.contours[x][0][1])
                if local_max[0] < global_x[0]:
                    global_x = local_max

        self.innerPt = global_x
        cv2.circle(image, self.innerPt, 5, (255, 255, 255), -1)

class Foot(Photo_Legit):
    def __init__(self, desc, path=None, in_image=None, left=False, right=False):
        Photo_Legit.__init__(self, desc, path, in_image)
        self.left = left
        self.right = right
        self.centered = None
        self.rotatedSecToe = None
        self.rotatedSecLine = None
        self.rotatedOtrLine = None
        self.maxContour = None
        self.middle = None
        self.toe1 = None
        self.toe2 = None
        self.toe3 = None
        self.toe4 = None
        self.foreFoot = None
        self.midFoot = None
        self.hindFoot = None
        self.AI = None
        self.KY = None

    def show(self, image=False, mask=False, centered=False, rotatedScToe=False, rotatedOuLine=False):
        dispImg = []
        if image:
            dispImg.append((self.image, 'image'))
        if mask:
            dispImg.append((self.mask, 'mask'))
        if centered:
            dispImg.append((self.centered, 'centered'))
        if rotatedScToe:
            dispImg.append((self.rotatedSecToe, 'rotated by second Toe'))

        if rotatedOuLine:
            dispImg.append((self.rotatedOtrLine,  'rotated by outer Line'))

        if not dispImg:
            pass
        else:
            for img, desc in dispImg:
                cv2.imshow(self.desc+' '+desc, img)
            cv2.waitKey()
            cv2.destroyAllWindows()

    def findMaxContour(self):
        c = max(self.contours, key=cv2.contourArea)
        self.maxContour = c

    def centerImage(self):
        # oblicza macierz obortu i obraca XD
        maxy = self.topPoint[1]  # y
        miny = self.bottomPoint[1]  # y
        maxx = self.rightPoint[0]  # x
        minx = self.leftPoint[0]  # x
        cx = (maxx + minx) / 2
        cy = (maxy + miny) / 2

        tx = self.col / 2 - cx
        ty = self.rows / 2 - cy

        M = np.float32([[1, 0, tx], [0, 1, ty]])
        dst = cv2.warpAffine(self.image, M, (self.col, self.rows))
        self.centered = dst

    def drawExtreme(self):
        cv2.circle(self.image, self.leftPoint, 4, (255, 255, 255), -1)
        cv2.circle(self.image, self.rightPoint, 4, (255, 255, 255), -1)
        cv2.circle(self.image, self.bottomPoint, 4, (255, 255, 255), -1)
        cv2.circle(self.image, self.topPoint, 4, (255, 255, 255), -1)

    def assingContour(self):
        try:
            newContours =[]
            for i in range(len(self.contours)):
                if(len(self.contours[i])>6):
                    newContours.append(self.contours[i])
            self.contours = newContours
            self.contours.sort(key=cv2.contourArea, reverse=True)
            middle = PartFoot(contours=self.contours[0], dsc='Środkowa część stopy')
            self.middle = middle

            toe1 = PartFoot(contours=self.contours[1], dsc='Pierwszy palec')
            self.toe1 = toe1

            toe2 = PartFoot(contours=self.contours[2], dsc='Drugi palec')
            self.toe2= toe2

            toe3 = PartFoot(contours=self.contours[3], dsc='Trzeci palec')
            self.toe3 = toe3

            if (len(self.contours) > 4):
                toe4 = PartFoot(contours=self.contours[4], dsc='Czwarty palec')
                self.toe4 = toe4

            if(len(self.contours)>5):
                toe5 = PartFoot(contours=self.contours[5], dsc='Piąty palec')
                self.toe5 = toe5
        except:
            pass

    def rotateAngle(self, omega):
        M = cv2.getRotationMatrix2D((self.col / 2, self.rows / 2), omega, 1)
        rotated = cv2.warpAffine(self.image, M, (self.col, self.rows))
        self.rotated = rotated

    def rotate (self, point1, point2, secToe=False, otrLine=False, secLine=False, x=False):
        rows, cols, _ = self.image.shape
        maxy = point1[1]  # y2
        maxx = point1[0]  # x2
        miny = point2[1]  # y1
        minx = point2[0]  # x1
        omega = math.degrees(math.atan((maxx - minx) / (maxy - miny)))

        omega = omega * (-1)

        M = cv2.getRotationMatrix2D((self.col / 2, self.rows / 2), omega, 1)
        rotated = cv2.warpAffine(self.image, M, (self.col, self.rows))
        if(secToe):
            self.rotatedSecToe = rotated
        if (otrLine):
            self.rotatedOtrLine = rotated
        if secLine:
            self.rotatedSecLine = rotated

    def calculateLengthAndDivide(self, point1, point2):
        dist = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        part = dist / 3
        index = np.where(self.middle.contours == int(point1[1] + part))
        index2 = np.where(self.middle.contours == int(point1[1] + part * 2))  # dla 2 punktów niżej szukamy indeksu dla którego y są równe

        index11 = index[0][0]
        index12 = index[0][1]  # indeks drugiego punktu w pierwszej częśći stopy

        index21 = index2[0][0]  # indeks pierwszego  punktu w 2 części stopy
        index22 = index2[0][1]

        point11 = tuple(self.middle.contours[index11][0])
        point12 = tuple(self.middle.contours[index12][0])

        point21 = tuple(self.middle.contours[index21][0])
        point22 = tuple(self.middle.contours[index22][0])

        cv2.line(self.mask, point11, point12, (0, 0, 0), 2)
        cv2.line(self.mask, point21, point22, (0, 0, 0), 2)
        #self.show(mask=True)

    def assignMiddleFootParts(self):
        lengthContour = []
        for c in self.contours:
            lengthContour.append((len(c), np.mean(c[:,0,1]), c))

        lengthContour.sort(key=lambda item: item[0], reverse=True)
        lengthContour = lengthContour[0:3]
        lengthContour.sort(key=lambda item: item[1])

        self.foreFoot = PartFoot(contours=lengthContour[0][2], dsc='Górna część środkowa stopy')
        self.hindFoot = PartFoot(contours=lengthContour[2][2], dsc='Dolna część stopy')
        self.midFoot = PartFoot(contours=lengthContour[1][2],  dsc="Środek środka stopy")

    def AIclassify(self):
        self.AI = (cv2.contourArea(self.midFoot.contours)) / (cv2.contourArea(self.foreFoot.contours) + cv2.contourArea(self.midFoot.contours) + cv2.contourArea(self.hindFoot.contours))

        if self.AI < 0.21:
            self.AIresult = 'high arch'
        elif self.AI > 0.26:
            self.AIresult = 'low arch'
        else:
            self.AIresult = 'normal arch'
        self.AI = self.AI

    def ClarkeAngle(self,image):

        if self.left == True:
            in1 = self.midFoot.innerPt
            out1 = self.foreFoot.extRight
            out2 = self.hindFoot.extRight
        if self.right == True:
            in1 = self.midFoot.innerPt
            out1 = self.foreFoot.extLeft
            out2 = self.hindFoot.extLeft


        distS = math.sqrt((out1[0] - in1[0]) ** 2 + (out1[1] - in1[1]) ** 2)
        distT = math.sqrt((out1[0] - out2[0]) ** 2 + (out1[1] - out2[1]) ** 2)
        distF = math.sqrt((out2[0] - in1[0]) ** 2 + (out2[1] - in1[1]) ** 2)

        clarkeAngle = math.acos((distF**2 - distT**2 - distS**2)/(-2*distT*distS))
        clarkeAngle= clarkeAngle* 180/math.pi

        self.Clarke = clarkeAngle

    def archWidth(self, right=False, left=False):
        point3 = (0, 0)
        point4 = (0, 0)
        if right:
            point1 = self.foreFoot.extLeft
            point2 = self.hindFoot.extLeft
        if left:
            point1 = self.foreFoot.extRight
            point2 = self.hindFoot.extRight

        y = int((point2[1] - point1[1]) / 2) + point1[1]
        newPoint = (point1[0], y)
        index = np.where(self.midFoot.contours[:, :, 1] == y)
        if left:
            x1 = index[0][0]
            x2 = index[0][1]
            point3 = min(self.midFoot.contours[x1][0][0], self.midFoot.contours[x2][0][0])
            point4 = max(self.midFoot.contours[x1][0][0], self.midFoot.contours[x2][0][0])

        if right:
            x1 = index[0][0]
            x2 = index[0][1]
            point3 = max(self.midFoot.contours[x1][0][0], self.midFoot.contours[x2][0][0])
            point4 = min(self.midFoot.contours[x1][0][0], self.midFoot.contours[x2][0][0])

        pointA = newPoint
        pointB = (point3, y)
        pointC = (point4, y)
        cv2.circle(self.image, pointC, 8, (255, 255, 255), -1)
        cv2.circle(self.image, pointB, 8, (255, 255, 255), -1)
        cv2.circle(self.image, pointA, 8, (255, 255, 255), -1)



        distAB = math.sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)
        distBC = math.sqrt((pointB[0] - pointC[0]) ** 2 + (pointB[1] - pointC[1]) ** 2)

        kyInd = distBC / distAB
        self.KY = kyInd


    def fingerAngle(self, right, left):
        point1 = (0,0)
        point2 = (0,0)
        if left:
            point1 = self.toe1.extRight
            point2 = self.foreFoot.extRight
        if right:
            point1 = self.toe1.extLeft
            point2 = self.foreFoot.extLeft

        point1 = (point1[0], point1[1]-10)
        point3 = point2[0], point1[1]

        cv2.line(self.image, point3, point1, (255, 0, 255), 1)
        cv2.line(self.image, point2, point3, (255, 0, 255), 1)
        cv2.line(self.image, point2, point1, (255, 0, 255), 1)

        dist12 = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        dist23 = math.sqrt((point2[0] - point3[0]) ** 2 + (point2[1] - point3[1]) ** 2)
        dist13 = math.sqrt((point1[0] - point3[0]) ** 2 + (point1[1] - point3[1]) ** 2)

        fingAngle = math.acos((dist13**2 - dist23**2 - dist12**2)/(-2*dist23*dist12))
        fingAngle= fingAngle* 180/math.pi
        self.alpha = fingAngle

    def line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])  # Typo was here

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div


        return x, y

    def gamma(self):
        point1 = self.foreFoot.extLeft
        point2 = self.foreFoot.extRight
        point3 = self.hindFoot.extLeft
        point4 = self.hindFoot.extRight

        cv2.circle(self.image, point1, 5, (255, 255, 255), -1)
        cv2.circle(self.image, point2, 5, (255, 255, 255), -1)
        cv2.circle(self.image, point3, 5, (255, 255, 255), -1)
        cv2.circle(self.image, point4, 5, (255, 255, 255), -1)
        #
        cv2.line(self.image, point3, point1, (255, 255, 255), 1)
        cv2.line(self.image, point2, point4, (255, 255, 255), 1)
        cv2.line(self.image, point2, point1, (255, 255, 255), 1)

        (x,y) = self.line_intersection((point1,point3), (point2, point4))
        point5 = (int(x), int(y))


        dist12 = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        dist15 = math.sqrt((point1[0] - point5[0]) ** 2 + (point1[1] - point5[1]) ** 2)
        dist25 = math.sqrt((point2[0] - point5[0]) ** 2 + (point2[1] - point5[1]) ** 2)

        gamma = math.acos((dist12 ** 2 - dist15 ** 2 - dist25 ** 2) / (-2 * dist15 * dist25))
        gamma = gamma * 180 / math.pi
        self.gammaA = gamma
