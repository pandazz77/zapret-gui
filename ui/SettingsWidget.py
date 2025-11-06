
import providers.factory
from ui.forms_uic.SettingsWidget import Ui_SettingsWidget
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QSettings
import providers
from core.globals import settings
from core.zapret_handler import ZapretHandler
from core.utils import threaded
import platform
import sys
import os
import logging

WIN_RUN_PATH = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
AUTOSTART_CLI_ARGS = "--tray --start"

class SettingsWidget(QWidget, Ui_SettingsWidget):
    strategyChanged = pyqtSignal(str)
    binsChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.strategiesCombo.addItems(providers.factory.AvailableStrategyProviders())
        self.binsCombo.addItems(providers.factory.AvailableBinsProviders())
        self.strategiesCombo.setCurrentText(settings.preffered_strategy_provider)
        self.binsCombo.setCurrentText(settings.preffered_bins_provider)

        if platform.system() == "Windows":
            self.qset = QSettings(WIN_RUN_PATH,QSettings.Format.NativeFormat)
            self.autostartCheck.setChecked(self.qset.contains("zapret_gui"))
        elif platform.system() == "Linux":
            self.autostartCheck.setDisabled(True)

        
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
        self._blockcheck()

    @threaded
    def _blockcheck(self):
        self.blockcheckBtn.setDisabled(True)
        self.blockcheckStatus.setText("Processing...")
        result = ZapretHandler.get_instance().blockcheck(1)
        self.blockcheckStatus.setText(str(result))
        self.blockcheckBtn.setDisabled(False)


    def on_autostart_changed(self,val:Qt.CheckState):
        if val == Qt.CheckState.Checked:
            if platform.system() == "Windows":
                if sys.executable.endswith("python.exe"):
                    executable = f"{sys.executable} {os.path.abspath(sys.argv[0])} {AUTOSTART_CLI_ARGS}"
                else:
                    executable = f"{sys.executable} {AUTOSTART_CLI_ARGS}"
                logging.info(f"AUTOSTART ON: {executable}")
                self.qset.setValue("zapret_gui",executable)

        else:
            if platform.system() == "Windows":
                self.qset.remove("zapret_gui")