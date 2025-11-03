import providers.factory
from ui.forms_uic.MainWindow import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QPixmap
from core.zapret_handler import ZapretHandler, ZapretStatus, _default_status_hook
import providers
from core.globals import settings
from ui.resources import resources
import atexit

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.label.setPixmap(QPixmap(":/images/zapret.png"))
        self.switchControl.setFixedHeight(50)
        self.switchControl.setText(None)
        self.switchControl.stateChanged.connect(self.on_switch_changed)

        self._tray_deactivated_icon = QIcon(':/images/tray_deactivated.png')
        self._tray_activated_icon = QIcon(':/images/tray_activated.png')

        self.zapret = ZapretHandler(
            providers.factory.GetBinsProvider(providers.factory.AvailableBinsProviders()[0]),
            providers.factory.GetStrategyProvider(providers.factory.AvailableStrategyProviders()[0])
        )
        self.zapret.status_hook = self.on_new_zapret_status
        atexit.register(self._atexit)

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

        self.tray = QSystemTrayIcon(self._tray_deactivated_icon)
        self.tray.show()
        self.tray.activated.connect(self.on_tray_activated)
        tray_menu = QMenu()
        show_action = QAction("Show",self)
        show_action.triggered.connect(self.show)
        exit_action = QAction("Exit",self)
        exit_action.triggered.connect(QApplication.quit)
        tray_menu.addActions([
            show_action,
            exit_action
        ])
        self.tray.setContextMenu(tray_menu)

        self.setFixedSize(310, 360)
        

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def _atexit(self):
        self.zapret.status_hook = _default_status_hook
    
    def display_text(self,txt:str):
        self.infoLabel.setText(txt)

    def on_tray_activated(self,reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isHidden():
                self.show()
            else:
                self.raise_()
                self.activateWindow()

    def on_switch_changed(self,state):
        if state:
            self.zapret.start(self.choosen_strategy)
        else:
            self.zapret.stop()

    def on_strategy_changed(self,text:str):
        settings.preffered_strategy = self.choosen_strategy
    
    def on_new_zapret_status(self,status:ZapretStatus):
        if status == ZapretStatus.STOPPED:
            self.tray.setIcon(self._tray_deactivated_icon)
            self.display_text("Stopped")
            self.strategyCombo.setDisabled(False)
        elif status == ZapretStatus.STARTING:
            self.strategyCombo.setDisabled(True)
            self.display_text(f"Starting \"{self.choosen_strategy}\" strategy..")
        elif status == ZapretStatus.STARTED:
            self.tray.setIcon(self._tray_activated_icon)
            self.display_text(f"""Connected via "{self.choosen_strategy}" strategy
Blockcheck status: {self.zapret.blockcheck()}
""")

    @property
    def choosen_strategy(self):
        return self.strategyCombo.currentData()