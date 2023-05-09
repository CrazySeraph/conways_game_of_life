import sys
import pygame
from PyQt6.QtWidgets import QApplication, QWidget, QFrame
from PyQt6.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set the size and title of the window
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('My Application')

        # Create a QFrame to hold the Pygame window
        self.frame = QFrame(self)
        self.frame.setGeometry(10, 10, 380, 380)

        # Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()

        # Create the Pygame window
        self.screen = pygame.display.set_mode((380, 380))

        # Show the window
        self.show()

    def run(self):
        while True:
            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw on the Pygame window
            self.screen.fill(pygame.Color('black'))
            pygame.draw.rect(self.screen, pygame.Color('white'), pygame.Rect(50, 50, 100, 100))

            # Update the Pygame window
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.run()
    sys.exit(app.exec())
