import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__),"InputDialog.ui"),self)
        self.NewFrameD = None
        self.NewSyntax = None
        self.NewFloat = None
        self.NewButton2 = None
        
    def saving(self):
        QApplication.processEvents()
        
    def new_dialog(self,row,column):
        NewFrameD = f"input_frameD{str(row)}_{str(column)}"
        NewSyntax = f"input_syntax{str(row)}_{str(column)}"
        NewButton2 = f"input_save_btn{str(row)}_{str(column)}"
        
        NewFloat  = f"input_float{str(row)}_{str(column)}"
        self.NewFrameD = NewFrameD
        self.NewSyntax = NewSyntax
        self.NewFloat = NewFloat
        self.NewButton2 = NewButton2
        setattr(self, NewFrameD, self.input_frameD)
        setattr(self, NewSyntax, self.input_syntax)
        setattr(self, NewFloat, self.input_float)
        setattr(self, NewButton2, self.input_save_btn)
    



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv) 
    window = Dialog() # Create an instance of our class
    window.show()
    sys.exit(app.exec_())   
