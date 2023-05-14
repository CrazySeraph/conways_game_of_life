from PyQt6.QtWidgets import QMainWindow, QApplication, QMenuBar
from PyQt6.QtGui import QAction

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)

        # add a button to the menu bar
        button_action = QAction('Button', self)
        button_action.setStatusTip('Button')
        button_action.triggered.connect(self.button_clicked)

        menubar.addAction(button_action)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menu Bar')
        self.show()

    def button_clicked(self):
        print('Button clicked')

if __name__ == '__main__':
    app = QApplication([])
    window = Main()
    app.exec()