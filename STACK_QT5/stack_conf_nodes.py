import os
from PyQt5.QtCore import *
from nodeeditor.utils import dumpException
from stack_conf import *
from stack_node_base import *

@register_node(OP_NODE_PRT_NODE)
class StackNode_PRT_Node(StackNode):
    icon = os.path.join(os.path.dirname(__file__),"icons/in.png")
    op_code = OP_NODE_PRT_NODE
    op_title = "PRT Node"
    content_label_objname = "stack_node_in/out"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[1,4])

    def initInnerClasses(self):
        self.content = StackInputContent(self)
        self.grNode = PrtGraphicsNode(self)

class PrtGraphicsNode(StackGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 200
        self.edge_size = 5
        self._padding = 5

class StackInputContent(StackContent):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.SansLabel = QLabel("Student Answer:", self)
        self.layout.addWidget(self.SansLabel)
        self.Sans = QLineEdit("test1", self)
        self.layout.addWidget(self.Sans)
        self.TansLabel = QLabel("Teacher Answer:", self)
        self.layout.addWidget(self.TansLabel)
        self.Tans = QLineEdit("test2", self)
        self.layout.addWidget(self.Tans)

    def serialize(self):
        res = super().serialize()
        res['Sans'] = self.Sans.text()
        res['Tans'] = self.Tans.text()

        return res

    def deserialize(self, data, hashmap=[]):
        res = super().deserialize(data, hashmap)
        try:
            valueSans = data['Sans']
            self.Sans.setText(valueSans)
            valueTans = data['Tans']
            self.Tans.setText(valueTans)
            return True & res
        except Exception as e:
            dumpException(e)

        return res

class StackOutputContent(StackContent):
    def initUI(self):
        self.lbl = QLabel("42", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)

# way how to register by function call
# register_node_now(OP_NODE_PRT_NODE, StackNode_PRT_Node)