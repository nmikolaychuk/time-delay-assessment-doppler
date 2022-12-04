import sys
from PyQt5 import QtWidgets

from main_logic import MainApp


def main():
    app = QtWidgets.QApplication(sys.argv)
    screen_geometry = app.desktop().screenGeometry()
    window = MainApp(screen_geometry)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
