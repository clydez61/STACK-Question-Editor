import os
import json
from collections import OrderedDict
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.sip import dump

from nodeeditor.utils import *
from nodeeditor.node_editor_window import NodeEditorWindow
from stack_sub_window import StackSubWindow
from stack_drag_listbox import QDMDragListbox
from stack_properties_box import PropertiesBox
from stack_conf import *
from stack_conf_nodes import *

import qss.nodeeditor_dark_resources

DEBUG = False

class StackWindow(NodeEditorWindow):
    # For parent widget to know modifications have been made within node editor
    nodeEditorModified = pyqtSignal()

    def initUI(self):
        self.name_company = 'University of Alberta'
        self.name_product = 'STACK Tools'

        self.stylesheet_filename = os.path.join(os.path.dirname(__file__), 'qss/nodeeditor.qss')
        loadStylesheets(
            os.path.join(os.path.dirname(__file__), 'qss/nodeeditor-dark.qss'),
            self.stylesheet_filename        
        )

        self.empty_icon = QIcon(".")

        if DEBUG:
            print("Registered nodes:")
            pp(STACK_NODES)

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.mdiArea.subWindowActivated.connect(self.updateEditorPropertiesBox)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createDocks()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()

        self.setWindowTitle("STACK Tools")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()
            # hacky fix for PyQt 5.14.x
            import sys
            sys.exit(0)

    def createActions(self):
        super().createActions()

        # self.actClose = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        # self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        # self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        # self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        # self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        # self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)

        # self.actSeparator = QAction(self)
        # self.actSeparator.setSeparator(True)

        # self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.showMaximized()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)

    def onFileOpen(self):
        fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file')

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        nodeeditor = StackSubWindow()
                        if nodeeditor.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.createMdiChild(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e: dumpException(e)

    def about(self):
        QMessageBox.about(self, "About STACK Tools",
                "STACK Tools is a program designed to simplify/ assist in the creation of Moodle STACK "
                "questions")

    def createMenus(self):
        pass
        # super().createMenus()

        # self.windowMenu = self.menuBar().addMenu("&Window")
        # self.updateWindowMenu()
        # self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        # self.menuBar().addSeparator()

        # self.helpMenu = self.menuBar().addMenu("&Help")
        # self.helpMenu.addAction(self.actAbout)

        # self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        # active = self.getCurrentNodeEditorWidget()
        # hasMdiChild = (active is not None)

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
        try:
            #print("update Edit Menu")
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            # self.actPaste.setEnabled(hasMdiChild)
            # self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            # self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            # self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            # self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            # self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e: dumpException(e)

    def mouseReleaseEvent(self, event):
        self.updateEditorPropertiesBox()
        super().mouseReleaseEvent(event)

    def updateEditorPropertiesBox(self):
        currentSubWnd = self.getCurrentNodeEditorWidget()
        if currentSubWnd is None:
            self.propertiesWidget.setNoSubWindowLayout()
        else:
            self.propertiesWidget.treeDataSignal.connect(self.storeTreeData)
            self.displayTreeData()
            if currentSubWnd.hasSelectedItem():
                self.displayNodeData(self.getNodeData())
                self.propertiesWidget.setNodeSelectedLayout()
            else:
                self.propertiesWidget.setNoneSelectedLayout()

    def displayTreeData(self):
        tree = self.getCurrentNodeEditorWidget()
        data = tree.treeSerialize()
        # When switching over to a new tree, stops the textChanged emit signal
        self.propertiesWidget.blockSignals(True)
        self.propertiesWidget.displayTreeData(data)
        self.propertiesWidget.blockSignals(False)

    def storeTreeData(self, data):
        tree = self.getCurrentNodeEditorWidget()
        tree.treeDeserialize(data)

    def displayNodeData(self, data):
        # When switching over to a new tree, stops the textChanged emit signal
        self.propertiesWidget.blockSignals(True)
        self.propertiesWidget.displayNodeData(data)
        self.propertiesWidget.blockSignals(False)
    
    def getNodeData(self):
        if self.getCurrentNodeEditorWidget().hasSelectedItem():
            return self.getCurrentNodeEditorWidget().getSelectedItems()[0].content.serialize()

    def storeNodeData(self, data):
        currentSubWnd = self.getCurrentNodeEditorWidget()
        if currentSubWnd.hasSelectedItem():
            # When a new node is selected, stops the TextChanged emit signal when writing node data
            currentSubWnd.blockSignals(True)
            currentSubWnd.getSelectedItems()[0].content.deserialize(data)
            currentSubWnd.blockSignals(False)

    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def onWindowPropertiesToolbar(self):
        if self.propertiesDock.isVisible():
            self.propertiesDock.hide()
        else:
            self.propertiesDock.show()

    def createToolBars(self):
        pass

    def createDocks(self):
        #List of nodes available to user
        self.nodesListWidget = QDMDragListbox()

        self.nodesDock = QDockWidget("Nodes")
        self.nodesDock.setWidget(self.nodesListWidget)
        self.nodesDock.setFloating(False)

        self.propertiesWidgetScroll = QScrollArea()
        self.propertiesWidgetScroll.setWidgetResizable(True)
        self.propertiesWidget = PropertiesBox()
        self.propertiesWidget.nodeDataSignal.connect(self.storeNodeData)

        self.propertiesWidgetScroll.setWidget(self.propertiesWidget)
        self.propertiesDock = QDockWidget("Properties")
        self.propertiesDock.setWidget(self.propertiesWidgetScroll)
        self.propertiesDock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.propertiesDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.nodesDock)

    def createStatusBar(self):
        #self.statusBar().showMessage("Ready")
        pass

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else StackSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        # nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.treeName = self.getNewSubWindowName()
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditorPropertiesBox)
        nodeeditor.scene.history.addHistoryModifiedListener(self.nodeEditorModified.emit)
        nodeeditor.nodeDataModified.connect(self.displayNodeData)
        nodeeditor.updatePropertiesSignal.connect(self.updateEditorPropertiesBox)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def getNewSubWindowName(self):
        name = "New Tree"
        if self.findChildViaTreeName(name) is None:
            return name
        
        i = 1
        while True:
            name = "New Tree - " + str(i)
            if self.findChildViaTreeName(name) is None:
                return name
            i = i+1

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.treeName)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def maybeSave(self):
        if not self.isModified():
            return True

        res = QMessageBox.warning(self, "About to lose your work?",
        "Are you sure you want to discard this tree?\nThis action cannot be undone!",
                QMessageBox.Discard | QMessageBox.Cancel
              )

        if res == QMessageBox.Cancel:
            return False

        return True

    def setSubWndModifiedFalse(self):
        for window in self.mdiArea.subWindowList():
            window.widget().scene.has_been_modified = False
            window.widget().setTitle()

    def closeAllSubWnd(self):
        for window in self.mdiArea.subWindowList():
            window.close()

    def findMdiChild(self, treeName):
        for window in self.mdiArea.subWindowList():
            if window.widget().treeName == treeName:
                return window
        return None

    def findChildViaTreeName(self, name):
        for window in self.mdiArea.subWindowList():
            if window.widget().treeName == name:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def serialize(self):
        subWndList = []
        for window in self.mdiArea.subWindowList():
            subWndList.append(window.widget().serialize())
        return subWndList

    def deserialize(self, data, hashmap=[]):
        for subWndData in data:
            subwindow = self.createMdiChild()
            subwindow.showMaximized()
            subwindow.widget().deserialize(subWndData)
            subwindow.widget().scene.history.clear()
            subwindow.widget().has_been_modified = False

    def exportSerialize(self):
        export = []
        for window in self.mdiArea.subWindowList():
            export.append(window.widget().exportSerialize())
        return export