
from ui.forms_uic.SettingsWidget import Ui_SettingsWidget
from PyQt6.QtWidgets import QWidget

class SettingsWidget(QWidget, Ui_SettingsWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)