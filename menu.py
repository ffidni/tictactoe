from PyQt5.QtGui import QFont, QCursor, QIcon, QFontDatabase
from PyQt5.QtCore import QEvent, Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QAction, QStackedWidget, QSizePolicy, QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QApplication, QPushButton, QHBoxLayout, QFrame, QSpacerItem
from sys import argv, exit

class Main(QStackedWidget):

	def __init__(self):
		super().__init__()
		self.setWindowTitle("Tic Tac Toe")
		self.resize(866, 607)

		self.m_pages = {}
		self.fullscreen = QAction("FullScreen", self)

		self.fullscreen.setShortcut("F11")
		self.fullscreen.triggered.connect(self.toggle_fullscreen)
		self.addAction(self.fullscreen)
		self.register(Menu(self), "Menu")
		self.goto("Menu")

	def toggle_fullscreen(self):
		if self.isFullScreen():
			self.showNormal()
		else:
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

	def changeEvent(self, event):
	    if event.type() == QEvent.WindowStateChange:
	        if event.oldState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
	        	self.m_pages["Menu"].info.resizeEvent(w_factor=1.3236363636363637, h_factor=1.2537067545304779)

class Menu(QWidget):
	goto_signal = pyqtSignal(str)

	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		self.w,self.h = self.parent.width(), self.parent.height()
		self.w_factor, self.h_factor = 1, 1
		self.installEventFilter(self)
		self.setStyleSheet("""background-color: #f0f0f0;""")
		self.init_ui()

	def init_ui(self):
		self.mlayout = QVBoxLayout()

		self.title = QLabel("Tic-Tac-Toe", self)
		self.info = Tutorial(self.parent)
		self.menu_selector = Board(background="transparent", border=False, is_menu=True, size=[125, 125], parent=self)
		self.top_spacer = QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.bottom_spacer = QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)

		self.title.setFont(QFont("Source Sans Pro", 55))
		self.menu_selector.box_0x0.clicked.connect(lambda: self.box_clicked("Start"))
		self.menu_selector.box_1x1.clicked.connect(lambda: self.box_clicked("How"))
		self.menu_selector.box_2x2.clicked.connect(lambda: self.box_clicked("Exit"))
		self.mlayout.addWidget(self.title, alignment=Qt.AlignHCenter)
		self.mlayout.addItem(self.top_spacer)
		self.mlayout.addWidget(self.menu_selector, alignment=Qt.AlignHCenter)
		self.mlayout.addItem(self.bottom_spacer)
		self.info.hide()
		self.setLayout(self.mlayout)

	def goto(self, name):
		self.goto_signal.emit(name)

	def box_clicked(self, name):
		if name == 'Start':
			pass
		elif name == 'How':
			self.mlayout.removeWidget(self.menu_selector)
			self.mlayout.removeItem(self.bottom_spacer)
			self.menu_selector.hide()

			self.mlayout.addWidget(self.info, alignment=Qt.AlignCenter)
			self.top_spacer.changeSize(0, 35)
			self.bottom_spacer.changeSize(0, 65)
			self.mlayout.addItem(self.bottom_spacer)
			self.info.show()
		else:
			self.parent.close()

	def resizeEvent(self, event):
		self.w_factor = self.width() / self.w 
		self.h_factor = self.height() / self.h
		self.info.resizeEvent(w_factor=self.w_factor, h_factor=self.h_factor)

		self.title.setFont(QFont("Source Sans Pro", 55*self.h_factor))
		self.top_spacer.changeSize(0, 10*self.h_factor if self.info.isHidden() else 35*self.h_factor)
		self.bottom_spacer.changeSize(0, 40*self.h_factor if self.info.isHidden() else 65*self.h_factor)
		self.menu_selector.resizeEvent(w_factor=self.w_factor, h_factor=self.h_factor)

class Tutorial(QDialog):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.w, self.h = 401, 343
		self.w_factor, self.h_factor = 1, 1
		self.init_ui()

	def init_ui(self):
		mlayout = QVBoxLayout()
		hlayout = QHBoxLayout()
		title_layout = QHBoxLayout()
		vlayout = QVBoxLayout()
		vlayout_2 = QVBoxLayout()

		self.back_button = QPushButton(self)
		self.info_title = QLabel("How to Play", self)
		self.info_text = QLabel("Every round, you have to place your mark to one of the box in a grid before the timer runs out. If a player manages to put 3 marks in a horizontally, vertically, or diagonally row, then the player will win the game, otherwise it's a tie.")
		self.practice_title = QLabel("Practice with an easy bot", self)
		self.practice_board = Board(border=True, size=[36, 36], parent=self)
		self.reset_button = QPushButton("Reset", self)
		self.top_spacer_2 = QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Minimum)
		self.bottom_spacer_2 = QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Minimum)
		self.board_spacer = QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
		#self.item_spacer = QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Fixed)

		self.setObjectName("InfoWidget")
		self.setStyleSheet("""QWidget{background-color: #eaeaea;}
							  #InfoWidget{
							  border: 1px solid black;
							  }""")

		self.setFixedSize(self.w, self.h)
		self.info_title.setFont(QFont("Arial", 10, weight=QFont.Bold))
		self.info_text.setWordWrap(True)
		self.info_text.setFixedSize(150, 200)
		self.info_text.setFont(QFont("Source Sans Pro", 10))
		self.info_text.setStyleSheet("""color: #333333;""")
		self.practice_title.setFont(QFont("Arial", 10, weight=QFont.Bold))
		self.practice_title.setStyleSheet("""color: #333333;""")
		self.back_button.setIcon(QIcon("Assets/Icons/back_icon.png"))
		self.back_button.setFixedSize(18, 23)
		self.back_button.setIconSize(QSize(18, 23))
		self.back_button.setStyleSheet("""background-color: transparent;""")
		self.back_button.clicked.connect(lambda: self.btn_clicked("Back"))
		self.reset_button.setStyleSheet("""border: 1px solid #757575;
									  background-color: white;
									  """)
		self.reset_button.setFixedSize(54, 25)

		mlayout.addWidget(self.back_button, alignment=Qt.AlignLeft)
		mlayout.addItem(self.top_spacer_2)


		title_layout.addWidget(self.info_title, alignment=Qt.AlignHCenter)
		vlayout.addWidget(self.info_text, alignment=Qt.AlignBottom | Qt.AlignHCenter)
		

		title_layout.addWidget(self.practice_title, alignment=Qt.AlignHCenter)
		vlayout_2.addWidget(self.practice_board, alignment=Qt.AlignHCenter)
		self.practice_board.layout.addWidget(self.reset_button, alignment=Qt.AlignHCenter)

		mlayout.setSpacing(0)
		hlayout.addLayout(vlayout)
		hlayout.addLayout(vlayout_2)
		mlayout.addLayout(title_layout)
		mlayout.addLayout(hlayout)
		mlayout.addItem(self.bottom_spacer_2)
		self.setLayout(mlayout)
		self.hide()

	def hide_widget(widget):
		self.mlayout.removeWidget(widget)
		self.mlayout.removeItem(self.bottom_spacer)
		widget.hide()

	def btn_clicked(self, command):
		if command == 'Back':
			#print(self.parent.m_pages["Menu"].menu_selector)
			main = self.parent.m_pages["Menu"]
			main.mlayout.removeWidget(self)
			main.mlayout.removeItem(main.bottom_spacer)
			self.hide()
			main.mlayout.addWidget(main.menu_selector, alignment=Qt.AlignCenter)
			main.top_spacer.changeSize(0, 10)
			main.bottom_spacer.changeSize(0, 40)
			main.mlayout.addItem(main.bottom_spacer)
			main.menu_selector.show()


	def resizeEvent(self, event=None, w_factor=None, h_factor=None):
		if w_factor and h_factor:
			if w_factor <= 1.3236363636363637:
				self.w_factor, self.h_factor = w_factor, h_factor 
				self.setFixedSize(self.w*self.w_factor, self.h*self.h_factor)
				self.back_button.setFixedSize(18*self.w_factor, 23*self.h_factor)
				self.back_button.setIconSize(QSize(18*self.w_factor, 23*self.h_factor))
				self.info_title.setFont(QFont("Arial", 10*self.h_factor, weight=QFont.Bold))
				self.practice_title.setFont(QFont("Arial", 10*self.h_factor, weight=QFont.Bold))
				self.info_text.setFixedSize(150*self.w_factor, 200*self.h_factor)
				self.info_text.setFont(QFont("Source Sans Pro", 10*self.h_factor))
				self.reset_button.setFixedSize(54*self.w_factor, 25*self.h_factor)
				self.top_spacer_2.changeSize(0, 30*self.h_factor)
				self.bottom_spacer_2.changeSize(0, 30*self.h_factor)
				self.practice_board.resizeEvent(w_factor=w_factor, h_factor=h_factor)

class Board(QWidget):

	def __init__(self, background="transparent", border=False, is_menu=False, size=[], parent=None):
		super().__init__()
		self.size = size
		self.parent = parent
		self.is_menu = is_menu
		self.background = background
		self.border = border
		self.init_ui()

	def init_ui(self):
		self.layout = QVBoxLayout()
		self.mlayout = QVBoxLayout()
		if not self.border:
			self.borders = {
				0:{0:("right", "bottom"),1:("left", "bottom", "right"),2:("left", "bottom")},
				1:{0:("top", "right", "bottom"),1:("top", "right", "left","bottom"),2:("top", "left", "bottom")},
				2:{0:("top", "right"),1:("top", "left","right"),2:("left", "top")}
				}
		self.boards = {}

		for row in range(3):
			self.boards[row] = []
			hlayout = QHBoxLayout()
			for col in range(3):
				exec(f"self.box_{row}x{col} = QPushButton(self)")
				curr = eval(f"self.box_{row}x{col}")

				stylesheet = self.setup_stylesheet(row, col)
				curr.setFont(QFont("Bahnschrift Light", 23))
				curr.setStyleSheet(stylesheet)
				curr.setFixedSize(self.size[0], self.size[1])
				self.boards[row].append(curr)
				hlayout.addWidget(curr)
				hlayout.setSpacing(0)

			self.mlayout.addLayout(hlayout)

		if self.is_menu:
			self.box_0x0.setText("Start")
			self.box_1x1.setText("How to\nPlay")
			self.box_2x2.setText("Exit")
		else:
			self.setup_clicked()

		self.mlayout.setSpacing(0)
		self.mlayout.setAlignment(Qt.AlignHCenter)
		self.layout.setSpacing(0)
		self.layout.addLayout(self.mlayout)
		self.setLayout(self.layout)

	def setup_clicked(self):
		self.box_0x0.clicked.connect(lambda: self.box_clicked(self.box_0x0))
		self.box_0x1.clicked.connect(lambda: self.box_clicked(self.box_0x1))
		self.box_0x2.clicked.connect(lambda: self.box_clicked(self.box_0x2))
		self.box_1x0.clicked.connect(lambda: self.box_clicked(self.box_1x0))
		self.box_1x1.clicked.connect(lambda: self.box_clicked(self.box_1x1))
		self.box_1x2.clicked.connect(lambda: self.box_clicked(self.box_1x2))
		self.box_2x0.clicked.connect(lambda: self.box_clicked(self.box_2x0))
		self.box_2x1.clicked.connect(lambda: self.box_clicked(self.box_2x1))
		self.box_2x2.clicked.connect(lambda: self.box_clicked(self.box_2x2))

	def setup_stylesheet(self, row, col):
		if self.border:
			stylesheet = f"""
						  background-color: {self.background};
						  border: 1px solid #424242;
						  """
		else:
			stylesheet = f"""
						 background-color: {self.background};
						 border-width: 1px;
						 border-style: solid;
						 """
			for value in self.borders[row][col]:
				stylesheet += f"\nborder-{value}: 1px solid #424242;"

		return stylesheet

	def box_clicked(self, widget, user_mark="X"):
		widget.setText(user_mark)

	def resizeEvent(self, event=None, w_factor=None, h_factor=None):
		if w_factor and h_factor:
			for i in range(3):
				for j in range(3):
					eval(f"self.box_{i}x{j}.setFixedSize(self.size[0]*w_factor, self.size[1]*h_factor)")
					eval(f"self.box_{i}x{j}.setFont(QFont('Bahnschrift Light', 23*h_factor))")

if __name__ == '__main__':
	app = QApplication(argv)
	QFontDatabase.addApplicationFont("Assets/Fonts/OpenSans-Regular.ttf")
	QFontDatabase.addApplicationFont("Assets/Fonts/SourceSansPro-Regular.ttf")
	QFontDatabase.addApplicationFont("Assets/Font/SourceSansPro-Black.tff")
	QFontDatabase.addApplicationFont("Assets/Font/SourceSansPro-SemiBold.tff")
	#win = Board("transparent", False)
	win = Main()
	win.show()
	exit(app.exec_())
