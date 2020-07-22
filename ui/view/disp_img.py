from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DispImg:
    def __init__(self):
        self.img()

    def img(self, img_path=None):
        self.frame = QWidget()
        self.label_Image = QLabel(self.frame)
        self.image_path = img_path  # path to your image file
        self.image_profile = QImage(self.image_path)  # QImage object
        self.image_profile = self.image_profile.scaled(250, 250, aspectRatioMode=Qt.KeepAspectRatio,
                                             transformMode=Qt.SmoothTransformation)  # To scale image for example and keep its Aspect Ratio
        self.label_Image.setPixmap(QPixmap.fromImage(self.image_profile))
