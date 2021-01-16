from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QIntValidator
from GUI import Ui_PiMage
from effects_filters import EffectsFilters
from image_enhancement import ImageEnhancement
from basic_operations import BasicOperations
import cv2
import sys
import os


class App(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_PiMage()
        self.setFixedSize(971, 714)
        self.ui.setupUi(self)

        self.image_exist = False

        self.ui.listWidget.setSpacing(5)
        self.enable_disable_buttons()

        # --- connections ---#
        self.ui.actionOpen.triggered.connect(self.open_image)
        self.ui.actionSave.triggered.connect(self.save_image)
        self.ui.actionSave_as.triggered.connect(self.save_as_image)
        self.ui.actionRemove_Image.triggered.connect(self.remove_image)
        self.ui.actionQuit.triggered.connect(self.quit_app)
        self.ui.applyButton.clicked.connect(self.applyButton_clicked)
        self.ui.applyManuelButton.clicked.connect(
            self.applyManuelEnhancement_clicked)
        self.ui.revertButton.clicked.connect(self.revertButton_click)
        self.ui.inverseButton.clicked.connect(self.invertButton_click)
        self.ui.contrastSlider.valueChanged.connect(self.slider_events)
        self.ui.brightnessSlider.valueChanged.connect(self.slider_events)

        self.ui.actionVertical.triggered.connect(self.flipVerticalButton_click)
        self.ui.actionHorizontal.triggered.connect(
            self.flipHorizontalButton_click)
        self.ui.actionVertical_Horizontal.triggered.connect(
            self.flipVertHorButton_click)

        self.ui.action90.triggered.connect(self.rotate90Button_click)
        self.ui.action180.triggered.connect(self.rotate180Button_click)
        self.ui.action270.triggered.connect(self.rotate270Button_click)

        # self.ui.actionCrop.triggered.connect(self.crop_click)

        self.ui.histogramNormalButton.clicked.connect(self.histogram_click)

    def enable_disable_buttons(self):
        if not self.image_exist:
            self.ui.actionCrop.setDisabled(True)
            self.ui.actionResize.setDisabled(True)
            # self.ui.actionRotate.setDisabled(True)
            self.ui.action90.setDisabled(True)
            self.ui.action180.setDisabled(True)
            self.ui.action270.setDisabled(True)
            # self.ui.actionFlip.setDisabled(True)
            self.ui.actionVertical.setDisabled(True)
            self.ui.actionHorizontal.setDisabled(True)
            self.ui.actionVertical_Horizontal.setDisabled(True)
            self.ui.rightToolsGroupBox.setDisabled(True)
            self.ui.listWidget.setDisabled(True)
        else:
            self.ui.actionCrop.setDisabled(False)
            self.ui.actionResize.setDisabled(False)
            # self.ui.actionRotate.setDisabled(False)
            self.ui.action90.setDisabled(False)
            self.ui.action180.setDisabled(False)
            self.ui.action270.setDisabled(False)
            # self.ui.actionFlip.setDisabled(False)
            self.ui.actionVertical.setDisabled(False)
            self.ui.actionHorizontal.setDisabled(False)
            self.ui.actionVertical_Horizontal.setDisabled(False)
            self.ui.rightToolsGroupBox.setDisabled(False)
            self.ui.listWidget.setDisabled(False)

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
        piximage = QImage(img.data, w, h, c * w, QImage.Format_RGB888)
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

        if path.split(".")[-1] not in ["png", "jpg", "jpeg", "PNG", "JPG", "JPEG"]:
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
            msg = QMessageBox.question(
                self, 'Are you sure?', "This will undo all changes!", QMessageBox.Yes | QMessageBox.No)
            if msg == QMessageBox.Yes:
                self.image = cv2.imread(self.im_path)
                pixmap = self.convert_to_pixmap(self.image, True)
                self.ui.imageLabel.setPixmap(pixmap)
                self.ui.listWidget.clear()
                self.list_widget_initialize()
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
        self.list_widget_initialize()
        self.ui.imageLabel.setPixmap(piximage)

    def slider_events(self):
        brightness = self.ui.brightnessSlider.value()
        contrast = self.ui.contrastSlider.value() / 10
        self.ui.brightnessValueLabel.setText(str(brightness))
        self.ui.contrastValueLabel.setText(str(contrast))
        self.image_enhancement = ImageEnhancement(self.image)
        self.manuel_enhan_image = self.image_enhancement.adjust_brightness_contrast(
            brightness, contrast)
        piximage = self.convert_to_pixmap(self.manuel_enhan_image, True)
        self.ui.imageLabel.setPixmap(piximage)

    def applyManuelEnhancement_clicked(self):
        self.image = self.manuel_enhan_image
        pixmap = self.convert_to_pixmap(self.image, True)
        self.ui.listWidget.clear()
        self.list_widget_initialize()
        self.ui.imageLabel.setPixmap(pixmap)
        self.set_default_sliders()

    def flipVerticalButton_click(self):
        self.basic_operations = BasicOperations(self.image)
        self.image = self.basic_operations.flip_image_vertical()
        piximage = self.convert_to_pixmap(self.image, True)
        self.ui.imageLabel.setPixmap(piximage)

    def flipHorizontalButton_click(self):
        self.basic_operations = BasicOperations(self.image)
        self.image = self.basic_operations.flip_image_horizontal()
        piximage = self.convert_to_pixmap(self.image, True)
        self.ui.imageLabel.setPixmap(piximage)

    def flipVertHorButton_click(self):
        self.basic_operations = BasicOperations(self.image)
        self.image = self.basic_operations.flip_image_horizontal_vertical()
        piximage = self.convert_to_pixmap(self.image, True)
        self.ui.imageLabel.setPixmap(piximage)

    def rotate90Button_click(self):
        self.basic_operations = BasicOperations(self.image)
        self.image = self.basic_operations.rotate_image_90()
        piximage = self.convert_to_pixmap(self.image, True)
        self.ui.imageLabel.setPixmap(piximage)

    def rotate180Button_click(self):
        self.basic_operations = BasicOperations(self.image)
        self.image = self.basic_operations.rotate_image_180()
        piximage = self.convert_to_pixmap(self.image, True)
        self.ui.imageLabel.setPixmap(piximage)

    def rotate270Button_click(self):
        self.basic_operations = BasicOperations(self.image)
        self.image = self.basic_operations.rotate_image_270()
        piximage = self.convert_to_pixmap(self.image, True)
        self.ui.imageLabel.setPixmap(piximage)

    def histogram_click(self):
        if self.image_exist:
            self.image_enhancement = ImageEnhancement(self.image)
            self.image = self.image_enhancement.histogram()
            piximage = self.convert_to_pixmap(self.image, True)
            self.ui.imageLabel.setPixmap(piximage)
        else:
            self.error_message("No Image Found", "Try opening an image!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    css = os.path.abspath(os.path.join("style", "style.css"))
    with open(css, "r") as file:
        app.setStyleSheet(file.read())
    window = App()
    window.show()
    sys.exit(app.exec_())
