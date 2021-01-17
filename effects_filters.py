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
        thermal = self.thermal_effect()
        chilly = self.chilly_effect()
        hot_pepper = self.hot_pepper()
        sandstorm=self.sandstorm()
        darkness=self.darkness()
        firestorm=self.firestorm()
        sunshine_cartoon=self.sunshine_cartoon()
        snow=self.snow()
        salt_and_pepper = self.salt_and_pepper()
        gray_nostalgia=self.gray_nostalgia()
        ghost=self.ghost()
        pastel=self.pastel()
        ice_blue=self.ice_blue()
        winter_time = self.winter_time()
        sweet_dreams = self.sweet_dreams()

        images = {
            "Pink Dream": pink_dream,
            "Painter's Hand": painters_hand,
            "Summer Sunset": summer_sunset,
            "Toony": toony,
            "Cyberpunk Neon": cyberpunk_neon,
            "Sweet Dreams": sweet_dreams,
            "Thermal": thermal,
            "Chilly": chilly,
            "Hot Pepper ": hot_pepper,
            "Salt and Pepper": salt_and_pepper,
            "Gray Nostalgia": gray_nostalgia,
            "Sandstorm": sandstorm,
            "Ghost": ghost,
            "Darkness": darkness,
            "Pastel": pastel,
            "Ice Blue": ice_blue,
            "Firestorm": firestorm,
            "Sunshine Cartoon": sunshine_cartoon,
            "Winter Time": winter_time,
            "Snow": snow,
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

    def sweet_dreams(self):
        new_image = cv2.applyColorMap(self.image, cv2.COLORMAP_TWILIGHT_SHIFTED)
        new_image = cv2.edgePreservingFilter(
            new_image, flags=1, sigma_s=40, sigma_r=0.6)
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

    def hot_pepper(self):
        # new_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        morph = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
        new_image = cv2.normalize(morph, None, 20, 255, cv2.NORM_MINMAX)
        new_image = cv2.applyColorMap(new_image, cv2.COLORMAP_HOT)
        return new_image

    def salt_and_pepper(self):
        new_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        (thresh, new_image) = cv2.threshold(new_image, 127, 255, cv2.THRESH_BINARY)
        return new_image

    def gray_nostalgia(self):
        mask_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        mask_image = cv2.medianBlur(mask_image, 3)
        new_image = cv2.applyColorMap(mask_image, cv2.COLORMAP_BONE)
        return new_image

    def sandstorm(self):
        new_image = cv2.applyColorMap(self.image, cv2.COLORMAP_PLASMA)
        kernel = np.array([[0.272, 0.321, 0.141],
                           [0.359, 0.686, 0.128],
                           [0.885, 0.669, 0.149]])
        new_image = cv2.transform(new_image, kernel)
        new_image[np.where(new_image > 255)] = 255  # normalizing
        return new_image

    def ghost(self):
        kernel = np.array([[0, -1, -1], [1, 0, -1], [1, 4, 0]])
        new_image = cv2.filter2D(self.image, -1, kernel)
        new_image = cv2.applyColorMap(new_image, cv2.COLORMAP_DEEPGREEN)
        return new_image

    def snow(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (25, 25), 0)
        image = cv2.divide(gray, gray_blur, scale=250.0)
        return image


    def pastel(self):
        new_image = cv2.medianBlur(self.image, 5)
        new_image = cv2.applyColorMap(new_image, cv2.COLORMAP_JET)
        return new_image


    def ice_blue(self):
        new_image = cv2.applyColorMap(self.image, cv2.COLORMAP_OCEAN)
        new_image = cv2.edgePreservingFilter(
            new_image, flags=1, sigma_s=70, sigma_r=0.5)
        return new_image

    def firestorm(self):
        new_image = cv2.applyColorMap(self.image, cv2.COLORMAP_PARULA)
        new_image = cv2.bitwise_not(new_image)
        return new_image

    def sunshine_cartoon(self):
        new_image = cv2.applyColorMap(self.image, cv2.COLORMAP_INFERNO)
        kernel = np.array([[2, -7, -5], [3, 4, -8], [2, 4, 6]])
        new_image = cv2.filter2D(new_image, -1, kernel)
        return new_image

    def winter_time(self):
        kernel = np.array([[0.868, 0.100, 0.553],
                           [0.545, 0.100, 0.734],
                           [0.546, 0.100, 0.453]])
        new_image = cv2.transform(self.image, kernel)
        colors = cv2.bilateralFilter(new_image, 1, 1, 1)
        mask_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
        mask_image = cv2.medianBlur(mask_image, 1)
        new_image = cv2.bitwise_and(colors, colors, mask=mask_image)
        return new_image

    def darkness(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (25, 25), 0)
        image = cv2.divide(gray, gray_blur, scale=250.0)
        new_image = cv2.bitwise_not(image)
        return new_image

    #--- New Functions can be added under here ---#

