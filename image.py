import cv2
import numpy as np

class Photo_Legit:
    def __init__(self,  desc=None, path=None, in_image=None):
        self.desc = desc
        if path is None:
            if in_image is not None:
                self.image = in_image
            else:
                print('Error, no image')
        else:
            self.image = cv2.imread(path, cv2.IMREAD_COLOR)
        self.rows = self.image.shape[0]
        self.col = self.image.shape[1]
        self.mask = None
        self.contours = None
        self.extremes = None
        self.bottomPoint = None
        self.topPoint = None
        self.rightPoint = None
        self.leftPoint = None
        self.rightFoot = None
        self.leftPoint = None
        self.allContourPoints = None
        self.h_min = 132
        self.h_max = 255
        self.s_min = 0
        self.s_max = 255
        self.v_min = 13
        self.v_max = 255

    def show(self):
        cv2.imshow(self.desc, self.image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def inheritFilter(self, second):
        self.h_min = second.h_min
        self.h_max = second.h_max
        self.s_min = second.s_min
        self.s_max = second.s_max
        self.v_min = second.v_min
        self.v_max = second.v_max

    def showMask(self):
        cv2.imshow('mask '+self.desc, self.mask)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def filterImage(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        normal = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        lower_red = np.array([self.h_min, self.s_min, self.v_min])
        upper_red = np.array([self.h_max, self.s_max, self.v_max])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        mask = cv2.medianBlur(mask, 3)
        self.mask = mask

    def drawCnts(self, mask=False, image=False ):
        if (mask):
            pass
        if (image):
            cv2.drawContours(self.image, self.contours, -1, (0, 255, 255), 2)

    def findContour(self):
        _, cnts, _ = cv2.findContours(self.mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        self.contours = cnts

    def findExtremePoints(self):
        self.extremes = []
        self.allContourPoints = []
        if len(self.contours) > 1:
            for c in self.contours:
                if len(c > 10):
                    for i in range(len(c)):
                        self.allContourPoints.append([c[i][0][0], c[i][0][0]])
                    extLeft = tuple(c[c[:, :, 0].argmin()][0])
                    extRight = tuple(c[c[:, :, 0].argmax()][0])
                    extTop = tuple(c[c[:, :, 1].argmin()][0])
                    extBot = tuple(c[c[:, :, 1].argmax()][0])

                    self.extremes.append(extLeft)
                    self.extremes.append(extRight)
                    self.extremes.append(extTop)
                    self.extremes.append(extBot)

        else:
            extLeft = tuple(self.contours[self.contours[:, :, 0].argmin()][0])
            extRight = tuple(self.contours[self.contours[:, :, 0].argmax()][0])
            extTop = tuple(self.contours[self.contours[:, :, 1].argmin()][0])
            extBot = tuple(self.contours[self.contours[:, :, 1].argmax()][0])

            self.extremes.append(extLeft)
            self.extremes.append(extRight)
            self.extremes.append(extTop)
            self.extremes.append(extBot)

        self.bottomPoint = max(self.extremes, key=lambda item: item[1])
        self.topPoint = min(self.extremes, key=lambda item: item[1])
        self.rightPoint = max(self.extremes, key=lambda item: item[0])
        self.leftPoint = min(self.extremes, key=lambda item: item[0])

    def centerMatrix(self):
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
        return dst

    def divideImage(self):
        y = int(self.image.shape[1] / 2)
        center = y
        for i in range(0, y):
            if i+y not in np.asarray(self.allContourPoints)[:,1]:
                center = y+i
                break
            elif y-i not in np.asarray(self.allContourPoints)[:,1]:
                center = y-i
                break
        rightFoot = self.image.copy()
        rightFoot[0:int(self.rows), 0:center] = (0, 0, 0)
        self.rightFoot = rightFoot

        leftFoot = self.image.copy()
        leftFoot[0:int(self.rows), center:self.col] = (0, 0, 0)
        self.leftFoot = leftFoot
