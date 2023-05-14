import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the main window
    window = QWidget()
    window.setWindowTitle("Custom Window Frame")
    window.setWindowFlag(Qt.WindowType.FramelessWindowHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    # Set the window background color to black
    palette = window.palette()
    palette.setColor(window.backgroundRole(), QColor(0, 0, 0))
    window.setPalette(palette)

    # Set the window size and show it
    window.setGeometry(100, 100, 500, 500)
    window.show()

    sys.exit(app.exec())
