from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRect
import sys



class MapEditor(QWidget):
    def __init__(self):
        super().__init__()

        # title and size of window
        self.setWindowTitle('Map Editor')
        self.setGeometry(100, 100, 1000, 1000)

        # create Grid Layout
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # create buttons
        self.draw_mode = None
        water_button = QPushButton('Water')
        grid_layout.addWidget(water_button)
        water_button.clicked.connect(lambda: self.set_draw_mode('water'))
        #lambda so we can give functions as parameters
        #without create new functions

        fire_button = QPushButton('Fire')
        grid_layout.addWidget(fire_button)
        fire_button.clicked.connect(lambda: self.set_draw_mode('fire'))
        wall_button = QPushButton('Wall')
        grid_layout.addWidget(wall_button)
        wall_button.clicked.connect(lambda: self.set_draw_mode('wall'))

        save_button = QPushButton('Save')
        grid_layout.addWidget(save_button)
        save_button.clicked.connect(lambda: self.save_to_text_file('MapEditorArena.txt'))

        # list of shapes,blue rectangle, red rectangle...
        self.shapes = []
        self.start_point = None


    #converts the drawn arena into a textfile and saves this
    def save_to_text_file(self, filename):
        image = self.grab().toImage()
        image = image.scaled(100, 100)

        with open(filename, 'w') as file:
            for y in range(image.height()):
                for x in range(image.width()):
                    color = image.pixelColor(x, y)
                    if color == Qt.red:
                        file.write('f')
                    elif color == Qt.blue:
                        file.write('a')
                    elif color == Qt.black:
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
            elif shape[0] == 'fire':
                pen = QPen(Qt.red)
                brush = QBrush(Qt.red)
            elif shape[0] == 'wall':
                pen = QPen(Qt.black)
                brush = QBrush(Qt.black)

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

            shape = (self.draw_mode, self.start_point.x(), self.start_point.y(), width, height)
            self.shapes.append(shape)
            self.update()

    def mouseReleaseEvent(self, event):
        if self.draw_mode is not None and self.start_point is not None:
            width = event.pos().x() - self.start_point.x()
            height = event.pos().y() - self.start_point.y()

            shape = (self.draw_mode, self.start_point.x(), self.start_point.y(), width, height)
            self.shapes.append(shape)
            self.update()

        self.start_point = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = MapEditor()
    editor.show()
    sys.exit(app.exec_())
