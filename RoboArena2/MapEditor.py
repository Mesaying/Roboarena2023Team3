import sys

from Menus import ExtrasMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi


class MapEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # graphical tile
        self.selected_graphical_tile = None

        # Load the UI file
        loadUi("MenuAssets\\MapEditor.ui", self)

        # Make the window non-resizable
        self.setFixedSize(self.size())

        # create buttons
        self.draw_mode = None

        self.water_button.clicked.connect(lambda: self.set_draw_mode("water"))

        self.fire_button.clicked.connect(lambda: self.set_draw_mode("fire"))

        self.wall_button.clicked.connect(lambda: self.set_draw_mode("wall"))

        self.boost_button.clicked.connect(lambda: self.set_draw_mode("boost"))

        self.spikes_button.clicked.connect(
            lambda: self.set_draw_mode("spikes")
        )

        self.new_button.clicked.connect(self.new_map)

        self.save_button.clicked.connect(
            lambda: self.save_to_text_file("MapEditorArena.txt")
        )

        self.undo_button.clicked.connect(self.undo_last_shape)

        self.load_button.clicked.connect(self.load_map_txt)

        self.back_button.clicked.connect(self.back)

        # list of shapes,blue rectangle, red rectangle...
        self.shapes = []
        self.start_point = None
        self.temp_shape = None

    def set_draw_mode(self, mode):
        self.draw_mode = mode

    def undo_last_shape(self):
        if self.shapes:
            self.shapes.pop()
            self.update()

    # converts the drawn arena into a textfile and saves it
    def save_to_text_file(self, filename):
        image = self.grab().toImage()  # makes screenshot of window
        image = image.scaled(
            100, 100
        )  # scales to size 100x100 so that 1 pixel is 1 tile

        with open(filename, "w") as file:
            for y in range(100):  # iterate through every pixel
                for x in range(100):
                    color = image.pixelColor(x, y)
                    if color == Qt.red:
                        file.write("f")
                    elif color == Qt.blue:
                        file.write("a")
                    elif color == Qt.black:
                        file.write("b")
                    elif color == Qt.gray:
                        file.write("s")
                    elif color == Qt.green:
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
                # Draw the graphical tile
                if len(shape) > 5:
                    graphical_tile = shape[5]
                    painter.drawPixmap(shape[1], shape[2], graphical_tile)
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
            elif shape[0] == "normal":
                pen = QPen(Qt.white)
                brush = QBrush(Qt.white)

            painter.setPen(pen)
            painter.setBrush(brush)

            painter.drawRect(*shape[1:])

        # Draw the temporary shape during mouse move
        if self.temp_shape:
            shape = self.temp_shape
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
            elif shape[0] == "normal":
                pen = QPen(Qt.white)
                brush = QBrush(Qt.white)

            painter.setPen(pen)
            painter.setBrush(brush)

            painter.drawRect(*shape[1:])

    def mousePressEvent(self, event):
        if self.draw_mode is not None:
            self.start_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.draw_mode is not None and self.start_point is not None:
            width = event.pos().x() - self.start_point.x()
            height = event.pos().y() - self.start_point.y()

            self.temp_shape = (
                self.draw_mode,
                self.start_point.x(),
                self.start_point.y(),
                width,
                height,
            )
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
        self.temp_shape = None

    def new_map(self):
        self.shapes = []
        self.update()

    def back(self):
        position = self.pos()
        x_coord = position.x()
        y_coord = position.y()
        self.extras_menu = ExtrasMenu(x_coord, y_coord)
        self.extras_menu.show()
        self.close()

    def load_map_txt(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Text Files (*.txt)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            file_path = selected_files[0]
            print("Selected file:", file_path)
            with open(file_path, "r") as file:
                text = (
                    file.read().replace(" ", "").replace("\n", "")
                )  # sprint bringen
                index = 0
                for x in range(100):
                    for y in range(100):
                        letter = text[index]
                        index = index + 1
                        print(letter)
                        if letter == "a":
                            self.set_draw_mode("water")
                        if letter == "f":
                            self.set_draw_mode("fire")
                        if letter == "s":
                            self.set_draw_mode("spikes")
                        if letter == "w":
                            self.set_draw_mode("wall")
                        if letter == "b":
                            self.set_draw_mode("boost")
                        if letter == "n":
                            self.set_draw_mode("normal")
                        shape = (
                            self.draw_mode,
                            y * 10,
                            x * 10,
                            1 * 10,
                            1 * 10,
                        )
                        self.shapes.append(shape)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapEditor()
    window.show()
    sys.exit(app.exec_())
