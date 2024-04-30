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

		# Add a button to send 'a' key press to the terminal
		self.button = QtWidgets.QPushButton("Send 'a'")
		self.button.clicked.connect(self.send_a_to_terminal)
		self.layout.addWidget(self.button)
		
		#horizontal layout for input and output textfield debug views:
		self.h_layout = QtWidgets.QHBoxLayout()
		self.layout.addLayout(self.h_layout)
		
		#input text edit:
		self.in_text_edit = QtWidgets.QTextEdit()
		self.h_layout.addWidget(self.in_text_edit)
		
		#output text edit:
		self.out_text_edit = QtWidgets.QTextEdit()
		self.h_layout.addWidget(self.out_text_edit)
		
		#register received data signal:
		self.terminal.receivedData.connect(self.on_received_data)
		
		#register send data signal:
		self.terminal.sendData.connect(self.on_send_data)
		
	def on_received_data(self, data):
		self.out_text_edit.append(data)
		
	#from sip: "void sendData(const char *,int);"
	def on_send_data(self, data, size):
		self.in_text_edit.append(data)

	def send_a_to_terminal(self):
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
		# self.installEventFilter(self)
		self.term_has_focus = False
	
	def notify(self, receiver, event):
		if event.type() == QtCore.QEvent.KeyPress:
			event_type = {v: k for k, v in vars(QtCore.QEvent).items() if not k.startswith('__')}.get(event.type())
			if receiver.parent():
				print(f"Event {event_type} sent to {receiver.objectName()} {receiver.__class__} {receiver.parent()}")
		return super().notify(receiver, event)


	def eventFilter(self, obj, event):
		if event.type() == QtCore.QEvent.KeyPress:
			# if self.term_has_focus:
			if isinstance(obj.parent(), QTermWidget):
				print("Term focused: ", type(obj))
				key = event.key()
				modifiers = event.modifiers()
				text = event.text()
				
				# if key == QtCore.Qt.Key_A:
				# 	return True
			else:
				print("Term not focused: ", type(obj))
		return super().eventFilter(obj, event)

if __name__ == "__main__":
	app = MyApp([])
	mainWindow = MainWindow()
	def on_focus():
		print("Terminal has focus")
		app.term_has_focus = True
	def on_lost_focus():
		print("Terminal lost focus")
		app.term_has_focus = False
	mainWindow.terminal.termLostFocus.connect(on_lost_focus)
	mainWindow.terminal.termGetFocus.connect(on_focus)
	mainWindow.show()
	app.exec_()