import os
import cv2
import numpy as np
from IPython.external.qt_for_kernel import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from typing import Final


def compute_distance(line):
    [[x1, y1], [x2, y2]] = line
    width = px_distance(x1, x2, y1, y2)
    return width


def px_distance(x1, x2, y1, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Form(QDialog):
    # constructor
    def __init__(self, viewer):
        super(Form, self).__init__()

        # Qt form
        grid_layout = QGridLayout()

        self.filename_box = QLineEdit()
        label = QLabel("Output file")
        self.save_btn = QPushButton("Save")
        self.save_btn.setEnabled(False)
        self.points_box = QLineEdit()

        grid_layout.setAlignment(Qt.AlignTop)
        grid_layout.setVerticalSpacing(30)
        grid_layout.addWidget(label, 0, 0, 1, 1)
        grid_layout.addWidget(self.filename_box, 0, 1, 1, 1)

        grid_layout.setVerticalSpacing(30)

        grid_layout.addWidget(QLabel("Real distance (mm)"), 1, 0, 2, 1)
        grid_layout.addWidget(self.points_box, 1, 1, 2, 1)

        grid_layout.setVerticalSpacing(30)
        grid_layout.addWidget(self.save_btn, 2, 0, 3, 3)

        self.setLayout(grid_layout)

        self.viewer = viewer
        # self.lines = lines
        self.display()

        self.connect_actions()

    def display(self):
        # setting window title
        self.setWindowTitle("Calibration")

        # setting geometry to the window
        self.setGeometry(100, 100, 100, 200)

    def connect_actions(self):
        """
        Events
        """
        self.viewer.layers['lines'].events.set_data.connect(self.get_data)
        self.filename_box.textChanged.connect(self.possible_save)
        self.viewer.layers['lines'].events.set_data.connect(self.possible_save)
        self.save_btn.clicked.connect(self.save)

    def get_data(self):
        print(self.viewer.layers['lines'].data)

    def possible_save(self):
        print(len(self.viewer.layers['lines'].data))
        # mm = int(self.points_box.text())

        if self.filename_box.text() != "" and len(self.viewer.layers['lines'].data) != 0 and self.points_box.text() != "":
            self.save_btn.setEnabled(True)
        else:
            self.save_btn.setEnabled(False)

    def save(self):
        # if len(self.viewer.layers['lines'].data) != 1:
        line = self.viewer.layers['lines'].data[-1]
        # else:
        #     line = self.viewer.layers['lines'].data

        nb_px = compute_distance(line)
        with open(os.path.join(r"C:\Users\tristan_cotte\PycharmProjects\calibration\Calibration\Files", self.filename_box.text()+".txt"), 'w') as f:
            f.write("Millimeters : " + self.points_box.text()+"\n")
            f.write("Pixels : " + str(nb_px))
