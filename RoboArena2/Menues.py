import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout,
                             QWidget)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Load the original image
        self.original_image = QPixmap("jack8.JPG")

        self.setWindowTitle("Buttons with Spacing")
        self.setGeometry(300, 300, 1000, 1000)

        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Make the window non-resizable
        self.setFixedSize(self.size())

        # Set margins and spacing
        layout.setContentsMargins(400, 100, 400, 300)  # left,top,right,bottom
        layout.setSpacing(100)  # space between buttons

        # Create the headline label
        headline_label = QLabel("RoboArena")
        headline_label.setAlignment(
            Qt.AlignCenter
        )  # Align the headline text to the center
        headline_label.setStyleSheet(
            "color: white; font-size: 40px;"
        )  # Set color and font size

        layout.addWidget(headline_label)

        # Create three buttons
        play_button = QPushButton("Play", self)
        settings_button = QPushButton("Settings", self)
        quit_button = QPushButton("Quit", self)

        # Add the buttons to the layout
        layout.addWidget(play_button)
        layout.addWidget(settings_button)
        layout.addWidget(quit_button)

        self.setLayout(layout)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.scaled_image)

    def resizeEvent(self, event):
        # Scale the image to the size of the window
        self.scaled_image = self.original_image.scaled(self.size())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
