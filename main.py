from PyQt6.QtWidgets import QApplication
from ui.MainWindow import MainWindow
import sys

def main(argv) -> int:
    app = QApplication(argv) 

    mw = MainWindow()
    mw.show() 

    return app.exec()

if __name__ == "__main__":
    sys.exit(main(sys.argv))