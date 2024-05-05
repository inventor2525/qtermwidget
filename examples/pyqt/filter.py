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

		# Create a splitter to divide the terminal and the rest of the layout
		self.splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
		self.layout.addWidget(self.splitter)

		# Initialize the terminal
		self.terminal = Terminal("bash", [])
		self.splitter.addWidget(self.terminal)

		# Create widget for the bottom layout
		self.bottomWidget = QtWidgets.QWidget()
		self.bottomLayout = QtWidgets.QVBoxLayout(self.bottomWidget)
		self.splitter.addWidget(self.bottomWidget)

		# Add input field to the bottom layout
		self.input_layout = QtWidgets.QVBoxLayout()
		self.bottomLayout.addLayout(self.input_layout)
		self.input_label = QtWidgets.QLabel("User Input:")
		self.input_label.setFixedHeight(20)
		self.input_layout.addWidget(self.input_label)
		self.user_input = QtWidgets.QTextEdit()
		self.user_input.setFixedHeight(100)
		self.input_layout.addWidget(self.user_input)

		self.buttons_layout = QtWidgets.QHBoxLayout()
		self.bottomLayout.addLayout(self.buttons_layout)
		
		# Add a button to send 'a' key press to the terminal
		self.send_button = QtWidgets.QPushButton("Send To Terminal")
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
		self.bottomLayout.addLayout(self.text_edits_layout)
		
		#input text edit:
		self.in_text_edit_layout = QtWidgets.QVBoxLayout()
		self.text_edits_layout.addLayout(self.in_text_edit_layout)
		self.in_text_label = QtWidgets.QLabel("Pty stdin:")
		self.in_text_edit_layout.addWidget(self.in_text_label)
		self.in_text_edit = QtWidgets.QTextEdit()
		self.in_text_edit_layout.addWidget(self.in_text_edit)
		
		#output text edit:
		self.out_text_edit_layout = QtWidgets.QVBoxLayout()
		self.text_edits_layout.addLayout(self.out_text_edit_layout)
		self.out_text_label = QtWidgets.QLabel("Pty stdout:")
		self.out_text_edit_layout.addWidget(self.out_text_label)
		self.out_text_edit = QtWidgets.QTextEdit()
		self.out_text_edit_layout.addWidget(self.out_text_edit)
		
		# #register received data signal:
		# self.terminal.receivedData.connect(self.on_received_data)
		
		# #register send data signal:
		# self.terminal.sendData.connect(self.on_send_data)
		
		self.terminal.receivedBytes.connect(self.on_received_bytes)
		self.terminal.sentBytes.connect(self.on_sent_bytes)
		
	def on_received_data(self, data):
		self.out_text_edit.append(data)
		
	#from sip: "void sendData(const char *,int);"
	def on_send_data(self, data, size):
		self.in_text_edit.append(data)

	def on_received_bytes(self, data:QtCore.QByteArray):
		self.out_text_edit.append(str(data))
	
	def on_sent_bytes(self, data:QtCore.QByteArray):
		self.in_text_edit.append(str(data))
		
	def send_to_terminal(self):
		event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_C, QtCore.Qt.ControlModifier)
		# self.terminal.sendKeyEvent(event)
		# def clear():
		# 	self.terminal.sendText("clear\n")
		# QtCore.QTimer.singleShot(1, clear)
		
		def send():
			self.terminal.sendText(self.user_input.toPlainText())
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

def thing(startline, endline):
	try:
		print([l_.characterValue() for l_ in mainWindow.terminal.getImage(startline, endline)])
	except Exception as e:
		print(e)
		
		
if __name__ == "__main__":
	app = MyApp([])
	mainWindow = MainWindow()
	mainWindow.show()
	app.exec_()