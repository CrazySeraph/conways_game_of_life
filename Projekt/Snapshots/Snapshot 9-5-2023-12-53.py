import sys

import numpy as np
import pygame
from PyQt6.QtWidgets import QApplication, QWidget, QFrame


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('My Application')
        self.frame = QFrame(self)
        self.frame.setGeometry(10, 10, 380, 380)
        self.array_now, self.array_next = np.zeros((100, 100), dtype=int), np.zeros((100, 100), dtype=int)
        self.active = 1
        self.square_size = 8
        self.rect_col, self.fill_col = pygame.Color('grey'), pygame.Color('white')
        self.screen_width, self.screen_height = 800, 800
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Conways game of Life - Kiste Edition")
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
                        print('+')
                    if event.key == pygame.K_KP_MINUS:
                        print('-')
                    if event.key == pygame.K_SPACE:
                        print('SPACE')
            self.screen.fill(pygame.Color('black'))
            self.draw_grid()
            self.Game_of_Life_Logic()
            pygame.display.flip()
            self.clock.tick(10)

    def draw_grid(self):
        for row in range(len(self.array_now)):
            for col in range(len(self.array_now)):
                rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(self.screen, self.rect_col, rect, 1)
                if self.array_now[row][col] == 1:
                    pygame.draw.rect(self.screen, self.fill_col, rect)

    def Game_of_Life_Logic(self):
        if self.active == 1:
            temp_array = np.zeros_like(self.array_now)
            for y in range(1, len(self.array_now) - 1):
                for x in range(1, len(self.array_now) - 1):
                    alive = np.sum(self.array_now[y-1:y+2, x-1:x+2]) - self.array_now[y, x]
                    if alive in [2, 3] and self.array_now[y][x] == 1:
                        temp_array[y][x] = 1
                    elif alive < 2 and self.array_now[y][x] == 1:
                        temp_array[y][x] = 0
                    elif alive > 3 and self.array_now[y][x] == 1:
                        temp_array[y][x] = 0
                    elif alive == 0 and self.array_now[y][x] == 0:
                        temp_array[y][x] = 1
            self.array_now = temp_array

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = Main()
    Main.setWindowTitle("Steurung für Game of Life")
    Main.run()
    sys.exit(app.exec())
