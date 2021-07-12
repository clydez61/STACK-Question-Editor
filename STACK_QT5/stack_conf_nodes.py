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
        self.height = 230
        self.edge_size = 5
        self._padding = 5

class StackInputContent(StackContent):
    nodeDataModified = pyqtSignal(dict)
    def initUI(self):
        self.dataSans = ''
        self.dataTans = ''
        self.dataTestType = ''
        self.dataTestOption = ''
        self.dataModTrue = '+'
        self.dataScoreTrue = ''
        self.dataPenaltyTrue = ''
        self.dataModFalse = '-'
        self.dataScoreFalse = ''
        self.dataPenaltyFalse = ''
        self.dataTrueFeedback = ''
        self.dataFalseFeedback = ''

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("Student Answer:", self))
        self.sans = QLineEdit("", self)
        self.sans.textChanged.connect(self.updateDataAndPropertiesWidget)
        self.layout.addWidget(self.sans)
        self.layout.addWidget(QLabel("Teacher Answer:", self))
        self.tans = QLineEdit("", self)
        self.tans.textChanged.connect(self.updateDataAndPropertiesWidget)
        self.layout.addWidget(self.tans)
        self.layout.addWidget(QLabel("Test Options:", self))
        self.testType = QComboBox(self)
        self.testType.addItems(['', 'AlgEquiv', 'CasEqual', 'CompletedSquare', 'Diff', 'EqualComAss', 'EquivFirst', 'EquivReasoning', 'Expanded', 'FacForm', 'Int', 'GT', 'GTE', 'NumAbsolute', 'NumDecPlaces', 'NumDecPlacesWrong', 'NumRelative', 'NumSigFigs', 'RegExp', 'SameType', 'Sets', 'SigFigsStrict', 'SingleFrac', 'String', 'StirngSloppy', 'SubstEquiv', 'SysEquiv', 'UnitsAbsolute', 'UnitsRelative', 'Units', 'UnitsStrictAbsolute', 'UnitsStrictRelative', 'UnitsStrictSigFig'])
        self.testType.currentIndexChanged.connect(self.updateDataAndPropertiesWidget)
        self.layout.addWidget(self.testType)
        self.layout.addWidget(QLabel("Test Option Parameters:", self))
        self.testOption = QLineEdit("", self)
        self.testOption.textChanged.connect(self.updateDataAndPropertiesWidget)
        self.layout.addWidget(self.testOption)

    def updateDataAndPropertiesWidget(self):
        self.dataSans = self.sans.text()
        self.dataTans = self.tans.text()
        self.dataTestType = self.testType.currentText()
        self.dataTestOption = self.testOption.text()

        self.updatePropertiesWidget()

    def updatePropertiesWidget(self):
        data = self.serialize()
        
        self.nodeDataModified.emit(data)

    def serialize(self):
        res = super().serialize()
        res['sans'] = self.dataSans
        res['tans'] = self.dataTans
        res['answertest'] = self.dataTestType
        res['testoptions'] = self.dataTestOption
        res['truescoremode'] = self.dataModTrue
        res['truescore'] = self.dataScoreTrue
        res['truepenalty'] = self.dataPenaltyTrue
        res['falsescoremode'] = self.dataModFalse
        res['falsescore'] = self.dataScoreFalse
        res['falsepenalty'] = self.dataPenaltyFalse
        res['truefeedback'] = self.dataTrueFeedback
        res['falsefeedback'] = self.dataFalseFeedback

        return res

    def deserialize(self, data, hashmap=[]):
        res = super().deserialize(data, hashmap)
        try:
            self.dataSans = data['sans']
            self.sans.setText(self.dataSans)
            self.dataTans = data['tans']
            self.tans.setText(self.dataTans)
            self.dataTestType = data['answertest']
            self.testType.setCurrentIndex(self.testType.findText(self.dataTestType))
            self.dataTestOption = data['testoptions']
            self.testOption.setText(self.dataTestOption)
            self.dataModTrue = data['truescoremode']
            self.dataScoreTrue = data['truescore']
            self.dataPenaltyTrue = data['truepenalty']
            self.dataModFalse = data['falsescoremode']
            self.dataScoreFalse = data['falsescore']
            self.dataPenaltyFalse = data['falsepenalty']
            self.dataTrueFeedback = data['truefeedback']
            self.dataFalseFeedback = data['falsefeedback']
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