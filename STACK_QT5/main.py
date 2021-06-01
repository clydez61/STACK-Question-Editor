import sys, os
from PyQt5 import QtWidgets,QtGui,QtCore,uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.sip import dump
import resource

from nodeeditor.utils import *
from nodeeditor.node_editor_window import NodeEditorWindow
from stack_sub_window import *
from stack_drag_listbox import *
from stack_conf import *
from stack_conf_nodes import *

import syntax_pars

WINDOW_SIZE = 0
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__),"main_window_new.ui"),self)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setWindowTitle('New file - unsaved[*]')
        self.actionSave.triggered.connect(lambda:self.save())
        self.actionOpen.triggered.connect(lambda:self.open())
        self.actionSave_as.triggered.connect(lambda:self.save_as())
        
        #TODO: Disable Edit menu items when mdiArea is not in focus.

        self.actionRedo.triggered.connect(lambda:NodeEditorWindow.onEditRedo(self))
        self.actionUndo.triggered.connect(lambda:NodeEditorWindow.onEditUndo(self))
        self.actionCut.triggered.connect(lambda:NodeEditorWindow.onEditCut(self))
        self.actionCopy.triggered.connect(lambda:NodeEditorWindow.onEditCopy(self))
        self.actionPaste.triggered.connect(lambda:NodeEditorWindow.onEditPaste(self))
        self.actionDelete.triggered.connect(lambda:NodeEditorWindow.onEditDelete(self))

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

        #check if window is modified
        self.qvar_box.document().modificationChanged.connect(self.setWindowModified)
        self.qtext_box.document().modificationChanged.connect(self.setWindowModified)
        self.gfeedback_box.document().modificationChanged.connect(self.setWindowModified)
        self.sfeedback_box.document().modificationChanged.connect(self.setWindowModified)
        self.grade_box.document().modificationChanged.connect(self.setWindowModified)
        self.penalty_box.document().modificationChanged.connect(self.setWindowModified)
        self.ID_box.document().modificationChanged.connect(self.setWindowModified)
        self.qnote_box.document().modificationChanged.connect(self.setWindowModified)
        self.tag_box.document().modificationChanged.connect(self.setWindowModified)

        self.empty_icon = QIcon(".")

        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.updateMenus()

        self.treeFrameLayout = QVBoxLayout()
        self.treeFrameLayout.addWidget(QDMDragListbox())
        self.treeFrame.setLayout(self.treeFrameLayout)

        nodeeditor = StackSubWindow()
        nodeeditor.setTitle()
        subwnd = self.createMdiChild(nodeeditor)
        subwnd.widget().fileNew()
        subwnd.show()

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
            pyout.write('   "defaultgrade":')
            pyout.write('"' + str(self.ID_box.toPlainText()) + '",\n')

        #penalty
        #add here
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
            pyout.write('   "defaultgrade":')
            pyout.write('"' + str(self.ID_box.toPlainText()) + '",\n')

        #penalty
        #add here
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

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else StackSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        subwnd.setWindowState(Qt.WindowMaximized)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        # nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        # nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def updateMenus(self):
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)
        #TODO: Work with Chen to sort out save and export features
        # self.actSave.setEnabled(hasMdiChild)
        # self.actSaveAs.setEnabled(hasMdiChild)
        # self.actClose.setEnabled(hasMdiChild)
        # self.actCloseAll.setEnabled(hasMdiChild)
        # self.actTile.setEnabled(hasMdiChild)
        # self.actCascade.setEnabled(hasMdiChild)
        # self.actNext.setEnabled(hasMdiChild)
        # self.actPrevious.setEnabled(hasMdiChild)
        # self.actSeparator.setVisible(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
         #print("update Edit Menu")
         active = self.getCurrentNodeEditorWidget()
         hasMdiChild = (active is not None)

         self.actionPaste.setEnabled(hasMdiChild)
         self.actionCut.setEnabled(hasMdiChild and active.hasSelectedItems())
         self.actionCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
         self.actionDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

         self.actionUndo.setEnabled(hasMdiChild and active.canUndo())
         self.actionRedo.setEnabled(hasMdiChild and active.canRedo())

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            print("Success")
            return activeSubWindow.widget()
        print("Fail")
        return None

    def about(self):
        QMessageBox.about(self, "About STACK Tools",
                "STACK Tools is a program designed to simplify/ assist in the creation of Moodle STACK "
                "questions")

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplicationhighlight = syntax_pars.PythonHighlighter(qvar_box.document())
window = MainWindow() # Create an instance of our class
app.exec_()