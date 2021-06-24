import sys, os, importlib,re
from PyQt5 import QtWidgets,QtGui,QtCore,uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from Input_Dialog import Dialog
import resource
import json
from pylatexenc.latex2text import LatexNodes2Text
from nodeeditor.utils import *
from nodeeditor.node_editor_window import NodeEditorWindow
from stack_window import StackWindow
from stack_sub_window import *
from stack_drag_listbox import *
from stack_conf import *
from stack_conf_nodes import *

import syntax_pars
list = []
WINDOW_SIZE = 0
class MainWindow(QtWidgets.QMainWindow):
    nodeEditorModified = pyqtSignal()

    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__),"main_window_new.ui"),self)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.Dialog = Dialog()
        self.setWindowTitle('New file - unsaved[*]')
        self.actionSave.triggered.connect(lambda:self.save())
        self.actionOpen.triggered.connect(lambda:self.onOpen())
        self.actionSave_as.triggered.connect(lambda:self.onSaveAs())
        self.actionExport.triggered.connect(lambda:self.onExport())

        #self.minimizeButton.clicked.connect(lambda: self.showMinimized()) 
        #self.closeButton.clicked.connect(lambda: self.close()) 
        #self.restoreButton.clicked.connect(lambda: self.restore_or_maximize_window())
       
        
        self.stackedWidget.setCurrentWidget(self.qedit_page)
        self.qvar_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.qvar_page))  
        self.qedit_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.qedit_page))        
        self.feedback_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.feedback_page))
        self.attributes_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.attributes_page))
        self.input_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.inputs_page))
        self.tree_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.tree_page))
        self.highlight = syntax_pars.PythonHighlighter(self.qvar_box.document())
        self.highlight2 = syntax_pars.PythonHighlighter(self.qtext_box.document())
        self.highlight3 = syntax_pars.PythonHighlighter(self.preview_box.document())
        self.tree_btn.clicked.connect(self.updateEditMenu)
        self.preview_btn.clicked.connect(self.preview)


        

        self.update_btn.clicked.connect(lambda: self.UpdateInput())
        self.savefile = None
        self.inputs = None
        self.NewFrame = None
        self.NewName = None
        self.NewSize = None
        self.NewAns = None
        self.MoreButton = None
        self.dialog_syntax = None
        self.history = None
        self.row = None
        self.column = None
        self.NewLayout = None
        self.NewGrid = None
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
        self.menuEdit.aboutToShow.connect(self.updateEditMenu)
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

    def onOpen(self):
        try:
            fname, filter = QFileDialog.getOpenFileName(self, 'Open STACK question from file', os.path.dirname(__file__), 'STACK Question (*.json);;All files (*)')

            if fname != '' and os.path.isfile(fname):
                with open(fname, 'r') as file:
                    data = json.loads(file.read())
                    self.deserialize(data['nonNodeData'])
                    self.nodeEditor.deserialize(data['nodeData'])
        except Exception as e: dumpException(e)

    def onSaveAs(self):
        try:
            nonNodeData = self.serialize()
            nodeData = self.nodeEditor.serialize()
            data = OrderedDict([
                ('nonNodeData', nonNodeData),
                ('nodeData', nodeData), 
            ])
            fname, filter = QFileDialog.getSaveFileName(self, 'Save STACK question to file', os.path.dirname(__file__), 'STACK Question (*.json);;All files (*)')
            if fname == '': return False

            self.setWindowTitle(fname)
            self.saveToFile(data, fname)
            return True
        except Exception as e: dumpException(e)

    def saveToFile(self, data, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(data, indent=4))
            print("saving to", filename, "was successful.")
            self.setWindowModified(False)
            self.filename = filename
        
        

        
    def preview(self):
        QApplication.processEvents()
        qtext_code = self.qtext_box.toPlainText()
        
        self.qtext_box.setAcceptRichText(True)
        self.preview_box.setAcceptRichText(True)
        #self.preview_box.setStyleSheet("color: rgb(85, 0, 255);")
        qtext_code = LatexNodes2Text().latex_to_text(qtext_code)
        stack_var = re.findall(r'\@[a-zA-z0-9]+\@', qtext_code)
        
        
        for elements in stack_var: 
            #font-size:8pt; to change            
            qtext_code = qtext_code.replace(elements,"{" + elements + "}")
        #self.preview_box.setStyleSheet("color: rgb(51, 51, 51);")
        
        print(qtext_code)
        self.preview_box.setText(qtext_code)

        
    def openDialog(self): #opens the dialog with the "more" button, openDialog() proceeds before set
        
        QApplication.processEvents()

        self.Dialog.input_save_btn.clicked.connect(lambda: self.set())

        syntax_content = {}
        try:
            for index, elem in enumerate(self.inputs):
                rows, lastrow = divmod(index, 4)


                #exec(f'self.connectClass.input_syntax{rows}_{lastrow}.setText({dialog_syntax})')
                #exec(f'history{index}.append("{dialog_syntax}")')
                

                #print(syntax_content)
                #syntax_content["syntax{}_{}".format(rows,lastrow)] = dialog_syntax
        except:
            pass
        
        self.Dialog.show()
    

    def expand(self,row,column):
        
        
        exec(f'self.input_frame{str(row)}_{str(column)}.setMaximumSize(QSize(300, 330))')

        NewSyntax = f"input_syntax{str(row)}_{str(column)}"
        NewFloat = f"input_float{str(row)}_{str(column)}"
        #NewSyntaxL = f"label_syntax{str(row)}_{str(column)}"
        #NewFloatL = f"label_float{str(row)}_{str(column)}"
        #NewlowestL = f"label_lowestTerms{str(row)}_{str(column)}"
        Newlowest =  f"input_lowestTerms{str(row)}_{str(column)}"
        NewGrid = f"NewGrid{str(row)}_{str(column)}"
        HideButton =  f"hide_btn{str(row)}_{str(column)}"

        symbols = {"self": self,"QLabel":QLabel,"QTextEdit":QTextEdit,"Qt":Qt,}




        exec(f'self.input_btn{row}_{column}.hide()')
        exec(f'self.label_syntax = QLabel(self.input_frame{str(row)}_{str(column)})',symbols)
      
        self.label_syntax.setObjectName(u"label_size")
        self.label_syntax.setText("Syntax Hints")       
        self.label_syntax.setMaximumSize(QSize(16777215, 30))
        self.label_syntax.setAlignment(Qt.AlignVCenter)
        #self.formLayout_2.addRow(5, QFormLayout.LabelRole, self.label_syntax)

        exec(f'self.input_syntax = QTextEdit(self.input_frame{str(row)}_{str(column)})',symbols)
        setattr(self,NewSyntax,self.input_syntax)
        self.input_syntax.setObjectName(u'input_size')
        self.input_syntax.setMaximumSize(QSize(16777215, 100))
    
        exec(f'self.input_layout{str(row)}_{str(column)}.addRow(self.label_syntax,self.input_syntax)',symbols)
        
        #self.formLayout_2.addRow(self.label_syntax,self.input_frame)
        #self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.input_syntax)

        self.label_float = QLabel(self.input_frame)
     
        self.label_float.setObjectName(u"input_float")
        self.label_float.setText("Forbid Float")

        

        self.input_float = QComboBox(self.input_frame)
        setattr(self,NewFloat,self.input_float)
        self.input_float.addItem(u"Yes")
        self.input_float.addItem(u"No")
        
        exec(f'self.input_layout{str(row)}_{str(column)}.addRow(self.label_float,self.input_float)',symbols)

        self.label_lowestTerms = QLabel(self.input_frame)
           
        self.label_lowestTerms.setText("Lowest Terms")
        

        self.input_lowestTerms = QComboBox(self.input_frame)
        setattr(self,Newlowest,self.input_lowestTerms)
        self.input_lowestTerms.addItem(u"Yes")
        self.input_lowestTerms.addItem(u"No")

        exec(f'self.input_layout{str(row)}_{str(column)}.addRow(self.label_lowestTerms,self.input_lowestTerms)',symbols)

        self.label_extraOptions = QLabel(self.input_frame)
        #setattr(self,NewExtra,self.label_lowestTerms)        
        self.label_extraOptions.setText("Extra Options")


        
        setattr(self,NewGrid,self.gridLayout)
        self.input_hideanswer = QCheckBox(self.input_frame)
        self.input_hideanswer.setObjectName(u"input_hideanswer")
        self.input_hideanswer.setText("Hide Answer")


        self.input_allowempty = QCheckBox(self.input_frame)
        self.input_allowempty.setObjectName(u"input_allowempty")
        self.input_allowempty.setText("Allow Empty")
        
        self.input_simplify = QCheckBox(self.input_frame)
        self.input_simplify.setText("Simplify")
        



        
        exec(f'self.input_layout{str(row)}_{str(column)}.addRow(self.label_extraOptions,self.input_hideanswer)',symbols)
        exec(f'self.input_layout{str(row)}_{str(column)}.addRow("",self.input_allowempty)',symbols)
        exec(f'self.input_layout{str(row)}_{str(column)}.addRow("",self.input_simplify)',symbols)

        self.hide_btn = QPushButton(self.input_frame)
        setattr(self,HideButton,self.hide_btn)        
        self.hide_btn.setText(u"Hide")
        exec(f'self.input_layout{str(row)}_{str(column)}.addRow(self.hide_btn)',symbols)
        exec(f'self.hide_btn{str(row)}_{str(column)}.clicked.connect(lambda:self.restore({row},{column}))',symbols)
        
        #exec(f'self.input_layout{str(row)}_{str(column)}.addRow(self.input_allowempty)',symbols)
        #exec(f'self.input_layout{str(row)}_{str(column)}.setAlignment(Qt.AlignRight)',symbols)

        
    def restore(self,row,column): #not sure if needed to go back?
        
        NewSyntax = f"input_syntax{str(row)}_{str(column)}"
        NewFloat = f"input_float{str(row)}_{str(column)}"
        #NewSyntaxL = f"label_syntax{str(row)}_{str(column)}"
        #NewFloatL = f"label_float{str(row)}_{str(column)}"
        #NewlowestL = f"label_lowestTerms{str(row)}_{str(column)}"
        Newlowest =  f"input_lowestTerms{str(row)}_{str(column)}"
        NewGrid = f"NewGrid{str(row)}_{str(column)}"
        HideButton =  f"hide_btn{str(row)}_{str(column)}"
        print(NewSyntax)

        exec(f'self.input_syntax{str(row)}_{str(column)}.setParent(None)')
        exec(f'self.input_float{str(row)}_{str(column)}.setParent(None)')
        exec(f"self.input_lowestTerms{str(row)}_{str(column)}.setParent(None)")

        #self.gridLayout_2.addWidget(self.input_frame, row, column, 1, 1)
    def set(self): #action after clicking the save button , passes 2nd window info to 1st window
        QApplication.processEvents()
        #self.connectClass = Dialog()
        syntax_content = {}
        
        for index, elem in enumerate(self.inputs):
            rows, lastrow = divmod(index, 4)                            
            self.Dialog.new_dialog(rows,lastrow)
            #index = 2, added 2
            exec(f'current_syntax = self.Dialog.input_syntax{rows}_{lastrow}.toPlainText()') #retrieve syntax hint

            #exec(f'syntax_content{rows}_{lastrow} = []; syntax_content{rows}_{lastrow}.append(current_syntax) ')

            #exec(f'print(self.connectClass.input_float{rows}_{lastrow}.currentText())')
        
        #exec(f'print(syntax_content{rows}_{lastrow})')
        
        self.Dialog.close()   

    def UpdateInput(self):
        QApplication.processEvents()
        current_text = self.qtext_box.toPlainText()
        inputs = re.findall(r'\[\[input:[a-zA-z0-9]+\]\]', current_text) 
        symbols = {"self": self}
        try:
            exec(f'self.input_frame.setParent(None)')
        except:
            pass
        for index, elem in enumerate(inputs):
            rows, lastrow = divmod(index, 4)                            
            self.addInput(rows,lastrow)
            
            #exec(f'self.input_btn{row}_{column}.clicked.connect(lambda: self.expand({row},{column}))',symbols) 
            exec(f'self.input_btn{rows}_{lastrow}.clicked.connect(lambda: self.expand({rows},{lastrow}))',symbols)        
            exec(f'self.input_name{rows}_{lastrow}.setText("{elem[8:-2]}")')
            exec(f'self.input_size{rows}_{lastrow}.setText("5")')
        
        
        #To store or save user input fo "input" section:
        #self.input_name.toPlainText() for Name
        #self.input_ans.toPlainText() for Model answer
        #self.input_size.toPlainText() for Box Size
        #unicode(self.input_type.currentText()) for Input Type
        self.inputs = inputs    

            #self.addInput()
            #i+=1

    def addInput(self,row,column): #triggers by clicking update 
        
        NewFrame = f"input_frame{str(row)}_{str(column)}"
        NewName = f"input_name{str(row)}_{str(column)}"
        NewLayout = f"input_layout{str(row)}_{str(column)}"
        
        
        NewAns = f"input_ans{str(row)}_{str(column)}"
        NewSize = f"input_size{str(row)}_{str(column)}"
        NewType = f"input_type{str(row)}_{str(column)}"
        MoreButton = f"input_btn{str(row)}_{str(column)}"
        self.NewFrame = NewFrame
        self.NewName = NewName
        self.NewSize = NewSize
        self.NewAns = NewAns
        self.MoreButton = MoreButton
        self.NewLayout = NewLayout
        self.input_frame = QFrame(self.ScrollPage)
        setattr(self, NewFrame, self.input_frame)

        self.input_frame.setMinimumSize(QSize(100, 100))
        self.input_frame.setMaximumSize(QSize(300, 300))
        
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setFrameShadow(QFrame.Raised)
        self.input_frame.setObjectName(u"QFrame")
        self.input_frame.setStyleSheet(u"font: 5pt \"MS Sans Serif\";color: rgb(255, 255, 222);background-color: rgb(51, 51, 51);border-color: rgb(255, 255, 0);")
        self.ScrollPage.setStyleSheet(u"#QFrame{border:2px solid rgb(255,0,0)}")
        self.formLayout_2 = QFormLayout(self.input_frame)
        self.formLayout_2.setObjectName(u"formLayout_2")
        setattr(self, NewLayout, self.formLayout_2)
        self.label_name = QLabel(self.input_frame)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setText("Name")
        self.label_name.setToolTip("The Name of the Input, can be used in the potential tree section\n Edit through the Question Text Section")
        self.label_name.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_name)

        self.input_name = QTextEdit(self.input_frame)
        self.input_name.setObjectName(u'input_name')
        self.input_name.setMaximumSize(QSize(16777215, 30))

        
       
        setattr(self,NewName,self.input_name)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.input_name)

        self.label_type = QLabel(self.input_frame)
        self.label_type.setObjectName(u"label_type")
        self.label_type.setText("Type")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_type)

        self.input_type = QComboBox(self.input_frame)
        self.input_type.addItem(u"Algebraic Input")
        self.input_type.addItem(u"Checkbox")
        self.input_type.addItem(u"Drop down List")
        self.input_type.addItem(u"Equivalence reasoning")
        self.input_type.addItem(u"Matrix")
        self.input_type.addItem(u"Notes")
        self.input_type.addItem(u"Numerical")
        self.input_type.addItem(u"Radio")
        self.input_type.addItem(u"Single Character")
        self.input_type.addItem(u"String")
        self.input_type.addItem(u"Text Area")
        self.input_type.addItem(u"True/False")
        self.input_type.addItem(u"Units")
        self.input_type.setObjectName(NewType)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.input_type)

        self.label_ans = QLabel(self.input_frame)
        self.label_ans.setObjectName(u"label_ans")
        self.label_ans.setText("Answer")
        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_ans)

        self.input_ans = QTextEdit(self.input_frame)
        self.input_ans.setObjectName(NewAns)
        self.input_ans.setMaximumSize(QSize(16777215, 30))
        setattr(self,NewAns,self.input_ans)
        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.input_ans)

        self.label_size = QLabel(self.input_frame)
        self.label_size.setObjectName(u"label_size")
        self.label_size.setText("Box Size")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_size)

        self.input_size = QTextEdit(self.input_frame)
        setattr(self,NewSize,self.input_size)
        self.input_size.setObjectName(u'input_size')
        self.input_size.setMaximumSize(QSize(16777215, 30))
        
        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.input_size)

        self.more_btn = QPushButton(self.NewFrame)
        setattr(self,MoreButton,self.more_btn)
        self.more_btn.setObjectName(u"more_btn")
        self.more_btn.setText(u"More..")
        symbols = {"self": self}
        
        

        #self.more_btn.clicked.connect(lambda: self.expand(row,column))
        
        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.more_btn)

        
        #self.gridLayout_2.addWidget(self.input_frame, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.input_frame, row, column, 1, 1)
        self.row = row
        self.column = column



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

        self.nodeEditorModified.connect(lambda:self.setWindowModified(True))

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
        self.menuEdit.addSeparator()
        self.nodesToolbar = self.menuEdit.addAction("Nodes Toolbar")
        self.nodesToolbar.setCheckable(True)
        self.nodesToolbar.triggered.connect(self.nodeEditor.onWindowNodesToolbar)
        self.propertiesToolbar = self.menuEdit.addAction("Properties Toolbar")
        self.propertiesToolbar.setCheckable(True)
        self.propertiesToolbar.triggered.connect(self.nodeEditor.onWindowPropertiesToolbar)
        self.menuEdit.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        # May contain other menu items
        self.updateEditMenu()

    def updateEditMenu(self):
        active = self.nodeEditor.getCurrentNodeEditorWidget() 
        self.actNew.setEnabled(self.nodeEditor.isVisible())
        self.nodesToolbar.setEnabled(self.nodeEditor.isVisible())
        self.nodesToolbar.setChecked(self.nodeEditor.nodesDock.isVisible())	
        self.propertiesToolbar.setEnabled(self.nodeEditor.isVisible())
        self.propertiesToolbar.setChecked(self.nodeEditor.propertiesDock.isVisible())

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


    def serialize(self):
        qvar = self.qvar_box.toPlainText()
        qtext = self.qtext_box.toPlainText()
        generalfeedback = self.gfeedback_box.toPlainText()
        specificfeedback = self.sfeedback_box.toPlainText()
        grade = self.grade_box.toPlainText()
        mainid = self.ID_box.toPlainText()
        qnote = self.qnote_box.toPlainText()
        tags = self.tag_box.toPlainText()
        return OrderedDict([
            ('questionVar', qvar),
            ('questionText', qtext),
            ('generalFeedback', generalfeedback),
            ('specificFeedback', specificfeedback),
            ('grade', grade),
            ('mainID', mainid),
            ('questionNote', qnote),
            ('tags', tags),
        ])
    
    def deserialize(self, data, hashmap=[]):
        try:
            self.qvar_box.setPlainText(data['questionVar'])
            self.qtext_box.setPlainText(data['questionText'])
            self.gfeedback_box.setPlainText(data['generalFeedback'])
            self.sfeedback_box.setPlainText(data['specificFeedback'])
            self.grade_box.setPlainText(data['grade'])
            self.ID_box.setPlainText(data['mainID'])
            self.qnote_box.setPlainText(data['questionNote'])
            self.tag_box.setPlainText(data['tags'])
        except Exception as e: dumpException(e)

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
        print(NewSyntax)
        NewFloat  = f"input_float{str(row)}_{str(column)}"
        self.NewFrameD = NewFrameD
        self.NewSyntax = NewSyntax
        self.NewFloat = NewFloat
        self.NewButton2 = NewButton2
        setattr(self, NewFrameD, self.input_frameD)
        setattr(self, NewSyntax, self.input_syntax)
        setattr(self, NewFloat, self.input_float)
        setattr(self, NewButton2, self.input_save_btn)
        

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv) 
  
    window = MainWindow() # Create an instance of our class
    
    window.show()
    sys.exit(app.exec_())   


        




