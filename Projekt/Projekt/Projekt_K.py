import sys
import pygame
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from PyQt5.QtCore import Qt

FPS = 10
screen_width, screen_height = 800, 800
array = np.zeros((100, 100), dtype=int)
square_size = 8
rect_col = pygame.Color('grey')
fill_col = pygame.Color('white')
activity = 0

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Conways game of Life - Kiste Edition")
clock = pygame.time.Clock()

def draw_grid():
    for row in range(len(array)):
        for col in range(len(array)):
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            pygame.draw.rect(screen, rect_col, rect, 1)
            if array[row][col] == 1:
                pygame.draw.rect(screen, fill_col, rect)

while True:
    screen.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row = mouse_pos[1] // square_size
            col = mouse_pos[0] // square_size
            if array[row][col] == 1:
                array[row][col] = 0
            else:
                array[row][col] = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_PLUS:
                print('+')
            if event.key == pygame.K_KP_MINUS:
                print('-')

    draw_grid()
    pygame.display.flip()
    clock.tick(FPS)