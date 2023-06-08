import importlib
import os
import sys
import threading

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.uic import loadUi


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width = 1000
        self.height = 1000

        # Load and display the image
        self.loadImage(r"MenuAssets\\arobot.jpg")

        # Load the UI file
        loadUi("MenuAssets\\MainMenu.ui", self)

        # Set the window title and add a headline
        self.setWindowTitle("Main Menu")
        self.headline = QLabel("RoboArena", self)
        self.headline.setGeometry(350, 100, 800, 100)
        font = self.headline.font()
        font.setPointSize(48)
        self.headline.setFont(font)

        # Make the window non-resizable
        self.setFixedSize(self.size())

        # Access the elements defined in the UI here
        # self.button.clicked.connect(self.buttonClicked)
        self.PlayButton.clicked.connect(self.playClicked)
        self.SettingsButton.clicked.connect(self.settingsClicked)
        self.QuitButton.clicked.connect(self.quitClicked)
        self.ExtrasButton.clicked.connect(self.extrasClicked)

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
        position = self.getWindowPos()
        x_coord = position.x()
        y_coord = position.y()
        self.play_menu = PlayMenu(x_coord, y_coord)
        self.play_menu.show()
        self.close()

    def settingsClicked(self):
        position = self.getWindowPos()
        x_coord = position.x()
        y_coord = position.y()
        self.settings_menu = SettingsMenu(x_coord, y_coord)
        self.settings_menu.show()
        self.close()

    def quitClicked(self):
        self.close()

    def extrasClicked(self):
        position = self.getWindowPos()
        x_coord = position.x()
        y_coord = position.y()
        self.extra_menu = ExtrasMenu(x_coord, y_coord)
        self.extra_menu.show()
        self.close()

    def getWindowPos(self):
        window_pos = self.pos()
        return window_pos

    def moveWindowPos(self):
        self.move(self.x_position, self.y_position)


class PlayMenu(MainMenu):
    def __init__(self, x_position, y_position):
        super().__init__()

        self.x_position = x_position
        self.y_position = y_position

        self.loadImage(r"MenuAssets\brobot.png")

        self.moveWindowPos()

        loadUi("MenuAssets\\PlayMenu.ui", self)

        self.SoloButton.clicked.connect(self.SoloClicked)
        self.MultiplayerButton.clicked.connect(self.MultiplayerClicked)
        self.BackButton.clicked.connect(self.BackClicked)

        # Set the window title and add a headline
        self.setWindowTitle("Play Menu")
        self.headline = QLabel("Play", self)
        self.headline.setGeometry(450, 100, 800, 100)
        font = self.headline.font()
        font.setPointSize(48)
        self.headline.setFont(font)

    def SoloClicked(self):
        print("g")

    def MultiplayerClicked(self):
        print("g")

    def BackClicked(self):
        self.main_menu = MainMenu()  # Pass the current main menu as parent
        self.main_menu.show()
        self.close()


class SettingsMenu(MainMenu):
    def __init__(self, x_position, y_position):
        super().__init__()

        self.x_position = x_position
        self.y_position = y_position

        self.loadImage(r"MenuAssets\robotc.png")

        self.moveWindowPos()

        loadUi("MenuAssets\\SettingsMenu.ui", self)

        self.GraphicsButton.clicked.connect(self.GraphicsClicked)
        self.BackButton.clicked.connect(self.BackClicked)

        # Set the window title and add a headline
        self.setWindowTitle("Settings Menu")
        self.headline = QLabel("Settings", self)
        self.headline.setGeometry(400, 100, 800, 100)
        font = self.headline.font()
        font.setPointSize(48)
        self.headline.setFont(font)

    def GraphicsClicked(self):
        print("g")

    def BackClicked(self):
        self.main_menu = MainMenu()  # Pass the current main menu as parent
        self.main_menu.show()
        self.close()


class ExtrasMenu(MainMenu):
    def __init__(self, x_position, y_position):
        super().__init__()

        self.x_position = x_position
        self.y_position = y_position

        self.loadImage(r"MenuAssets\scaryrobot.png")

        self.moveWindowPos()

        loadUi("MenuAssets\\ExtrasMenu.ui", self)

        self.MapEditorButton.clicked.connect(self.MapEditorClicked)
        self.BackButton.clicked.connect(self.BackClicked)

        # Set the window title and add a headline
        self.setWindowTitle("Extras")
        self.headline = QLabel("Extras", self)
        self.headline.setGeometry(400, 100, 800, 100)
        font = self.headline.font()
        font.setPointSize(48)
        self.headline.setFont(font)

    def MapEditorClicked(self):
        MapEditor = importlib.import_module("MapEditor").MapEditor
        self.map_editor = MapEditor()
        self.map_editor.show()
        self.close()

    def BackClicked(self):
        self.main_menu = MainMenu()
        self.main_menu.show()
        self.close()


class MusicPlayer:
    def __init__(self):
        self.media_player = QMediaPlayer()
        media = QMediaContent(QUrl.fromLocalFile("Sounds/A Journey Awaits.mp3"))
        self.media_player.setMedia(media)
        self.media_player.setVolume(10)  # Adjust the volume as needed

        self.media_player.mediaStatusChanged.connect(self.restart_playback)

    def restart_playback(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

    def play(self):
        self.media_player.play()


if __name__ == "__main__":
    # Create the QApplication instance in the main thread
    app = QApplication(sys.argv)

    # Create an instance of the MusicPlayer class
    music_player = MusicPlayer()

    # Run the music playback in a separate thread
    thread = threading.Thread(target=music_player.play)
    thread.start()

    # Continue with the main program execution
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())
