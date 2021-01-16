import scipy.interpolate as inter
import numpy as np
import cv2


class EffectsFilters():

    def __init__(self, image):
        super().__init__()
        self.image = image

    def all_effects(self):
        black_and_white = self.black_and_white()
        watercolor = self.watercolor()
        painters_hand = self.painters_hand()  # issue here !
        pen_sketch_gray = self.pen_sketch_gray()
        pen_sketch_colored = self.pen_sketch_colored()
        sepia = self.sepia()
        gaussian_blur = self.gaussian_blur()
        median_blur = self.median_blur()
        emboss = self.emboss()
        thermal = self.thermal_effect()
        chilly = self.chilly_effect()
        edge_preserving = self.edge_preserving()
        sharpen = self.sharpen()
        images = {
            "Black and White": black_and_white,
            "Watercolor": watercolor,
            "Pen Skecth with Gray": pen_sketch_gray,
            "Pen Skecth with Color": pen_sketch_colored,
            "Painter's Hand": painters_hand,
            "Sepia": sepia,
            "Gaussian Blur": gaussian_blur,
            "Median Blur": median_blur,
            "Emboss": emboss,
            "Thermal": thermal,
            "Chilly": chilly,
            "Edge Preserving": edge_preserving,
            "Sharpen": sharpen
        }
        return images

    def black_and_white(self):
        new_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return new_image

    def watercolor(self):
        new_image = cv2.stylization(self.image, sigma_s=60, sigma_r=0.6)
        return new_image

    def painters_hand(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
        morph = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
        new_image = cv2.normalize(morph, None, 20, 255, cv2.NORM_MINMAX)
        return new_image

    def pen_sketch_gray(self):
        new_image, _ = cv2.pencilSketch(
            self.image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        return new_image

    def pen_sketch_colored(self):
        _, new_image = cv2.pencilSketch(
            self.image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        return new_image

    def sepia(self):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(self.image, kernel)
        sepia[np.where(sepia > 255)] = 255  # normalizing
        return sepia

    def gaussian_blur(self):
        new_image = cv2.GaussianBlur(self.image, (35, 35), 0)
        return new_image

    def median_blur(self):
        new_image = cv2.medianBlur(self.image, 41)
        return new_image

    def emboss(self):
        kernel = np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]])
        new_image = cv2.filter2D(self.image, -1, kernel)
        return new_image

    # using this method in warm, cool effects
    def spread_table(self, x, y):
        spline = inter.UnivariateSpline(x, y)
        return spline(range(256))

    def thermal_effect(self):  # could be warm_effect ! there is an issue
        decrease_table = self.spread_table(
            [0, 64, 128, 256], [0, 80, 160, 256])
        increase_table = self.spread_table(
            [0, 64, 128, 256], [0, 50, 100, 256])

        red_channel, green_channel, blue_channel = cv2.split(self.image)
        red_channel = cv2.LUT(red_channel, increase_table).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, decrease_table).astype(np.uint8)

        new_image = cv2.merge((red_channel, green_channel, blue_channel))
        return new_image

    def chilly_effect(self):  # could be cool_effect ! there is an issue
        decrease_table = self.spread_table(
            [0, 64, 128, 256], [0, 80, 160, 256])
        increase_table = self.spread_table(
            [0, 64, 128, 256], [0, 50, 100, 256])

        red_channel, green_channel, blue_channel = cv2.split(self.image)
        red_channel = cv2.LUT(red_channel, decrease_table).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, increase_table).astype(np.uint8)

        new_image = cv2.merge((red_channel, green_channel, blue_channel))
        return new_image

    def edge_preserving(self):
        new_image = cv2.edgePreservingFilter(
            self.image, flags=1, sigma_s=60, sigma_r=0.4)
        return new_image

    def sharpen(self):
        new_image = cv2.detailEnhance(self.image, sigma_s=10, sigma_r=0.15)
        return new_image

    #--- New Functions can be added under here ---#
