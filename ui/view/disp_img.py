from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

class DispImg:
    def __init__(self, *img_path):
        self.img(img_path)
    def img(self, *img_path):
        self.frame = QWidget()
        self.label_Image = QLabel(self.frame)
        self.image_path = r'C:\Users\Sameer\Desktop\Comic\img\thumbnails\Dead Rabbit.jpg'  # path to your image file
        print(img_path[0])
        self.image_profile = QImage(self.image_path)  # QImage object
        self.image_profile = self.image_profile.scaled(250, 250, aspectRatioMode=Qt.KeepAspectRatio,
                                             transformMode=Qt.SmoothTransformation)  # To scale image for example and keep its Aspect Ratio
        self.label_Image.setPixmap(QPixmap.fromImage(self.image_profile))
