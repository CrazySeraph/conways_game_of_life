import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QSlider, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, \
    QSpinBox


class Example(QWidget):

    def __init__(self):
        super().__init__()

        # Set the maximum value for the slider
        self.maxslider = 50

        # Create a button to start and stop the animation
        self.pause_button = QPushButton('Start', self)
        self.pause_button.clicked.connect(self.on_pause_click)
        self.pause_button.setStyleSheet('''
            QPushButton {
                background-color: #50C878;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 30px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #3CB371;
                color: white;
            }
        ''')

        # Create buttons to move the animation left and right
        self.left_button = QPushButton('◀', self)
        self.left_button.clicked.connect(self.on_left_click)
        self.left_button.setStyleSheet('''
            QPushButton {
                background-color: #F08080;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 30px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #CD5C5C;
                color: white;
            }
        ''')
        self.right_button = QPushButton('▶', self)
        self.right_button.clicked.connect(self.on_right_click)
        self.right_button.setStyleSheet('''
            QPushButton {
                background-color: #F08080;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 30px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #CD5C5C;
                color: white;
            }
        ''')

        # Create a slider to adjust the speed of the animation
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(1, self.maxslider)
        self.slider.setValue(self.maxslider // 2)
        self.slider.valueChanged.connect(self.on_slider_change)
        self.slider.setStyleSheet('''
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
            }

            QSlider::handle:horizontal {
                background: #50C878;
                border: none;
                height: 30px;
                width: 30px;
                margin: -10px 0;
                border-radius: 20px;
            }

            QSlider::handle:horizontal:hover {
                background: #3CB371;
                border: none;
                height: 30px;
                width: 30px;
                margin: -10px 0;
                border-radius: 20px;
            }
        ''')

        # Set up the main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Add the pause button to the top of the layout
        main_layout.addWidget(self.pause_button)

        # Add some spacing between the pause button and the slider
        main_layout.addSpacing(40)

        # Add the slider to the layout
        main_layout.addWidget(self.slider)

        # Add the left and right buttons to the layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.left_button)
        button_layout.addWidget(self.right_button)
        button_layout.setContentsMargins(0, 20, 0, 0)
        main_layout.addLayout(button_layout)

        self.show()

    def on_pause_click(self):
        # handle pause button click
        pass

    def on_left_click(self):
        # handle left button click
        pass

    def on_right_click(self):
        # handle right button click
        pass

    def on_slider_change(self, value):
        # handle slider value change
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())
