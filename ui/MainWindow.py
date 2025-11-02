import providers.factory
from ui.forms_uic.MainWindow import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow
from core.zapret_handler import ZapretHandler
import providers

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.switchControl.setFixedHeight(50)
        self.switchControl.setText(None)
        self.switchControl.stateChanged.connect(self.on_switch_changed)

        self.zapret = ZapretHandler(
            providers.factory.GetBinsProvider(providers.factory.AvailableBinsProviders()[0]),
            providers.factory.GetStrategyProvider(providers.factory.AvailableStrategyProviders()[0])
        )

        # TODO: threaded
        if not self.zapret.strategy.available:
            self.zapret.strategy.update()
        self.zapret.strategy.load()

        if not self.zapret.bin.available:
            self.zapret.bin.update()

        for name in self.zapret.strategy.names:
            self.strategyCombo.addItem(name,name)

        self.display_text("DISCONNECTED")

    def display_text(self,txt:str):
        self.infoLabel.setText(txt)

    def on_switch_changed(self,state):
        if state:
            self.zapret.start(self.choosen_strategy)
        else:
            self.zapret.stop()

    @property
    def choosen_strategy(self):
        return self.strategyCombo.currentData()