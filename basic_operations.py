import numpy as np
import cv2
from PIL import Image

class BasicOperations():

    def __init__(self, image):
        super().__init__()
        self.image = image

    # rotate with PIL
    # def rotate(self, degrees_to_rotate):
    #    image_obj = Image.open(self)
    #    rotated_image = image_obj.rotate(degrees_to_rotate)
    #    return rotated_image

    def rotate_image_90(self):
        new_image = cv2.rotate(self.image, cv2.cv2.ROTATE_90_CLOCKWISE)
        return new_image

    def rotate_image_180(self):
        new_image = cv2.rotate(self.image, cv2.cv2.ROTATE_180)
        return new_image

    def rotate_image_270(self):
        new_image = cv2.rotate(self.image, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        return new_image

    def flip_image_vertical(self):
        new_image = cv2.flip(self.image, 0)
        return new_image

    def flip_image_horizontal(self):
        new_image = cv2.flip(self.image, 1)
        return new_image

    def flip_image_horizontal_vertical(self):
        new_image = cv2.flip(self.image, -1)
        return new_image

    def resize_image(self):
        scale = 50  # percent of original size
        width = self.image.shape[1]
        height = int(self.image.shape[0] * scale / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)
        return resized

    # --- New Functions can be added under here ---#
