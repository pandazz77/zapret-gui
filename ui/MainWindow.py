import providers.factory
from ui.forms_uic.MainWindow import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow
from core.zapret_handler import ZapretHandler, ZapretStatus, _default_status_hook
import providers
from core.globals import settings

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
        self.zapret.status_hook = self.on_new_zapret_status

        # TODO: threaded
        if not self.zapret.strategy.available:
            self.zapret.strategy.update()
        self.zapret.strategy.load()

        if not self.zapret.bin.available:
            self.zapret.bin.update()

        for name in self.zapret.strategy.names:
            self.strategyCombo.addItem(name,name)
        self.strategyCombo.currentTextChanged.connect(self.on_strategy_changed)
        self.strategyCombo.setCurrentText(settings.preffered_strategy)

        self.display_text("Disconnected")

    def closeEvent(self, event):
        self.zapret.status_hook = _default_status_hook
        event.accept()
        self.deleteLater()
    
    def display_text(self,txt:str):
        self.infoLabel.setText(txt)

    def on_switch_changed(self,state):
        if state:
            self.zapret.start(self.choosen_strategy)
        else:
            self.zapret.stop()

    def on_strategy_changed(self,text:str):
        settings.preffered_strategy = self.choosen_strategy
    
    def on_new_zapret_status(self,status:ZapretStatus):
        if status == ZapretStatus.STOPPED:
            self.display_text("Stopped")
            self.strategyCombo.setDisabled(False)
        elif status == ZapretStatus.STARTING:
            self.strategyCombo.setDisabled(True)
            self.display_text(f"Starting \"{self.choosen_strategy}\" strategy..")
        elif status == ZapretStatus.STARTED:
            self.display_text(f"""Connected via "{self.choosen_strategy}" strategy
Blockcheck status: {self.zapret.blockcheck()}
""")

    @property
    def choosen_strategy(self):
        return self.strategyCombo.currentData()