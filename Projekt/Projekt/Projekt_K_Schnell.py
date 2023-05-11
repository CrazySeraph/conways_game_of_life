import sys
import numpy as np
import pygame
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QFrame, QPushButton, \
    QSlider
from scipy.signal import convolve2d


class Main(QWidget):
    def __init__(self):
        super().__init__()

        # Fenster Eigenschaften
        self.setGeometry(100, 100, 200, 400)
        self.setWindowTitle('Game of Life Steuerung')

        # Frame erstellen
        self.frame = QFrame(self)
        self.frame.setGeometry(10, 10, 400, 400)

        # Array für Game of Life
        self.array_now = np.zeros((100, 100), dtype=int)

        # Simulationsstatus und Zellengröße
        self.active = False
        self.square_size = 10

        # Farben für die Zellen
        self.rect_col, self.fill_col = pygame.Color('grey'), pygame.Color('white')

        # Aufsetzung des Pygame Fensters
        self.screen_width, self.screen_height = 1000, 1000
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Conways game of Life - Kiste Edition")

        # Die Simulationsgeschwindigkeit wird festgelegt
        # PyQt6 UI Elemente
        self.speed = 10
        self.maxslider = 50
        self.pause_button = QPushButton('▶️', self)
        self.pause_button.setGeometry(20, 20, self.width() - 40, 60)
        self.pause_button.clicked.connect(self.on_pause_click)
        self.left_button = QPushButton('\u23EA', self)
        self.left_button.setGeometry(20, 100, 60, 60)
        self.left_button.clicked.connect(self.on_left_click)
        self.right_button = QPushButton('\u23E9', self)
        self.right_button.setGeometry(self.width() - 80, 100, 60, 60)
        self.right_button.clicked.connect(self.on_right_click)
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(1, self.maxslider)
        self.slider.setValue(self.maxslider // 2)
        self.slider.valueChanged.connect(self.on_slider_change)
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
                    if event.key == pygame.K_KP_PLUS:
                        self.on_right_click()
                    if event.key == pygame.K_KP_MINUS:
                        self.on_left_click()
                    if event.key == pygame.K_SPACE:
                        self.on_pause_click()
            self.screen.fill(pygame.Color('black'))
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
        self.pause_button.setText('⏸️' if self.active else '▶️')

    def on_slider_change(self, value):
        self.speed = value

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

    def closeEvent(self, event):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = Main()
    Main.run()
    sys.exit(app.exec())