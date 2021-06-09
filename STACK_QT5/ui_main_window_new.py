# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_newfrjFCK.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

import local_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1071, 674)
        MainWindow.setStyleSheet(u"QMenu::item{background: rgb(51, 51, 51)}QMenu::item:selected{background:#616161}\n"
"QFrame{}")
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.Canada))
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName(u"actionSave_as")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionCut = QAction(MainWindow)
        self.actionCut.setObjectName(u"actionCut")
        self.actionCopy = QAction(MainWindow)
        self.actionCopy.setObjectName(u"actionCopy")
        self.actionPaste = QAction(MainWindow)
        self.actionPaste.setObjectName(u"actionPaste")
        self.actionDelete = QAction(MainWindow)
        self.actionDelete.setObjectName(u"actionDelete")
        self.actionNew_Tree = QAction(MainWindow)
        self.actionNew_Tree.setObjectName(u"actionNew_Tree")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color: rgb(25, 25, 25);")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_header = QFrame(self.centralwidget)
        self.main_header.setObjectName(u"main_header")
        self.main_header.setMaximumSize(QSize(16777215, 50))
        self.main_header.setStyleSheet(u"QFrame{\n"
"	border-bottom: 1px solid #000;\n"
"	\n"
"	background-color: rgb(0, 0, 0);\n"
"}")
        self.main_header.setFrameShape(QFrame.WinPanel)
        self.main_header.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.main_header)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tittle_bar_container = QFrame(self.main_header)
        self.tittle_bar_container.setObjectName(u"tittle_bar_container")
        self.tittle_bar_container.setFrameShape(QFrame.StyledPanel)
        self.tittle_bar_container.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.tittle_bar_container)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.left_menu_toggle = QFrame(self.tittle_bar_container)
        self.left_menu_toggle.setObjectName(u"left_menu_toggle")
        self.left_menu_toggle.setMinimumSize(QSize(50, 0))
        self.left_menu_toggle.setMaximumSize(QSize(50, 16777215))
        self.left_menu_toggle.setStyleSheet(u"QFrame{\n"
"	background-color: #000;\n"
"}\n"
"QPushButton{\n"
"	padding: 5px 10px;\n"
"	border: none;\n"
"	border-radius: 5px;\n"
"	background-color: #000;\n"
"	color: #fff;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(0, 92, 157);\n"
"}")
        self.left_menu_toggle.setFrameShape(QFrame.StyledPanel)
        self.left_menu_toggle.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.left_menu_toggle)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.left_menu_toggle_btn = QPushButton(self.left_menu_toggle)
        self.left_menu_toggle_btn.setObjectName(u"left_menu_toggle_btn")
        self.left_menu_toggle_btn.setMinimumSize(QSize(0, 50))
        self.left_menu_toggle_btn.setMaximumSize(QSize(50, 16777215))
        self.left_menu_toggle_btn.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/icons/cil-menu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.left_menu_toggle_btn.setIcon(icon)
        self.left_menu_toggle_btn.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.left_menu_toggle_btn)


        self.horizontalLayout_5.addWidget(self.left_menu_toggle)

        self.tittle_bar = QFrame(self.tittle_bar_container)
        self.tittle_bar.setObjectName(u"tittle_bar")
        self.tittle_bar.setStyleSheet(u"QLabel{\n"
"	color: #fff;\n"
"}")
        self.tittle_bar.setFrameShape(QFrame.StyledPanel)
        self.tittle_bar.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.tittle_bar)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.title_label = QLabel(self.tittle_bar)
        self.title_label.setObjectName(u"title_label")
        font = QFont()
        font.setFamily(u"MS Sans Serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(u"font: 14pt \"MS Sans Serif\";")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.title_label)


        self.horizontalLayout_5.addWidget(self.tittle_bar)


        self.horizontalLayout_2.addWidget(self.tittle_bar_container)


        self.verticalLayout.addWidget(self.main_header)

        self.main_body = QFrame(self.centralwidget)
        self.main_body.setObjectName(u"main_body")
        self.main_body.setStyleSheet(u"")
        self.main_body.setFrameShape(QFrame.StyledPanel)
        self.main_body.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.main_body)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.left_side_menu = QFrame(self.main_body)
        self.left_side_menu.setObjectName(u"left_side_menu")
        self.left_side_menu.setMaximumSize(QSize(50, 16777215))
        self.left_side_menu.setStyleSheet(u"QFrame{\n"
"	background-color: #000;\n"
"}\n"
"QPushButton{\n"
"	padding: 20px 10px;\n"
"	border: none;\n"
"	border-radius: 10px;\n"
"	background-color: #000;\n"
"	color: #fff;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(0, 92, 157);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color:  rgb(0, 92, 157);\n"
"	border-bottom: 2px solid rgb(255, 165, 24);\n"
"}")
        self.left_side_menu.setFrameShape(QFrame.NoFrame)
        self.left_side_menu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.left_side_menu)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(7, 0, 0, 0)
        self.left_menu_top_buttons = QFrame(self.left_side_menu)
        self.left_menu_top_buttons.setObjectName(u"left_menu_top_buttons")
        self.left_menu_top_buttons.setStyleSheet(u"font: 75 9pt \"MS Sans Serif\";")
        self.left_menu_top_buttons.setFrameShape(QFrame.StyledPanel)
        self.left_menu_top_buttons.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.left_menu_top_buttons)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(0)
        self.formLayout.setVerticalSpacing(0)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.qedit_btn = QPushButton(self.left_menu_top_buttons)
        self.qedit_btn.setObjectName(u"qedit_btn")
        self.qedit_btn.setMinimumSize(QSize(100, 0))
        self.qedit_btn.setStyleSheet(u"background-image: url(:/icons/icons/cil-airplay.png);\n"
"background-repeat: none;\n"
"padding-left: 50px;\n"
"background-position: center left;")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.qedit_btn)

        self.feedback_btn = QPushButton(self.left_menu_top_buttons)
        self.feedback_btn.setObjectName(u"feedback_btn")
        self.feedback_btn.setMinimumSize(QSize(100, 0))
        self.feedback_btn.setStyleSheet(u"background-image: url(:/icons/icons/cil-speech.png);\n"
"background-repeat: none;\n"
"padding-left: 50px;\n"
"background-position: center left;\n"
"")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.feedback_btn)

        self.attributes_btn = QPushButton(self.left_menu_top_buttons)
        self.attributes_btn.setObjectName(u"attributes_btn")
        self.attributes_btn.setMinimumSize(QSize(100, 0))
        self.attributes_btn.setStyleSheet(u"background-image: url(:/icons/icons/cil-equalizer.png);\n"
"background-repeat: none;\n"
"padding-left: 50px;\n"
"background-position: center left;")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.attributes_btn)

        self.input_btn = QPushButton(self.left_menu_top_buttons)
        self.input_btn.setObjectName(u"input_btn")
        self.input_btn.setMinimumSize(QSize(100, 0))
        self.input_btn.setMaximumSize(QSize(16777215, 16777215))
        self.input_btn.setStyleSheet(u"background-image: url(:/icons/icons/cil-input.png);\n"
"background-repeat: none;\n"
"padding-left: 50px;\n"
"background-position: center left;")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.input_btn)

        self.tree_btn = QPushButton(self.left_menu_top_buttons)
        self.tree_btn.setObjectName(u"tree_btn")
        self.tree_btn.setMinimumSize(QSize(100, 0))
        self.tree_btn.setMaximumSize(QSize(100, 16777215))
        self.tree_btn.setStyleSheet(u"background-image: url(:/icons/icons/cil-view-quilt.png);\n"
"background-repeat: none;\n"
"padding-left: 50px;\n"
"background-position: center left;")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.tree_btn)


        self.verticalLayout_3.addWidget(self.left_menu_top_buttons)


        self.horizontalLayout.addWidget(self.left_side_menu)

        self.center_main_items = QFrame(self.main_body)
        self.center_main_items.setObjectName(u"center_main_items")
        self.center_main_items.setStyleSheet(u"")
        self.center_main_items.setFrameShape(QFrame.StyledPanel)
        self.center_main_items.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.center_main_items)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.center_main_items)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"font: 14pt \"MS Sans Serif\";\n"
"color: rgb(255, 255, 222);\n"
"\n"
"QTextEdit{\n"
"color: rgb(255, 255, 222);\n"
"background-color: rgb(51, 51, 51);\n"
"}\n"
"")
        self.qedit_page = QWidget()
        self.qedit_page.setObjectName(u"qedit_page")
        self.qedit_page.setStyleSheet(u"QTextEdit{\n"
"color: rgb(255, 255, 222);\n"
"background-color: rgb(51, 51, 51);\n"
"}")
        self.gridLayout = QGridLayout(self.qedit_page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.qvar_label = QLabel(self.qedit_page)
        self.qvar_label.setObjectName(u"qvar_label")
        self.qvar_label.setMaximumSize(QSize(400, 200))
        self.qvar_label.setStyleSheet(u"color: rgb(255, 255, 222);\n"
"font: 75 14pt \"MS Sans Serif\";")

        self.gridLayout.addWidget(self.qvar_label, 0, 0, 1, 1, Qt.AlignHCenter|Qt.AlignTop)

        self.qtext_label = QLabel(self.qedit_page)
        self.qtext_label.setObjectName(u"qtext_label")
        self.qtext_label.setMaximumSize(QSize(200, 200))
        self.qtext_label.setToolTipDuration(-1)
        self.qtext_label.setLayoutDirection(Qt.LeftToRight)
        self.qtext_label.setStyleSheet(u"color: rgb(255, 255, 222);\n"
"font: 75 14pt \"MS Sans Serif\";")

        self.gridLayout.addWidget(self.qtext_label, 0, 1, 1, 1, Qt.AlignHCenter)

        self.right_side_menu = QFrame(self.qedit_page)
        self.right_side_menu.setObjectName(u"right_side_menu")
        self.right_side_menu.setMaximumSize(QSize(100, 16777215))
        self.right_side_menu.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.right_side_menu.setFrameShape(QFrame.NoFrame)
        self.right_side_menu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.right_side_menu)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.html_btn = QPushButton(self.right_side_menu)
        self.html_btn.setObjectName(u"html_btn")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/cil-code.png", QSize(), QIcon.Normal, QIcon.Off)
        self.html_btn.setIcon(icon1)

        self.verticalLayout_4.addWidget(self.html_btn)


        self.gridLayout.addWidget(self.right_side_menu, 1, 2, 1, 1)

        self.qvar_box = QPlainTextEdit(self.qedit_page)
        self.qvar_box.setObjectName(u"qvar_box")
        self.qvar_box.setStyleSheet(u"background-color: rgb(51, 51, 51);")

        self.gridLayout.addWidget(self.qvar_box, 1, 0, 1, 1)

        self.qtext_box = QTextEdit(self.qedit_page)
        self.qtext_box.setObjectName(u"qtext_box")
        self.qtext_box.setStyleSheet(u"background-color: rgb(51, 51, 51);")

        self.gridLayout.addWidget(self.qtext_box, 1, 1, 1, 1)

        self.stackedWidget.addWidget(self.qedit_page)
        self.feedback_page = QWidget()
        self.feedback_page.setObjectName(u"feedback_page")
        self.feedback_page.setStyleSheet(u"QTextEdit{\n"
"color: rgb(255, 255, 222);\n"
"background-color: rgb(51, 51, 51);\n"
"}")
        self.gridLayout_3 = QGridLayout(self.feedback_page)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.sfeedback_label = QLabel(self.feedback_page)
        self.sfeedback_label.setObjectName(u"sfeedback_label")

        self.gridLayout_3.addWidget(self.sfeedback_label, 0, 1, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.gfeedback_label = QLabel(self.feedback_page)
        self.gfeedback_label.setObjectName(u"gfeedback_label")

        self.gridLayout_3.addWidget(self.gfeedback_label, 0, 0, 1, 1, Qt.AlignHCenter)

        self.gfeedback_box = QTextEdit(self.feedback_page)
        self.gfeedback_box.setObjectName(u"gfeedback_box")

        self.gridLayout_3.addWidget(self.gfeedback_box, 1, 0, 1, 1)

        self.sfeedback_box = QTextEdit(self.feedback_page)
        self.sfeedback_box.setObjectName(u"sfeedback_box")

        self.gridLayout_3.addWidget(self.sfeedback_box, 1, 1, 1, 1)

        self.right_side_menu2 = QFrame(self.feedback_page)
        self.right_side_menu2.setObjectName(u"right_side_menu2")
        self.right_side_menu2.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.right_side_menu2.setFrameShape(QFrame.StyledPanel)
        self.right_side_menu2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.right_side_menu2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.html_btn2 = QPushButton(self.right_side_menu2)
        self.html_btn2.setObjectName(u"html_btn2")
        self.html_btn2.setIcon(icon1)

        self.verticalLayout_5.addWidget(self.html_btn2)


        self.gridLayout_3.addWidget(self.right_side_menu2, 1, 2, 1, 1)

        self.stackedWidget.addWidget(self.feedback_page)
        self.attributes_page = QWidget()
        self.attributes_page.setObjectName(u"attributes_page")
        self.attributes_page.setStyleSheet(u"QTextEdit{\n"
"color: rgb(255, 255, 222);\n"
"background-color: rgb(51, 51, 51);\n"
"}")
        self.gridLayout_4 = QGridLayout(self.attributes_page)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.ID_box = QTextEdit(self.attributes_page)
        self.ID_box.setObjectName(u"ID_box")
        self.ID_box.setMinimumSize(QSize(0, 0))
        self.ID_box.setMaximumSize(QSize(16777215, 30))
        self.ID_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.gridLayout_4.addWidget(self.ID_box, 1, 1, 1, 1)

        self.ID_label = QLabel(self.attributes_page)
        self.ID_label.setObjectName(u"ID_label")

        self.gridLayout_4.addWidget(self.ID_label, 1, 0, 1, 1)

        self.tag_label = QLabel(self.attributes_page)
        self.tag_label.setObjectName(u"tag_label")

        self.gridLayout_4.addWidget(self.tag_label, 3, 0, 1, 1)

        self.grade_box = QTextEdit(self.attributes_page)
        self.grade_box.setObjectName(u"grade_box")
        self.grade_box.setMaximumSize(QSize(16777215, 30))
        self.grade_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.gridLayout_4.addWidget(self.grade_box, 0, 1, 1, 1)

        self.grade_label = QLabel(self.attributes_page)
        self.grade_label.setObjectName(u"grade_label")

        self.gridLayout_4.addWidget(self.grade_label, 0, 0, 1, 1)

        self.qnote_box = QTextEdit(self.attributes_page)
        self.qnote_box.setObjectName(u"qnote_box")

        self.gridLayout_4.addWidget(self.qnote_box, 2, 1, 1, 1)

        self.qnote_label = QLabel(self.attributes_page)
        self.qnote_label.setObjectName(u"qnote_label")

        self.gridLayout_4.addWidget(self.qnote_label, 2, 0, 1, 1)

        self.tag_box = QTextEdit(self.attributes_page)
        self.tag_box.setObjectName(u"tag_box")

        self.gridLayout_4.addWidget(self.tag_box, 3, 1, 1, 1)

        self.stackedWidget.addWidget(self.attributes_page)
        self.inputs_page = QWidget()
        self.inputs_page.setObjectName(u"inputs_page")
        self.verticalLayout_6 = QVBoxLayout(self.inputs_page)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.scrollArea = QScrollArea(self.inputs_page)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.ScrollPage = QWidget()
        self.ScrollPage.setObjectName(u"ScrollPage")
        self.ScrollPage.setGeometry(QRect(0, 0, 997, 515))
        self.ScrollPage.setStyleSheet(u"#input_frame{\n"
"border:2px solid rgb(255,0,0)\n"
"}")
        self.gridLayout_2 = QGridLayout(self.ScrollPage)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.input_frame = QFrame(self.ScrollPage)
        self.input_frame.setObjectName(u"input_frame")
        self.input_frame.setMinimumSize(QSize(100, 100))
        self.input_frame.setMaximumSize(QSize(200, 250))
        self.input_frame.setStyleSheet(u"font: 5pt \"MS Sans Serif\";\n"
"color: rgb(255, 255, 222);\n"
"background-color: rgb(51, 51, 51);\n"
"border-color: rgb(255, 255, 0);\n"
"")
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_frame.setFrameShadow(QFrame.Raised)
        self.label_name = QLabel(self.input_frame)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setGeometry(QRect(11, 11, 37, 16))
        self.label_name.setAlignment(Qt.AlignCenter)
        self.input_name = QTextBrowser(self.input_frame)
        self.input_name.setObjectName(u"input_name")
        self.input_name.setGeometry(QRect(67, 11, 122, 30))
        self.input_name.setMaximumSize(QSize(16777215, 30))
        self.label_type = QLabel(self.input_frame)
        self.label_type.setObjectName(u"label_type")
        self.label_type.setGeometry(QRect(11, 47, 32, 16))
        self.input_type = QComboBox(self.input_frame)
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.addItem("")
        self.input_type.setObjectName(u"input_type")
        self.input_type.setGeometry(QRect(67, 47, 122, 20))
        self.label_ans = QLabel(self.input_frame)
        self.label_ans.setObjectName(u"label_ans")
        self.label_ans.setGeometry(QRect(11, 73, 44, 16))
        self.input_ans = QTextEdit(self.input_frame)
        self.input_ans.setObjectName(u"input_ans")
        self.input_ans.setGeometry(QRect(67, 73, 122, 30))
        self.input_ans.setMaximumSize(QSize(16777215, 30))
        self.label_size = QLabel(self.input_frame)
        self.label_size.setObjectName(u"label_size")
        self.label_size.setGeometry(QRect(11, 109, 50, 16))
        self.input_size = QTextEdit(self.input_frame)
        self.input_size.setObjectName(u"input_size")
        self.input_size.setGeometry(QRect(67, 109, 122, 30))
        self.input_size.setMaximumSize(QSize(16777215, 30))
        self.more_btn = QPushButton(self.input_frame)
        self.more_btn.setObjectName(u"more_btn")
        self.more_btn.setGeometry(QRect(67, 145, 75, 24))

        self.gridLayout_2.addWidget(self.input_frame, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.ScrollPage)

        self.verticalLayout_6.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.inputs_page)
        self.tree_page = QWidget()
        self.tree_page.setObjectName(u"tree_page")
        self.horizontalLayout_6 = QHBoxLayout(self.tree_page)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.NodeEditorLayout = QGridLayout()
        self.NodeEditorLayout.setObjectName(u"NodeEditorLayout")

        self.horizontalLayout_6.addLayout(self.NodeEditorLayout)

        self.stackedWidget.addWidget(self.tree_page)

        self.verticalLayout_2.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.center_main_items)


        self.verticalLayout.addWidget(self.main_body)

        self.main_footer = QFrame(self.centralwidget)
        self.main_footer.setObjectName(u"main_footer")
        self.main_footer.setMinimumSize(QSize(0, 50))
        self.main_footer.setMaximumSize(QSize(16777215, 30))
        self.main_footer.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(0, 0, 0);\n"
"	border-top-color: solid 1px  rgb(0, 0, 0);\n"
"}\n"
"QLabel{\n"
"	color: #fff;\n"
"}")
        self.main_footer.setFrameShape(QFrame.WinPanel)
        self.main_footer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.main_footer)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_7 = QLabel(self.main_footer)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_10.addWidget(self.label_7)


        self.verticalLayout.addWidget(self.main_footer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1071, 23))
        self.menuBar.setStyleSheet(u"background-color: rgb(51, 51, 51);\n"
"color: rgb(255, 255, 222);")
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menuBar)
        self.menuEdit.setObjectName(u"menuEdit")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport)
        self.menuEdit.addAction(self.actionNew_Tree)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionDelete)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_as.setText(QCoreApplication.translate("MainWindow", u"Save as..", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
#if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
#if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionCut.setText(QCoreApplication.translate("MainWindow", u"Cut", None))
#if QT_CONFIG(shortcut)
        self.actionCut.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.actionCopy.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
#if QT_CONFIG(shortcut)
        self.actionCopy.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.actionPaste.setText(QCoreApplication.translate("MainWindow", u"Paste", None))
#if QT_CONFIG(shortcut)
        self.actionPaste.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.actionDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
#if QT_CONFIG(shortcut)
        self.actionDelete.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.actionNew_Tree.setText(QCoreApplication.translate("MainWindow", u"New Tree", None))
        self.left_menu_toggle_btn.setText("")
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"STACK Question Maker", None))
        self.qedit_btn.setText(QCoreApplication.translate("MainWindow", u"Display", None))
        self.feedback_btn.setText(QCoreApplication.translate("MainWindow", u"Feedback ", None))
        self.attributes_btn.setText(QCoreApplication.translate("MainWindow", u"Attributes", None))
        self.input_btn.setText(QCoreApplication.translate("MainWindow", u"Inputs", None))
        self.tree_btn.setText(QCoreApplication.translate("MainWindow", u"Tree", None))
#if QT_CONFIG(tooltip)
        self.qvar_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Maxima code is used to create and randomise the parameters of the question. Any forms of calculations should be done within this section. </p><p>Variables and function names can be a combination of letters followed by a combination of numbers. For exmaple: height1.An example of invalid variable name would be &quot;h2s&quot; where a number is between letters</p><p><span style=\" font-weight:600;\">Syntax rules:</span></p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Values are assigned to variables using a colon (:), for example,<span style=\" font-weight:600;\">aa:4</span></li><li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Custom functions are defined using colon equals (:=), for example, <span style=\" font-weight:600;\">f(x):=x^2</s"
                        "pan> and the function called and stored for example, <span style=\" font-weight:600;\">y: f(2)</span></li><li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Equal sign (=) is used in equations, which could themselves be assigned to a variable, for example, <span style=\" font-weight:600;\">eqn:x^2-4=0</span>;</li></ul></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.qvar_label.setText(QCoreApplication.translate("MainWindow", u"Question Variables", None))
#if QT_CONFIG(tooltip)
        self.qtext_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>This is the text of the question that will be displayed to students.</p><p>Mathematics can be included using LATEX syntax. Use the LATEX delineator \\( . . . \\) for inline maths and \\[ . . . \\] for displayed maths.</p><p>Use {@ . . . @} to include any variable values created in the &quot;Question Variable&quot; section</p><p><span style=\" font-weight:600;\">Sample Question:</span></p><p>---Question variables---</p><p>base : 1+rand(4)</p><p>height : 2+rand(5)</p><p>area: base * height /2</p><p>---Question Text---</p><p>Given a triangle with base = {@base@}, height = {height@}, determine the area. [[input:area_student]]</p><p>Output:</p><p><img src=\":/icons/icons/sampletext.png\"/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.qtext_label.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.qtext_label.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.qtext_label.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.qtext_label.setText(QCoreApplication.translate("MainWindow", u"Question Text", None))
#if QT_CONFIG(statustip)
        self.html_btn.setStatusTip(QCoreApplication.translate("MainWindow", u"we", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.html_btn.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.html_btn.setText("")
        self.qtext_box.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Sans Serif'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.sfeedback_label.setText(QCoreApplication.translate("MainWindow", u"Specific Feedback", None))
#if QT_CONFIG(tooltip)
        self.gfeedback_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>This is the text given to the student once they have used all their permitted attempts at the question, or once they have given a correct answer. It is typically used to give a worked solution to the particular randomised question instance asked.<br/></p><p>This section behaves similarly to the Question text section: LATEX formatting can be included as well as values of any question variables.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.gfeedback_label.setText(QCoreApplication.translate("MainWindow", u"General Feedback", None))
        self.html_btn2.setText("")
#if QT_CONFIG(tooltip)
        self.ID_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>This is a unique identifier which can be given to a question. It is used to identify the question when using outside of a quiz, for example when embedded within other areas of Moodle</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ID_label.setText(QCoreApplication.translate("MainWindow", u"ID Number", None))
#if QT_CONFIG(tooltip)
        self.tag_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>This section of the form allows user-speci ed tags (identi er texts) to be added to a question. Within the Question bank, questions can be searched for by tags. Tags can also be used within a quiz, to allow an included question to be randomly selected from all questions with particular tags.</p><p>Syntax: One line per tag</p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tag_label.setText(QCoreApplication.translate("MainWindow", u"Tags", None))
#if QT_CONFIG(tooltip)
        self.grade_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The overall grade that the entire question (including all potential trees) is worth. Type in any numeric value</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.grade_label.setText(QCoreApplication.translate("MainWindow", u"Grade", None))
#if QT_CONFIG(tooltip)
        self.qnote_label.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Question note is text unique to a particular randomisation of a question, and is used to distinguish between different randomised question instances.</p><p>Type in any text that may help you identify these variables or any other useful information that you would like to be reminded of when editing the question.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.qnote_label.setText(QCoreApplication.translate("MainWindow", u"Question Note", None))
        self.label_name.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.label_type.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.input_type.setItemText(0, QCoreApplication.translate("MainWindow", u"Algebraic Input", None))
        self.input_type.setItemText(1, QCoreApplication.translate("MainWindow", u"Checkbox", None))
        self.input_type.setItemText(2, QCoreApplication.translate("MainWindow", u"Drop down list", None))
        self.input_type.setItemText(3, QCoreApplication.translate("MainWindow", u"Equivalence reasoning", None))
        self.input_type.setItemText(4, QCoreApplication.translate("MainWindow", u"Matrix", None))
        self.input_type.setItemText(5, QCoreApplication.translate("MainWindow", u"Notes", None))
        self.input_type.setItemText(6, QCoreApplication.translate("MainWindow", u"Numerical", None))
        self.input_type.setItemText(7, QCoreApplication.translate("MainWindow", u"Radio", None))
        self.input_type.setItemText(8, QCoreApplication.translate("MainWindow", u"String", None))
        self.input_type.setItemText(9, QCoreApplication.translate("MainWindow", u"Text area", None))
        self.input_type.setItemText(10, QCoreApplication.translate("MainWindow", u"True/False", None))
        self.input_type.setItemText(11, QCoreApplication.translate("MainWindow", u"Units", None))

        self.label_ans.setText(QCoreApplication.translate("MainWindow", u"Answer", None))
        self.label_size.setText(QCoreApplication.translate("MainWindow", u"Box size", None))
        self.more_btn.setText(QCoreApplication.translate("MainWindow", u"More..", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"v 1.0", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

