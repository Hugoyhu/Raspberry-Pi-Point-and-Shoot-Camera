import ViewWidget
from PyQt5.QtWidgets import QApplication
import sys
import Constants
import os

#
# Local Utils
#

def initialize():
    if not os.path.isdir(Constants.VIDEO_FOLDER_PATH):
        os.makedirs(Constants.VIDEO_FOLDER_PATH)

    if not os.path.isdir(Constants.IMAGE_FOLDER_PATH):
        os.makedirs(Constants.IMAGE_FOLDER_PATH)

    return

#
# Main Program
#

initialize()

app = QApplication(sys.argv)
resolution = app.desktop().size()

window = ViewWidget.ViewWidget()
window.startWindow(resolution)

sys.exit(app.exec_())
