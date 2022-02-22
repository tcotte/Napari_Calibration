import os
import cv2
import numpy as np
from IPython.external.qt_for_kernel import QtGui
from PyQt5.QtGui import QKeySequence, QIcon, QPixmap
from PyQt5.QtWidgets import *
from typing import Final

from main import pixel_per_mm


CALIBRATION_FOLDER: Final = r"C:\Users\tristan_cotte\PycharmProjects\calibration\Calibration\Files"
CALIBRATION_FILE: Final = os.path.join(r"C:\Users\tristan_cotte\PycharmProjects\calibration\Calibration\Files", "out.txt")


def get_calibration():
    with open(CALIBRATION_FILE) as f:
        lines = f.readlines()

    # print(lines)
    # print(lines[0].strip(" : "))
    mm = lines[0].split(" : ")[-1].replace("\n", "")
    px = lines[1].split(" : ")[-1]

    return float(mm), float(px)




def compute_distance(line):
    [[x1, y1], [x2, y2]] = line
    width = px_distance(x1, x2, y1, y2)

    mm, px = get_calibration()
    ratio = pixel_per_mm(px, mm)
    real_width = width / ratio
    return real_width


def px_distance(x1, x2, y1, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Form(QDialog):
    # constructor
    def __init__(self, viewer):
        super(Form, self).__init__()
        self.viewer = viewer
        # self.lines = lines

        self.display()
        self.connect_actions()

    def display(self):
        # setting window title
        self.setWindowTitle("Form")

        # setting geometry to the window
        self.setGeometry(100, 100, 250, 800)

    def connect_actions(self):
        """
        Events
        """
        # event data appeared when a rectangle is created (when user clicks before drag the mouse) or removed
        # if 'Shapes' in self.viewer.layers:
        # self.viewer.layers['lines'].events.data.connect(self.get_data)
        self.viewer.layers['lines'].events.set_data.connect(self.get_data)
        # event set_data appeared when any rectangle coordinate changed

    def get_data(self):
        print("ok")
        print(self.viewer.layers['lines'].data)

        for line in self.viewer.layers['lines'].data:
            print(compute_distance(line))

    # def add_line(self):
    #     print(self.viewer.layers['lines'].data)
