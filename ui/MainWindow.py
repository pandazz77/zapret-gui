from ui.forms_uic.MainWindow import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.switchControl.setFixedHeight(50)
        self.switchControl.setText(None)