import numpy as np
import cv2


class ImageEnhancement():

    def __init__(self, image):
        super().__init__()
        self.image = image

    def inverse_image(self):
        new_image = cv2.bitwise_not(self.image)
        return new_image

    def adjust_brightness_contrast(self, brightness, contrast):
        new_image = cv2.addWeighted(
            self.image, contrast, self.image, 0, brightness)
        return new_image

    #--- New Functions can be added under here ---#
