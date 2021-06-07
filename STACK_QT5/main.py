import sys, os, importlib
from PyQt5 import QtWidgets,QtGui,QtCore,uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.sip import dump
import resource
import json

from nodeeditor.utils import *
from nodeeditor.node_editor_window import NodeEditorWindow
from stack_window import StackWindow
from stack_sub_window import *
from stack_drag_listbox import *
from stack_conf import *
from stack_conf_nodes import *

import syntax_pars

WINDOW_SIZE = 0
class MainWindow(QtWidgets.QMainWindow):
    nodeEditorModified = pyqtSignal()

    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__),"main_window_new.ui"),self)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setWindowTitle('New file - unsaved[*]')
        self.actionSave.triggered.connect(lambda:self.save())
        self.actionOpen.triggered.connect(lambda:self.open())
        self.actionSave_as.triggered.connect(lambda:self.save_as())
        self.actionExport.triggered.connect(lambda:self.onExport())

        #self.minimizeButton.clicked.connect(lambda: self.showMinimized()) 
        #self.closeButton.clicked.connect(lambda: self.close()) 
        #self.restoreButton.clicked.connect(lambda: self.restore_or_maximize_window())
        
        self.stackedWidget.setCurrentWidget(self.qedit_page)
        self.qedit_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.qedit_page))        
        self.feedback_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.feedback_page))
        self.attributes_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.attributes_page))
        self.input_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.inputs_page))
        self.tree_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.tree_page))
        self.highlight = syntax_pars.PythonHighlighter(self.qvar_box.document())

        self.savefile = None
 
        self.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        #setting ToolTip
  
        #html button for question text
        self.html_btn.setCheckable(True)
        self.html_btn.toggle()
        self.html_btn.clicked.connect(lambda:self.htmltoggle())
        self.qtext_box.acceptRichText()

        #html button for general feedback
        self.html_btn2.setCheckable(True)
        self.html_btn2.toggle()
        self.html_btn2.clicked.connect(lambda:self.htmltoggle2())
        
        
        self.empty_icon = QIcon(".")

        self.nodeEditor = StackWindow()
        self.NodeEditorLayout.addWidget(self.nodeEditor)

        self.nodeEditor.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self.nodeEditor)
        self.windowMapper.mapped[QWidget].connect(self.nodeEditor.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.updateMenus()
        

        self.checkModified()

        def moveWindow(e):
            # Detect if the window is  normal size
            # ###############################################  
            if self.isMaximized() == False: #Not maximized
                # Move window only when window is normal size  
                # ###############################################
                #if left mouse button is clicked (Only accept left mouse button clicks)
                #FIXME: hasatrr() is a hacky fix, come up with solution to prevent click-drag of left-menu toggle button.
                if e.buttons() == Qt.LeftButton and hasattr(self, 'clickPosition'):  
                    #Move window 
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.main_header.mouseMoveEvent = moveWindow    
        self.left_menu_toggle_btn.clicked.connect(lambda: self.slideLeftMenu())        
        self.show()
        
        #add input here (row,column)
        self.addInput(0,1)
        self.addInput(0,2)
        self.addInput(0,3)
        self.addInput(1,1)
 
    def addInput(self,row,column):
        NewFrame = setattr(self, "new_frame", "")
        NewName = f"input_name({str(row)},{str(column)})"
        NewAns = f"input_ans({str(row)},{str(column)})"
        NewSize = f"input_size({str(row)},{str(column)})"
        NewType = f"input_type({str(row)},{str(column)})"
        
        print(NewFrame)
        NewFrame = QFrame(self.ScrollPage)


        NewFrame.setMinimumSize(QSize(100, 100))
        NewFrame.setMaximumSize(QSize(200, 250))
        
        NewFrame.setFrameShape(QFrame.StyledPanel)
        NewFrame.setFrameShadow(QFrame.Raised)
        NewFrame.setObjectName(u"QFrame")
        NewFrame.setStyleSheet(u"font: 5pt \"MS Sans Serif\";\n"
"color: rgb(255, 255, 222);\n"
"background-color: rgb(51, 51, 51);\n"
"border-color: rgb(255, 255, 0);\n"
"")
        self.ScrollPage.setStyleSheet(u"#QFrame{"
"border:2px solid rgb(255,0,0)"
"}")
        self.formLayout_2 = QFormLayout(NewFrame)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_name = QLabel(NewFrame)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setText("Name")
        self.label_name.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_name)

        self.input_name = QTextBrowser(NewFrame)
        self.input_name.setObjectName(NewName)
        self.input_name.setMaximumSize(QSize(16777215, 30))

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.input_name)

        self.label_type = QLabel(NewFrame)
        self.label_type.setObjectName(u"label_type")
        self.label_type.setText("Type")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_type)

        self.input_type = QComboBox(NewFrame)
        self.input_type.addItem("Algebraic Input")
        self.input_type.addItem("Checkbox")
        self.input_type.addItem("Drop down List")
        self.input_type.addItem("Equivalence reasoning")
        self.input_type.addItem("Matrix")
        self.input_type.addItem("Notes")
        self.input_type.addItem("Numerical")
        self.input_type.addItem("Radio")
        self.input_type.addItem("Single Character")
        self.input_type.addItem("String")
        self.input_type.addItem("Text Area")
        self.input_type.addItem("True/False")
        self.input_type.addItem("Units")
        self.input_type.setObjectName(NewType)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.input_type)

        self.label_ans = QLabel(NewFrame)
        self.label_ans.setObjectName(u"label_ans")
        self.label_ans.setText("Answer")
        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_ans)

        self.input_ans = QTextEdit(NewFrame)
        self.input_ans.setObjectName(NewAns)
        self.input_ans.setMaximumSize(QSize(16777215, 30))

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.input_ans)

        self.label_size = QLabel(NewFrame)
        self.label_size.setObjectName(u"label_size")
        self.label_size.setText("Box Size")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_size)

        self.input_size = QTextEdit(NewFrame)
        self.input_size.setObjectName(NewSize)
        self.input_size.setMaximumSize(QSize(16777215, 30))

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.input_size)

        self.more_btn = QPushButton(NewFrame)
        self.more_btn.setObjectName(u"more_btn")
        self.more_btn.setText("More..")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.more_btn)


        #self.gridLayout_2.addWidget(self.input_frame, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(NewFrame, row, column, 1, 1)
        

    def checkModified(self):
        #set up checks to see if window is modified
        self.qvar_box.document().modificationChanged.connect(self.setWindowModified)
        self.qtext_box.document().modificationChanged.connect(self.setWindowModified)
        self.gfeedback_box.document().modificationChanged.connect(self.setWindowModified)
        self.sfeedback_box.document().modificationChanged.connect(self.setWindowModified)
        self.grade_box.document().modificationChanged.connect(self.setWindowModified)
        
        self.ID_box.document().modificationChanged.connect(self.setWindowModified)
        self.qnote_box.document().modificationChanged.connect(self.setWindowModified)
        self.tag_box.document().modificationChanged.connect(self.setWindowModified)

        self.nodeEditorModified.connect(self.nodeEditorSetWindowModified)

    def nodeEditorSetWindowModified(self):
        self.setWindowModified(True)

    def createActions(self):
        self.actNew = QAction('&New', self, shortcut='Ctrl+N', statusTip="Create new graph", triggered=self.onFileNew)

    def createMenus(self):
        self.menuEdit.clear()

        self.menuEdit.addAction(self.actNew)
        self.menuEdit.addAction(self.nodeEditor.actUndo)
        self.menuEdit.addAction(self.nodeEditor.actRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.nodeEditor.actCut)
        self.menuEdit.addAction(self.nodeEditor.actCopy)
        self.menuEdit.addAction(self.nodeEditor.actPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.nodeEditor.actDelete)

        self.menuEdit.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        # May contain other menu items
        self.updateEditMenu()

    def updateEditMenu(self):
        active = self.nodeEditor.getCurrentNodeEditorWidget() 

        hasMdiChild = (active is not None)
        self.nodeEditor.actPaste.setEnabled(hasMdiChild)
        self.nodeEditor.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
        self.nodeEditor.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
        self.nodeEditor.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

        self.nodeEditor.actUndo.setEnabled(hasMdiChild and active.canUndo())
        self.nodeEditor.actRedo.setEnabled(hasMdiChild and active.canRedo())

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)

    


    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else StackSubWindow()
        subwnd = self.nodeEditor.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.nodeEditorModified.emit)
        nodeeditor.addCloseEventListener(self.nodeEditor.onSubWndClose)
        return subwnd

    def htmltoggle(self):
        textformat = self.qtext_box.toPlainText()        
        if self.html_btn.isChecked():
            htmlformat = repr(self.qtext_box.toPlainText())
            
            htmlformat = r'<p>' + textformat.replace("\n", "<br>") + r'</p>'
            print(htmlformat)
            
            self.qtext_box.setPlainText(htmlformat)

            self.html_btn.setStyleSheet("background-color : lightblue")
  
        else:
            
            self.qtext_box.setHtml(textformat)


    def htmltoggle2(self):
        textformat = self.gfeedback_box.toPlainText()        
        if self.html_btn2.isChecked():
            htmlformat = repr(self.gfeedback_box.toPlainText())
            
            htmlformat = r'<p>' + textformat.replace("\n", "<br>") + r'</p>'
            
            
            self.gfeedback_box.setPlainText(htmlformat)

            self.html_btn2.setStyleSheet("background-color : lightblue")
  
        else:
            
            self.gfeedback_box.setHtml(textformat)    

    def onExport(self):
        print(self.isWindowModified())

    def open(self):
        fname = QFileDialog.getOpenFileName(self,'Open File','STACK_QT5','(*.py)') #(*.py *.xml *.txt)
        path = fname[0]
        split_string = path.rsplit("/",1)
        imp_path = split_string[0] 
        imp_path += '/'
        name = split_string[-1].split(".")
        imp_name = name[0]
        
        if imp_name and imp_path != '':
            sys.path.insert(0, imp_path)
            
            mod = importlib.import_module(imp_name)

        #make the variable global
            print(f"path:{imp_path},name = {imp_name}")

            #self.qvar_box.clear()
            self.qvar_box.setPlainText(mod.question.get('questionvariables')[1:-1])     
            self.qtext_box.setPlainText(mod.question.get('questiontext')[1:-1])           
            self.gfeedback_box.setPlainText(mod.question.get('generalfeedback')[1:-1])               
            self.sfeedback_box.insertPlainText(mod.question.get('specificfeedback')[1:-1])               
            self.grade_box.setPlainText(mod.question.get('defaultgrade'))     
            #self.penalty_box.setPlainText(mod.question.get('penalty'))
            self.ID_box.setPlainText(mod.question.get('idnumber'))       
            self.qnote_box.setPlainText(mod.question.get('questionnote')[1:-1])  

            key = mod.question.get('tags')
            result = ''
            for elements in key['tag']: 
                result += str(elements) + "\n" 
            self.tag_box.setText(result)
            print(f"path is {imp_path}, name is {imp_name}")

    def save_as(self):
        if not self.isWindowModified():
            return
        savefile, _ = QFileDialog.getSaveFileName(self,'Save File','STACK_QT5','(*.py)')
        if savefile:
            pyout = open(savefile,'w')
            pyout.write("question = {")

            #writing question text
            pyout.write('   "questiontext":"""\n')
            pyout.write(str(self.qtext_box.toPlainText()))
            pyout.write('\n""",\n')

            #writing question variables
            pyout.write('   "questionvariables":"""\n')
            pyout.write(str(self.qvar_box.toPlainText()))
            pyout.write('\n""",\n')

            #writing general feedback
            pyout.write('   "generalfeedback":"""\n')
            pyout.write(str(self.gfeedback_box.toPlainText()))
            pyout.write('\n""",\n')
            
            #writing default grade
            pyout.write('   "defaultgrade":')
            pyout.write('"' + str(self.grade_box.toPlainText()) + '",\n')

            #writing question note
            pyout.write('   "questionnote":"""\n')
            pyout.write(str(self.qnote_box.toPlainText()))
            pyout.write('\n""",\n')

            # writing tags
            pyout.write('   "tags":{\n')
            pyout.write('       "tag": [\n')                
            pyout.write(str(self.tag_box.toPlainText()) + '\n')
            pyout.write('       ]\n')
            pyout.write('   },\n')

            #writing ID
            pyout.write('   "idnumber":')
            pyout.write('"' + str(self.ID_box.toPlainText()) + '",\n')

            #penalty
      
          
            pyout.write("\n}")
                                    
            self.savefile = savefile
            self.setWindowTitle(str(os.path.basename(savefile)))

    def save(self):
        # if savefile[0] already exists, then save, if savefile[0] does not, then open save_file    
        if not self.isWindowModified():
            return

        if not self.savefile:
            self.save_as()
        else:
            pyout = open(self.savefile,'w')
            pyout.write("question = {")

            #writing question text
            pyout.write('   "questiontext":"""\n')
            pyout.write(str(self.qtext_box.toPlainText()))
            pyout.write('\n""",\n')

            #writing question variables
            pyout.write('   "questionvariables":"""\n')
            pyout.write(str(self.qvar_box.toPlainText()))
            pyout.write('\n""",\n')

            #writing general feedback
            pyout.write('   "generalfeedback":"""\n')
            pyout.write(str(self.gfeedback_box.toPlainText()))
            pyout.write('\n""",\n')
            
            #writing default grade
            pyout.write('   "defaultgrade":')
            pyout.write('"' + str(self.grade_box.toPlainText()) + '",\n')

            #writing question note
            pyout.write('   "questionnote":"""\n')
            pyout.write(str(self.qnote_box.toPlainText()))
            pyout.write('\n""",\n')

            # writing tags
            pyout.write('   "tags":{\n')
            pyout.write('       "tag": [\n')                
            pyout.write(str(self.tag_box.toPlainText()) + '\n')
            pyout.write('       ]\n')
            pyout.write('   },\n')

            #writing ID
            pyout.write('   "idnumber":')
            pyout.write('"' + str(self.ID_box.toPlainText()) + '",\n')

            #penalty

            pyout.write("\n}")
   
    def restore_or_maximize_window(self):
        # Global windows state
        global WINDOW_SIZE #The default value is zero to show that the size is not maximized
        win_status = WINDOW_SIZE

        if win_status == 0:
        	# If the window is not maximized
        	WINDOW_SIZE = 1 #Update value to show that the window has been maxmized
        	self.showMaximized()

        	# Update button icon  when window is maximized
        	self.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-restore.png"))#Show minized icon
        else:
        	# If the window is on its default size
            WINDOW_SIZE = 0 #Update value to show that the window has been minimized/set to normal size (which is 800 by 400)
            self.showNormal()

            # Update button icon when window is minimized
            self.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-maximize.png"))#Show maximize icon

    def mousePressEvent(self, event):
       
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
    
    def slideLeftMenu(self):
        # Get current left menu width
        width = self.left_side_menu.width()

        # If minimized
        if width == 50:
            # Expand menu
            newWidth = 150
        # If maximized
        else:
            # Restore menu
            newWidth = 50

        # Animate the transition
        self.animation = QPropertyAnimation(self.left_side_menu, b"minimumWidth")#Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)#Start value is the current menu width
        self.animation.setEndValue(newWidth)#end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplicationhighlight = syntax_pars.PythonHighlighter(qvar_box.document())
window = MainWindow() # Create an instance of our class
app.exec_()