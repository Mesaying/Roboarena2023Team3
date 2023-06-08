import os
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.uic import loadUi


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width = 1000
        self.height = 1000

        # Load and display the image
        self.loadImage(r"MenuAssets\arobot.jpg")

        # Load the UI file
        loadUi("MenuAssets/MainMenu.ui", self)

        # Make the window non-resizable
        self.setFixedSize(self.size())

        # Access the elements defined in the UI here
        # self.button.clicked.connect(self.buttonClicked)
        self.PlayButton.clicked.connect(self.playClicked)
        self.SettingsButton.clicked.connect(self.settingsClicked)
        self.QuitButton.clicked.connect(self.quitClicked)

    def loadImage(self, path):
        # Path to the image (use the absolute path)
        image_path = os.path.abspath(path)

        # Load the image and create a QLabel widget
        pixmap = QPixmap(image_path)
        image_label = QLabel(self)

        # Resize the image to match the window size
        pixmap = pixmap.scaled(self.width, self.height)

        # Set the pixmap to the QLabel
        image_label.setPixmap(pixmap)

        # Set the position and size of the QLabel to cover the whole window
        image_label.setGeometry(0, 0, self.width, self.height)

    def playClicked(self):
        self.play_menu = PlayMenu()  # Pass the current main menu as parent
        self.play_menu.show()
        self.close()

    def settingsClicked(self):
        print("Settings button clicked")

    def quitClicked(self):
        self.close()


class PlayMenu(MainMenu):
    def __init__(self):
        super().__init__()

        self.loadImage(r"MenuAssets\arobot.jpg")

        loadUi("MenuAssets/PlayMenu.ui", self)

        self.SoloButton.clicked.connect(self.SoloClicked)
        self.MultiplayerButton.clicked.connect(self.MultiplayerClicked)
        self.BackButton.clicked.connect(self.BackClicked)

    def SoloClicked(self):
        print("g")

    def MultiplayerClicked(self):
        print("g")

    def BackClicked(self):
        self.main_menu = MainMenu()  # Pass the current main menu as parent
        self.main_menu.show()
        self.close()


class SettingsMenu(MainMenu):
    def __init__(self):
        super().__init__()

        self.loadImage(r"MenuAssets\arobot.jpg")

        loadUi("MenuAssets/SettingsMenu.ui", self)

        self.SoloButton.clicked.connect(self.SoundClicked)
        self.MultiplayerButton.clicked.connect(self.GraphicsClicked)
        self.BackButton.clicked.connect(self.BackClicked)

    def SoundClicked(self):
        print("g")

    def GraphicsClicked(self):
        print("g")

    def BackClicked(self):
        self.main_menu = MainMenu()  # Pass the current main menu as parent
        self.main_menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())
