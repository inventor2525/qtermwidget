from PyQt5 import QtWidgets
from QTermWidget import QTermWidget

from PyQt5 import QtCore

class Terminal(QTermWidget):
	def __init__(self, process: str, args: list):
		super().__init__(0)
		self.finished.connect(self.close)
		self.setTerminalSizeHint(False)
		self.setColorScheme("DarkPastels")
		self.setShellProgram(process)
		self.setArgs(args)
		self.startShellProgram()
		
		#create a timmer to ...bla...
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.bla)
		self.timer.start(100)
		
		self.show()
	
	def bla(self):
		self.timer.stop()
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.bla)
		self.timer.start(100) #so I can set a breakpoint here for debug console use.
	
	def keyPressEvent(self, event):
		super().keyPressEvent(event)
	
	def keyReleaseEvent(self, event):
		super().keyReleaseEvent(event)
	
	def mousePressEvent(self, event):
		super().mousePressEvent(event)
	
	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		
	def mouseMoveEvent(self, event):
		super().mouseMoveEvent(event)
		
	def sendKeyEvent(self, key):
		if key == QtCore.Qt.Key_Escape:
			self.close()
		else:
			super().sendKeyEvent(key)

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	args = [] #["--clean", "--noplugin"]
	term = Terminal("bash", args)
	app.exec()
