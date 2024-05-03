from pyqtbuild import PyQtBindings, PyQtProject
from enum import Enum

class Rendition(Enum):
    DEFAULT = 0
    BOLD = 1
    BLINK = 2
    UNDERLINE = 4
    REVERSE = 8
    ITALIC = 16
    CURSOR = 32
    EXTENDED_CHAR = 64
    FAINT = 128
    STRIKEOUT = 256
    CONCEAL = 512
    OVERLINE = 1024
    
class QTermWidget(PyQtProject):
    def __init__(self):
        super().__init__()
        self.bindings_factories = [QTermWidgetBindings]

class QTermWidgetBindings(PyQtBindings):
    def __init__(self, project):
        super().__init__(project, name='QTermWidget', sip_file='qtermwidget.sip', qmake_QT=['widgets'], include_dirs=["/usr/include/qtermwidget5/"])
        self._project = project

    def apply_user_defaults(self, tool):
        self.libraries.append('qtermwidget5')
        super().apply_user_defaults(tool)
