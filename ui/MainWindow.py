from ui.forms_uic.MainWindow import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow
from core.globals import VERSION

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.footerLabel.setText(f"ZapretGUI v{VERSION}")

        self.setFixedSize(310, 360)
        self.switchPageBtn.clicked.connect(self.on_switch_page)

    def on_switch_page(self):
        if self.stackedWidget.currentWidget() == self.main:
            # open settings widget
            self.stackedWidget.setCurrentWidget(self.settings)
            self.switchPageBtn.setText("GO BACK")
        else:
            # open main widget
            self.stackedWidget.setCurrentWidget(self.main)
            self.switchPageBtn.setText("SETTINGS")

