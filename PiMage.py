from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from GUI import Ui_PiMage
from effects_filters import EffectsFilters
from image_enhancement import ImageEnhancement
import cv2
import sys
import os


class App(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_PiMage()
        self.setFixedSize(982, 824)
        self.ui.setupUi(self)

        self.image_exist = False

        self.ui.listWidget.setSpacing(5)
        self.enable_disable_buttons()

        #--- connections ---#
        self.ui.actionOpen.triggered.connect(self.open_image)
        self.ui.actionSave.triggered.connect(self.save_image)
        self.ui.actionSave_as.triggered.connect(self.save_as_image)
        self.ui.actionRemove_Image.triggered.connect(self.remove_image)
        self.ui.actionQuit.triggered.connect(self.quit_app)
        self.ui.applyButton.clicked.connect(self.applyButton_clicked)
        self.ui.revertButton.clicked.connect(self.revertButton_click)
        self.ui.inverseButton.clicked.connect(self.invertButton_click)
        self.ui.contrastSlider.valueChanged.connect(self.slider_events)
        self.ui.brightnessSlider.valueChanged.connect(self.slider_events)

    def enable_disable_buttons(self):
        if not self.image_exist:
            self.ui.actionCrop.setDisabled(True)
            self.ui.actionResize.setDisabled(True)
            self.ui.actionRotate.setDisabled(True)
            self.ui.actionFlip.setDisabled(True)
            self.ui.applyButton.setDisabled(True)
            self.ui.revertButton.setDisabled(True)
            self.ui.brightnessSlider.setDisabled(True)
            self.ui.contrastSlider.setDisabled(True)
            self.ui.inverseButton.setDisabled(True)
            self.ui.histogramNormalButton.setDisabled(True)
            self.ui.contrastEnhancementButton.setDisabled(True)
        else:
            self.ui.actionCrop.setDisabled(False)
            self.ui.actionResize.setDisabled(False)
            self.ui.actionRotate.setDisabled(False)
            self.ui.actionFlip.setDisabled(False)
            self.ui.applyButton.setDisabled(False)
            self.ui.revertButton.setDisabled(False)
            self.ui.brightnessSlider.setDisabled(False)
            self.ui.contrastSlider.setDisabled(False)
            self.ui.inverseButton.setDisabled(False)
            self.ui.histogramNormalButton.setDisabled(False)
            self.ui.contrastEnhancementButton.setDisabled(False)

    def set_default_sliders(self):
        self.ui.brightnessSlider.setValue(0)
        self.ui.contrastSlider.setValue(1)

    def error_message(self, title, msg):
        msgbox = QMessageBox()
        msgbox.setWindowTitle(title)
        msgbox.setText(msg)
        msgbox.setIcon(msgbox.Critical)
        msgbox.exec_()

    def scale_image(self, width, height):
        k = self.ui.imageLabel.frameGeometry().height() / height
        if width * k <= self.ui.imageLabel.frameGeometry().width():
            w = width * k
            h = self.ui.imageLabel.frameGeometry().height()
        else:
            k = self.ui.imageLabel.frameGeometry().width() / width
            w = self.ui.imageLabel.frameGeometry().width()
            h = height * k

        return w, h

    def convert_to_pixmap(self, img, bgr2rgb):
        if bgr2rgb:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        piximage = QImage(img.data, w, h, c*w, QImage.Format_RGB888)
        w, h = self.scale_image(piximage.width(), piximage.height())
        piximage = piximage.scaled(int(w), int(h))
        piximage = QPixmap.fromImage(piximage)
        return piximage

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName()
        if path == "":  # if there is no path at all return
            return

        self.im_path = path  # self.im_path is our original image path
        # self.image will be the last configurated image
        self.image = cv2.imread(self.im_path)
        self.ui.listWidget.clear()

        if path.split(".")[-1] not in ["png", "jpg"]:
            self.error_message("Unsupported File Error",
                               "Unsupported file, file must be .jpg or .png")
        else:
            pixmap = QPixmap(path)
            # set these values to global value for save as function
            width, height = self.scale_image(pixmap.width(), pixmap.height())
            pixmap = pixmap.scaled(int(width), int(height))
            self.image_exist = True
            self.ui.imageLabel.setPixmap(pixmap)
            self.list_widget_initialize()
        self.enable_disable_buttons()

    def save_image(self):
        if self.image_exist:
            msg = QMessageBox.question(
                self, 'SURE?', "This will overwrite to original image!", QMessageBox.Yes | QMessageBox.No)
            if msg == QMessageBox.Yes:
                image_path = self.im_path
                try:
                    cv2.imwrite(image_path, self.image)
                except Exception as e:
                    self.error_message(
                        "Error occured while saving!", "Error Message: ", str(e))
        else:
            self.error_message(
                "Image Error", "There is no image in the app. Please upload one.")

    def save_as_image(self):
        if self.image_exist:
            image_path, _ = QFileDialog.getSaveFileName()
            if not image_path.endswith("png") or not image_path.endswith("jpg"):
                image_path = image_path + ".png"
            try:
                cv2.imwrite(image_path, self.image)
            except Exception as e:
                self.error_message(
                    "Error occured while saving!", "Error Message: ", str(e))
        else:
            self.error_message(
                "Image Error", "There is no image in the app. Please upload one.")

    def remove_image(self):
        if self.image_exist:
            self.image_exist = False
            self.im_path = ""
            self.ui.imageLabel.clear()
            self.ui.listWidget.clear()
            self.set_default_sliders()
        else:
            self.error_message("No Image Found!",
                               "There is no image to remove from canvas!")
        self.enable_disable_buttons()

    def quit_app(self):
        self.close()

    def list_widget_initialize(self):
        self.effects_filters = EffectsFilters(self.image)
        self.images = self.effects_filters.all_effects()  # dictionary
        for i in self.images:
            self.images[i] = cv2.cvtColor(self.images[i], cv2.COLOR_BGR2RGB)
            px = self.convert_to_pixmap(self.images[i], False)
            if not px.isNull():
                self.icons = QtWidgets.QListWidgetItem(
                    QtGui.QIcon(px), i)
                self.iconSize = QtCore.QSize(200, 200)
                self.ui.listWidget.setIconSize(self.iconSize)
                self.ui.listWidget.addItem(self.icons)

    def applyButton_clicked(self):
        if not self.image_exist:  # if there is no image dont do anything
            return
        if len(self.ui.listWidget.selectedIndexes()) == 0:
            return
        else:
            self.set_default_sliders()
            selection = self.ui.listWidget.selectedIndexes()[0].row()
            filtered_image = list(self.images.values())[selection]
            self.image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB)
            filtered_image = self.convert_to_pixmap(filtered_image, False)
            self.ui.imageLabel.setPixmap(filtered_image)

    def revertButton_click(self):
        if self.image_exist:
            self.image = cv2.imread(self.im_path)
            pixmap = QPixmap(self.im_path)
            width, height = self.scale_image(pixmap.width(), pixmap.height())
            pixmap = pixmap.scaled(int(width), int(height))
            self.ui.imageLabel.setPixmap(pixmap)
            self.enable_disable_buttons()
            self.set_default_sliders()
        else:
            self.error_message("No Image Found", "Try opening an image!")

    def invertButton_click(self):
        if not self.image_exist:
            return
        self.set_default_sliders()
        self.image_enhancement = ImageEnhancement(self.image)
        self.image = self.image_enhancement.inverse_image()
        piximage = self.convert_to_pixmap(self.image, True)
        self.ui.imageLabel.setPixmap(piximage)

    def slider_events(self):
        brightness = self.ui.brightnessSlider.value()
        contrast = self.ui.contrastSlider.value()
        self.ui.brightnessValueLabel.setText(str(brightness))
        self.ui.contrastValueLabel.setText(str(contrast))
        self.image_enhancement = ImageEnhancement(self.image)
        adjusted_image = self.image_enhancement.adjust_brightness_contrast(
            brightness, contrast)
        self.image = adjusted_image
        piximage = self.convert_to_pixmap(adjusted_image, True)
        self.ui.imageLabel.setPixmap(piximage)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    css = os.path.abspath(os.path.join("style", "style.css"))
    with open(css, "r") as file:
        app.setStyleSheet(file.read())
    window = App()
    window.show()
    sys.exit(app.exec_())
