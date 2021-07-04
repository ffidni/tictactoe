from packages import *

class Board(QWidget):

	def __init__(self, background="transparent", border=False, is_menu=False, size=[], game_settings=None, parent=None):
		super().__init__()
		self.size = size
		self.parent = parent
		self.is_menu = is_menu
		self.background = background
		self.border = border
		self.settings = game_settings
		self.bot_delay = 800
		self.mark_counter = 0
		self.winner_pos = ()
		if self.settings:
			self.mode = self.settings["Mode"]
			if self.mode:
				self.game_info(self.mode, self.settings["Difficulty"])

		self.init_ui()

	def init_ui(self):
		self.layout = QVBoxLayout()
		self.board_layout = QVBoxLayout()
		self.name_layout = QHBoxLayout()

		try:
			self.parent.p1_name.setText(f"{self.p1['Mark']} {self.p1['Name']}")
			self.parent.p2_name.setText(f"{self.p2['Name']} {self.p2['Mark']}")
		except:
			pass

		self.boards = {}
		for row in range(3):
			self.boards[row] = []
			hlayout = QHBoxLayout()
			for col in range(3):
				exec(f"self.box_{row}x{col} = QPushButton(self)")
				curr = eval(f"self.box_{row}x{col}")
				stylesheet = self.setup_stylesheet(row, col)

				curr.setFont(QFont("Bahnschrift Light", 23 if self.is_menu else 46))
				curr.setStyleSheet(stylesheet)
				curr.setFixedSize(self.size[0], self.size[1])
				self.boards[row].append(curr)
				hlayout.addWidget(curr)
				hlayout.setSpacing(0)

			self.board_layout.addLayout(hlayout)

		if self.is_menu:
			self.box_1x1.setText("Start")
			self.box_1x1.clicked.connect(self.parent.start)
		else:
			self.setup_clicked()
			if self.mode == 'Bot Practice':
				self.layout.addWidget(self.timer_text, alignment=Qt.AlignHCenter)
				self.layout.addLayout(self.name_layout)

		self.board_layout.setSpacing(0)
		self.board_layout.setAlignment(Qt.AlignHCenter)
		self.layout.addLayout(self.board_layout)
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

			return stylesheet

	def game_info(self, mode, difficulty):
		self.p1 = {"Name":self.settings["P1"]["Name"]}
		self.p2 = {"Name":self.settings["P2"]["Name"]}
		self.current_mark = None
		self.difficulty = difficulty
		self.game_started = True
		self.info_board = self.parent.game_info.info_board
		self.randomize_mark()

		self.turns = choice(("P1", "P2"))

		if self.turns == 'P1':
			self.current_mark = self.p1["Mark"]
		else:
			self.current_mark = self.p2["Mark"]

		self.start_game()

	def start_game(self):
		self.show_turn()
		if self.mode == 'Bot':
			if self.turns == 'P2':
				self.show_turn()
				QTimer.singleShot(self.bot_delay, self.bot_turns)

	def randomize_mark(self):
		self.p1["Mark"] = choice(("〇", "🞩"))
		self.p2["Mark"] = "〇" if self.p1["Mark"] == '🞩' else "🞩"

	def box_clicked(self, box):
		if not box.text():
			if self.game_started:
				self.player_turns(box)

	def random_box(self, stepped=[]):
		row, col = randint(0, 2), randint(0, 2)
		box = self.boards[row][col]

		if len(stepped) == 9:
			stepped.clear()
			return None
		if box.text():
			if box not in stepped:
				stepped.append(box)
			return self.random_box(stepped)
		else:
			return box

	def set_chance(self):
		chance = None
		if self.difficulty == 'Medium':
			chance = 0.5
		elif self.difficulty == 'Hard':
			chance = 1
		return chance

	def ai_turn(self):
		chance = self.set_chance()
		if random() < chance:
			self.ai_place()
		else:
			box = self.random_box()

		return box

	def ai_place(self):
		row = self.check_row(ai=True)  
		diag = self.check_diag(ai=True)  
		col = self.check_col(ai=True)  

	def bot_turns(self, from_start=False):
		if self.game_started:
			if self.turns == 'P2':
				if self.difficulty == 'Easy':
					box = self.random_box()
				else:
					box = self.ai_turn()

				if box:
					self.mark_counter += 1
					box.setText(self.current_mark)
					self.is_ended()
					self.change_turns()
				else:
					self.bot_turns()

	def player_turns(self, box, turns=None):
		if self.game_started:
			if self.mode == 'Bot':
				if self.turns == 'P1':
					self.mark_counter += 1
					box.setText(self.current_mark)
					self.is_ended()
					self.change_turns()
					QTimer.singleShot(self.bot_delay, self.bot_turns)
			else:
				self.mark_counter += 1
				box.setText(self.current_mark)
				self.is_ended()
				self.change_turns()

	def change_turns(self):
		if self.game_started:
			if self.turns == 'P1':
				self.turns = "P2"
				self.current_mark = self.p2["Mark"]
			else:
				self.turns = "P1"
				self.current_mark = self.p1["Mark"]

			self.show_turn()
			self.parent.game_info.fit_content()

	def show_turn(self):
		turn = self.p2 if self.turns == 'P2' else self.p1
		if turn == self.p1:
			self.parent.p2_name.setStyleSheet("color: gray;")
			self.parent.p1_name.setStyleSheet("color: black")
		else:
			self.parent.p1_name.setStyleSheet("color: gray;")
			self.parent.p2_name.setStyleSheet("color: black;")
		self.info_board.setText(f"{turn['Name']} turn!")


	def check_col(self, ai=False):
		for i in range(3):
			board = self.boards
			mark = board[i][0].text()
			if mark:
				if mark == board[i][1].text() and mark == board[i][2].text():
					self.winner_pos = ((i, 0), (i, 1), (i, 2))
					return True
		return False

	def check_diag(self, ai=False):
		board = self.boards
		mark = board[0][0].text()
		mark_2 = board[0][2].text()
		if mark:
			if mark == board[1][1].text() and mark == board[2][2].text():
				self.winner_pos = ((0, 0), (1, 1), (2, 2))
				return True
		if mark_2:
			if mark_2 == board[1][1].text() and mark_2 == board[2][0].text():
				self.winner_pos = ((0, 2), (1, 1), (0, 0))
				return True
		return False

	def check_row(self, ai=False):
		for i in range(3):
			board = self.boards
			mark = board[0][i].text()
			if mark:
				if mark == board[1][i].text() and mark == board[2][i].text():
					self.winner_pos = ((0, i), (1, i), (2, i))
					return True
		return False

	def show_win(self, winner):
		self.game_started = False
		self.info_board.setText(f"{winner['Name']} won!")
		for pos in self.winner_pos:
			self.boards[pos[0]][pos[1]].setStyleSheet("""background: green;
														 border: 1px solid #424242;
														 color: white;""")
		QTimer.singleShot(3500, lambda: self.parent.goto("Settings"))

	def show_tie(self):
		self.game_started = False
		self.info_board.setText("It's a tie! GG")
		QTimer.singleShot(3500, lambda: self.parent.goto("Settings"))

	def is_ended(self):
		if 4 < self.mark_counter <= 9:
			evaluate = [self.check_col(), self.check_diag(), self.check_row()]
			if any(evaluate):
				winner = self.p1 if self.current_mark == self.p1["Mark"] else self.p2
				self.show_win(winner)
			else:
				if self.mark_counter == 9:
					self.show_tie()

	def resizeEvent(self, event=None, w_factor=None, h_factor=None):
		if w_factor and h_factor:
			for i in range(3):
				for j in range(3):
					eval(f"self.box_{i}x{j}.setFixedSize(self.size[0]*w_factor, self.size[1]*h_factor)")
					eval(f"self.box_{i}x{j}.setFont(QFont('Bahnschrift Light', 23*h_factor))")
