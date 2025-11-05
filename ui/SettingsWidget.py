
import providers.factory
from ui.forms_uic.SettingsWidget import Ui_SettingsWidget
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal
import providers
from core.globals import settings
from core.zapret_handler import ZapretHandler
from core.utils import TaskQueue

class SettingsWidget(QWidget, Ui_SettingsWidget):
    strategyChanged = pyqtSignal(str)
    binsChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tasks = TaskQueue()

        self.strategiesCombo.addItems(providers.factory.AvailableStrategyProviders())
        self.binsCombo.addItems(providers.factory.AvailableBinsProviders())
        self.strategiesCombo.setCurrentText(settings.preffered_strategy_provider)
        self.binsCombo.setCurrentText(settings.preffered_bins_provider)
        
        self.strategiesCombo.currentTextChanged.connect(self.on_strategy_changed)
        self.binsCombo.currentTextChanged.connect(self.on_bin_changed)
        self.blockcheckBtn.clicked.connect(self.on_blockcheck)
        self.blockcheckStatus.setText("undefined")
        self.autostartCheck.checkStateChanged.connect(self.on_autostart_changed)

    def on_strategy_changed(self,name:str):
        settings.preffered_strategy_provider = name
        self.strategyChanged.emit(settings.preffered_strategy_provider)
        print(name)

    def on_bin_changed(self,name:str):
        settings.preffered_bins_provider = name
        self.binsChanged.emit(settings.preffered_bins_provider)
        print(name)

    def on_blockcheck(self):
        self.tasks.add(self._blockcheck)

    def _blockcheck(self):
        self.blockcheckBtn.setDisabled(True)
        self.blockcheckStatus.setText("Processing...")
        result = ZapretHandler.get_instance().blockcheck(1)
        self.blockcheckStatus.setText(str(result))
        self.blockcheckBtn.setDisabled(False)


    def on_autostart_changed(self,val:Qt.CheckState):
        print(val)