import numpy as np
import cv2

from app import VALUES


class efp:

    def __init__(self):
        self.contours = None
        self.images_mask = None

    def read_data(self):
        data_path = 'Images/Layers/mtr_'
        self.contours = cv2.imread('static/Images/mtr_contours.png', cv2.IMREAD_UNCHANGED)
        self.images_mask = {label: cv2.imread(data_path + label + '.png', cv2.IMREAD_UNCHANGED)[:, :, 3] for label in VALUES.img_labels}

    def get_contours(self):
        return self.contours

    def generate_efp(self, experiment, mode):
        for label in VALUES.img_labels:
            self.set_colour(label, [255, 164, 0, 255])

    def set_colour(self, label, colour):
        self.contours[np.where(self.images_mask[label] != 0)] = colour
