from PyQt5.QtWidgets import *
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode

class StackGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_size = 5
        self._padding = 5

class StackContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label,self)
        lbl.setObjectName(self.node.content_label_objname)

class StackNode(Node):
    irom = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "stack_node_bg"

    def __init__(self, scene, inputs=[2,2], outputs=[1]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

    def initInnerClasses(self):
        self.content = StackContent(self)
        self.qtNode = StackGraphicsNode(self)