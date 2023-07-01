import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QMainWindow
from PyQt5.uic import loadUi

GRID_SIZE = 20
GRID_CELL_SIZE = 50


class MapEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        loadUi("MenuAssets\\MapEditor.ui", self)

        # Make the window non-resizable
        self.setFixedSize(self.size())

        # Create a 2D grid to store the drawn shapes
        self.grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]

        # Initialize the grid with empty labels
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                label = QLabel(self)
                label.setGeometry(
                    col * GRID_CELL_SIZE,
                    row * GRID_CELL_SIZE,
                    GRID_CELL_SIZE,
                    GRID_CELL_SIZE,
                )
                label.setStyleSheet(
                    "background-color: white; border: 1px solid gray;"
                )
                self.grid[row][col] = label

        # Create buttons and connect signals
        self.water_button.clicked.connect(lambda: self.set_draw_mode("water"))
        self.fire_button.clicked.connect(lambda: self.set_draw_mode("fire"))
        self.wall_button.clicked.connect(lambda: self.set_draw_mode("wall"))
        self.boost_button.clicked.connect(lambda: self.set_draw_mode("boost"))
        self.spikes_button.clicked.connect(
            lambda: self.set_draw_mode("spikes")
        )
        self.normal_button.clicked.connect(lambda: self.set_draw_mode(("normal")))
        self.undo_button.clicked.connect(lambda: self.undo())
        self.new_button.clicked.connect(lambda: self.clear_grid())
        self.save_button.clicked.connect(lambda: self.save_to_text_file())


        # Initialize draw mode to None
        self.draw_mode = None

        # Array to save state of grid
        self.tile_array = [["n"] * GRID_SIZE for _ in range(GRID_SIZE)]
        print(self.tile_array)

        # List of all drawn tiles
        self.tiles_drawn = []

    def set_draw_mode(self, mode):
        self.draw_mode = mode

    def mousePressEvent(self, event):
        if self.draw_mode and event.buttons() == Qt.LeftButton:
            row = event.y() // GRID_CELL_SIZE
            col = event.x() // GRID_CELL_SIZE

            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                label = self.grid[row][col]
                image_path = ""

                if self.draw_mode == "water":
                    image_path = "TileImages\\Water_tile.png"
                    self.tile_array[row][col] = "a"
                elif self.draw_mode == "fire":
                    image_path = "TileImages\\Fire_tile.png"
                    self.tile_array[row][col] = "f"
                elif self.draw_mode == "wall":
                    image_path = "TileImages\\Wall_tile.png"
                    self.tile_array[row][col] = "w"
                elif self.draw_mode == "boost":
                    image_path = "TileImages\\Boost_tile.png"
                    self.tile_array[row][col] = "b"
                elif self.draw_mode == "spikes":
                    image_path = "TileImages\\Spike_tile.png"
                    self.tile_array[row][col] = "s"
                else:
                    image_path = "TileImages\\Normal_tile.png"
                    self.tile_array[row][col] = "n"

                pixmap = QPixmap(image_path)
                label.setPixmap(pixmap.scaled(GRID_CELL_SIZE, GRID_CELL_SIZE))

                self.tiles_drawn.append([row , col])

    def clear_grid(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                label = self.grid[row][col]
                label.clear()  # Remove the pixmap from the label
                label.setStyleSheet(
                    "background-color: white; border: 1px solid gray;"
                )

    def save_to_text_file(self):
        # opens dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Map", "", "Text Files (*.txt)"
        )

        with open(file_path, "w") as file:
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    file.write(str(self.tile_array[row][col]))


    def undo(self):
        # removes last drawn tile
        if len(self.tiles_drawn) > 0:
            pos = self.tiles_drawn.pop(0)

            row = pos[0]
            col = pos[1]

            label = self.grid[row][col]
            label.clear()  # Remove the pixmap from the label
            label.setStyleSheet(
            "background-color: white; border: 1px solid gray;"
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapEditor()
    window.show()
    sys.exit(app.exec_())
