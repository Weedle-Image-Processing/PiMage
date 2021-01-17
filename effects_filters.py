import scipy.interpolate as inter
import numpy as np
import cv2


class EffectsFilters():

    def __init__(self, image):
        super().__init__()
        self.image = image

    def all_effects(self):
        pink_dream = self.pink_dream()
        painters_hand = self.painters_hand()
        summer_sunset = self.summer_sunset()
        toony = self.toony()
        cyberpunk_neon = self.cyberpunk_neon()
        gaussian_blur = self.gaussian_blur()
        median_blur = self.median_blur()
        emboss = self.emboss()
        thermal = self.thermal_effect()
        chilly = self.chilly_effect()
        edge_preserving = self.edge_preserving()
        sharpen = self.sharpen()
        images = {
            "Pink Dream": pink_dream,
            "Painter's Hand": painters_hand,
            "Summer Sunset": summer_sunset,
            "Toony": toony,
            "Cyberpunk Neon": cyberpunk_neon,
            "Gaussian Blur": gaussian_blur,
            "Median Blur": median_blur,
            "Emboss": emboss,
            "Thermal": thermal,
            "Chilly": chilly,
            "Edge Preserving": edge_preserving,
            "Sharpen": sharpen,
        }
        return images

    def pink_dream(self):
        new_image = cv2.applyColorMap(self.image, cv2.COLORMAP_PINK)
        new_image = cv2.stylization(new_image, sigma_s=60, sigma_r=0.6)
        return new_image

    def painters_hand(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
        morph = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
        new_image = cv2.normalize(morph, None, 20, 255, cv2.NORM_MINMAX)
        return new_image

    def summer_sunset(self):
        new_image = cv2.applyColorMap(self.image, cv2.COLORMAP_SUMMER)
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        new_image = cv2.transform(new_image, kernel)
        new_image[np.where(new_image > 255)] = 255  # normalizing
        return new_image

    def toony(self):
        colors = cv2.bilateralFilter(self.image, 9, 300, 300)
        mask_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        mask_image = cv2.medianBlur(mask_image, 5)
        mask_image = cv2.adaptiveThreshold(
            mask_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        new_image = cv2.bitwise_and(colors, colors, mask=mask_image)
        return new_image

    def cyberpunk_neon(self):
        new_image = cv2.applyColorMap(self.image, cv2.COLORMAP_PLASMA)
        new_image = cv2.edgePreservingFilter(
            new_image, flags=1, sigma_s=60, sigma_r=0.4)
        return new_image

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
