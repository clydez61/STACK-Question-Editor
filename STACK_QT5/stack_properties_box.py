from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.sip import dump

from stack_conf import *

from nodeeditor.utils import dumpException

from math import ceil

class PropertiesBox(QStackedWidget):
    treeDataSignal = pyqtSignal(dict)
    nodeDataSignal = pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        noSubWindowLayout = QVBoxLayout()
        noSubWindowLayout.setAlignment(Qt.AlignTop)
        noneSelectedLayout = QVBoxLayout()
        nodeSelectedLayout = QVBoxLayout()

        noSubWindowText = QLabel("A potential response tree has not been selected yet!")
        noSubWindowText.setWordWrap(True)
        noSubWindowLayout.addWidget(noSubWindowText)

        noneSelectedLayout.addWidget(QLabel("Potential Repsone Tree Mark:"))
        self.PRTValue = QLineEdit()
        self.PRTValue.textChanged.connect(self.transmitTreeData)
        noneSelectedLayout.addWidget(self.PRTValue)
        noneSelectedLayout.addWidget(QLabel("Feedback Variables:"))
        self.feedbackVar = QTextEdit()
        self.feedbackVar.textChanged.connect(self.transmitTreeData)
        self.feedbackVar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.feedbackVar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.feedbackVar.document().documentLayout().documentSizeChanged.connect(self.wrapHeightToContents)
        noneSelectedLayout.addWidget(self.feedbackVar)

        nodeSelectedLayout.addWidget(QLabel("Student Answer:"))
        self.sans = QLineEdit("", self)
        self.sans.textChanged.connect(self.transmitNodeData)
        nodeSelectedLayout.addWidget(self.sans)
        nodeSelectedLayout.addWidget(QLabel("Teacher Answer:", self))
        self.tans = QLineEdit("", self)
        self.tans.textChanged.connect(self.transmitNodeData)
        nodeSelectedLayout.addWidget(self.tans)
        nodeSelectedLayout.addWidget(QLabel("Test Options:", self))
        self.testType = QComboBox(self)
        self.testType.addItems(['', 'AlgEquiv', 'CasEqual', 'CompletedSquare', 'Diff', 'EqualComAss', 'EquivFirst', 'EquivReasoning', 'Expanded', 'FacForm', 'Int', 'GT', 'GTE', 'NumAbsolute', 'NumDecPlaces', 'NumDecPlacesWrong', 'NumRelative', 'NumSigFigs', 'RegExp', 'SameType', 'Sets', 'SigFigsStrict', 'SingleFrac', 'String', 'StirngSloppy', 'SubstEquiv', 'SysEquiv', 'UnitsAbsolute', 'UnitsRelative', 'Units', 'UnitsStrictAbsolute', 'UnitsStrictRelative', 'UnitsStrictSigFig'])
        self.testType.currentIndexChanged.connect(self.transmitNodeData)
        nodeSelectedLayout.addWidget(self.testType)
        nodeSelectedLayout.addWidget(QLabel("Test Option Parameters:", self))
        self.testOption = QLineEdit("", self)
        self.testOption.textChanged.connect(self.transmitNodeData)
        nodeSelectedLayout.addWidget(self.testOption)
        nodeSelectedLayout.addWidget(QLabel("True (Score):", self))
        self.scoreTrue = QLineEdit("", self)
        self.scoreTrue.textChanged.connect(self.transmitNodeData)
        nodeSelectedLayout.addWidget(self.scoreTrue)
        nodeSelectedLayout.addWidget(QLabel("False (Penalty):", self))
        self.scoreFalse = QLineEdit("", self)
        self.scoreFalse.textChanged.connect(self.transmitNodeData)
        nodeSelectedLayout.addWidget(self.scoreFalse)
        nodeSelectedLayout.addWidget(QLabel("Feedback when True:", self))
        self.trueFeedback = QTextEdit()
        self.trueFeedback.textChanged.connect(self.transmitNodeData)
        self.trueFeedback.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.trueFeedback.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.trueFeedback.document().documentLayout().documentSizeChanged.connect(self.wrapHeightToContents)
        nodeSelectedLayout.addWidget(self.trueFeedback)
        self.feedbackFalseLabel = QLabel("Feedback when False:", self)
        nodeSelectedLayout.addWidget(self.feedbackFalseLabel)
        self.falseFeedback = QTextEdit()
        self.falseFeedback.textChanged.connect(self.transmitNodeData)
        self.falseFeedback.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.falseFeedback.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.falseFeedback.document().documentLayout().documentSizeChanged.connect(self.wrapHeightToContents)
        nodeSelectedLayout.addWidget(self.falseFeedback)

        self.noSubWindowWidget = QWidget()
        self.noSubWindowWidget.setLayout(noSubWindowLayout)
        self.noneSelectedWidget = QWidget()
        self.noneSelectedWidget.setLayout(noneSelectedLayout)
        self.nodeSelectedWidget = QWidget()
        self.nodeSelectedWidget.setLayout(nodeSelectedLayout)

        self.addWidget(self.noSubWindowWidget)
        self.addWidget(self.noneSelectedWidget)
        self.addWidget(self.nodeSelectedWidget)

        self.originalFeedbackHeight = self.trueFeedback.document().size().height()

    def wrapHeightToContents(self):
        pass
        fm = QFontMetrics(self.trueFeedback.currentFont())

        docTrueHeightGrow = self.trueFeedback.document().size().height()
        docFalseHeightGrow = self.falseFeedback.document().size().height()
        docFeedbackVarHeightGrow = self.feedbackVar.document().size().height()

        self.trueFeedback.setMinimumHeight(docTrueHeightGrow)
        self.falseFeedback.setMinimumHeight(docFalseHeightGrow)
        self.feedbackVar.setMinimumHeight(docFeedbackVarHeightGrow)

    def transmitTreeData(self):
        transmit = {}
        transmit['PRTValue'] = self.PRTValue.text()
        transmit['feedbackVar'] = self.feedbackVar.toPlainText()
        self.treeDataSignal.emit(transmit)

    def displayTreeData(self, data):
        self.PRTValue.setText(data['PRTValue'])
        self.feedbackVar.setPlainText(data['feedbackVar'])

    def displayNodeData(self, data):
        self.sans.setText(data['sans'])
        self.tans.setText(data['tans'])
        self.testType.setCurrentIndex(self.testType.findText(data['testType']))
        self.testOption.setText(data['testOption'])
        self.scoreTrue.setText(data['scoreTrue'])
        self.scoreFalse.setText(data['scoreFalse'])
        self.trueFeedback.setPlainText(data['trueFeedback'])
        self.falseFeedback.setPlainText(data['falseFeedback'])

    def transmitNodeData(self):
        transmit = {}
        transmit['sans'] = self.sans.text()
        transmit['tans'] = self.tans.text()
        transmit['testType'] = self.testType.currentText()
        transmit['testOption'] = self.testOption.text()
        transmit['modTrue'] = '+'
        transmit['scoreTrue'] = self.scoreTrue.text()
        transmit['penaltyTrue'] = ''
        transmit['modFalse'] = '-'
        transmit['scoreFalse'] = self.scoreFalse.text()
        transmit['penaltyFalse'] = ''
        transmit['trueFeedback'] = self.trueFeedback.toPlainText()
        transmit['falseFeedback'] = self.falseFeedback.toPlainText()
        self.nodeDataSignal.emit(transmit)

    def setNoSubWindowLayout(self):
        self.setCurrentWidget(self.noSubWindowWidget)

    def setNoneSelectedLayout(self):
        self.setCurrentWidget(self.noneSelectedWidget)

    def setNodeSelectedLayout(self):
        self.setCurrentWidget(self.nodeSelectedWidget)


