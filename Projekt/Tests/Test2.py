import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1280, 720))

cell_size = 50
zoom_level = 1

def draw_grid():
    for x in range(0, screen.get_width(), cell_size):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, screen.get_height()))
    for y in range(0, screen.get_height(), cell_size):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (screen.get_width(), y))

def zoom_in():
    global cell_size, zoom_level
    if zoom_level < 3:
        cell_size *= 2
        zoom_level += 1

def zoom_out():
    global cell_size, zoom_level
    if zoom_level > 1:
        cell_size //= 2
        zoom_level -= 1

def draw_zoom_in_button():
    rect = pygame.Rect(1200, 10, 60, 60)
    pygame.draw.rect(screen, (0, 255, 0), rect)
    font = pygame.font.Font(None, 40)
    text = font.render("+", True, (255, 255, 255))
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)
    return rect

def draw_zoom_out_button():
    rect = pygame.Rect(1200, 80, 60, 60)
    pygame.draw.rect(screen, (255, 0, 0), rect)
    font = pygame.font.Font(None, 40)
    text = font.render("-", True, (255, 255, 255))
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)
    return rect

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                zoom_in()
            elif event.button == 5:
                zoom_out()
            elif event.button == 1:
                zoom_in_button_rect = draw_zoom_in_button()
                zoom_out_button_rect = draw_zoom_out_button()
                if zoom_in_button_rect.collidepoint(event.pos):
                    zoom_in()
                elif zoom_out_button_rect.collidepoint(event.pos):
                    zoom_out()

    screen.fill((0, 0, 0))
    draw_zoom_in_button()
    draw_zoom_out_button()
    draw_grid()
    pygame.display.flip()
