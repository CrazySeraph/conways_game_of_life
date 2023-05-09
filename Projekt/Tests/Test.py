import pygame
import numpy
import PyQt5

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Conways game of Life - Kiste Edition")

grid = [[0 for x in range(10)] for y in range(10)]

cell_size = 10
grid_width = 100
grid_height = 100
zoom_level = 1.0
zoom_speed = 0.1

def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (199,197,197), rect, 1)

def draw_zoom_in_button():
    rect = pygame.Rect(600, 10, 30, 30)
    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
    pygame.draw.polygon(screen, (255, 255, 255), ((615, 20), (615, 25), (610, 25), (610, 30), (605, 30), (605, 25), (600, 25), (600, 20)))

def draw_zoom_out_button():
    rect = pygame.Rect(600, 50, 30, 30)
    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
    pygame.draw.polygon(screen, (255, 255, 255), ((605, 60), (605, 65), (610, 65), (610, 70), (615, 70), (615, 65), (620, 65), (620, 60)))

def zoom_in():
    global zoom_level, cell_size, grid_width, grid_height
    zoom_level += zoom_speed
    cell_size = int(cell_size / zoom_level)
    grid_width = int(grid_width / zoom_level)
    grid_height = int(grid_height / zoom_level)

def zoom_out():
    global zoom_level, cell_size, grid_width, grid_height
    zoom_level -= zoom_speed
    cell_size = int(cell_size / zoom_level)
    grid_width = int(grid_width / zoom_level)
    grid_height = int(grid_height / zoom_level)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.Rect(600, 10, 30, 30).collidepoint(event.pos):
                    zoom_in()
                elif pygame.Rect(600, 50, 30, 30).collidepoint(event.pos):
                    zoom_out()
    
    screen.fill((0, 0, 0))
    draw_zoom_in_button()
    draw_zoom_out_button()    
    draw_grid()
    pygame.display.flip()
    pygame.display.update()
pygame.quit()