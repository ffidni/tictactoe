from PyQt5.QtGui import QFont, QCursor, QIcon
from PyQt5.QtCore import QEvent, Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QApplication, QPushButton, QHBoxLayout
from sys import argv, exit



class Tutorial(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.setStyleSheet("background-color: red;")
		

if __name__ == '__main__':
	app = QApplication(argv)
	win = Tutorial()
	win.show()
	exit(app.exec_())