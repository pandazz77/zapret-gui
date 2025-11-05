from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream
from ui.MainWindow import MainWindow
from ui.resources import resources
import sys
import argparse
from core.globals import setup_logging

def main() -> int:
    app = QApplication(sys.argv) 

    parser = argparse.ArgumentParser(description='Zapret GUI')
    parser.add_argument(
        '--loglevel',
        default='INFO', # Уровень по умолчанию
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Уровень логирования (по умолчанию: INFO)'
    )
    parser.add_argument(
        "--tray",
        action="store_true",
        help='start application in tray mode'
    )
    parser.add_argument(
        "--start",
        action="store_true",
        help='start zapret'
    )
    args = parser.parse_args()
    log_level = args.loglevel.upper()
    setup_logging(log_level)

    qss_file = QFile(":/styles/dark_theme.qss") # Путь к ресурсу
    if qss_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(qss_file)
        style = stream.readAll()
        app.setStyleSheet(style)
        qss_file.close()
    else:
        print("Cannot find application style")

    mw = MainWindow(args.start)
    if not args.tray:
        mw.show()
    else:
        mw.hide() 

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())