import sys
import pygame
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtWinExtras import QtWin


# Variablen Definition
FPS = 10
screen_width, screen_height = 800, 800
array = np.zeros((100, 100), dtype=int)
square_size = 8
rect_col = pygame.Color('grey')
fill_col = pygame.Color('white')
activity = 0

# Pygame initialisierung
pygame.init()
clock = pygame.time.Clock()


class PygameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.surface = None
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(screen_width, screen_height)
        self.surface = pygame.display.set_mode((screen_width, screen_height))

    def update(self, arr):
        self.surface.fill(pygame.Color('black'))
        for row in range(len(arr)):
            for col in range(len(arr)):
                rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
                pygame.draw.rect(self.surface, rect_col, rect, 1)
                if arr[row][col] == 1:
                    pygame.draw.rect(self.surface, fill_col, rect)

        pygame.display.flip()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conways game of Life - Kiste Edition")
        self.setGeometry(200, 200, screen_width + 20, screen_height + 40)

        self.pygame_widget = PygameWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.pygame_widget)
        self.setLayout(layout)

        self.timer = self.startTimer(1000 // FPS)

    def timerEvent(self, event):
        self.pygame_widget.update(array)

    def closeEvent(self, event):
        pygame.quit()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
