import sys
import os
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from ete3 import Tree



class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__(1, 8)
        self.setHorizontalHeaderLabels(["AnswerTest","Student\nAnswer","Model\nAnswer","Error range","Grade(True)","Grade(False)","Next Node(True)","Next Node(False)"])
        self.verticalHeader().setDefaultSectionSize(40)
        self.horizontalHeader().setDefaultSectionSize(190)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def _addRow(self):
        rowCount = self.rowCount()
        self.insertRow(rowCount )
        
    def _removeRow(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)

    def _copyRow(self):
        self.insertRow(self.rowCount())
        rowCount = self.rowCount()
        columnCount = self.columnCount()

        for j in range(columnCount):
            if not self.item(rowCount-2, j) is None:
                self.setItem(rowCount-1, j, QTableWidgetItem(self.item(rowCount-2, j).text()))
    
    def _generateVisual(self):
        os.system('cmd /k "dot C:\\Users\\zhouc\\Python_Workspace\\STACK_GUI\\dotfile.dot -Tsvg -o D:\\image.svg"')

    def save_as_dot(table):
        array = []
        num_rows, num_cols = table.rowCount(), table.columnCount()
        for col in range(num_cols):
            rows = []
            for row in range(num_rows):
                item = table.item(row, col)
                rows.append(item.text() if item else '')
            array.append(rows)
        index = []
        strAttrib = ""
        dotfile = open("STACK_GUI\\dotfile.dot", "w")
        dotfile.write("digraph{\n")
        for i in range(len(array[0])):
            index.append(i+1)
            if len(array[6][i]) > 0 :
                dotfile.write(str(index[i]) + "->"  + array[6][i] + "\n")

        for i in range(len(array[0])):
            if len(array[7][i]) > 0 :
                dotfile.write(str(index[i]) + "->"  + array[7][i] + "\n")

        # 2 [label = "Node:2\nTrue:Node 3(+1)"]
        #print(index)
        for i in range(len(index)):
            strAttrib += (str(index[i]) + f'[label = "Node {str(index[i])}\\n')
            strAttrib += ("True: ")

            if len(array[6][i]) > 0 :
                strAttrib += (f'Node {array[6][i]}')

            if len(array[4][i]) > 0 :
                strAttrib += (f"(+{array[4][i]})")
            strAttrib += ("\\nFalse: ")

            if len(array[7][i]) > 0 :
                strAttrib += (f'Node {array[7][i]}')

            if len(array[5][i]) > 0 :
                strAttrib += (f"(+{array[5][i]})")
            strAttrib += ('"]\n')
        dotfile.write(strAttrib)
        dotfile.write("}")  
        
        
        



       

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1800, 600)
        self.setWindowTitle("STACK")

        mainLayout = QHBoxLayout()
        table = TableWidget()
        mainLayout.addWidget(table)
        buttonLayout = QVBoxLayout()

        button_new = QPushButton('New')
        button_new.clicked.connect(table._addRow)
        buttonLayout.addWidget(button_new)

        button_copy = QPushButton('Copy')
        button_copy.clicked.connect(table._copyRow)
        buttonLayout.addWidget(button_copy)

        button_remove = QPushButton('Remove')
        button_remove.clicked.connect(table._removeRow)
        buttonLayout.addWidget(button_remove, alignment=Qt.AlignTop)

        button_visual = QPushButton('Generate Visual')
        button_visual.clicked.connect(table._generateVisual)
        buttonLayout.addWidget(button_visual)

        button_visual = QPushButton('Save as dot')
        button_visual.clicked.connect(table.save_as_dot)
        buttonLayout.addWidget(button_visual)

        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

   
if __name__ == "__main__":    
    app = QApplication(sys.argv)
    app.setStyleSheet('QPushButton{font-size: 20px; width: 200px; height: 50px}')   
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())



