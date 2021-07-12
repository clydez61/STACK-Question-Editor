from typing import ByteString
from collections import OrderedDict
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from nodeeditor.node_editor_widget import NodeEditorWidget
from nodeeditor.utils import dumpException
from nodeeditor.node_edge import EDGE_TYPE_DIRECT, EDGE_TYPE_BEZIER
from stack_conf import *
from stack_node_base import *

DEBUG = False
DEBUG_CONTEXT = False

class StackSubWindow(NodeEditorWidget):
    nodeDataModified = pyqtSignal(dict)
    updatePropertiesSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.initNewNodeActions()

        self.initData()

        self.setTitle()

        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)
        self.scene.setNodeClassSelector(self.getNodeClassFromData)

        self._close_event_listeners = []

    def initData(self):
        self._treeName = ''
        self.PRTValue = ''
        self.feedbackVar = ''

    def getNodeClassFromData(self, data):
        if 'op_code' not in data: return Node
        return get_class_from_opcode(data['op_code'])

    def initNewNodeActions(self):
        self.node_actions = {}
        keys = list(STACK_NODES.keys())
        keys.sort()
        for key in keys:
            node = STACK_NODES[key]
            self.node_actions[node.op_code] = QAction(QIcon(node.icon), node.op_title)
            self.node_actions[node.op_code].setData(node.op_code)

    def initNodesContextMenu(self):
        context_menu = QMenu(self)
        keys = list(STACK_NODES.keys())
        keys.sort()
        for key in keys: context_menu.addAction(self.node_actions[key])
        return context_menu

    def setTitle(self):
        name = self.treeName
        name = name + ("*" if self.isModified() else "")
        self.setWindowTitle(name)

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onDragEnter(self, event):
            if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
                event.acceptProposedAction()
            else:
                #print("... denied drag enter event")
                event.setAccepted(False)

    def onDrop(self, event):
            if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
                eventData = event.mimeData().data(LISTBOX_MIMETYPE)
                dataStream = QDataStream(eventData, QIODevice.ReadOnly)
                pixmap = QPixmap()
                dataStream >> pixmap
                op_code = dataStream.readInt()
                text = dataStream.readQString()
                
                mouse_position = event.pos()
                scene_position = self.scene.grScene.views()[0].mapToScene(mouse_position)

                if DEBUG: print("GOT DROP: (%d) '%s'" % (op_code, text), "mouse:", mouse_position, "scene:", scene_position)

                try:
                    node = get_class_from_opcode(op_code)(self.scene)
                    node.setPos(scene_position.x(), scene_position.y())
                    node.content.nodeDataModified.connect(self.nodeDataModified.emit)
                    self.scene.history.storeHistory("Created node %s" % node.__class__.__name__)
                except Exception as e: dumpException(e)

                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                print("... drop ignored, not requested format '%s'" % LISTBOX_MIMETYPE)
                event.ignore()

    def mouseReleaseEvent(self, event):
        self.updatePropertiesSignal.emit()
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        try:
            item = self.scene.getItemAt(event.pos())
            if DEBUG_CONTEXT: print(item)

            if type(item) == QGraphicsProxyWidget:
                item = item.widget()

            if hasattr(item, 'node') or hasattr(item, 'socket'):
                self.handleNodeContextMenu(event)
            elif hasattr(item, 'edge'):
                self.handleEdgeContextMenu(event)
            #elif item is None:
            else:
                self.handleNewNodeContextMenu(event)

            return super().contextMenuEvent(event)
        except Exception as e: dumpException(e)

    def handleNodeContextMenu(self, event):
        if DEBUG_CONTEXT: print("CONTEXT: NODE")
        context_menu = QMenu(self)
        markDirtyAct = context_menu.addAction("Mark Dirty")
        markDirtyDescendantsAct = context_menu.addAction("Mark Descendants Dirty")
        markInvalidAct = context_menu.addAction("Mark Invalid")
        unmarkInvalidAct = context_menu.addAction("Unmark Invalid")
        evalAct = context_menu.addAction("Eval")
        action = context_menu.exec(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if type(item) == QGraphicsProxyWidget:
            item = item.widget()

        if hasattr(item, 'node'):
            selected = item.node
        if hasattr(item, 'socket'):
            selected = item.socket.node

        if DEBUG_CONTEXT: print("got item:", selected)
        if selected and action == markDirtyAct: selected.markDirty()
        if selected and action == markDirtyDescendantsAct: selected.markDescendantsDirty()
        if selected and action == markInvalidAct: selected.markInvalid()
        if selected and action == unmarkInvalidAct: selected.markInvalid(False)
        if selected and action == evalAct:
            val = selected.eval()
            if DEBUG_CONTEXT: print("EVALUATED:", val)
    
    def handleEdgeContextMenu(self, event):
        if DEBUG_CONTEXT: print("CONTEXT: EDGE")
        context_menu = QMenu(self)
        bezierAct = context_menu.addAction("Bezier Edge")
        directAct = context_menu.addAction("Direct Edge")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if hasattr(item, 'edge'):
            selected = item.edge

        if selected and action == bezierAct: selected.edge_type = EDGE_TYPE_BEZIER
        if selected and action == directAct: selected.edge_type = EDGE_TYPE_DIRECT
    
    def handleNewNodeContextMenu(self, event):
        if DEBUG_CONTEXT: print("CONTEXT: EMPTY SPACE")
        context_menu = self.initNodesContextMenu()
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action is not None:
            new_stack_node = get_class_from_opcode(action.data())(self.scene)
            scene_pos = self.scene.getView().mapToScene(event.pos())
            new_stack_node.setPos(scene_pos.x(), scene_pos.y())
            print("Selected node:", new_stack_node)

    def hasSelectedItem(self):
        """Is there only one thing selected in the :class:`nodeeditor.node_scene.Scene`?

        :return: ``True`` if there is only one thing selected in the `Scene`
        :rtype: ``bool``
        """
        return len(self.getSelectedItems()) == 1

    def treeSerialize(self):
        res = OrderedDict()
        res['name'] = self.treeName
        res['value'] = self.PRTValue
        res['feedbackvariables'] = self.feedbackVar
        return res

    def treeDeserialize(self, data):
        self.treeName = data['name']
        self.PRTValue = data['value']
        self.feedbackVar = data['feedbackvariables']

    @property
    def treeName(self):
        return self._treeName

    @treeName.setter
    def treeName(self, name):
        self._treeName = name
        self.setTitle()


    def serialize(self):
        nodeData = self.scene.serialize()
        treeData = self.treeSerialize()
        return OrderedDict([
            ('nodeData', nodeData),
            ('treeData', treeData),
        ])

    def deserialize(self, data):
        self.treeDeserialize(data['treeData'])
        self.scene.deserialize(data['nodeData'])

    def exportSerialize(self):
        export = OrderedDict()
        nodes = []
        nodeData = self.scene.serialize()
        treeData = self.treeSerialize()

        export.update(treeData)

        i = 0
        nodeIDMap = {}
        nodeInputMap = {}
        nodeTrueMap = {}
        nodeFalseMap = {}
        for node in nodeData['nodes']:
            nodeIDMap[node['id']] = i

            for inputSocket in node['inputs']:
                if inputSocket['socket_type'] == 2:
                    nodeInputMap[inputSocket['id']] = i

            for outputSocket in node['outputs']:
                if outputSocket['socket_type'] == 1:
                    nodeTrueMap[i] = outputSocket['id']

                if outputSocket['socket_type'] == 4:
                    nodeFalseMap[i] = outputSocket['id']

            i = i+1

        for node in nodeData['nodes']:
            nodeContent = node['content']
            nodeContent['truenextnode'] = -1
            nodeContent['falsenextnode'] = -1
            nodeContent['name'] = nodeIDMap[node['id']]

            for edge in nodeData['edges']:
                if nodeTrueMap[nodeContent['name']] == edge['start']:
                    nodeContent['truenextnode'] = nodeInputMap[edge['end']]

                elif nodeFalseMap[nodeContent['name']] == edge['start']:
                    nodeContent['falsenextnode'] = nodeInputMap[edge['end']]

            nodes.append(nodeContent)

        export['node'] = nodes

        return export