import configparser
import importlib
import os
import sys

from Arena import *
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel, QMainWindow,
                             QMessageBox)
from PyQt5.uic import loadUi

# Set up config file
config = configparser.ConfigParser()
config.read("config.txt")


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
        font.setBold(True)
        self.headline.setFont(font)

        # Make the window non-resizable
        self.setFixedSize(self.size())

        # Access the elements defined in the UI here
        # self.button.clicked.connect(self.buttonClicked)
        self.PlayButton.clicked.connect(self.playClicked)
        self.SettingsButton.clicked.connect(self.settingsClicked)
        self.QuitButton.clicked.connect(self.quitClicked)
        self.ExtrasButton.clicked.connect(self.extrasClicked)

    def update_position(self):
        position = self.getWindowPos()
        x_coord = position.x()
        y_coord = position.y()

        config.read("config.txt")  # Path to config file
        config.set("Position", "x", str(x_coord))
        config.set("Position", "y", str(y_coord))

        # Overwrite config file
        with open("config.txt", "w") as config_file:
            config.write(config_file)

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
        self.setCentralWidget(PlayMenu())

    def settingsClicked(self):
        self.setCentralWidget(SettingsMenu())

    def quitClicked(self):
        self.close()
        sys.exit()

    def extrasClicked(self):
        self.setCentralWidget(ExtrasMenu())


class PlayMenu(MainMenu):
    def __init__(self):
        super().__init__()

        self.loadImage(r"MenuAssets\\brobot.png")

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
        font.setBold(True)
        self.headline.setFont(font)

    def SoloClicked(self):
        self.setCentralWidget(SoloMenu())

    def MultiplayerClicked(self):
        print("g")

    def BackClicked(self):
        self.setCentralWidget(MainMenu())


class SettingsMenu(MainMenu):
    def __init__(self):
        super().__init__()

        self.loadImage(r"MenuAssets\\robotc.png")

        loadUi("MenuAssets\\SettingsMenu.ui", self)

        self.GraphicsButton.clicked.connect(self.GraphicsClicked)
        self.BackButton.clicked.connect(self.BackClicked)

        # Connect the slider valueChanged signal to a function
        self.SoundSlider.valueChanged.connect(self.sliderValueChanged)

        # Get music volume from config file
        config.read("config.txt")  # Path to config file
        music = config.getint("Settings", "music")

        # QLabel for displaying volume text
        self.musicLabel = QLabel(self)
        self.musicLabel.setGeometry(600, 370, 181, 121)

        # Display Volume Label and chane font
        font = QFont()
        font.setPointSize(14)  # Set the desired font size
        font.setBold(True)  # Optionally, set the font weight to bold
        self.musicLabel.setFont(font)
        self.musicLabel.setText(f"Volume: {music}")

        # Set the window title and add a headline
        self.setWindowTitle("Settings Menu")
        self.headline = QLabel("Settings", self)
        self.headline.setGeometry(400, 100, 800, 100)
        font = self.headline.font()
        font.setPointSize(48)
        font.setBold(True)
        self.headline.setFont(font)

    def sliderValueChanged(self, value):
        # Update the configuration file with the new volume value
        config = configparser.ConfigParser()
        config.read("config.txt")  # Path to config file
        config.set("Settings", "music", str(value))

        # Overwrite config file
        with open("config.txt", "w") as config_file:
            config.write(config_file)

        self.musicLabel.setText(f"Volume: {value}")

        print("Slider value changed:", value)

    def GraphicsClicked(self):
        print("g")

    def BackClicked(self):
        self.setCentralWidget(MainMenu())


class ExtrasMenu(MainMenu):
    def __init__(self):
        super().__init__()

        self.loadImage(r"MenuAssets\\scaryrobot.png")

        loadUi("MenuAssets\\ExtrasMenu.ui", self)

        self.MapEditorButton.clicked.connect(self.MapEditorClicked)
        self.BackButton.clicked.connect(self.BackClicked)

        # Set the window title and add a headline
        self.setWindowTitle("Extras")
        self.headline = QLabel("Extras", self)
        self.headline.setGeometry(400, 100, 800, 100)
        font = self.headline.font()
        font.setPointSize(48)
        font.setBold(True)
        self.headline.setFont(font)

    def MapEditorClicked(self):
        MapEditor = importlib.import_module("MapEditor").MapEditor
        self.setCentralWidget(MapEditor())

    def BackClicked(self):
        self.setCentralWidget(MainMenu())


class SoloMenu(MainMenu):
    def __init__(self):
        super().__init__()

        self.loadImage(r"MenuAssets\\robotc.png")

        loadUi("MenuAssets\\SoloMenu.ui", self)

        # To prevent starting the game without robot/arena choosen
        self.robot_selected = False
        self.arena_selected = False

        self.PlayButton.clicked.connect(self.PlayClicked)
        self.RobotButton.clicked.connect(self.RobotClicked)
        self.ArenaButton.clicked.connect(self.ArenaClicked)
        self.BackButton.clicked.connect(self.BackClicked)

        # Set the window title and add a headline
        self.setWindowTitle("Solo")
        self.headline = QLabel("Solo", self)
        self.headline.setGeometry(400, 100, 800, 100)
        font = self.headline.font()
        font.setPointSize(48)
        font.setBold(True)
        self.headline.setFont(font)

        # To select Robot class
        self.robot_class_list = ["Destroyer", "Tank", "Velocity"]

    def PlayClicked(self):
        if self.RobotButton.text() == "Robot":
            error_message = "No Robot selected"
            QMessageBox.critical(self, "Error", error_message)
        elif self.ArenaButton.text() == "Arena":
            error_message = "No Arena selected"
            QMessageBox.critical(self, "Error", error_message)
        else:
            self.setCentralWidget(Arena())

    def RobotClicked(self):
        robot_class = self.robot_class_list.pop(0)
        self.robot_class_list.append(robot_class)
        self.RobotButton.setText(robot_class)
        config.read("config.txt")  # Path to config file
        config.set("Class", "selected_class", robot_class)
        # Overwrite config file
        with open("config.txt", "w") as config_file:
            config.write(config_file)

    def ArenaClicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose Arena", "", "Text Files (*.txt)"
        )

        if file_path:
            self.ArenaButton.setText(file_path)
            config.read("config.txt")  # Path to config file
            config.set("Map", "selected_map", file_path)
            # Overwrite config file
            with open("config.txt", "w") as config_file:
                config.write(config_file)

    def BackClicked(self):
        self.setCentralWidget(PlayMenu())


class MusicPlayer:
    def __init__(self):
        self.media_player = QMediaPlayer()
        media = QMediaContent(QUrl.fromLocalFile("Sounds\\nicebassiguess.mp3"))
        self.media_player.setMedia(media)

        # Get Volume from config file
        config = configparser.ConfigParser()
        config.read("config.txt")  # Path to config file
        self.music = config.getint("Settings", "music")

        # Adjust volume
        self.media_player.setVolume(self.music)

        self.media_player.mediaStatusChanged.connect(self.restart_playback)

        # Create a QTimer to update the volume regularly
        self.music_timer = QTimer()
        self.music_timer.timeout.connect(self.update_music)
        self.music_timer.start(500)

    def restart_playback(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

    def update_music(self):
        # Get Volume from config file
        config.read("config.txt")  # Path to config file
        self.music = config.getint("Settings", "music")

        # Adjust volume
        self.media_player.setVolume(self.music)

    def play(self):
        self.media_player.play()


if __name__ == "__main__":
    # Create the QApplication instance in the main thread
    app = QApplication(sys.argv)

    # Create an instance of the MusicPlayer class
    music_player = MusicPlayer()

    # Run the music playback in the main thread
    music_player.play()

    # Continue with the main program execution
    window = MainMenu()
    window.move(config.getint("Position", "x"), config.getint("Position", "y"))
    window.show()
    sys.exit(app.exec_())
