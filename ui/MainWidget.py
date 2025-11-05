import providers.factory
from ui.forms_uic.MainWidget import Ui_MainWidget
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from core.zapret_handler import ZapretHandler, ZapretStatus
from core.utils import TaskQueue
import providers
from core.globals import settings

class MainWidget(QWidget, Ui_MainWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.display_text("IDLE")
        self.infoLabel.setWordWrap(True)

        self.label.setPixmap(QPixmap(":/images/zapret.png"))
        self.switchControl.setFixedHeight(50)
        self.switchControl.setText(None)
        self.switchControl.stateChanged.connect(self.on_switch_changed)

        self.zapret = ZapretHandler(
            providers.factory.GetBinsProvider(providers.factory.AvailableBinsProviders()[0]),
            providers.factory.GetStrategyProvider(providers.factory.AvailableStrategyProviders()[0])
        )
        self.zapret.new_status.connect(self.on_new_zapret_status,Qt.ConnectionType.DirectConnection)

        self.tasks = TaskQueue()

        self.checkAvailable()

        self.fillStrategies()
        self.strategyCombo.currentTextChanged.connect(self.on_strategy_changed)

    def fillStrategies(self):
        if not self.zapret.strategy.names:
            return
        for name in self.zapret.strategy.names:
            self.strategyCombo.addItem(name,name)
        if not settings.preffered_strategy:
            settings.preffered_strategy = self.zapret.strategy.names[0]
        self.strategyCombo.setCurrentText(settings.preffered_strategy)

    def checkAvailable(self):
        if not self.zapret.strategy.available:
            self.tasks.add(self._updateStrats)
        else:
            self.zapret.strategy.load()
        
        if not self.zapret.bin.available:
            self.tasks.add(self._updateBins)
        
    def _updateBins(self):
        self.switchControl.setDisabled(True)
        self.display_text("Updating bins...")
        self.zapret.bin.update()
        self.switchControl.setDisabled(False)
        self.display_text("IDLE")


    def _updateStrats(self):
        self.switchControl.setDisabled(True)
        self.display_text("Updating strategies...")
        self.zapret.strategy.update()
        self.switchControl.setDisabled(False)
        self.fillStrategies()
        self.display_text("IDLE")
    
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