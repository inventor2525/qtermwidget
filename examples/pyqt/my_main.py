from PyQt5 import QtWidgets, QtGui
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
		
		self.installEventFilter(self)
		
		# Connect signals
		self.termGetFocus.connect(self.onFocus)
		self.termLostFocus.connect(self.onLostFocus)

	def onFocus(self):
		print("Terminal has focus")
		self.has_focus = True

	def onLostFocus(self):
		print("Terminal lost focus")
		self.has_focus = False

	def eventFilter(self, obj, event):
		if event.type() == QtCore.QEvent.FocusIn:
			self.has_focus = True
		elif event.type() == QtCore.QEvent.FocusOut:
			self.has_focus = False
		return super().eventFilter(obj, event)
	
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
			
	def focusInEvent(self, event):
		self.has_focus = True
		super().focusInEvent(event)

	def focusOutEvent(self, event):
		self.has_focus = False
		super().focusOutEvent(event)
	
	def keyPressEvent(self, event):
		# Capture the key press event and do something with it
		key = event.key()
		modifiers = event.modifiers()
		text = event.text()

		# You can block the event from being passed to the terminal by not calling the base class method
		# For example, let's block the 'a' key
		if key == QtCore.Qt.Key_A:
			return
		else:
			super().keyPressEvent(event)

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
		
		#text edit:
		self.text_edit = QtWidgets.QTextEdit()
		self.layout.addWidget(self.text_edit)
		
		# Install an event filter on the terminal
		self.terminal.installEventFilter(self)

	def eventFilter(self, obj, event):
		# print(event.type())
		event_type = {v: k for k, v in vars(QtCore.QEvent).items() if not k.startswith('__')}.get(event.type())
		# print(f"Event type: {event_type}")
		if event.type() in (QtCore.QEvent.KeyPress, QtCore.QEvent.KeyRelease, QtCore.QEvent.ShortcutOverride):
			# Capture the key press event and do something with it
			key = event.key()
			modifiers = event.modifiers()
			text = event.text()

			# You can block the event from being passed to the terminal by returning True
			# For example, let's block the 'a' key
			if key == QtCore.Qt.Key_A:
				return True
			return True
		# If you don't block the event, it will be passed to the terminal
		else:
			return super().eventFilter(obj, event)

	def send_a_to_terminal(self):
		# Create a QKeyEvent object representing a press of the 'a' key
		event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_A, QtCore.Qt.NoModifier, 'a')
		# Call the sendKeyEvent method with the QKeyEvent object
		self.terminal.sendKeyEvent(event)

class MyApp(QtWidgets.QApplication):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.installEventFilter(self)

	def eventFilter(self, obj, event):
		# print(type(obj))
		if event.type() == QtCore.QEvent.KeyPress:
			if isinstance(self.focusObject(), QTermWidget):
				# Capture the key press event and do something with it
				key = event.key()
				modifiers = event.modifiers()
				text = event.text()

				# You can block the event from being passed to the terminal by returning True
				# For example, let's block the 'a' key
				if key == QtCore.Qt.Key_A:
					return True
		return super().eventFilter(obj, event)

if __name__ == "__main__":
	app = MyApp([])
	mainWindow = MainWindow()
	mainWindow.show()
	app.exec_()