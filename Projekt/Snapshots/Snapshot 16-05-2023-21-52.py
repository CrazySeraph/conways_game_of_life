import configparser
import os
import sys

import numpy as np
import pygame
import qdarkstyle
from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QAction
from PyQt6.QtWidgets import QApplication, QWidget, QFrame, QPushButton, QSlider, QHBoxLayout, QVBoxLayout, \
    QLabel, QSpacerItem, QSizePolicy, QMenuBar, QFileDialog, QWidgetAction
from keras.datasets import mnist
from scipy.signal import convolve2d


########################################################################################################################
#                                             PROJEKT_K -- Main                                                        #
########################################################################################################################

(x_train, _), (_, _) = mnist.load_data()
class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 200, 400)
        self.setWindowTitle('Game of Life Steuerung')

        self.frame = QFrame(self)
        self.frame.setGeometry(10, 10, 400, 400)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        correct_dir = os.path.abspath(os.path.join(parent_dir, './Simulation Files'))
        self.simulationpath = correct_dir
        self.active, self.rand_lvl = False, 0.50
        self.background_col, self.rect_col, self.fill_col = pygame.Color("#E8E8E8"), pygame.Color(
            '#AAAAAA'), pygame.Color('#1E90FF')
        self.sim_x, self.sim_y = 100, 100
        self.screen_width, self.screen_height = 1000, 1000
        self.array_now = np.zeros((self.sim_y, self.sim_x), dtype=int)
        self.array_state = self.array_now
        self.square_size = int(self.screen_width / len(self.array_now))
        self.speed = 10
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Conways game of Life - Kiste Edition")

        self.configdir = os.path.abspath(os.path.join(parent_dir, './Configs'))
        self.configmode = configparser.ConfigParser()
        self.configmode.read(self.configdir + '/mode.ini')
        self.DarkStyle = False
        if self.configmode.getboolean('StyleMode', 'mode'):
            self.Swap_UI()

        self.mb_close_icon, self.mb_max_icon, self.mb_min_icon, self.mac_mode_bool = '\u2716', '\U0001F5D6', '\U0001F5D5', False
        self.menu_bar = QMenuBar()
        self.mb_close = QAction(self.mb_close_icon, self)
        self.mb_close.triggered.connect(self.closeEvent)
        self.mb_max = QAction(self.mb_max_icon, self)
        self.mb_max.triggered.connect(self.maxEvent)
        self.mb_min = QAction(self.mb_min_icon, self)
        self.mb_min.triggered.connect(self.minEvent)
        self.settings = self.menu_bar.addMenu('Settings')
        self.UISwap = QAction('Swap UI', self)
        self.UISwap.setShortcut('Ctrl+Shift+U')
        self.UISwap.setStatusTip('Swaps the UI')
        self.UISwap.triggered.connect(self.Swap_UI)
        self.settings.addAction(self.UISwap)
        self.simulation = self.menu_bar.addMenu('Simulation')
        self.save_simu = QAction('Save Simulation', self)
        self.save_simu.setShortcut('Ctrl+Shift+s')
        self.save_simu.setStatusTip('Saves the Simulation')
        self.save_simu.triggered.connect(self.save_simulation)
        self.load_simu = QAction('Load Simulation', self)
        self.load_simu.setShortcut('Ctrl+Shift+l')
        self.load_simu.setStatusTip('Loads the Simulation')
        self.load_simu.triggered.connect(self.load_simulation)
        self.rand_simu = QAction('Randomize Simulation', self)
        self.rand_simu.setShortcut('Ctrl+Shift+r')
        self.rand_simu.setStatusTip('Randomizes the Simulation')
        self.rand_simu.triggered.connect(self.rand_simulation)
        self.rand_slider_a = QWidgetAction(self)
        self.rand_slider_a.setDefaultWidget(QSlider(Qt.Orientation.Horizontal))
        rand_slider = self.rand_slider_a.defaultWidget()
        rand_slider.setRange(1, 100)
        rand_slider.setSingleStep(1)
        rand_slider.setValue(int(self.rand_lvl * 100))
        rand_slider.valueChanged.connect(self.on_rand_slider_change)
        self.imp_image = QAction('Import an Image', self)
        self.imp_image.setShortcut('Ctrl+Shift+i')
        self.imp_image.setStatusTip('import an image to display in the simulation')
        self.imp_image.triggered.connect(lambda: self.import_image('load'))
        self.rand_image = QAction('Load a random Image', self)
        self.rand_image.setShortcut('Ctrl+Shift+m')
        self.rand_image.setStatusTip(
            'Loads 9 random images from a dataset and combines them into one then displays them')
        self.rand_image.triggered.connect(lambda: self.import_image('gen'))
        self.simulation.addActions(
            (self.save_simu, self.load_simu, self.rand_simu, self.rand_slider_a, self.imp_image, self.rand_image))
        self.menu_bar.addActions((self.mb_close, self.mb_max, self.mb_min))
        self.menu_bar.addMenu(self.simulation)
        self.menu_bar.addMenu(self.settings)

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
        self.maxslider = 50
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
        self.slider_label = QLabel(self)
        self.slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.slider_label.setText(str(f"Ticks pro Sekunde: {self.slider.value()}"))
        self.slider_label.setStyleSheet('''
            QLabel {
                font-size: 20px;
                color: #808080;
                margin-top: 10px;
            }
        ''')
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
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_board)
        self.reset_button.setStyleSheet('''
            QPushButton {
                background-color: #F7DC6F;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 30px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #D4B85D;
                color: white;
            }
        ''')
        self.clear_button = QPushButton('Clear', self)
        self.clear_button.clicked.connect(self.clear_board)
        self.clear_button.setStyleSheet('''
            QPushButton {
                background-color: #F7DC6F;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 30px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #D4B85D;
                color: white;
            }
        ''')

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(self.pause_button)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.slider)
        main_layout.addWidget(self.slider_label)
        main_layout.setMenuBar(self.menu_bar)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.left_button)
        button_layout.addWidget(self.right_button)
        button_layout.setContentsMargins(0, 20, 0, 0)
        spacer = QSpacerItem(1, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        button_layout.addItem(spacer)

        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(self.reset_button)
        button_layout2.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)
        main_layout.addLayout(button_layout2)
        self.setLayout(main_layout)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.show()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    row = mouse_pos[1] // self.square_size
                    col = mouse_pos[0] // self.square_size
                    self.array_now[row][col] = 0 if self.array_now[row][col] == 1 else 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_PLUS or event.key == pygame.K_RIGHT:
                        self.on_right_click()
                    if event.key == pygame.K_KP_MINUS or event.key == pygame.K_LEFT:
                        self.on_left_click()
                    if event.key == pygame.K_SPACE:
                        self.on_pause_click()
                    if (event.mod & pygame.KMOD_CTRL) and (event.mod & pygame.KMOD_SHIFT):
                        if event.key == pygame.K_u:
                            self.Swap_UI()
                        if event.key == pygame.K_s:
                            self.save_simulation()
                        if event.key == pygame.K_l:
                            self.load_simulation()
                        if event.key == pygame.K_r:
                            self.rand_simulation()
                        if event.key == pygame.K_i:
                            self.import_image()

            self.screen.fill(pygame.Color(self.background_col))
            self.draw_grid()
            self.Game_of_Life_Logic()
            pygame.display.flip()
            self.clock.tick(self.speed)

    def draw_grid(self):
        length = len(self.array_now)
        for row in range(length):
            for col in range(length):
                rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(self.screen, self.rect_col, rect, 1)
                if self.array_now[row][col] == 1:
                    pygame.draw.rect(self.screen, self.fill_col, rect)

    def Game_of_Life_Logic(self):
        if self.active:
            kernel = np.array([[1, 1, 1],
                               [1, 0, 1],
                               [1, 1, 1]])
            convolved = convolve2d(self.array_now, kernel, mode='same')
            self.array_now = np.where((self.array_now == 1) & ((convolved < 2) | (convolved > 3)), 0, self.array_now)
            self.array_now = np.where((self.array_now == 1) & ((convolved == 2) | (convolved == 3)), 1, self.array_now)
            self.array_now = np.where((self.array_now == 0) & (convolved == 3), 1, self.array_now)

    def on_pause_click(self):
        self.active = not self.active
        self.pause_button.setText('Pause' if self.active else 'Start')
        pause_style = self.pause_button.styleSheet()
        if self.pause_button.text() == 'Pause':
            pause_style = pause_style.replace("background-color: #50C878", "background-color: #F08080")
            pause_style = pause_style.replace("background-color: #3CB371", "background-color: #CD5C5C")
            self.array_state = self.array_now
        else:
            pause_style = pause_style.replace("background-color: #F08080", "background-color: #50C878")
            pause_style = pause_style.replace("background-color: #CD5C5C", "background-color: #3CB371")
        self.pause_button.setStyleSheet(pause_style)

    def on_slider_change(self, value):
        self.speed = value
        self.slider_label.setText(str(f"Ticks pro Sekunde: {self.slider.value()}"))

    def on_rand_slider_change(self, value):
        self.rand_lvl = round((value - 1) / 99 * (1 - 0.01) + 0.01, 2)

    def on_left_click(self):
        if self.slider.value() > 1:
            self.slider.setValue(self.slider.value() - 1)
        else:
            print('Verlangsamung nicht möglich!')

    def on_right_click(self):
        if self.slider.value() < self.maxslider:
            self.slider.setValue(self.slider.value() + 1)
        else:
            print('Beschleunigung nicht möglich!')

    def keyEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Space:
            self.on_pause_click()
        elif event.key() == Qt.Key.Key_Right:
            self.on_right_click()
        elif event.key() == Qt.Key.Key_Left:
            self.on_left_click()

    def reset_board(self):
        if self.active:
            self.on_pause_click()
        if not self.active:
            self.array_now = self.array_state

    def clear_board(self):
        self.array_now.fill(0)

    def closeEvent(self, event):
        self.configmode.set('StyleMode', 'mode', str(self.DarkStyle))
        with open(self.configdir + '/mode.ini', 'w') as configfile:
            self.configmode.write(configfile)
        pygame.quit()
        sys.exit()

    def Swap_UI(self):
        if not self.DarkStyle:
            self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            self.background_col, self.rect_col, self.fill_col = pygame.Color("#1E1E1E"), pygame.Color(
                "#424242"), pygame.Color("#EDEDED")
            self.DarkStyle = True
        else:
            self.setStyleSheet('')
            self.background_col, self.rect_col, self.fill_col = pygame.Color("#E8E8E8"), pygame.Color(
                '#AAAAAA'), pygame.Color('#1E90FF')
            self.DarkStyle = False

    def maxEvent(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def minEvent(self):
        self.showMinimized()

    def save_simulation(self):
        file_path, _ = QFileDialog().getSaveFileName(self, "Save Simulation", self.simulationpath,
                                                     "Numpy Files (*.npy)")

        if file_path:
            try:
                np.save(file_path, self.array_now)
                print('Simulation saved successfully')
            except Exception as error:
                print('Error while saving the Simulation: ', error)

    def load_simulation(self):
        file_path, _ = QFileDialog().getOpenFileName(self, "Select Simulation File", self.simulationpath,
                                                     "Numpy Files (*.npy)")

        if self.active:
            self.on_pause_click()
        if file_path and not self.active:
            try:
                self.array_now = np.load(file_path)
            except Exception as error:
                print('Error while loading the Simulation: ', error)

    def rand_simulation(self):
        rand_1 = 1 - self.rand_lvl
        rand_2 = 1 - rand_1
        if self.active:
            self.on_pause_click()
        if not self.active:
            self.array_now = np.random.choice([0, 1], size=(100, 100), p=(rand_1, rand_2))

    def import_image(self, stringvar):
        if stringvar == 'load':
            file_path, _ = QFileDialog().getOpenFileName(self, "Select Simulation File", '',
                                                         "Image Files (*.png *.jpg *.jpeg)")
            if self.active:
                self.on_pause_click()
            if file_path and not self.active:
                try:
                    image = Image.open(file_path)
                    image.thumbnail((100, 100))
                except Exception as error:
                    print('Error while loading the Image: ', error)
        elif stringvar == 'gen':
            random_indices = np.random.choice(len(x_train), size=9, replace=False)
            grid_size = (3, 3)
            combined_image = np.zeros((grid_size[0] * 28, grid_size[1] * 28))
            for i, idx in enumerate(random_indices):
                row = i // grid_size[1]
                col = i % grid_size[1]
                image = x_train[idx]
                row_start = row * 28
                row_end = (row + 1) * 28
                col_start = col * 28
                col_end = (col + 1) * 28
                combined_image[row_start:row_end, col_start:col_end] = image
                image = Image.fromarray(combined_image.astype(np.uint8))
        image_gray = image.convert("L")
        image_binary = image_gray.point(lambda p: int(p > 128))
        image_array = np.array(image_binary)
        copy_array = np.zeros((100, 100))
        height, width = image_array.shape
        start_row = (100 - height) // 2
        start_col = (100 - width) // 2
        copy_array[start_row:start_row + height, start_col:start_col + width] = image_array
        self.array_now = copy_array

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = Main()
    Main.run()
    sys.exit(app.exec())
