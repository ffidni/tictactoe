from packages import *
from board import *

class Game(QWidget):
	goto_signal = pyqtSignal(str)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.settings = self.parent.settings
		self.init_ui()

	def init_ui(self):
		self.widget_management()
		self.layout_management()

	def widget_management(self):
		self.p1_name = QLabel(self.settings["P1"]["Name"])
		self.p2_name = QLabel(self.settings["P2"]["Name"])
		self.game_info = GameInfo(self)
		self.board = Board(background="#EAEAEA", size=[115, 115], border=True, game_settings=self.settings, parent=self)
		self.button_widget = ButtonWidget(self)

		self.p1_name.setFont(QFont("Source Sans Pro", 12))
		self.p2_name.setFont(QFont("Source Sans Pro", 12))
		self.button_widget.surrender_btn.clicked.connect(self.surrender)
		self.button_widget.toggle_btn.clicked.connect(lambda: self.toggle(self.button_widget.toggle_btn.text()))

	def layout_management(self):
		mlayout = QVBoxLayout()
		name_layout = QHBoxLayout()		

		name_layout.addSpacing(50)
		name_layout.addWidget(self.p1_name, alignment=Qt.AlignCenter)
		name_layout.addWidget(self.p2_name, alignment=Qt.AlignCenter)
		name_layout.addSpacing(50)
		mlayout.addSpacing(3)
		mlayout.addWidget(self.game_info)
		mlayout.addSpacing(20)
		mlayout.addLayout(name_layout)
		mlayout.addWidget(self.board)
		mlayout.addWidget(self.button_widget)
		mlayout.addSpacing(10)
		self.setLayout(mlayout)

	def goto(self, name):
		self.goto_signal.emit(name)

	def toggle(self, command):
		if self.settings['Mode'] == 'Bot':
			if command == ' Pause':
				current_board = self.board.info_board.text()
				if 'won' not in current_board and 'tie' not in current_board:
					self.board.game_started = False
					self.board.info_board.setText("Paused")
					self.button_widget.toggle_btn.setIcon(QIcon("Assets/Icons/resume_button.png"))
					self.button_widget.toggle_btn.setText(" Resume")
			else:
				self.board.game_started = True
				turn = self.board.p1 if self.board.current_mark == self.board.p1['Mark'] else self.board.p2
				self.board.info_board.setText(f"{turn['Name']} turn!")
				if turn == self.board.p2:
					QTimer.singleShot(400, self.board.bot_turns)
				self.button_widget.toggle_btn.setIcon(QIcon("Assets/Icons/pause_button.png"))
				self.button_widget.toggle_btn.setText(" Pause")

	def surrender(self):
		winner = self.board.p2 if self.board.p1["Mark"] == self.board.current_mark else self.board.p1
		self.board.show_win(winner)

	def resizeEvent(self, event):
		pass

class GameInfo(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.init_ui()

	def init_ui(self):
		self.widget_management()
		self.layout_management()

	def widget_management(self):
		self.info_w, self.info_h = 180, 30
		self.clock = QPushButton(icon=QIcon("Assets/Icons/clock.png"))
		self.best_of = QLabel(f"Best of: 3")
		self.score = QLabel("Score: 0-0")
		self.line = QFrame()
		self.info_board = QLabel()

		self.clock.setFixedSize(58, 58)
		self.clock.setIconSize(QSize(58, 58))
		self.clock.setStyleSheet("""background: transparent;
									border: none;""")
		self.best_of.setFont(QFont("Source Sans Pro", 16))
		self.score.setFont(QFont("Source Sans Pro", 16))
		self.line.setFrameShape(QFrame.HLine)
		self.line.setFixedWidth(230)
		self.info_board.setFixedSize(self.info_w, self.info_h)
		self.info_board.setFont(QFont("Source Sans Pro", 12))
		self.info_board.setAlignment(Qt.AlignCenter)
		self.info_board.setStyleSheet("""background: white;
										 border: 1px solid lightgray;""")

	def layout_management(self):
		mlayout = QVBoxLayout()
		spacer = QSpacerItem(350, 0, QSizePolicy.Fixed, QSizePolicy.Fixed)

		mlayout.addSpacing(20)
		mlayout.addWidget(self.clock, alignment=Qt.AlignCenter | Qt.AlignBottom)
		mlayout.addWidget(self.line, alignment=Qt.AlignCenter | Qt.AlignBottom)
		mlayout.addWidget(self.info_board, alignment=Qt.AlignCenter | Qt.AlignTop)
		mlayout.setSpacing(0)
		mlayout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(mlayout)

	def fit_content(self):
		text = self.info_board.text()
		font = QFont("Source Sans Pro", 0)
		fm = QFontMetrics(font)
		width = fm.width(text)
		line_width = self.line.width()
		if width > self.info_board.width():
			self.info_board.setFixedSize(width+60, self.info_h)

		info_board_width = self.info_board.width()
		if line_width < info_board_width:
			plus = info_board_width-line_width
			self.line.setFixedWidth((line_width+plus)+15)

class ButtonWidget(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.init_ui()

	def init_ui(self):
		self.widget_management()
		self.setup_stylesheet()
		self.layout_management()

	def widget_management(self):
		self.surrender_btn = QPushButton(" Surrender")
		self.toggle_btn = QPushButton(" Pause")

		self.surrender_btn.setIcon(QIcon("Assets/Icons/surrender_flag.png"))
		self.surrender_btn.setFixedSize(100, 32)
		self.surrender_btn.setIconSize(QSize(24, 24))
		if self.parent.settings['Mode'] == 'Bot':
			self.toggle_btn.setIcon(QIcon("Assets/Icons/pause_button.png"))
		else:
			self.toggle_btn.setIcon(QIcon("Assets/Icons/pause_button_disabled.png"))
		self.toggle_btn.setFixedSize(100, 32)
		self.toggle_btn.setIconSize(QSize(24, 24))

	def setup_stylesheet(self):
		self.surrender_btn.setStyleSheet("""QPushButton{
							  					background: #f5f5f5;
							  					border: 1px solid #e0e0e0;
							  			   }
							  				QPushButton:hover{
							  					background: #eeeeee;
							  			   }""")
		if self.parent.settings['Mode'] == 'Bot':
			self.toggle_btn.setStyleSheet("""QPushButton{
								  					background: #f5f5f5;
								  					border: 1px solid #e0e0e0;
								  			   }
								  				QPushButton:hover{
								  					background: #eeeeee;
								  			   }""")
		else:
			self.toggle_btn.setStyleSheet("""QPushButton{
													color: gray;
								  					background: #f5f5f5;
								  					border: 1px solid #e0e0e0;
								  			   }""")


	def layout_management(self):
		self.main_layout = QHBoxLayout()

		self.main_layout.addWidget(self.surrender_btn, alignment=Qt.AlignRight)
		self.main_layout.addWidget(self.toggle_btn, alignment=Qt.AlignLeft)
		self.setLayout(self.main_layout)
		