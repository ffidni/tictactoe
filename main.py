from packages import *
from board import *
from settings import *
from game import *

class Main(QStackedWidget):

	def __init__(self):
		super().__init__()
		self.w, self.h = 678, 587
		self.w_factor, self.h_factor = 1, 1

		self.setWindowTitle("Tic Tac Toe")
		self.setWindowIcon(QIcon("Assets/Icons/icon.png"))
		self.setObjectName("Main")
		self.setStyleSheet("""#Main{background: #2E2E2F;}""")
		self.setFixedSize(self.w, self.h)
		self.resize(self.w, self.h)
		self.installEventFilter(self)

		self.m_pages = {}
		self.fullscreen = QAction("FullScreen", self)

		self.fullscreen.setShortcut("F11")
		self.fullscreen.triggered.connect(self.toggle_fullscreen)
		self.addAction(self.fullscreen)
		self.register(Settings(self), "Settings")
		self.goto("Settings")

	def toggle_fullscreen(self):
		if self.isFullScreen():
			self.showNormal()
		else:
			self.max_screen()
			self.showFullScreen()

	def register(self, widget, name):
		self.m_pages[name] = widget
		self.addWidget(widget)
		widget.goto_signal.connect(self.goto)

	@pyqtSlot(str)
	def goto(self, name):
		if name in self.m_pages:
			widget = self.m_pages[name]
			self.setCurrentWidget(widget)

if __name__ == '__main__':
	app = QApplication(argv)
	app.setStyleSheet("""QComboBox{
								background-color: #D1D1D1;
								border: 1px solid black;
							}
							QComboBox:drop-down{
								border-image: url('Assets/Icons/down_arrow.png');
								width: 22px;
								height: 22px;
							}
						    QComboBox QAbstractItemView {
						         border: none;
						    }
							QComboBox QAbstractItemView::item:selected{ 
								selection-border-color: red;
							}
							QSpinBox{
								background-color: #D1D1D1;
								border: 1px solid black;
							}
							QSpinBox:down-button{
								border: none;
							}
							QSpinBox:up-button{
								border: none;
							}
							QLineEdit{
								background: #D1D1D1;
							}

						""")
	QFontDatabase.addApplicationFont("Assets/Fonts/OpenSans-Regular.ttf")
	QFontDatabase.addApplicationFont("Assets/Fonts/SourceSansPro-Regular.ttf")
	QFontDatabase.addApplicationFont("Assets/Font/SourceSansPro-Black.tff")
	QFontDatabase.addApplicationFont("Assets/Font/SourceSansPro-SemiBold.tff")
	win = Main()
	win.show()
	exit(app.exec_())