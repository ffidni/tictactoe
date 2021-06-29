from packages import *


class WinnerLine(QWidget):

	def __init__(self):
		super().__init__()
		self.setWindowTitle("Winner Line Sketch")
		self.init_ui()

	def init_ui(self):
		frame = QFrame(self)
		frame.setFrameShape(QFrame.HLine)
		frame.rotate()

if __name__ == '__main__':
	app = QApplication(argv)
	win = WinnerLine()
	win.show()
	exit(app.exec_())

"""
'HLine'                                                                                                                                                                                                             
'VLine'                                                                                                                                                                                                             
'midLineWidth'                                                                                                                                                                                                      
'setLineWidth'                                                                                                                                                                                                      
'setMidLineWidth'  
"""