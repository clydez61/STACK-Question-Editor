import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__),"InputDialog.ui"),self)
        

    def saving(self):
        QApplication.processEvents()


if __name__ == "__main__":
    '''import sys
    app = QtWidgets.QApplication(sys.argv)
    more_dialog = QtWidgets.QDialog()
    ui = Ui_more_dialog()
    ui.setupUi(more_dialog)
    more_dialog.show()
    sys.exit(app.exec_())'''
    app = QtWidgets.QApplication(sys.argv) 
    window = Dialog() # Create an instance of our class
    window.show()
    sys.exit(app.exec_())   
