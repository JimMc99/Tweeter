from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
import sys

from tweeter import TrumpTweeter


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.trump_tweeter = TrumpTweeter()

        self.setWindowTitle('Trump says:')

        self.label = QLabel(self.trump_tweeter.new_tweet())
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        button = QPushButton('New tweet!')
        button.clicked.connect(self.onButtonClick)

        layout = QVBoxLayout()

        layout.addWidget(self.label)
        layout.addWidget(button)

        widget = QWidget()
        widget.setMinimumWidth(800)
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    @pyqtSlot(bool)
    def onButtonClick(self, checked):
        print('Button pressed')
        self.label.setText(self.trump_tweeter.new_tweet())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
