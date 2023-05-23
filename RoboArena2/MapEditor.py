import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPainter, QPen
from PyQt5.QtWidgets import QGridLayout, QPushButton, QApplication, QWidget


class MapEditor(QWidget):
    def __init__(self):
        super().__init__()

        # title and size of window
        self.setWindowTitle("Map Editor")
        self.setGeometry(100, 100, 1000, 1000)

        # create the main layout
        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # create buttons
        self.draw_mode = None
        water_button = QPushButton("Water")
        water_button.setMaximumWidth(100)
        water_button.setMaximumHeight(30)
        water_button.clicked.connect(lambda: self.set_draw_mode("water"))
        main_layout.addWidget(water_button, 1, 0, 1, 1)

        fire_button = QPushButton("Fire")
        fire_button.setMaximumWidth(100)
        fire_button.setMaximumHeight(30)
        fire_button.clicked.connect(lambda: self.set_draw_mode("fire"))
        main_layout.addWidget(fire_button, 1, 1, 1, 1)

        wall_button = QPushButton("Wall")
        wall_button.setMaximumWidth(100)
        wall_button.setMaximumHeight(30)
        wall_button.clicked.connect(lambda: self.set_draw_mode("wall"))
        main_layout.addWidget(wall_button, 1, 2, 1, 1)

        boost_button = QPushButton("Boost")
        boost_button.setMaximumWidth(100)
        boost_button.setMaximumHeight(30)
        boost_button.clicked.connect(lambda: self.set_draw_mode("boost"))
        main_layout.addWidget(boost_button, 1, 3, 1, 1)

        spikes_button = QPushButton("Spikes")
        spikes_button.setMaximumWidth(100)
        spikes_button.setMaximumHeight(30)
        spikes_button.clicked.connect(lambda: self.set_draw_mode("spikes"))
        main_layout.addWidget(spikes_button, 1, 4, 1, 1)

        save_button = QPushButton("Save")
        save_button.setMaximumWidth(100)
        save_button.setMaximumHeight(30)
        save_button.clicked.connect(
            lambda: self.save_to_text_file("MapEditorArena.txt")
        )
        main_layout.addWidget(save_button, 1, 5, 1, 1)

        # Add an empty stretch to push buttons to the bottom
        main_layout.setRowStretch(0, 1)

        # change size, position of buttons
        water_button.setGeometry(50, 50, 100, 30)
        fire_button.setGeometry(50, 100, 100, 30)
        wall_button.setGeometry(50, 150, 100, 30)
        boost_button.setGeometry(50, 200, 100, 30)
        spikes_button.setGeometry(50, 250, 100, 30)
        save_button.setGeometry(50, 300, 100, 30)

        # list of shapes,blue rectangle, red rectangle...
        self.shapes = []
        self.start_point = None

    # converts the drawn arena into a textfile and saves this
    def save_to_text_file(self, filename):
        image = self.grab().toImage()  # makes screenshot of window
        image = image.scaled(
            100, 100
        )  # scales to size 100x100 so that 1 pixel is 1 tile

        with open(filename, "w") as file:
            for y in range(image.height()):
                for x in range(image.width()):
                    color = image.pixelColor(x, y)
                    if color == Qt.red:
                        file.write("f")
                    elif color == Qt.blue:
                        file.write("a")
                    elif color == Qt.black:
                        file.write("b")
                    else:
                        file.write("n")

    def paintEvent(self, event):
        # Create a QPainter object
        painter = QPainter(self)

        # Draw the shapes
        for shape in self.shapes:
            if shape[0] == "water":
                pen = QPen(Qt.blue)
                brush = QBrush(Qt.blue)
            elif shape[0] == "fire":
                pen = QPen(Qt.red)
                brush = QBrush(Qt.red)
            elif shape[0] == "wall":
                pen = QPen(Qt.black)
                brush = QBrush(Qt.black)
            elif shape[0] == "spikes":
                pen = QPen(Qt.gray)
                brush = QBrush(Qt.gray)
            elif shape[0] == "boost":
                pen = QPen(Qt.green)
                brush = QBrush(Qt.green)

            painter.setPen(pen)
            painter.setBrush(brush)

            painter.drawRect(*shape[1:])

    def set_draw_mode(self, mode):
        self.draw_mode = mode

    def mousePressEvent(self, event):
        if self.draw_mode is not None:
            self.start_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.draw_mode is not None and self.start_point is not None:
            width = event.pos().x() - self.start_point.x()
            height = event.pos().y() - self.start_point.y()

            shape = (
                self.draw_mode,
                self.start_point.x(),
                self.start_point.y(),
                width,
                height,
            )
            self.shapes.append(shape)
            self.update()

    def mouseReleaseEvent(self, event):
        if self.draw_mode is not None and self.start_point is not None:
            width = event.pos().x() - self.start_point.x()
            height = event.pos().y() - self.start_point.y()

            shape = (
                self.draw_mode,
                self.start_point.x(),
                self.start_point.y(),
                width,
                height,
            )
            self.shapes.append(shape)
            self.update()

        self.start_point = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = MapEditor()
    editor.show()
    sys.exit(app.exec_())