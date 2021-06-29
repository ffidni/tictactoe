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
				curr.setFont(QFont("Bahnschrift Light", 23 if self.is_menu else 46))
				curr.setStyleSheet(stylesheet)
				curr.setFixedSize(self.size[0], self.size[1])
				self.boards[row].append(curr)
				hlayout.addWidget(curr)
				hlayout.setSpacing(0)

			self.board_layout.addLayout(hlayout)

		#print(self.is_menu)
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
		#print("setup clicked")
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

	def bot_ai(self):
		pass

	def bot_turns(self, from_start=False):
		if self.game_started:
			if self.turns == 'P2':
				box = self.random_box()
				if box:
					self.mark_counter += 1
					box.setText(self.current_mark)
					self.is_ended()
					self.change_turns()

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


	def check_col(self):
		counters = [[], [], []]
		for i in range(3):
			for j in range(3):
				text = self.boards[i][j].text()
				if text:
					if not counters[i]:
						counters[i].append(text)
					elif counters[i][-1] == text:
						counters[i].append(text)

		return any([len(counter) == 3 for counter in counters])

	def check_diag(self):
		left_counter = []
		right_counter = []
		for i,j in zip(range(3), reversed(range(3))):
			left_text = self.boards[i][i].text()
			right_text = self.boards[i][j].text()
			if left_text:
				if not left_counter:
					left_counter.append(left_text)
				elif left_counter[-1] == left_text:
					left_counter.append(left_text)
			if right_text:
				if not right_counter:
					right_counter.append(right_text)
				elif right_counter[-1] == right_text:
					right_counter.append(right_text)
						
		return any((len(left_counter) == 3, len(right_counter) == 3))

	def check_row(self):
		counters = [[], [], []]
		for i in range(3):
			for j in range(3):
				text = self.boards[j][i].text()
				if text:
					if not counters[i]:
						counters[i].append(text)
					elif counters[i][-1] == text:
						counters[i].append(text)

		return any([len(counter) == 3 for counter in counters])

	def show_win(self, winner):
		if winner == self.p1:
			self.parent.p1_name.setStyleSheet("color: green;")
			self.parent.p2_name.setStyleSheet("color: red;")
		else:
			self.parent.p1_name.setStyleSheet("color: red;")
			self.parent.p2_name.setStyleSheet("color: green;")
		self.game_started = False
		self.info_board.setText(f"{winner['Name']} won!")
		for i in range(3):
			for j in range(3):
				mark = self.boards[i][j]
				stylesheet = ""
				if mark.text() == winner['Mark']:
					stylesheet = f"""background-color: {self.background};
									 color: green;
					  				 border: 1px solid #424242;"""
				else:
					stylesheet = f"""background-color: {self.background};
									 color: red;
					  				 border: 1px solid #424242;"""
				mark.setStyleSheet(stylesheet)
		QTimer.singleShot(3500, lambda: self.parent.goto("Settings"))

	def show_tie(self):
		self.game_started = False
		self.info_board.setText("It's a tie! GG")
		QTimer.singleShot(3500, lambda: self.parent.goto("Settings"))

	def is_ended(self):
		if 4 < self.mark_counter < 9:
			counters = [self.check_col(), self.check_diag(), self.check_row()]
			if any(counters):
				winner = self.p1 if self.current_mark == self.p1["Mark"] else self.p2
				self.show_win(winner)
		elif self.mark_counter == 9:
			self.show_tie()




	def resizeEvent(self, event=None, w_factor=None, h_factor=None):
		if w_factor and h_factor:
			for i in range(3):
				for j in range(3):
					eval(f"self.box_{i}x{j}.setFixedSize(self.size[0]*w_factor, self.size[1]*h_factor)")
					eval(f"self.box_{i}x{j}.setFont(QFont('Bahnschrift Light', 23*h_factor))")

class Timer(QThread):
	seconds_signal = pyqtSignal(int)
	finished_signal = pyqtSignal(bool)

	def __init__(self, seconds, parent):
		super().__init__(parent)
		self.parent = parent
		self.seconds = seconds+1

	def run(self):
		while (self.seconds > 0):
			self.seconds -= 1
			self.parent.info_board.setText(f"Timer: {self.seconds}s")
			sleep(1)
		self.finished_signal.emit(True)

	def stop(self):
		self.seconds = 0
		self.terminate()