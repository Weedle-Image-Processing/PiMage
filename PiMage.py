from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from GUI import Ui_PiMage
from effects_filters import EffectsFilters
import cv2
import sys
import os


class App(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_PiMage()
        self.ui.setupUi(self)

        self.image_exist = False
        self.ui.listWidget.setSpacing(5)

        self.ui.actionOpen.triggered.connect(self.open_image)
        self.ui.actionSave.triggered.connect(self.save_image)
        self.ui.actionSave_as.triggered.connect(self.save_as_image)
        self.ui.actionRemove_Image.triggered.connect(self.remove_image)
        self.ui.actionQuit.triggered.connect(self.quit_app)
        self.ui.applyButton.clicked.connect(self.applyButton_clicked)
        self.ui.revertButton.clicked.connect(self.revertButton_click)

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

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName()
        if path == "":  # if there is no path at all return
            return

        self.im_path = path
        self.ui.listWidget.clear()

        if path.split(".")[-1] not in ["png", "jpg"]:
            self.error_message("Unsupported File Error",
                               "Unsupported file, file must be .jpg or .png")
        else:
            pixmap = QPixmap(path)
            # set these values to global value for save as function
            width, height = self.scale_image(pixmap.width(), pixmap.height())
            pixmap = pixmap.scaled(int(width), int(height))
            self.pixmap = pixmap
            self.image_exist = True
            self.ui.imageLabel.setPixmap(pixmap)
            self.list_widget_initialize()

    def save_image(self):
        if self.image_exist:
            msg = QMessageBox.question(
                self, 'SURE?', "This will overwrite to original image!", QMessageBox.Yes | QMessageBox.No)
            if msg == QMessageBox.Yes:
                image_path = self.im_path
                self.ui.imageLabel.pixmap().toImage().save(image_path, 'PNG')
        else:
            self.error_message(
                "Image Error", "There is no image in the app. Please upload one.")

    def save_as_image(self):
        if self.image_exist:
            image_path, _ = QFileDialog.getSaveFileName()
            if not image_path.endswith("png") or not image_path.endswith("jpg"):
                image_path = image_path + ".png"
            self.ui.imageLabel.pixmap().toImage().save(image_path, 'PNG')
        else:
            self.error_message(
                "Image Error", "There is no image in the app. Please upload one.")

    def remove_image(self):
        if self.image_exist:
            self.image_exist = False
            self.im_path = ""
            self.ui.imageLabel.clear()
            self.ui.listWidget.clear()
        else:
            self.error_message("No Image Found!",
                               "There is no image to remove from canvas!")

    def quit_app(self):
        self.close()

    def list_widget_initialize(self):
        self.effects_filters = EffectsFilters(self.im_path)
        self.images = self.effects_filters.all_effects()  # dictionary
        for i in self.images:
            self.images[i] = cv2.cvtColor(self.images[i], cv2.COLOR_BGR2RGB)
            h, w, c = self.images[i].shape
            qimage = QImage(self.images[i].data, w,
                            h, c*w, QImage.Format_RGB888)
            px = QPixmap.fromImage(qimage)
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
            selection = self.ui.listWidget.selectedIndexes()[0].row()
            filtered_image = list(self.images.values())[selection]
            h, w, c = filtered_image.shape
            qimage = QImage(filtered_image.data, w, h,
                            c*w, QImage.Format_RGB888)
            w, h = self.scale_image(qimage.width(), qimage.height())
            qimage = qimage.scaled(int(w), int(h))

            self.ui.imageLabel.setPixmap(QPixmap.fromImage(qimage))

    def revertButton_click(self):
        if self.image_exist:
            pixmap = QPixmap(self.im_path)
            width, height = self.scale_image(pixmap.width(), pixmap.height())
            pixmap = pixmap.scaled(int(width), int(height))
            self.pixmap = pixmap
            self.ui.imageLabel.setPixmap(pixmap)
        else:
            self.error_message("No Image Found", "Try opening an image!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
