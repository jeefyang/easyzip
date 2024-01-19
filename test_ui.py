from PyQt6.QtCore import Qt
from Ui_main import Ui_MainWindow
import sys
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QListView, QAbstractItemView, QTreeView, QApplication, QDialog, QPushButton, QMessageBox, QWidget
from Ui_update import Ui_Update

class MyMainWin(Ui_Update):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mywin = MyMainWin()
    mywin.show()
    sys.exit(app.exec())
    pass
