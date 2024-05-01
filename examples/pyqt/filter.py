from PyQt5 import QtWidgets, QtGui
from QTermWidget import QTermWidget
from PyQt5.QtCore import QCoreApplication, QEvent, QMetaObject
from PyQt5.QtWidgets import QApplication

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

class MainWindow(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QtWidgets.QVBoxLayout(self)

		# Initialize the terminal
		self.terminal = Terminal("bash", [])
		self.layout.addWidget(self.terminal)
		
		
		self.buttons_layout = QtWidgets.QHBoxLayout()
		self.layout.addLayout(self.buttons_layout)
		
		# Add a button to send 'a' key press to the terminal
		self.send_button = QtWidgets.QPushButton("Send 'a'")
		self.send_button.clicked.connect(self.send_to_terminal)
		self.buttons_layout.addWidget(self.send_button)
		
		# Add a toggle button to block all key presses to the terminal
		self.block_button = QtWidgets.QToolButton()
		self.block_button.setText("Block All Key Presses")
		self.block_button.setCheckable(True)
		def toggle_block(checked):
			app.should_block = checked
		self.block_button.toggled.connect(toggle_block)
		self.buttons_layout.addWidget(self.block_button)
		
		#horizontal layout for input and output textfield debug views:
		self.text_edits_layout = QtWidgets.QHBoxLayout()
		self.layout.addLayout(self.text_edits_layout)
		
		#input text edit:
		self.in_text_edit = QtWidgets.QTextEdit()
		self.text_edits_layout.addWidget(self.in_text_edit)
		
		#output text edit:
		self.out_text_edit = QtWidgets.QTextEdit()
		self.text_edits_layout.addWidget(self.out_text_edit)
		
		#register received data signal:
		self.terminal.receivedData.connect(self.on_received_data)
		
		#register send data signal:
		self.terminal.sendData.connect(self.on_send_data)
		
	def on_received_data(self, data):
		self.out_text_edit.append(data)
		
	#from sip: "void sendData(const char *,int);"
	def on_send_data(self, data, size):
		self.in_text_edit.append(data)

	def send_to_terminal(self):
		event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_C, QtCore.Qt.ControlModifier)
		# self.terminal.sendKeyEvent(event)
		# def clear():
		# 	self.terminal.sendText("clear\n")
		# QtCore.QTimer.singleShot(1, clear)
		
		def send():
			self.terminal.sendText(self.in_text_edit.toPlainText())
		QtCore.QTimer.singleShot(1, send)

class MyApp(QtWidgets.QApplication):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.installEventFilter(self)
		self.should_block = False
	
	def eventFilter(self, obj, event):
		if self.should_block:
			if isinstance(obj.parent(), QTermWidget):
				return True
		if event.type() == QtCore.QEvent.KeyPress:
				key = event.key()
				modifiers = event.modifiers()
				text = event.text()
				
				if self.should_block:
					return True
		return super().eventFilter(obj, event)

if __name__ == "__main__":
	app = MyApp([])
	mainWindow = MainWindow()
	mainWindow.show()
	app.exec_()