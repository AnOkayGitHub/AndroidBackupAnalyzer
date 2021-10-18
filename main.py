import sys
import Application
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5 import QtGui


def main():
    # Program entry point
    print("App launching...")

    # Configure application widget
    app = QApplication(sys.argv)
    main_window = Application.Application()
    widget = QStackedWidget()
    widget.addWidget(main_window)
    widget.setFixedWidth(500)
    widget.setFixedHeight(400)
    widget.setWindowTitle("Android Backup Analyzer")
    widget.setWindowIcon(QtGui.QIcon("logo.png"))

    # Display application
    widget.show()

    # Exiting application
    try:
        sys.exit(app.exec())
    except:
        print("Closing application.")


if __name__ == "__main__":
    main()
