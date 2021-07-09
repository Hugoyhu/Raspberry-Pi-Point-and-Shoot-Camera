import sys
import os
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton, QWidget
import PyQt5.QtGui as qtgui
import PyQt5.QtCore as qtcore
import CameraController
import Constants

class ViewWidget(QWidget):
    BUTTON_WIDTH = 100

    def __init__(self):
        super().__init__()

        self.camera = CameraController.CameraController()
        self.camera.imageCaptureEventHandler = self.imageCaptureEventHandler

        return

    def startWindow(self, resolution):

        # create UI
        width = resolution.width()
        height = resolution.height()

        xOffset = 0

        leftButton = QPushButton('<', self)
        leftButton.pressed.connect(self.mediaViewerLeftButton)
        leftButton.resize(ViewWidget.BUTTON_WIDTH, height)
        leftButton.move(xOffset, 0)
        xOffset += leftButton.width()

        self.imageLabel = QLabel(self)
        self.imageLabel.resize(width - 2*ViewWidget.BUTTON_WIDTH, height)
        self.imageLabel.move(xOffset, 0)
        self.imageLabel.setAlignment(qtcore.Qt.AlignCenter)
        self.imageLabel.mouseDoubleClickEvent = self.doubleClickEventHandler
        xOffset += self.imageLabel.width()

        rightButton = QPushButton('>', self)
        rightButton.pressed.connect(self.mediaViewerRightButton)
        rightButton.resize(ViewWidget.BUTTON_WIDTH, height)
        rightButton.move(xOffset, 0)


        # TODO: Add sync for Multithreading
        self.mediaList = os.listdir(Constants.IMAGE_FOLDER_PATH)
        self.mediaList.sort()
        self.index = len(self.mediaList)

        self.displayStill(self.index-1)

        self.showMaximized()

        return

    def mediaViewerLeftButton(self):
        if len(self.mediaList) == 0:
            return

        if self.index > 1:
            # loading image
            self.index -= 1

            # adding image to label

            self.displayStill(self.index-1)

    def mediaViewerRightButton(self):
        if len(self.mediaList) == 0:
            return

        if self.index < len(self.mediaList):
            # loading image
            self.index += 1

            # adding image to label

            self.displayStill(self.index-1)

    # requires a valid index; otherwise it will do nothing
    def displayStill(self, index):
        if index < 0:
            return

        if index > len(self.mediaList) -1:
            return

        imgFileName = os.path.join(Constants.IMAGE_FOLDER_PATH, self.mediaList[index])
        piximage = qtgui.QPixmap(imgFileName)
        piximage = piximage.scaled(qtcore.QSize(self.imageLabel.size()), qtcore.Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(piximage)

    def doubleClickEventHandler(self, e):
        self.close()

    def closeWindow(self):
        self.close()

    def imageCaptureEventHandler(self, fileName):
        self.mediaList.append(fileName)
