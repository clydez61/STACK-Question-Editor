import os, sys, inspect
from PyQt5.QtWidgets import *

#Below is only necessary if using nodeeditor directly in project and is two directories above
#sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", "..")

from nodeeditor.utils import loadStylesheet
from nodeeditor.node_editor_window import NodeEditorWindow

from stack_window import StackWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    wnd = StackWindow()
    
    wnd.show()

    sys.exit(app.exec_())