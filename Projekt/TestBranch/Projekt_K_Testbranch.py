import sys
import numpy as np
import pygame
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QFrame, QPushButton, \
    QSlider
import time

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

        # Simulationsstatus und zellengröße
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

        # Die Simulationsgeschwindgkeit wird festgelegt
        # PyQt6 UI Elemente
        self.speed = 10
        self.pause_button = QPushButton('▶️', self)
        self.pause_button.setGeometry(20, 20, self.width() - 40, 60)
        self.pause_button.clicked.connect(self.on_pause_click)
        self.left_button = QPushButton('', self)
        self.left_button.setGeometry(20, 100, 60, 60)
        self.left_button.setText('\u23EA')
        self.left_button.clicked.connect(self.on_left_click)
        self.right_button = QPushButton('', self)
        self.right_button.setGeometry(self.width() - 80, 100, 60, 60)
        self.right_button.setText('\u23E9')
        self.right_button.clicked.connect(self.on_right_click)
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 20)
        self.slider.setValue(10)
        self.slider.valueChanged.connect(self.on_slider_change)
        self.slider.setParent(self)
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
                    if self.array_now[row][col] == 1:
                        self.array_now[row][col] = 0
                    else:
                        self.array_now[row][col] = 1
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
        for row in range(len(self.array_now)):
            for col in range(len(self.array_now)):
                rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(self.screen, self.rect_col, rect, 1)
                if self.array_now[row][col] == 1:
                    pygame.draw.rect(self.screen, self.fill_col, rect)

    def Game_of_Life_Logic(self):
        if self.active:
            temp_array = np.zeros_like(self.array_now)
            for y in range(1, len(self.array_now) - 1):
                for x in range(1, len(self.array_now) - 1):
                    alive = np.sum(self.array_now[y - 1:y + 2, x - 1:x + 2]) - self.array_now[y, x]
                    if alive in [2, 3] and self.array_now[y][x] == 1:
                        temp_array[y][x] = 1
                    elif alive < 2 and self.array_now[y][x] == 1:
                        temp_array[y][x] = 0
                    elif alive > 3 and self.array_now[y][x] == 1:
                        temp_array[y][x] = 0
                    elif alive == 3 and self.array_now[y][x] == 0:
                        temp_array[y][x] = 1
            self.array_now = temp_array

    def on_pause_click(self):
        if self.active:
            self.active = False
            self.pause_button.setText('▶️')
        elif not self.active:
            self.active = True
            self.pause_button.setText('⏸️')

    def on_slider_change(self, value):
        self.speed = value

    def on_left_click(self):
        if self.slider.value() == 1:
            print('Verlangsamung nicht möglich!')
        else:
            value = self.slider.value() - 1
            self.slider.setValue(value)

    def on_right_click(self):
        if self.slider.value() == 20:
            print('Beschleunigung nicht möglich!')
        else:
            value = self.slider.value() + 1
            self.slider.setValue(value)

    def closeEvent(self, event):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = Main()
    Main.run()
    sys.exit(app.exec())
