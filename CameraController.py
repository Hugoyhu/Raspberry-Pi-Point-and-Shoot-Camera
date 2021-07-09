from picamera import PiCamera
from gpiozero import Button
import datetime
import os
import Constants

class CameraController:

    def __init__(self):
        # Button control
        self.softwareButton = Button(17)
        self.imageButton = Button(22)
        self.videoButton = Button(23)

        # create instance of picamera
        self.camera = PiCamera()
        self.camera.framerate = 15

        # register event handlers
        self.imageButton.when_released = self.captureStill
        self.softwareButton.when_released = self.previewCamera
        self.videoButton.when_released = self.captureVideo

        # register camera settings
        self.videoStatus = False
        self.previewStatus = False
        self.imagePreviewStatus = False

        self.imageCaptureEventHandler = None

    def captureStill(self):
        # set resolution to 5K
        previewWasOn = False
        if self.camera.preview:
            self.camera.stop_preview()
            previewWasOn = True

        # save default camera resolution
        defRes = self.camera.resolution

        self.camera.resolution = (4056, 3040)

        # determine file name

        fileName = "IMG-" + datetime.datetime.now().isoformat() + ".jpg"
        filePath = os.path.join(Constants.IMAGE_FOLDER_PATH, fileName)

        # capture to file
        self.camera.capture(filePath)

        # restore default camera resolution
        self.camera.resolution = defRes

        if previewWasOn:
            self.camera.start_preview(alpha=255, fullscreen=True, window=(0,0,320,240))

        if self.imageCaptureEventHandler is not None:
            self.imageCaptureEventHandler(fileName)

        return

    def previewCamera(self):
        if not self.camera.preview:
            self.camera.start_preview(alpha=255, fullscreen=True, window=(0,0,320,240))
        else:
            self.camera.stop_preview()

        self.previewStatus = not self.previewStatus
        return

    def captureVideo(self):
        if self.videoStatus:
            self.camera.stop_recording()
        else:
            # set resolution to 720p
            previewWasOn = False
            if self.camera.preview:
                self.camera.stop_preview()
                previewWasOn = True

            defRes = self.camera.resolution

            self.camera.resolution = (720, 480)

            # determine file name

            fileName = "VID-" + datetime.datetime.now().isoformat() + ".h264"
            filePath = os.path.join(Constants.VIDEO_FOLDER_PATH, fileName)

            # capture to file
            self.camera.start_recording(filePath)

            self.camera.resolution = defRes

            if previewWasOn:
                self.camera.start_preview(alpha=255, fullscreen=True, window=(0,0,320,240))

        self.videoStatus = not self.videoStatus


