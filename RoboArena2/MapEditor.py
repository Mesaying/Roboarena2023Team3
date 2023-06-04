from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap
from PyQt5.QtCore import Qt

import sys

class MapEditor(QWidget):
    def __init__(self):
        super().__init__()

        # graphical tile
        self.selected_graphical_tile = None

        # title and size of window
        self.setWindowTitle('Map Editor')
        self.setGeometry(100, 100, 1000, 1000)

        # create the main layout
        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # create buttons
        self.draw_mode = None
        water_button = QPushButton('Water')
        water_button.setMaximumWidth(100)
        water_button.setMaximumHeight(30)
        water_button.clicked.connect(lambda: self.set_draw_mode('water'))
        main_layout.addWidget(water_button, 1, 0, 1, 1) #widget, row, column, rowspan colspan

        fire_button = QPushButton('Fire')
        fire_button.setMaximumWidth(100)
        fire_button.setMaximumHeight(30)
        fire_button.clicked.connect(lambda: self.set_draw_mode('fire'))
        main_layout.addWidget(fire_button, 1, 1, 1, 1)

        wall_button = QPushButton('Wall')
        wall_button.setMaximumWidth(100)
        wall_button.setMaximumHeight(30)
        wall_button.clicked.connect(lambda: self.set_draw_mode('wall'))
        main_layout.addWidget(wall_button, 1, 2, 1, 1)

        boost_button = QPushButton('Boost')
        boost_button.setMaximumWidth(100)
        boost_button.setMaximumHeight(30)
        boost_button.clicked.connect(lambda: self.set_draw_mode('boost'))
        main_layout.addWidget(boost_button, 1, 3, 1, 1)

        spikes_button = QPushButton('Spikes')
        spikes_button.setMaximumWidth(100)
        spikes_button.setMaximumHeight(30)
        spikes_button.clicked.connect(lambda: self.set_draw_mode('spikes'))
        main_layout.addWidget(spikes_button, 1, 4, 1, 1)

        new_button = QPushButton("New")
        new_button.setMaximumWidth(100)
        new_button.setMaximumHeight(30)
        new_button.clicked.connect(self.new_map)
        main_layout.addWidget(new_button, 1, 6, 1, 1)

        save_button = QPushButton('Save')
        save_button.setMaximumWidth(100)
        save_button.setMaximumHeight(30)
        save_button.clicked.connect(lambda: self.save_to_text_file('MapEditorArena.txt'))
        main_layout.addWidget(save_button, 1, 5, 1, 1)

        undo_button = QPushButton("Undo")
        undo_button.setMaximumWidth(100)
        undo_button.setMaximumHeight(30)
        undo_button.clicked.connect(self.undo_last_shape)
        main_layout.addWidget(undo_button, 1, 8, 1, 1)

        # Add an empty stretch to push buttons to the bottom
        main_layout.setRowStretch(0, 1)

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

    #converts the drawn arena into a textfile and saves it
    def save_to_text_file(self, filename):
        image = self.grab().toImage()    #makes screenshot of window
        image = image.scaled(100, 100)   #scales to size 100x100 so that 1 pixel is 1 tile

        with open(filename, 'w') as file:
            for y in range(image.height()):  #iterate through every pixel
                for x in range(image.width()):
                    color = image.pixelColor(x, y)
                    if color == Qt.red:
                        file.write('f')
                    elif color == Qt.blue:
                        file.write('a')
                    elif color == Qt.black:
                        file.write('b')
                    elif color == Qt.gray:
                        file.write('s')
                    elif color == Qt.green:
                        file.write('b')
                    else:
                        file.write('n')


    def paintEvent(self, event):
        # Create a QPainter object
        painter = QPainter(self)

        # Draw the shapes
        for shape in self.shapes:
            if shape[0] == 'water':
                pen = QPen(Qt.blue)
                brush = QBrush(Qt.blue)
                # Draw the graphical tile
                if len(shape) > 5:
                    graphical_tile = shape[5]
                    painter.drawPixmap(shape[1], shape[2], graphical_tile)
            elif shape[0] == 'fire':
                pen = QPen(Qt.red)
                brush = QBrush(Qt.red)
            elif shape[0] == 'wall':
                pen = QPen(Qt.black)
                brush = QBrush(Qt.black)
            elif shape[0] == 'spikes':
                pen = QPen(Qt.gray)
                brush = QBrush(Qt.gray)
            elif shape[0] == 'boost':
                pen = QPen(Qt.green)
                brush = QBrush(Qt.green)

            painter.setPen(pen)
            painter.setBrush(brush)

            painter.drawRect(*shape[1:])

        # Draw the temporary shape during mouse move
        if self.temp_shape:
            shape = self.temp_shape
            if shape[0] == 'water':
                pen = QPen(Qt.blue)
                brush = QBrush(Qt.blue)
            elif shape[0] == 'fire':
                pen = QPen(Qt.red)
                brush = QBrush(Qt.red)
            elif shape[0] == 'wall':
                pen = QPen(Qt.black)
                brush = QBrush(Qt.black)
            elif shape[0] == 'spikes':
                pen = QPen(Qt.gray)
                brush = QBrush(Qt.gray)
            elif shape[0] == 'boost':
                pen = QPen(Qt.green)
                brush = QBrush(Qt.green)

            painter.setPen(pen)
            painter.setBrush(brush)

            painter.drawRect(*shape[1:])


    def mousePressEvent(self, event):
        if self.draw_mode is not None:
            self.start_point = event.pos()

            if self.draw_mode == 'water' and self.selected_graphical_tile is not None:
                width = self.selected_graphical_tile.width()
                height = self.selected_graphical_tile.height()
                self.shapes.append(
                    ('water', self.start_point.x(), self.start_point.y(), width, height, self.selected_graphical_tile))
                self.update()

    def mouseMoveEvent(self, event):
        if self.draw_mode is not None and self.start_point is not None:
            width = event.pos().x() - self.start_point.x()
            height = event.pos().y() - self.start_point.y()

            self.temp_shape = (self.draw_mode, self.start_point.x(), self.start_point.y(), width, height)
            self.update()

    def mouseReleaseEvent(self, event):
        if self.draw_mode is not None and self.start_point is not None:
            width = event.pos().x() - self.start_point.x()
            height = event.pos().y() - self.start_point.y()

            shape = (self.draw_mode, self.start_point.x(), self.start_point.y(), width, height)
            self.shapes.append(shape)
            self.update()

        self.start_point = None
        self.temp_shape = None

    def new_map(self):
        self.shapes = []
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = MapEditor()
    editor.show()
    sys.exit(app.exec_())
