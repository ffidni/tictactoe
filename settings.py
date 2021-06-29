from packages import *
from game import *
from board import *

class Settings(QWidget):
	goto_signal = pyqtSignal(str)

	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		self.setWindowTitle("Tic Tac Toe")
		self.installEventFilter(self)
		#self.setMinimumSize(self.w, self.h)
		self.init_ui()

	def init_ui(self):
		self.settings = {"P1":{"Name":""}, "P2":{"Name":""}, "Mode":"", "Difficulty":False}
		self.game_page = False
		self.widget_management()
		self.layout_management()
		self.setup_stylesheet()

	def widget_management(self):
		self.title = QPushButton("Tic Tac Toe")
		self.board = Board(background="#EAEAEA", size=[105, 105], border=True, is_menu=True, parent=self)
		self.settings_title = QLabel("Game Settings")
		self.play_with = QLabel("Play with:")
		self.play_with_input = QComboBox()
		self.difficulty = QLabel("Difficulty:")
		self.difficulty_input = QComboBox()
		self.change_name = QLabel("Edit Name:")
		self.p1_input = QLineEdit("Input player 1 name")
		self.p2_input = QLineEdit("Bot")

		for name in ('play_with', 'difficulty'):
			name_label = eval(f"self.{name}")
			name_input = eval(f"self.{name}_input")
			name_label.setFont(QFont("MS Shell Dlg 2", 10))
			name_input.setFixedSize(135, 30)


		self.title.setFont(QFont("MS Shell Dlg 2", 28))
		self.title.setIcon(QIcon("Assets/Icons/logo.png"))
		self.title.setFixedSize(300, 100)
		self.title.setIconSize(QSize(32, 32))
		self.board.installEventFilter(self)
		self.settings_title.setFont(QFont("Source Sans Pro", 24))
		self.play_with_input.currentTextChanged.connect(self.show_difficulty)
		self.play_with_input.addItem("Bot")
		self.play_with_input.addItem("Friend")
		self.difficulty_input.addItem("Easy")
		self.difficulty_input.addItem("Medium")
		self.difficulty_input.addItem("Hard")
		self.change_name.setFont(QFont("MS Shell Dlg 2", 10))
		self.p1_input.setFixedSize(135, 30)
		self.p1_input.installEventFilter(self)
		self.p2_input.setFixedSize(135, 30)
		self.p2_input.installEventFilter(self)

	def layout_management(self):
		self.main_layout = QVBoxLayout()
		self.body_layout = QHBoxLayout()
		self.input_layout = QVBoxLayout()

		self.main_layout.addSpacing(50)
		self.main_layout.addWidget(self.title, alignment=Qt.AlignCenter)
		self.body_layout.addSpacing(50)
		self.body_layout.addWidget(self.board)
		self.input_layout.addSpacing(60)
		self.input_layout.addWidget(self.settings_title, alignment=Qt.AlignCenter | Qt.AlignBottom)
		self.input_layout.addSpacing(20)
		self.input_layout.addWidget(self.play_with, alignment=Qt.AlignCenter | Qt.AlignBottom)
		self.input_layout.addWidget(self.play_with_input, alignment=Qt.AlignCenter)
		self.input_layout.addWidget(self.difficulty, alignment=Qt.AlignCenter | Qt.AlignBottom)
		self.input_layout.addWidget(self.difficulty_input, alignment=Qt.AlignCenter)
		self.input_layout.addSpacing(30)
		self.input_layout.addWidget(self.change_name, alignment=Qt.AlignCenter | Qt.AlignBottom)
		self.input_layout.addWidget(self.p1_input, alignment=Qt.AlignCenter)
		self.input_layout.addWidget(self.p2_input, alignment=Qt.AlignCenter)
		self.input_layout.addSpacing(130)
		self.body_layout.addSpacing(50)
		self.body_layout.addLayout(self.input_layout)
		self.body_layout.addSpacing(30)
		self.main_layout.addLayout(self.body_layout)

		self.setLayout(self.main_layout)

	def setup_stylesheet(self):
		#self.setStyleSheet("""background: #f0f0f0;""")
		#self.setObjectName("Main")
		#self.setStyleSheet("""#Main{
		#					    background: yellow;
		#					   }""")
		self.title.setStyleSheet("""background: transparent;
									border: none;""")
		self.p1_input.setStyleSheet("""color: gray;""")
		if self.difficulty.isHidden():
			self.p2_input.setStyleSheet("""color: gray;""")
		else:
			self.p2_input.setStyleSheet("""color: black;""")

	def show_difficulty(self, text):
		if text == 'Friend':
			self.p2_input.setText("Input player 2 name")
			self.p2_input.setStyleSheet("""color: gray;""")
			self.input_layout.removeWidget(self.difficulty)
			self.input_layout.removeWidget(self.difficulty_input)
			self.difficulty.hide()
			self.difficulty_input.hide()
		else:
			try:
				self.p2_input.setText("Bot")
				self.p2_input.setStyleSheet("""color: black;""")
				self.input_layout.insertWidget(5, self.difficulty, alignment=Qt.AlignCenter | Qt.AlignBottom)
				self.input_layout.insertWidget(6, self.difficulty_input, alignment=Qt.AlignCenter | Qt.AlignBottom)
				self.difficulty.show()
				self.difficulty_input.show()
			except:
				pass

	def goto(self, page):
		self.goto_signal.emit(page)

	def start(self):
		p1_name = self.p1_input.text()
		p2_name = self.p2_input.text()
		mode = self.play_with_input.currentText()

		if p1_name == 'Input player 1 name':
			p1_name = "Player 1"
		if p2_name == 'Input player 2 name':
			if self.mode == 'Bot':
				p2_name = "Bot"
			else:
				p2_name = "Player 2"

		self.settings["P1"]["Name"] = p1_name
		self.settings["P2"]["Name"] = p2_name
		self.settings["Mode"] = mode
		if not self.difficulty_input.isHidden():
			self.settings["Difficulty"] = self.difficulty_input.currentText()

		self.p1_input.setText(p1_name)
		self.p1_input.setStyleSheet("""color: black;""")
		self.p2_input.setText(p2_name)
		self.parent.register(Game(self), "Game")
		game_page = self.parent.m_pages["Game"]

		self.goto("Game")

	def eventFilter(self, obj, event):
		if (event.type() == QEvent.MouseButtonPress):
			if event.button() == Qt.LeftButton:
				if obj == self.p1_input or obj == self.p2_input:
					text = obj.text()
					if text == 'Input player 1 name' or text == 'Input player 2 name' or not text:
						obj.setText("")
						obj.setStyleSheet("""color: black;""")
				else:
					focused_widget = QApplication.focusWidget()
					if isinstance(focused_widget, QLineEdit):
						if not self.p1_input.text():
							self.p1_input.setText("Input player 1 name")
							self.p1_input.setStyleSheet("""color: gray;""")
						if not self.p2_input.text():
							self.p2_input.setText("Input player 2 name")
							self.p2_input.setStyleSheet("""color: gray;""")
						focused_widget.clearFocus()

		return super().eventFilter(obj, event)

	def resizeEvent(self, event):
		self.w_factor = self.width() / self.parent.w
		self.h_factor = self.height() / self.parent.h

		print(self.width(), self.height())




if __name__ == '__main__':
	app = QApplication(argv)
	app.setStyleSheet("""QComboBox{
								background-color: white;
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
								background-color: white;
								border: 1px solid black;
							}
							QSpinBox:down-button{
								border: none;
							}
							QSpinBox:up-button{
								border: none;
							}

						""")
	QFontDatabase.addApplicationFont("Assets/Fonts/OpenSans-Regular.ttf")
	QFontDatabase.addApplicationFont("Assets/Fonts/SourceSansPro-Regular.ttf")
	QFontDatabase.addApplicationFont("Assets/Font/SourceSansPro-Black.tff")
	QFontDatabase.addApplicationFont("Assets/Font/SourceSansPro-SemiBold.tff")
	win = Settings()
	win.show()
	exit(app.exec_())