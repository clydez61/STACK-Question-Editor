import sys, os, importlib,re
from subprocess import run

from PyQt5 import QtWidgets,QtGui,QtCore,QtWebEngineWidgets,uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

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
selectedfonts = {"Arial":[0,0]}
selectedsizes = {}
gselectedfonts = {}
gselectedsizes = {}
syntax_dict = {}
float_dict = {}
defaultfont = ''
#retrieve input info
varname_dict = {}
vartype_dict = {}
varans_dict = {}
varboxsize_dict = {}
lowestterm_dict = {}
hideanswer_dict = {}
allowempty_dict = {}
simplify_dict = {}
qvar_content = ''
reserved_content = ''
qvar_definition = []
qvar_declaration = []
vardict = {}

global fontItem
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QtWidgets.QMainWindow):
    qvar_content = ''    
    
    
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__),"main_window_new.ui"),self)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        
        
        self.filename = None
        
        self.setTitle()
        self.actionSave.triggered.connect(lambda:self.onSave())
        self.actionOpen.triggered.connect(lambda:self.onOpen())
        self.actionSave_as.triggered.connect(lambda:self.onSaveAs())
        self.actionExport.triggered.connect(lambda:self.onExport())
        #self.minimizeButton.clicked.connect(lambda: self.showMinimized()) 
        self.actionDocumentation.triggered.connect(lambda:self.Documentation())
        self.actionVideos.triggered.connect(lambda:self.TutorialVids())
        #self.restoreButton.clicked.connect(lambda: self.restore_or_maximize_window())
        #self.setWindowIcon(QtGui.QIcon(u'STACK-Question-Editor\\STACK_QT5\\icons\\STACK_logo.png'))
        
        self.stackedWidget.setCurrentWidget(self.qedit_page)
        self.qvar_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.qvar_page))  
        self.qedit_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.qedit_page))        
        self.feedback_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.feedback_page))
        self.attributes_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.attributes_page))
        self.input_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.inputs_page))
        self.tree_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.tree_page))
        self.highlight = syntax_pars.PythonHighlighter(self.qvar_box.document())
        #self.highlight2 = syntax_pars.PythonHighlighter(self.qtext_box.document())
        #self.highlight3 = syntax_pars.PythonHighlighter(self.preview_box.document())
        self.tree_btn.clicked.connect(self.updateEditMenu)


        self.qtext_box.textChanged.connect(lambda:self.preview(1))
        self.gfeedback_box.textChanged.connect(lambda:self.preview(2))
        


        self.update_btn.clicked.connect(lambda: self.UpdateInput())
        self.force_close = True
        self.savefile = None
        self.inputs = None
        self.NewFrame = None
        self.NewName = None
        self.NewSize = None
        self.NewAns = None
        self.NewType = None
        self.MoreButton = QPushButton
        self.dialog_syntax = None
        self.widgetname = None
        self.row = None
        self.column = None
        self.NewLayout = None
        self.NewGrid = None
        self.NewSyntax = None
        self.NewFloat = None
        self.Newlowest = None
        self.HideAnswer = None
        self.AllowEmpty = None
        self.Simplify = None
        self.cursor = None
        self.more_btn_checked = None
        self.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")

        #setting ToolTip

        #setting rich text bar images

        self.preview_box = QWebEngineView(self.previewBaseWidget)
        self.preview_box.setObjectName(u"preview_box")
        self.preview_box.setStyleSheet(u"/*color: rgb(5, 32, 37);*/\n"
            "/* background-color: rgb(233, 246, 248) */\n"
            "\n"
            "background-color: rgb(51, 51, 51);"
            "border-color: rgb(190, 229, 235);")


        self.horizontalLayout_7.addWidget(self.preview_box)

        self.previewScroll_box.setWidget(self.previewBaseWidget)

        self.gridLayout.addWidget(self.previewScroll_box, 2, 1, 1, 1)        
        
        self.gpreview_box = QWebEngineView(self.scrollAreaWidgetContents)
        self.gpreview_box.setObjectName(u"gpreview_box")
        self.gpreview_box.setStyleSheet(u"color: rgb(5, 32, 37);\n"
            "\n"
            "border-color: rgb(190, 229, 235);")

        self.horizontalLayout_8.addWidget(self.gpreview_box)
        
        self.empty_icon = QIcon(".")

        self.nodeEditor = StackWindow()
        self.NodeEditorLayout.addWidget(self.nodeEditor)

        self.nodeEditor.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.nodeEditor.updateEditMenuSignal.connect(self.updateEditMenu)
        self.windowMapper = QSignalMapper(self.nodeEditor)
        self.windowMapper.mapped[QWidget].connect(self.nodeEditor.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.updateMenus()

        self.checkModified()
        self.menuTreeEdit.aboutToShow.connect(self.updateEditMenu)
        def moveWindow(e):
            # Detect if the window is  normal size
            # ###############################################  
            if self.isMaximized() == False: #Not maximized
                # Move window only when window is normal size   
                # ###############################################
                #if left mouse button is clicked (Only accept left mouse button clicks)

                #FIXME(Arthur): hasatrr() is a hacky fix, come up with solution to prevent click-drag of left-menu toggle button.
                if e.buttons() == Qt.LeftButton and hasattr(self, 'clickPosition'):  
                    #Move window 
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.main_header.mouseMoveEvent = moveWindow    
        self.left_menu_toggle_btn.clicked.connect(lambda: self.slideLeftMenu())    

      

    #Setting up rich text bar
        self.html_btn.setCheckable(True)       
        self.html_btn.clicked.connect(lambda:self.htmltoggle(1))
        

        #html button for general feedback
        self.html_btn2.setCheckable(True)      
        self.html_btn2.clicked.connect(lambda:self.htmltoggle(2))
        
        
        self.qtext_box.selectionChanged.connect(lambda:self.updatefont(1))
        #self.qtext_box.cursorPositionChanged.connect(lambda:self.updatefont(1))
        self.qtext_box.textChanged.connect(lambda:self.resetfont(1))

        self.qtext_box.selectionChanged.connect(lambda:self.updatesize(1))
        self.qtext_box.textChanged.connect(lambda:self.resetsize(1))
        self.qtext_box.textChanged.connect(self.createVariables)
        
        self.qvar_box.textChanged.connect(lambda:self.reserveVariables())
        
        
        self.gfeedback_box.selectionChanged.connect(lambda:self.updatefont(2))
        self.gfeedback_box.textChanged.connect(lambda:self.resetfont(2))
        self.gfeedback_box.selectionChanged.connect(lambda:self.updatesize(2))
        self.gfeedback_box.textChanged.connect(lambda:self.resetsize(2))
        

        self.tfont_box.addItems(["Arial", "Times", "Courier", "Georgia", "Verdana",  "Trebuchet",""])
        self.tfont_box.activated.connect(lambda:self.setFont(1))
    
        self.gfont_box.addItems(["Arial", "Times", "Courier", "Georgia", "Verdana",  "Trebuchet",""])
        self.gfont_box.activated.connect(lambda:self.setFont(2))    


        self.tsize_box.addItems(["6.75","7.5", "10", "12", "13.5", "18",  "24",''])
        self.qtext_box.setFontPointSize(float(12))
        self.tsize_box.setCurrentText('12')
        self.tsize_box.activated.connect(lambda:self.setFontSize(1))

        self.gsize_box.addItems(["6.75","7.5", "10", "12", "13.5", "18",  "24",''])
        self.gfeedback_box.setFontPointSize(float(12))
        self.gsize_box.setCurrentText('12')
        self.gsize_box.activated.connect(lambda:self.setFontSize(2))        


        self.tbold_btn.setCheckable(True)     
        self.tbold_btn.clicked.connect(lambda:self.boldText(1))

        self.gbold_btn.setCheckable(True)        
        self.gbold_btn.clicked.connect(lambda:self.boldText(2))
        

        self.titalic_btn.setCheckable(True)
        self.titalic_btn.clicked.connect(lambda:self.italicText(1))

        self.gitalic_btn.setCheckable(True)
        self.gitalic_btn.clicked.connect(lambda:self.italicText(2))

        self.tunderline_btn.setCheckable(True)
        self.tunderline_btn.clicked.connect(lambda:self.underlineText(1))

        self.gunderline_btn.setCheckable(True)
        self.gunderline_btn.clicked.connect(lambda:self.underlineText(2))

        self.tleft_align_btn.clicked.connect(lambda : self.qtext_box.setAlignment(Qt.AlignLeft))
        self.tcenter_align_btn.clicked.connect(lambda : self.qtext_box.setAlignment(Qt.AlignCenter))
        self.tright_align_btn.clicked.connect(lambda : self.qtext_box.setAlignment(Qt.AlignRight))

        self.gleft_align_btn.clicked.connect(lambda : self.gfeedback_box.setAlignment(Qt.AlignLeft))
        self.gcenter_align_btn.clicked.connect(lambda : self.gfeedback_box.setAlignment(Qt.AlignCenter))
        self.gright_align_btn.clicked.connect(lambda : self.gfeedback_box.setAlignment(Qt.AlignRight))
  
        self.tordered_list_btn.clicked.connect(lambda:self.bulletList(1))
        self.ttext_color_btn.clicked.connect(lambda:self.setColor(1))
        self.tbcolor_btn.clicked.connect(lambda:self.setBackgroundColor(1))

        self.gordered_list_btn.clicked.connect(lambda:self.bulletList(2))
        self.gtext_color_btn.clicked.connect(lambda:self.setColor(2))
        self.gbcolor_btn.clicked.connect(lambda:self.setBackgroundColor(2))

        
        
        
        
        self.show()



    def Documentation(self):
        url = QtCore.QUrl('https://docs.google.com/document/d/1rZ9RJFigjOELxRBzx6KPmEsl4QGB08tMCKCmzmV7G7s/edit?usp=sharing')
        if not QtGui.QDesktopServices.openUrl(url):
            QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')      

    def TutorialVids(self):
        url = QtCore.QUrl('https://drive.google.com/drive/folders/1VzFX-3eJVG8yWiVm665R5XpyyhZC-SyQ?usp=sharing')
        if not QtGui.QDesktopServices.openUrl(url):
            QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')    

    def clearInputs(self):
        item = self.gridLayout_2.itemAt(0)

        while item is not None:
            item.widget().setParent(None)
            item = self.gridLayout_2.itemAt(0)

    def setTitle(self):
        global title
        title = "STACK Question Editor - "
        title = title + (os.path.basename(self.filename) + '[*]' if self.filename is not None else "New Question[*]")

        self.setWindowTitle(title)
        
    def onOpen(self):
        try:
            fname, filter = QFileDialog.getOpenFileName(self, 'Open STACK question from file', os.path.dirname(__file__), 'STACK Question (*.json);;All files (*)')

            if fname != '' and os.path.isfile(fname):
                self.nodeEditor.closeAllSubWnd()
                self.clearInputs()
                with open(fname, 'r') as file:
                    data = json.loads(file.read())
                    #self.qtext_box.blockSignals(True)
                    
                    self.deserialize(data['nonNodeData'])
                    #self.qtext_box.blockSignals(False)
                    #NOTE(Arthur): Hacky fix to add node data and having the properties box working, fix later.
                    currentWidget = self.stackedWidget.currentWidget()
                    self.stackedWidget.setCurrentWidget(self.tree_page)
                    self.nodeEditor.deserialize(data['nodeData'])
                    self.stackedWidget.setCurrentWidget(currentWidget)
                    self.filename = fname

                
                         
                self.setTitle()
                self.setWindowModified(False)

        except Exception as e: dumpException(e)

    def onSave(self):
        data = self.serialize()
        # if not self.isWindowModified():
            # NOTE(Arthur): Skipping the return since the "input" section of this software does not
            # set window as modified when the "input" is modified

            # return
        # else:

        if self.filename is not None:
            self.saveToFile(data, self.filename)
            
        else:
            self.onSaveAs()

    def onSaveAs(self):
        global title
        try:
            data = self.serialize()
            fname, filter = QFileDialog.getSaveFileName(self, 'Save STACK question to file', os.path.dirname(__file__), 'STACK Question (*.json);;All files (*)')
            if fname == '': return False

            self.saveToFile(data, fname)
            self.filename = fname
            self.setTitle()
            return True
        except Exception as e: dumpException(e)

    def saveToFile(self, data, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(data, indent=4))
            #print("saving to", filename, "was successful.")
            self.setWindowModified(False)
            self.nodeEditor.setSubWndModifiedFalse()

    def handleSelectionChanged(self):
        
        cursor = self.qtext_box.textCursor()
        
        return [cursor.selectionStart(), cursor.selectionEnd()];
    
    def handleSelectionChanged2(self):
        
        cursor3 = self.gfeedback_box.textCursor()
        
        return [cursor3.selectionStart(), cursor3.selectionEnd()];
        
    def setFont(self,n):
        global font
        global font2
        if n == 1:
            
            font = self.tfont_box.currentText()
            self.qtext_box.blockSignals(True)
            self.qtext_box.setCurrentFont(QFont(font)) 
            self.qtext_box.blockSignals(False)
            selectedfonts[self.tfont_box.currentText()] = self.handleSelectionChanged()
            
        if n == 2:
            gfont = self.gfont_box.currentText()
            self.gfeedback_box.blockSignals(True)
            self.gfeedback_box.setCurrentFont(QFont(gfont)) 
            self.gfeedback_box.blockSignals(False)
            gselectedfonts[self.gfont_box.currentText()] = self.handleSelectionChanged2()        
        
        #just set for the following cursor locations, set font to ""             
        
    def updatefont(self,n):
        global defaultfont
        
        if n == 1:
            maxFontKey = ''
            cursor2 = self.qtext_box.textCursor() 

            #maxFontIndex = itemMaxValue[1][1]
            for textfont, cursorindex in selectedfonts.items():
                if cursor2.selectionStart() >= cursorindex[0] and cursor2.selectionEnd() < cursorindex[1]:  #if in range of a saved font index range                  
                    self.tfont_box.setCurrentText(textfont)  
                                                   
                    break  
                else:
                    self.tfont_box.setCurrentText('')   


                itemMaxValue = max(selectedfonts.items(), key=lambda x : x[1][1])
        
                maxFontKey = itemMaxValue[0]
                if cursor2.selectionStart() == len(self.qtext_box.toPlainText()):
                    
                    self.tfont_box.setCurrentText(maxFontKey)
                    selectedfonts[maxFontKey][1] = len(self.qtext_box.toPlainText())

                
                    #selectedfonts[self.tfont_box.currentText()] = [cursorindex[0],len(self.qtext_box.toPlainText())]
                  
        if n == 2:
            maxFontKey2 = ''
            cursor4 = self.gfeedback_box.textCursor() 
            
            for textfont, cursorindex in gselectedfonts.items():
                if cursor4.selectionStart() >= cursorindex[0] and cursor4.selectionEnd() <= cursorindex[1]:                    
                    self.gfont_box.setCurrentText(textfont)    
                                
                    break
                else:                    
                    self.gfont_box.setCurrentText("")                           
                itemMaxValue = max(gselectedfonts.items(), key=lambda x : x[1][1])
        
                maxFontKey2 = itemMaxValue[0]
                if cursor4.selectionStart() == len(self.gfeedback_box.toPlainText()):
                    
                    self.gfont_box.setCurrentText(maxFontKey2)
                    gselectedfonts[maxFontKey2][1] = len(self.gfeedback_box.toPlainText()) 
                
        
    def createVariables(self): #updates everytime qtext_box changes
        global qvar_content
        global stack_var
        global input_var

        if self.html_btn.isChecked() == False:
            qtext_code = self.qtext_box.toPlainText()
            stack_var = re.findall(r'[\{\[][\@\[][\w-]+[\@\]][\}\]]', qtext_code)
            for index,element in enumerate(stack_var):
                stack_var[index] = element[2:-2]
            vardict = {key:'' for i, key in enumerate(stack_var)}
            
            #vardict: automatically detected variables
            #qvar: reserved variables, including comments
            for line in self.reserveVariables():       
                variable = re.split(':',line)[0]
                try:
                    definition = re.split(':',line)[1]
                except:
                    definition = ''
                if variable in vardict: #if variable name exists in both qvar & qtext
                    vardict[variable] = definition
                if definition !='': #if there is a fully defined var, or a half defined var in qvar
                    vardict[variable] = definition

           
              
            result = json.dumps(vardict)    
             
            # printing result as string
            result = result.replace(r'",','\n')
            result = result.replace(r'"','')
            result = result.replace('{','')
            result = result.replace('}','')

            
            result = result.replace(' ','')     
            result = result.replace(r'*/'+ ':\n',r'*/'+'\n') 
            result = result.replace(r'*/'+ ':',r'*/')     
                
            randomVarHint =   r'/*Define Randomized/Plain Value variables*/'        
            #self.qvar_box.setPlainText(randomVarHint + '\n')
            
            self.qvar_box.setPlainText(result)

            inputVarHint = r'/*Define Answer Variables through Algebraic expressions*/'
            #self.qvar_box.appendPlainText(inputVarHint + '\n')
                               

    def reserveVariables(self): #detects changes in qvar_edit, if changed, update
        global reserved_content
        global qvar_definition
        global qvars
        
        reserved_content = self.qvar_box.toPlainText()
        #comments = re.findall(r'/*[\w-]+*/',reserved_content)
        qvars = re.split('[\n]',reserved_content)
        
        return qvars   
        
     

    def resetfont(self,n):
        
        
        if n == 1:
            for textfont, cursorindex in selectedfonts.items():
 
                if len(self.qtext_box.toPlainText()) <= cursorindex[1] and len(self.qtext_box.toPlainText()) > cursorindex[0]:
                    selectedfonts[textfont] = [cursorindex[0],len(self.qtext_box.toPlainText())]
                    pass               
                elif len(self.qtext_box.toPlainText()) <= cursorindex[0]:
                        
                    selectedfonts[textfont] = [-1,-1]

        if n == 2:
            for textfont, cursorindex in gselectedfonts.items():
                if len(self.gfeedback_box.toPlainText()) < cursorindex[1] and len(self.gfeedback_box.toPlainText()) > cursorindex[0]:
                    gselectedfonts[textfont] = [cursorindex[0],len(self.gfeedback_box.toPlainText())]
                    
                elif len(self.gfeedback_box.toPlainText()) <= cursorindex[0]:
                        
                    gselectedfonts[textfont] = [-1,-1]            
                #self.tfont_box.setCurrentText("Arial")

    def setFontSize(self,n):
        if n == 1:
            value = self.tsize_box.currentText()
            self.qtext_box.blockSignals(True)
            self.qtext_box.setFontPointSize(float(value))
            self.qtext_box.blockSignals(False)
            selectedsizes[self.tsize_box.currentText()] = self.handleSelectionChanged()
        if n == 2:
            value = self.gsize_box.currentText()
            self.gfeedback_box.blockSignals(True)
            self.gfeedback_box.setFontPointSize(float(value))
            self.gfeedback_box.blockSignals(False)
            gselectedsizes[self.gsize_box.currentText()] = self.handleSelectionChanged2()

    def updatesize(self,n):
        if n == 1:
            maxSizeKey = ''
            cursor2 = self.qtext_box.textCursor()
            
            for textsize, cursorindex in selectedsizes.items():
                if cursor2.selectionStart() >= cursorindex[0] and cursor2.selectionEnd() <= cursorindex[1]:
                    
                    self.tsize_box.setCurrentText(textsize)
                    
                    break
                else:               
                    self.tsize_box.setCurrentText('')
                itemMaxValue = max(selectedsizes.items(), key=lambda x : x[1][1])
        
                maxSizeKey = itemMaxValue[0]
                if cursor2.selectionStart() == len(self.gfeedback_box.toPlainText()):
                    
                    self.tsize_box.setCurrentText(maxSizeKey)
                    selectedsizes[maxSizeKey][1] = len(self.gfeedback_box.toPlainText())         
        if n == 2:
            MaxSizeKey2 = ''
            cursor4 = self.qtext_box.textCursor()
            
            for textsize, cursorindex in gselectedsizes.items():
                if cursor4.selectionStart() >= cursorindex[0] and cursor4.selectionEnd() <= cursorindex[1]:
                    
                    self.gsize_box.setCurrentText(textsize)
                    
                    break
                else:               
                    self.gsize_box.setCurrentText('12')       
                itemMaxValue = max(gselectedsizes.items(), key=lambda x : x[1][1])
        
                MaxSizeKey2 = itemMaxValue[0]
                if cursor4.selectionStart() == len(self.gfeedback_box.toPlainText()):
                    
                    self.gsize_box.setCurrentText(MaxSizeKey2)
                    gselectedsizes[MaxSizeKey2][1] = len(self.gfeedback_box.toPlainText())  

    def resetsize(self,n):
        if n == 1:
            for textsize, cursorindex in selectedsizes.items():
                if len(self.qtext_box.toPlainText()) < cursorindex[1] and len(self.qtext_box.toPlainText()) > cursorindex[0]:
                    selectedsizes[textsize] = [cursorindex[0],len(self.qtext_box.toPlainText())]
                    
                elif len(self.qtext_box.toPlainText()) <= cursorindex[0]:
                        
                    selectedsizes[textsize] = [-1,-1]
                    #self.tfont_box.setCurrentText("Arial") 
            
        if n == 2:
            for textsize, cursorindex in gselectedsizes.items():
                if len(self.gfeedback_box.toPlainText()) < cursorindex[1] and len(self.gfeedback_box.toPlainText()) > cursorindex[0]:
                    gselectedsizes[textsize] = [cursorindex[0],len(self.gfeedback_box.toPlainText())]
                    
                elif len(self.gfeedback_box.toPlainText()) <= cursorindex[0]:
                        
                    gselectedsizes[textsize] = [-1,-1]
        
    def setColor(self,n):         
        color = QColorDialog.getColor()
        if n == 1:
            self.qtext_box.setTextColor(color)
        if n == 2:
            self.gfeedback_box.setTextColor(color)
            
    def setBackgroundColor(self,n):     
        color = QColorDialog.getColor()
        if n == 1:
            self.qtext_box.setTextBackgroundColor(color)
        if n == 2:
            self.gfeedback_box.setTextBackgroundColor(color)

    def boldText(self,n):
        if n == 1:
            if self.tbold_btn.isChecked():
                self.qtext_box.setFontWeight(QFont.Bold)
            else:
                self.qtext_box.setFontWeight(QFont.Normal)  
        if n == 2:
            if self.gbold_btn.isChecked():
                self.gfeedback_box.setFontWeight(QFont.Bold)
            else:
                self.gfeedback.setFontWeight(QFont.Normal)            

    def italicText(self,n):
        state = self.qtext_box.fontItalic()
        if n == 1:
            self.qtext_box.setFontItalic(not(state)) 
        if n == 2:
            self.gfeedback_box.setFontItalic(not(state)) 

    def underlineText(self,n):
        state = self.qtext_box.fontUnderline()
        if n == 1:
            self.qtext_box.setFontUnderline(not(state))     
        if n == 2:
            self.gfeedback_box.setFontUnderline(not(state)) 

    def bulletList(self,n):        
        if n == 1:
            cursor = self.qtext_box.textCursor()
            cursor.insertList(QtGui.QTextListFormat.ListDisc)
        if n == 2:
            cursor = self.gfeedback_box.textCursor()
            cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def preview(self,n):
        if n == 1:
            #QApplication.processEvents()
            qtext_code = self.qtext_box.toHtml()
            
            #self.qtext_box.setAcceptRichText(True)
           
            
            #qtext_code = LatexNodes2Text().latex_to_text(qtext_code)
            #qtext_code = mdtex2html.convert(qtext_code)
            
            stack_var = re.findall(r'\[\[[\w-]+\]\]', qtext_code)
            random_var = re.findall(r'\{\@[\w-]+\@\}', qtext_code)
            for variables in stack_var:
                qtext_code = qtext_code.replace(variables,'_____')
            for variables in random_var:
                qtext_code = qtext_code.replace(variables, r'\textcolor{blue}{' + f'{variables[2:-2]}' + r'}')
                

            htmlstart= """
             <html><head>
            <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script></head>
             <body>
                         
             """
            htmlend = '</body></html>'  
            
            displaycode = htmlstart + qtext_code + htmlend                  
            
            
            self.preview_box.setHtml(displaycode)
        if n == 2:
            #QApplication.processEvents()

            qtext_code = self.gfeedback_box.toHtml()
            
            random_var = re.findall(r'\{\@[\w-]+\@\}', qtext_code)   
            
            for variables in random_var:
                qtext_code = qtext_code.replace(variables,r'\textcolor{blue}{' + f'{variables[2:-2]}' + r'}')

            htmlstart= """
             <html><head>
            <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script></head>
             <body>
             <mathjax>             
             """
            htmlend = '</mathjax></body></html>'  
            
            displaycode2 = htmlstart + qtext_code + htmlend        
            
            self.gpreview_box.setHtml(displaycode2)
        
    def onGenerateTreePartial(self):
        feedbackVariable = self.qvar_box.toPlainText()
        if self.retrieveInput() == False: 
            print("Inputs have not been generated yet!")
            return
        inputs = self.serializeInputs()

        feedbackVariable = re.sub(r"""(.*[^\w](rand_with_step|rand_with_prohib|rand|rand_selection).*\n)""", '', feedbackVariable)
        for input in inputs:
            print(input)
            #Search through questionvariable and replace non-LHS variables with input variables
            feedbackVariable = re.sub(r"""\b"""+ input['tans'] +r"""\b(?!([a-zA-Z0-9_]|$)*:)""", input['name'], feedbackVariable)
            #Search through questionvariable and replace LHS variables with variables with "prt" + input name
            feedbackVariable = re.sub(input['tans']+r"""(?=:)""", 'prt'+input['name'], feedbackVariable)
       
        currentWidget = self.stackedWidget.currentWidget()
        self.stackedWidget.setCurrentWidget(self.tree_page)

        try:
            self.nodeEditor.generateTree(inputs, feedbackVariable)
        except Exception as e: dumpException(e)
        
        self.stackedWidget.setCurrentWidget(currentWidget)

    def onGenerateTree(self):
        if self.retrieveInput() == False: 
            print("Inputs have not been generated yet!")
            return
        inputs = self.serializeInputs()

        currentWidget = self.stackedWidget.currentWidget()
        self.stackedWidget.setCurrentWidget(self.tree_page)

        try:
            self.nodeEditor.generateTreeNoPartialMarks(inputs)
        except Exception as e: dumpException(e)
        
        self.stackedWidget.setCurrentWidget(currentWidget)

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
        #self.more_btn_checked = more_btn_checked
        exec(f'global more_btn_checked ; more_btn_checked= self.input_btn{str(row)}_{str(column)}.isChecked()')
        if more_btn_checked == True:
            #exec(f'self.input_frame{str(row)}_{str(column)}.setMaximumSize(QSize(300, 330))')

            NewSyntax = f"input_syntax{str(row)}_{str(column)}"
            NewFloat = f"input_float{str(row)}_{str(column)}"
            NewSyntaxL = f"label_syntax{str(row)}_{str(column)}"
            NewFloatL = f"label_float{str(row)}_{str(column)}"
            NewlowestL = f"label_lowestTerms{str(row)}_{str(column)}"
            Newlowest =  f"input_lowestTerms{str(row)}_{str(column)}"
            
            
            HideAnswer = f"input_hideanswer{str(row)}_{str(column)}"
            AllowEmpty = f"input_allowempty{str(row)}_{str(column)}"
            Simplify = f"input_simplify{str(row)}_{str(column)}"
            NewextraOptions = f"label_extraOptions{str(row)}_{str(column)}"
            symbols = {"self": self,"QLabel":QLabel,"QTextEdit":QTextEdit,"Qt":Qt,"QComboBox":QComboBox}

            
            self.NewSyntax = NewSyntax
            self.NewFloat = NewFloat
            self.Newlowest = Newlowest
            self.HideAnswer = HideAnswer
            self.AllowEmpty = AllowEmpty
            self.Simplify = Simplify
            
            exec(f'self.input_btn{row}_{column}.setParent(None)')
            
            exec(f'self.label_syntax = QLabel(self.input_frame{str(row)}_{str(column)})',symbols)
            setattr(self,NewSyntaxL,self.label_syntax)
            self.label_syntax.setObjectName(u"label_size")
            self.label_syntax.setToolTip("The syntax hint will appear in the answer box\n whenever this is left blank by the student.")
            self.label_syntax.setText("Syntax Hints")       
            self.label_syntax.setMaximumSize(QSize(16777215, 30))
            self.label_syntax.setAlignment(Qt.AlignVCenter)
            #self.formLayout_2.addRow(5, QFormLayout.LabelRole, self.label_syntax)

            exec(f'self.input_syntax = QTextEdit(self.input_frame{str(row)}_{str(column)})',symbols)
            setattr(self,NewSyntax,self.input_syntax)
            self.input_syntax.setObjectName(u'input_size')
            self.input_syntax.setMaximumSize(QSize(16777215, 100))
        
            exec(f'self.input_layout{str(row)}_{str(column)}.addRow(self.label_syntax,self.input_syntax)',symbols)
            
            #self.label_float = QLabel(self.input_frame)
            exec(f'self.label_float = QLabel(self.input_frame{str(row)}_{str(column)})',symbols)
            setattr(self,NewFloatL,self.label_float)
            self.label_float.setObjectName(u"input_float")
            self.label_float.setToolTip("If set to yes, then any answer of the student \nwhich has a floating-point number will be rejected as invalid.")
            self.label_float.setText("Forbid Float")

            

            #self.input_float = QComboBox(self.input_frame)
            exec(f'self.input_float = QComboBox(self.input_frame{str(row)}_{str(column)})',symbols)
            setattr(self,NewFloat,self.input_float)
            self.input_float.addItem(u"Yes")
            self.input_float.addItem(u"No")
            self.input_float.setCurrentIndex(1)
            
            exec(f'self.input_layout{str(row)}_{str(column)}.addRow(self.label_float,self.input_float)',symbols)
            
            #self.label_lowestTerms = QLabel(self.input_frame)
            exec(f'self.label_lowestTerms = QLabel(self.input_frame{str(row)}_{str(column)})',symbols)
            setattr(self,NewlowestL,self.label_lowestTerms)   
            self.label_lowestTerms.setText("Lowest Terms")
            

            #self.input_lowestTerms = QComboBox(self.input_frame)
            exec(f'self.input_lowestTerms = QComboBox(self.input_frame{str(row)}_{str(column)})',symbols)
            setattr(self,Newlowest,self.input_lowestTerms)
            self.label_lowestTerms.setToolTip("When this option is set to yes, \n any coefficients or other rational numbers in an expression, \n must be written in lowest terms. \n Otherwise the answer is rejected as 'invalid'.")
            self.input_lowestTerms.addItem(u"No")
            self.input_lowestTerms.addItem(u"Yes")

            
            exec(f'self.input_layout{str(row)}_{str(column)}.addRow(self.label_lowestTerms,self.input_lowestTerms)',symbols)

            #self.label_extraOptions = QLabel(self.input_frame)
            exec(f'self.label_extraOptions = QLabel(self.input_frame{str(row)}_{str(column)})',symbols)
            setattr(self,NewextraOptions,self.label_extraOptions)
            
                
            self.label_extraOptions.setText("Extra Options")


            
            
            self.input_hideanswer = QCheckBox(self.input_frame)
            
            setattr(self,HideAnswer,self.input_hideanswer)
            self.input_hideanswer.setToolTip("Only supported in the string input type for JSXGraph related opreations,\n see 'Help' for details")
            self.input_hideanswer.setObjectName(u"input_hideanswer")
            self.input_hideanswer.setText("Hide Answer")


            self.input_allowempty = QCheckBox(self.input_frame)
            setattr(self,AllowEmpty,self.input_allowempty)
            self.input_allowempty.setToolTip("Normally a blank answer will be marked 'invalid',\n checking this allows blank answers to be validated as incorrect ")
            self.input_allowempty.setObjectName(u"input_allowempty")
            self.input_allowempty.setText("Allow Empty")
            
            self.input_simplify = QCheckBox(self.input_frame)
            self.input_simplify.setToolTip("Allows students to use customly created functions to simplify algebraic calculations,\n this can be used in combination with syntax hint")
            setattr(self,Simplify,self.input_simplify)
            self.input_simplify.setText("Simplify")
                       
            exec(f'self.input_layout{str(row)}_{str(column)}.addRow(self.label_extraOptions,self.input_hideanswer)',symbols)
            exec(f'self.input_layout{str(row)}_{str(column)}.addRow("",self.input_allowempty)',symbols)
            exec(f'self.input_layout{str(row)}_{str(column)}.addRow("",self.input_simplify)',symbols)

            exec(f'self.input_layout{str(row)}_{str(column)}.addRow(self.input_btn{row}_{column})',symbols)

            exec(f'self.input_btn{str(row)}_{str(column)}.setText("Save")',symbols)

            
            
            try:
                
                exec(f'self.input_syntax{str(row)}_{str(column)}.setText(syntax_dict["{str(row)}_{str(column)}"])')
                
                exec(f'self.input_float{str(row)}_{str(column)}.setCurrentText(float_dict["{str(row)}_{str(column)}"])')
                exec(f'self.input_lowestTerms{str(row)}_{str(column)}.setCurrentText(lowestterm_dict["{str(row)}_{str(column)}"])')
                if hideanswer_dict[f"{str(row)}_{str(column)}"] == True:
                    exec(f'self.input_hideanswer{str(row)}_{str(column)}.setChecked(True)')
                else:
                    exec(f'self.input_hideanswer{str(row)}_{str(column)}.setChecked(False)')
                if allowempty_dict[f"{str(row)}_{str(column)}"] == True:
                    exec(f'self.input_allowempty{str(row)}_{str(column)}.setChecked(True)')
                else:
                    exec(f'self.input_allowempty{str(row)}_{str(column)}.setChecked(False)')
                if simplify_dict[f"{str(row)}_{str(column)}"] == True:
                    exec(f'self.input_simplify{str(row)}_{str(column)}.setChecked(True)')
                else:
                    exec(f'self.input_simplify{str(row)}_{str(column)}.setChecked(False)')
            except:
                pass
        else:
            
            #save the input fields before removing
            self.normal_dict_save(row,column)
            self.expand_dict_save(row,column)
            
            exec(f'self.input_btn{str(row)}_{str(column)}.setText("More..")')

            exec(f'self.label_syntax{str(row)}_{str(column)}.setParent(None)')
            exec(f'self.input_syntax{str(row)}_{str(column)}.setParent(None)')

            exec(f'self.label_float{str(row)}_{str(column)}.setParent(None)')
            exec(f'self.input_float{str(row)}_{str(column)}.setParent(None)')

            exec(f"self.label_lowestTerms{str(row)}_{str(column)}.setParent(None)")
            exec(f"self.input_lowestTerms{str(row)}_{str(column)}.setParent(None)")

            exec(f"self.input_hideanswer{str(row)}_{str(column)}.setParent(None)")
            exec(f"self.input_allowempty{str(row)}_{str(column)}.setParent(None)")
            exec(f"self.input_simplify{str(row)}_{str(column)}.setParent(None)")
            exec(f"self.label_extraOptions{str(row)}_{str(column)}.setParent(None)")
            
    def expand_dict_save(self,row,column):
        QApplication.processEvents()
        widgetname = f'{row}_{column}'
        exec(f'global syntax; syntax = self.input_syntax{str(row)}_{str(column)}.toPlainText()')                               
        syntax_dict.update({"{}".format(widgetname):syntax})

        exec(f'global allow_float; allow_float = self.input_float{str(row)}_{str(column)}.currentText()')
        float_dict.update({"{}".format(widgetname):allow_float})
        
        exec(f'global lowest_terms; lowest_terms = self.input_lowestTerms{str(row)}_{str(column)}.currentText()')
        lowestterm_dict.update({"{}".format(widgetname):lowest_terms})

        exec(f"global hide_answer; hide_answer = self.input_hideanswer{str(row)}_{str(column)}.isChecked()")
        hideanswer_dict.update({"{}".format(widgetname):hide_answer})

        exec(f"global allow_empty; allow_empty = self.input_allowempty{str(row)}_{str(column)}.isChecked()")
        allowempty_dict.update({"{}".format(widgetname):allow_empty})

        exec(f"global simplify; simplify = self.input_simplify{str(row)}_{str(column)}.isChecked()")
        simplify_dict.update({"{}".format(widgetname):simplify})                  
                   

        self.widgetname = widgetname

    def normal_dict_save(self,row,column):
        QApplication.processEvents()
        widgetname = f'{row}_{column}'

        exec(f"global varname; varname = self.input_name{str(row)}_{str(column)}.toPlainText()")
        varname_dict.update({"{}".format(widgetname):varname})


        exec(f"global vartype; vartype = self.input_type{str(row)}_{str(column)}.currentText()")
        vartype_dict.update({"{}".format(widgetname):vartype})

        exec(f"global varboxsize; varboxsize = self.input_size{str(row)}_{str(column)}.toPlainText()")
        varboxsize_dict.update({"{}".format(widgetname):varboxsize})

        exec(f"global varans; varans = self.input_ans{str(row)}_{str(column)}.toPlainText()")
        varans_dict.update({"{}".format(widgetname):varans})    
        
    def retrieveInput(self):
        #copy this line to your save function,before you call dicts
        if self.row == None: return False
        for i in range(self.row+1):
            for j in range(self.column+1):
                QApplication.processEvents()
                self.normal_dict_save(i,j)
                self.expand_dict_save(i,j)
        
        # I made dictionaries for each term it will automatically update as user fill in,
        # you just need to call them, here below is the list of dicts, the key name is in the format of "row"_"column"
        # this function "retreieveInput" currently binded to the "Help -> Temporary save" on the menubar, feel free to remove
        # Also now you can type whatever input name you want inside [[]], changed it 

        # print(syntax_dict,float_dict,lowestterm_dict, hideanswer_dict ,allowempty_dict ,simplify_dict )
        # print(varname_dict,vartype_dict,varans_dict,varboxsize_dict)
        
        # print('input retrieved')       

    def UpdateInput(self):
        QApplication.processEvents()
        
        current_text = self.qtext_box.toPlainText()
        inputs = re.findall(r'\[\[[\w-]+\]\]', current_text) 
        symbols = {"self": self}
        
        try:
            exec(f'self.input_frame{str(self.row)}_{str(self.column)}.setParent(None)')
        except:
            pass
        for index, elem in enumerate(inputs):
            rows, lastrow = divmod(index, 4) 
                   
            self.addInput(rows,lastrow)

            exec(f'self.input_btn{rows}_{lastrow}.clicked.connect(lambda: self.expand({rows},{lastrow}))',symbols) 
            widgetname2 = f'{rows}_{lastrow}'              

            self.input_name.setText('stu_' + elem[2:-2])  
            self.input_ans.setText(elem[2:-2])          
            self.input_size.setText("5")

            

            
            #self.input_size.toPlainText() for Box Size
            #unicode(self.input_type.currentText()) for Input Type
            
            #NOTE(Arthur): Very janky workaround to init the data in the 'more...' section
            exec(f'self.input_btn{rows}_{lastrow}.toggle()', symbols)
            self.expand(rows, lastrow)
            exec(f'self.input_btn{rows}_{lastrow}.toggle()', symbols)
            self.expand(rows, lastrow)


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
        self.NewType = NewType
        self.MoreButton = MoreButton
        self.NewLayout = NewLayout
        self.input_frame = QFrame(self.ScrollPage)
        setattr(self, NewFrame, self.input_frame)

        
        #self.input_frame.setMinimumSize(QSize(100, 100))
        self.input_frame.setMaximumWidth(250)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_frame.sizePolicy().hasHeightForWidth())
        self.input_frame.setSizePolicy(sizePolicy)     
        
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
        self.label_name.setToolTip("The variable name of student input, used in the potential tree section for 'Student Answer'\n, automatically defined")
        self.label_name.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_name)

        self.input_name = QTextEdit(self.input_frame)
        self.input_name.setReadOnly(True)
        self.input_name.setStyleSheet(" background-color: rgb(106, 106, 106)",)
        self.input_name.setObjectName(u'input_name')
        self.input_name.setMaximumSize(QSize(16777215, 30))

        
        
       
        setattr(self,NewName,self.input_name)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.input_name)

        self.label_type = QLabel(self.input_frame)
        self.label_type.setToolTip("The type of input entered by student,\nfor filling in the blank purposes use Algebraic Input,\nfor further details refer to 'Help'")
        self.label_type.setObjectName(u"label_type")
        self.label_type.setText("Type")
        self.label_type.setToolTip
        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_type)

        self.input_type = QComboBox(self.input_frame)
        setattr(self,NewType,self.input_type)
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
        self.label_ans.setToolTip("The variable name of teacher input, used in the potential tree section for 'Student Answer',\n defined through the Question Text Section")
        self.label_ans.setObjectName(u"label_ans")
        self.label_ans.setText("Answer")
        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_ans)

        self.input_ans = QTextEdit(self.input_frame)
        self.input_ans.setObjectName(NewAns)
        self.input_ans.setReadOnly(True)
        self.input_ans.setStyleSheet("background-color:  rgb(106, 106, 106)")
        self.input_ans.setMaximumSize(QSize(16777215, 30))
        setattr(self,NewAns,self.input_ans)
        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.input_ans)

        self.label_size = QLabel(self.input_frame)
        self.label_size.setToolTip("Width of the input box, defaulted as 5 \n but will expand automatically adjust length as student input becomes longer")
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
        self.more_btn.setCheckable(True)
        


        symbols = {"self": self}
        
        

        #self.more_btn.clicked.connect(lambda: self.expand(row,column))
        
        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.more_btn)

        
        
        self.gridLayout_2.addWidget(self.input_frame, row, column, 1, 1)
        self.row = row
        self.column = column

        return self.formLayout_2

    def checkModified(self):
        #set up checks to see if window is modified
        self.qvar_box.document().modificationChanged.connect(self.setWindowModified)
        self.qtext_box.document().modificationChanged.connect(self.setWindowModified)
        self.gfeedback_box.document().modificationChanged.connect(self.setWindowModified)
        #self.sfeedback_box.document().modificationChanged.connect(self.setWindowModified)
        self.grade_box.document().modificationChanged.connect(self.setWindowModified)
        
        self.qnote_box.document().modificationChanged.connect(self.setWindowModified)
        self.tag_box.document().modificationChanged.connect(self.setWindowModified)

        self.nodeEditor.nodeEditorModified.connect(lambda:self.setWindowModified(True))

        
    def createActions(self):
        self.actNew = QAction('&New Tree', self, shortcut='Ctrl+N', statusTip="Create new graph", triggered= self.onFileNew)
        self.actGenerateTree = QAction('Generate Tree (Allow partial marks for partially correct work)', self, statusTip="Generate a PRT using student inputs to allow students to recieve partial marks for partially correct work", triggered= self.onGenerateTreePartial)
        self.actGenerateTreeNoPartial = QAction('Generate Tree (Only use original teacher answers)', self, statusTip="Generate a PRT only using teacher answers. This means no partial marks for partially correct work.", triggered= self.onGenerateTree)

    def createMenus(self):
        self.menuTreeEdit.clear()
        self.menuTreeEdit.addAction(self.actNew)
        self.menuTreeEdit.addAction(self.nodeEditor.actUndo)
        self.menuTreeEdit.addAction(self.nodeEditor.actRedo)
        self.menuTreeEdit.addSeparator()
        self.menuTreeEdit.addAction(self.nodeEditor.actCut)
        self.menuTreeEdit.addAction(self.nodeEditor.actCopy)
        self.menuTreeEdit.addAction(self.nodeEditor.actPaste)
        self.menuTreeEdit.addSeparator()
        self.menuTreeEdit.addAction(self.nodeEditor.actDelete)
        self.menuTreeEdit.addSeparator()
        self.nodesToolbar = self.menuTreeEdit.addAction("Nodes Toolbar")
        self.nodesToolbar.setCheckable(True)
        self.nodesToolbar.triggered.connect(self.nodeEditor.onWindowNodesToolbar)
        self.propertiesToolbar = self.menuTreeEdit.addAction("Properties Toolbar")
        self.propertiesToolbar.setCheckable(True)
        self.propertiesToolbar.triggered.connect(self.nodeEditor.onWindowPropertiesToolbar)
        self.menuTreeEdit.aboutToShow.connect(self.updateEditMenu)

        self.menuGenerate.clear()
        self.menuGenerate.addAction(self.actGenerateTree)
        self.menuGenerate.addAction(self.actGenerateTreeNoPartial)

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
            subwnd = self.nodeEditor.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)

    def htmltoggle(self,n):
        if n == 1: 
            textformat = self.qtext_box.toPlainText()        
            if self.html_btn.isChecked():
                
                htmlformat = self.qtext_box.toHtml()              
                self.qtext_box.setPlainText(htmlformat)

            else:                
                self.qtext_box.setHtml(textformat)
        if n == 2:
            textformat = self.gfeedback_box.toPlainText()        
            if self.html_btn2.isChecked():

                htmlformat = self.gfeedback_box.toHtml()                                
                self.gfeedback_box.setPlainText(htmlformat)                    
            else:
                
                self.gfeedback_box.setHtml(textformat)   

    def exportTags(self):
        tags = self.tag_box.toPlainText()
        return re.findall(r".*[^\n]", tags)

    def open(self):
        #NOTE(Arthur): Relic function, may be used for translating STACK .py files to .json in the future
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
            self.qnote_box.setPlainText(mod.question.get('questionnote')[1:-1])  

            key = mod.question.get('tags')
            result = ''
            for elements in key['tag']: 
                result += str(elements) + "\n" 
            self.tag_box.setText(result)

            #print(f"path is {imp_path}, name is {imp_name}")

    def onExport(self):
        fileExport, filter = QFileDialog.getSaveFileName(self,'Export File','STACK_QT5','(*.xml)')
        if fileExport == '': return False
        
        self.exportToFile(fileExport)

    def generateSpecificFeedback(self):
        specificfeedback = ''
        treeNames = self.nodeEditor.getAllSubWindowNames()
        for treeName in treeNames:
            treeName = re.sub(r' ', '_', treeName)
            specificfeedback = specificfeedback + '[[feedback:' + treeName + ']]\n'

        return specificfeedback

    def generateGrade(self):
        if self.grade_box.toPlainText() == '': return 1
        else: return float(self.grade_box.toPlainText())




    def automateInputSave(self):     
        current_qtext = self.qtext_box.toHtml()
        # current_qtext = re.sub(r'\\', r'\', current_qtext)
        # if self.html_btn.isChecked() == False:
        #     current_qtext = self.qtext_box.toHtml()
        # elif self.html_btn.isChecked() == True:
        #     current_qtext = self.qtext_box.toPlainText()
        inputAutomation = re.findall(r'\[\[[\w-]+\]\]', current_qtext) 
        for input in inputAutomation:
            newinput = r'[[input:stu_' + input[2:] 
            current_qtext = current_qtext.replace(input,newinput)
        randomVarSyntax = re.findall(r'\{\@[\w-]+\@\}',current_qtext)
        for vars in randomVarSyntax:
            current_qtext = current_qtext.replace(vars,vars[1:-1])
        # qtext_syntax = re.findall(r'\\', current_qtext) 
        # for syntaxP in qtext_syntax:
        #     newsyntax = str(syntaxP) + str(syntaxP)
        #     current_qtext = current_qtext.replace(syntaxP,newsyntax)
            
        return current_qtext

    def automateGFeedback(self):     
        if self.html_btn2.isChecked() == False:
            current_feedback = self.gfeedback_box.toHtml()
        elif self.html_btn2.isChecked() == True:
            current_feedback = self.gfeedback_box.toPlainText()

        feedback_syntax = re.findall(r'\\', current_feedback)
        print(feedback_syntax) 
        for syntaxP in feedback_syntax:
            newsyntax = str(syntaxP) + str(syntaxP)
            current_feedback = current_feedback.replace(syntaxP,newsyntax)
            
        return f'''{current_feedback}'''

    def exportToFile(self, fileExport):
        try:
            data = OrderedDict([
                ("questiontext", self.automateInputSave()),
                ("questionvariables", str(self.qvar_box.toPlainText())),
                ("generalfeedback", self.automateGFeedback()),
                ("specificfeedback", self.generateSpecificFeedback()),
                ("defaultgrade", self.generateGrade()),
                ("questionnote", str(self.qnote_box.toPlainText())),
                ("tags", self.exportTags()),
                ("input", self.exportSerializeInputs()),
                ("prt", self.nodeEditor.exportSerialize()),
            ])
        except Exception as e: dumpException(e)

        fileExportPy = re.sub(r".xml", ".py", fileExport)

        with open(fileExportPy,'w') as file:

            file.write("""options["grading"]="manual"\nquestion = {""")

            # file.write(json.dumps(data, indent=4))
            #writing question text
            file.write('   "questiontext":"""\n')
            file.write(str(self.automateInputSave()))
            file.write('\n""",\n')

            #writing question variables
            file.write('   "questionvariables":"""\n')
            file.write(str(self.qvar_box.toPlainText()))
            file.write('\n""",\n')

            #writing general feedback
            file.write('   "generalfeedback":"""\n')
            file.write(str(self.gfeedback_box.toHtml()))
            file.write('\n""",\n')
            
            #writing default grade
            file.write('   "defaultgrade":')
            file.write('"' + str(self.grade_box.toPlainText()) + '",\n')

            #writing question note
            file.write('   "questionnote":"""\n')
            file.write(str(self.qnote_box.toPlainText()))
            file.write('\n""",\n')

            # writing tags 
            file.write('   "tags":{\n')
            file.write('       "tag": [\n')                
            file.write(str(self.exportTags()) + '\n')
            file.write('       ]\n')
            file.write('   },\n')

            #penalty
        
            file.write('   "input":' + json.dumps(self.exportSerializeInputs(), indent=4) + ",\n")

            #NOTE(Arthur): nodeEditor.exportSerialize() outputs string!
            file.write('   "prt":' + self.nodeEditor.exportSerialize())

            file.write("}")

        outputDir = os.path.dirname(fileExport)

        pathToQCreate = os.path.abspath(os.path.dirname(__file__) + "/dependencies/tools/qcreate.py")

        run("python " + pathToQCreate + " -o" + outputDir + " " + fileExportPy)

        if os.path.exists(fileExportPy):
            os.remove(fileExportPy)

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
        super().mousePressEvent(event)
    
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
        self.animation.setDuration(200)
        self.animation.setStartValue(width)#Start value is the current menu width
        self.animation.setEndValue(newWidth)#end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()



    def serialize(self):
        qvar = self.qvar_box.toPlainText()
        qtext = self.qtext_box.toHtml()
        inputs = self.serializeInputs()
        generalfeedback = self.gfeedback_box.toHtml()
        grade = self.grade_box.toPlainText()
        qnote = self.qnote_box.toPlainText()
        tags = self.tag_box.toPlainText()
        nodeData = self.nodeEditor.serialize()
        return OrderedDict([
            ('nonNodeData', OrderedDict([
                ('questionVar', qvar),
                ('questionText', qtext),
                ('inputs', inputs),
                ('generalFeedback', generalfeedback),
                ('grade', grade),
                ('questionNote', qnote),
                ('tags', tags)])
            ),
            ('nodeData', nodeData),
        ])
    
    def deserialize(self, data, hashmap=[]):
        try:
            self.qvar_box.setPlainText(data['questionVar'])
            self.qtext_box.setHtml(data['questionText'])
            self.deserializeInputs(data['inputs'])
            self.gfeedback_box.setHtml(data['generalFeedback'])
            self.grade_box.setPlainText(data['grade'])
            self.qnote_box.setPlainText(data['questionNote'])
            self.tag_box.setPlainText(data['tags'])
        except Exception as e: dumpException(e)

    def serializeInputs(self):
        inputs = []
        try:
            if self.retrieveInput() == False: return inputs
            for key in varname_dict:
                inputs.append(
                    OrderedDict([
                        ('name', varname_dict[key]),
                        ('type', vartype_dict[key]),
                        ('tans', varans_dict[key]),
                        ('boxsize', varboxsize_dict[key]),
                        ('syntaxhint', syntax_dict[key]),
                        ('forbidfloat', float_dict[key]),
                        ('requirelowestterms', lowestterm_dict[key]),
                        ('hideAnswer', hideanswer_dict[key]),
                        ('allowEmpty', allowempty_dict[key]),
                        ('simplify', simplify_dict[key]),
                    ])
                )
        except Exception as e: dumpException(e)

        return inputs

    def exportSerializeInputs(self):
        inputs = self.serializeInputs()
        
        exportInputs = []
        inputType = {'Algebraic Input': 'algebraic', 'Checkbox': 'checkbox', 'Drop down List': 'dropdown', 'Equivalence reasoning': 'equiv', 'Matrix': 'matrix', 'Notes': 'notes', 'Numerical': 'numerical', 'Radio': 'radio', 'Single Character': 'singlechar', 'String': 'string', 'Text Area': 'textarea', 'True/False': 'boolean', 'Units': 'units'}

        for input in inputs:
            options = ''
            exportInput = OrderedDict([
                ('name', input['name']),
                ('type', inputType[input['type']]),
                ('tans', input['tans']),
                ('boxsize', int(input['boxsize'])),
                ('syntaxhint', input['syntaxhint']),
            ])

            if input['forbidfloat'] == 'Yes':
                exportInput['forbidfloat'] = 1

            else:
                exportInput['forbidfloat'] = 0

            if input['requirelowestterms'] == 'Yes':
                exportInput['requirelowestterms'] = 1

            else:
                exportInput['requirelowestterms'] = 0

            if input['hideAnswer'] == True:
                options + 'hideanswer, '

            if input['allowEmpty'] == True:
                options + 'allowempty, '

            if input['simplify'] == True:
                options + 'simp, '

            options = re.sub(r',[\s]*$','', options)

            exportInput['options'] = options

            exportInputs.append(exportInput)
        
        return exportInputs

    def deserializeInputs(self, data, hashmap=[]):
        symbols = {"self": self}

        try:
            exec(f'self.input_frame.setParent(None)')
        except:
            pass
        for index, subData in enumerate(data):
            rows, lastrow = divmod(index, 4)                          
            self.addInput(rows,lastrow)

            exec(f'self.input_btn{rows}_{lastrow}.clicked.connect(lambda: self.expand({rows},{lastrow}))',symbols)

            self.input_name.setText(subData['name'])                  
            self.input_type.setCurrentIndex(self.input_type.findText(subData['type']))         
            self.input_ans.setText(subData['tans'])
            self.input_size.setText(subData['boxsize'])

            #NOTE(Arthur): Very janky workaround to init and store the data in the 'more...' section
            exec(f'self.input_btn{rows}_{lastrow}.toggle()', symbols)
            self.expand(rows, lastrow)

            self.input_syntax.setText(subData['syntaxhint'])
            self.input_float.setCurrentIndex(self.input_float.findText(subData['forbidfloat']))
            self.input_lowestTerms.setCurrentIndex(self.input_lowestTerms.findText(subData['requirelowestterms']))
            self.input_hideanswer.setCheckState(subData['hideAnswer'])
            self.input_allowempty.setCheckState(subData['allowEmpty'])
            self.input_simplify.setCheckState(subData['simplify'])

            exec(f'self.input_btn{rows}_{lastrow}.toggle()', symbols)
            self.expand(rows, lastrow)

        #self.inputs = inputs

    def closeEvent(self, event):
        quit_msg = ''
        checkSaveStatus = re.findall(r'New Question', title)
        if checkSaveStatus != []:
            quit_msg = 'You have not selected a save location.\nAre you sure you want to ignore and exit?'
        elif self.isWindowModified() == True and checkSaveStatus == []:
            quit_msg = "Your lastest changes have not been saved.\nWould you like to save and exit or ignore changes?"

        if quit_msg != '':
            reply = QMessageBox.question(self, 'Exit Confirmation', 
                    quit_msg, QMessageBox.Save | QMessageBox.Ignore | QMessageBox.Cancel)
        else:
            event.accept()
            return
        if reply == QMessageBox.Save:
            self.onSave()
            event.accept()
        elif reply == QMessageBox.Ignore:
            event.accept()
        else:
            event.ignore()

       



        

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv) 
  
    window = MainWindow() # Create an instance of our class
    
    window.show()
    sys.exit(app.exec_())   

