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

    def histogram(self):
        img = np.asarray(self.image)
        flat = img.flatten()
        hist = np.zeros(256)
        for pixel in flat:
            hist[pixel] += 1
        a = iter(hist)
        b = [next(a)]
        for i in a:
            b.append(b[-1] + i)
        cs = np.array(b)
        nj = (cs - cs.min()) * 255
        N = cs.max() - cs.min()
        cs = nj / N
        cs = cs.astype('uint8')
        img_new = cs[flat]
        img_new = np.reshape(img_new, img.shape)
        return img_new

    # --- New Functions can be added under here ---#
