import sys
import os
import threading

from PyQt5.QtCore import QUrl, QThread, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.uic import loadUi
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import importlib
import configparser




class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width = 1000
        self.height = 1000

        # Load and display the image
        self.loadImage(r"MenuAssets\\arobot.jpg")

        # Load the UI file
        loadUi("MenuAssets\MainMenu.ui", self)

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
        self.play_menu = PlayMenu(x_coord,y_coord)
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

        loadUi('MenuAssets\PlayMenu.ui', self)

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

        loadUi('MenuAssets\SettingsMenu.ui', self)

        self.GraphicsButton.clicked.connect(self.GraphicsClicked)
        self.BackButton.clicked.connect(self.BackClicked)

        # Connect the slider valueChanged signal to a function
        self.SoundSlider.valueChanged.connect(self.sliderValueChanged)

        # Get Volume from config file
        config = configparser.ConfigParser()
        config.read('config.txt')  # Path to config file
        volume = config.getint('Settings', 'volume')


        # QLabel for displaying volume text
        self.volumeLabel = QLabel(self)
        self.volumeLabel.setGeometry(600, 462, 181, 121)

        # Display Volume Label and chane font
        font = QFont()
        font.setPointSize(14)  # Set the desired font size
        font.setBold(True)  # Optionally, set the font weight to bold
        self.volumeLabel.setFont(font)
        self.volumeLabel.setText(f"Volume: {volume}")

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
        config.read('config.txt')  # Path to config file
        config.set('Settings', 'volume', str(value))

        # Overwrite config file
        with open('config.txt', 'w') as config_file:
            config.write(config_file)

        self.volumeLabel.setText(f"Volume: {value}")

        print("Slider value changed:", value)



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

        loadUi('MenuAssets\ExtrasMenu.ui', self)

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
        MapEditor = importlib.import_module('MapEditor').MapEditor
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
        media = QMediaContent(QUrl.fromLocalFile("Sounds/nicebassiguess.mp3"))
        self.media_player.setMedia(media)

        # Get Volume from config file
        config = configparser.ConfigParser()
        config.read('config.txt')  # Path to config file
        self.volume = config.getint('Settings', 'volume')

        # Adjust volume
        self.media_player.setVolume(self.volume)

        self.media_player.mediaStatusChanged.connect(self.restart_playback)

        # Create a QTimer to update the volume regularly
        self.volume_timer = QTimer()
        self.volume_timer.timeout.connect(self.update_volume)
        self.volume_timer.start(1000)

    def restart_playback(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

    def update_volume(self):
        # Get Volume from config file
        config = configparser.ConfigParser()
        config.read('config.txt')  # Path to config file
        self.volume = config.getint('Settings', 'volume')

        # Adjust volume
        self.media_player.setVolume(self.volume)

    def play(self):
        self.media_player.play()


if __name__ == '__main__':
    # Create the QApplication instance in the main thread
    app = QApplication(sys.argv)

    # Create an instance of the MusicPlayer class
    music_player = MusicPlayer()

    # Run the music playback in the main thread
    music_player.play()

    # Continue with the main program execution
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())
