from PyQt5.QtGui import QFont, QCursor, QIcon, QFontDatabase
from PyQt5.QtCore import QEvent, Qt, pyqtSignal, pyqtSlot, QSize, QTimer, QThread
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QStyledItemDelegate, QMainWindow, QComboBox, QSpinBox, QFormLayout, QDialog, QDesktopWidget, QAction, QStackedWidget, QSizePolicy, QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QApplication, QPushButton, QHBoxLayout, QFrame, QSpacerItem
from random import randint, choice
from sys import argv, exit
from time import sleep


#app = QApplication([])
#msg = QMessageBox()
#msg.setIcon(QMessageBox.Critical)
#msg.setText("Error")
#msg.setInformativeText('More information')
#msg.setWindowTitle("Error")
#msg.exec_()