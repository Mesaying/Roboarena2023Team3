#!/usr/bin/python

import sys

from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(250, 150)
        self.center()

        self.setWindowTitle("Center")
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
