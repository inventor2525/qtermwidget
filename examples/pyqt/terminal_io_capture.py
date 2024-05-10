import ast
from PyQt5 import QtWidgets, QtGui
from QTermWidget import QTermWidget
from PyQt5.QtCore import QCoreApplication, QEvent, QMetaObject
from PyQt5.QtWidgets import QApplication
from typing import List

from PyQt5 import QtCore
import re

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

		self.terminal_label = QtWidgets.QLabel("The terminal emulator (this is what you are use to interacting with):")
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
		self.input_label = QtWidgets.QLabel("User Input (this could be a human or an LLM)")
		self.input_label.setFixedHeight(20)
		self.input_layout.addWidget(self.input_label)
		self.input_label2 = QtWidgets.QLabel("This can contain text, key combos, and scroll events (copy paste from stdin for examples):")
		self.input_label2.setFixedHeight(20)
		self.input_layout.addWidget(self.input_label2)
		self.user_input = QtWidgets.QTextEdit()
		self.user_input.setFixedHeight(100)
		self.input_layout.addWidget(self.user_input)

		self.buttons_layout = QtWidgets.QHBoxLayout()
		self.bottomLayout.addLayout(self.buttons_layout)
		
		# Add a button to send 'a' key press to the terminal
		self.send_button = QtWidgets.QPushButton("Send Above To Terminal")
		self.send_button.clicked.connect(self.send_to_terminal)
		self.buttons_layout.addWidget(self.send_button)
		
		# Add a toggle button to block all key presses to the terminal
		self.block_button = QtWidgets.QToolButton()
		self.block_button.setText("Block All User Input To Terminal")
		self.block_button.setCheckable(True)
		def toggle_block(checked):
			app.should_block = checked
		self.block_button.toggled.connect(toggle_block)
		self.buttons_layout.addWidget(self.block_button)
		
		self.pty_text_label = QtWidgets.QLabel("This is how a shell talks to the terminal emulator (above) when you type:")
		self.bottomLayout.addWidget(self.pty_text_label)
		
		#horizontal layout for input and output textfield debug views:
		self.text_edits_layout = QtWidgets.QHBoxLayout()
		self.bottomLayout.addLayout(self.text_edits_layout)
		
		#input text edit:
		self.in_text_edit_layout = QtWidgets.QVBoxLayout()
		self.text_edits_layout.addLayout(self.in_text_edit_layout)
		self.in_text_label = QtWidgets.QLabel("Pty stdin (the direct input to the shell):")
		self.in_text_edit_layout.addWidget(self.in_text_label)
		self.in_text_edit = QtWidgets.QTextEdit()
		self.in_text_edit_layout.addWidget(self.in_text_edit)
		
		#output text edit:
		self.out_text_edit_layout = QtWidgets.QVBoxLayout()
		self.text_edits_layout.addLayout(self.out_text_edit_layout)
		self.out_text_label = QtWidgets.QLabel("Pty stdout (the direct output of the shell):")
		self.out_text_edit_layout.addWidget(self.out_text_label)
		self.out_text_edit = QtWidgets.QTextEdit()
		self.out_text_edit_layout.addWidget(self.out_text_edit)
		
		# print getImage() output to text edit:
		self.image_text_label = QtWidgets.QLabel("Terminal screen contents")
		self.bottomLayout.addWidget(self.image_text_label)
		self.image_text_label2 = QtWidgets.QLabel("This is the current rendered plain text only state of the terminal, after interpreting all that stuff above:")
		self.bottomLayout.addWidget(self.image_text_label2)
		self.image_text_edit = QtWidgets.QTextEdit()
		self.image_text_edit.setReadOnly(True)
		self.bottomLayout.addWidget(self.image_text_edit)
		
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
		self.out_text_edit.append(str(data)[2:-1])
		
		def render():
			self.image_text_edit.setText("\n".join(self.getWholeStrImage()))
		QtCore.QTimer.singleShot(50, render)
	
	def on_sent_bytes(self, data:QtCore.QByteArray):
		self.in_text_edit.append(str(data)[2:-1])
	
	def send_to_terminal(self, user_input: str):
		user_input = self.user_input.toPlainText()
		user_input = user_input.replace("\\\n", "<escaped_newline>")
		lines = user_input.split("\n")
		line = 0
		def send():
			nonlocal line
			input_text = lines[line]
			input_text = input_text.replace("<escaped_newline>", "\\\n")
			# Convert the input text to bytes
			bytes_to_send = QtCore.QByteArray(ast.literal_eval(f"b'{input_text}'"))

			# Send the bytes to the terminal
			self.terminal.sendBytes(bytes_to_send)
			line += 1
			if line < len(lines):
				QtCore.QTimer.singleShot(500, send)
		send()
		
	def getStrImage(self, startline:int, endline:int) -> List[str]:
		lines = []
		try:
			num_lines = endline - startline + 1
			image = self.terminal.getImage(startline, endline)
			columns = self.terminal.screenColumnsCount()
			for i in range(num_lines):
				line = image[i*columns:(i+1)*columns]
				lines.append("".join([chr(l_.characterValue()) for l_ in line]))
		except Exception as e:
			print(e)
		return lines

	def getWholeStrImage(self) -> List[str]:
		return self.getStrImage(0, self.terminal.historyLinesCount()+self.terminal.screenLinesCount())
	
	def print_whole_image(self):
		print("\n\n\n\nPrinting whole image:\n=================")
		print("\n".join(self.getWholeStrImage()))
		print("=================\n\n\n\n")
		
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