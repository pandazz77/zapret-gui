from ui.forms_uic.MainWindow import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from core.globals import VERSION
from core.zapret_handler import ZapretStatus
from ui.resources import resources

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.footerLabel.setText(f"ZapretGUI v{VERSION}")

        self.setFixedSize(310, 360)
        self.switchPageBtn.clicked.connect(self.on_switch_page)

        self._tray_deactivated_icon = QIcon(':/images/tray_deactivated.png')
        self._tray_activated_icon = QIcon(':/images/tray_activated.png')
        self.tray: QSystemTrayIcon = None
        self.tray_actions: dict[str,QAction] = {}
        self._initTray()

        self.main.zapret.new_status.connect(self.on_new_zapret_status)
        self.settings.strategyChanged.connect(self.main.on_new_strategy_provider)
        self.settings.binsChanged.connect(self.main.on_new_bins_provider)


    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def on_new_zapret_status(self,status:ZapretStatus):
        if status == ZapretStatus.STOPPED:
            self.tray.setIcon(self._tray_deactivated_icon)
            self.tray_actions["start_stop"].setText("Start")
        elif status == ZapretStatus.STARTING:
            ...
        elif status == ZapretStatus.STARTED:
            self.tray.setIcon(self._tray_activated_icon)
            self.tray_actions["start_stop"].setText("Stop")

    def _initTray(self):
        if self.tray is not None:
            return

        self.tray = QSystemTrayIcon(self._tray_deactivated_icon)
        self.tray.show()
        self.tray.activated.connect(self.on_tray_activated)
        tray_menu = QMenu()
        self.tray_actions = {
            "show": QAction("Show",self),
            "start_stop": QAction("Start",self),
            "exit": QAction("Exit",self)
        }
        self.tray_actions["show"].triggered.connect(self.show)
        self.tray_actions["exit"].triggered.connect(QApplication.quit)
        self.tray_actions["start_stop"].triggered.connect(self.main.switchControl.click)
        tray_menu.addActions(self.tray_actions.values())
        self.tray.setContextMenu(tray_menu)

    def on_tray_activated(self,reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isHidden():
                self.show()
            else:
                self.raise_()
                self.activateWindow()

    def on_switch_page(self):
        if self.stackedWidget.currentWidget() == self.main:
            # open settings widget
            self.stackedWidget.setCurrentWidget(self.settings)
            self.switchPageBtn.setText("GO BACK")
        else:
            # open main widget
            self.stackedWidget.setCurrentWidget(self.main)
            self.switchPageBtn.setText("SETTINGS")

