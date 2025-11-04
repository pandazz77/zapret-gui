from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream
from ui.MainWindow import MainWindow
from ui.resources import resources
import sys

def main() -> int:
    app = QApplication(sys.argv) 

    qss_file = QFile(":/styles/dark_theme.qss") # Путь к ресурсу
    if qss_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(qss_file)
        style = stream.readAll()
        app.setStyleSheet(style)
        qss_file.close()
    else:
        print("Cannot find application style")

    mw = MainWindow()
    mw.show() 

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())