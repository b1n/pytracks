# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wpg_config_exe.ui'
#
# Created: Tue Jan 26 00:48:04 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_WPagConfigExe(object):
    def setupUi(self, WPagConfigExe):
        WPagConfigExe.setObjectName(_fromUtf8("WPagConfigExe"))
        WPagConfigExe.resize(718, 571)
        self.gridLayout = QtGui.QGridLayout(WPagConfigExe)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frmID = QtGui.QFrame(WPagConfigExe)
        self.frmID.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmID.setFrameShadow(QtGui.QFrame.Raised)
        self.frmID.setLineWidth(1)
        self.frmID.setObjectName(_fromUtf8("frmID"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frmID)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lblID = QtGui.QLabel(self.frmID)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblID.sizePolicy().hasHeightForWidth())
        self.lblID.setSizePolicy(sizePolicy)
        self.lblID.setObjectName(_fromUtf8("lblID"))
        self.gridLayout_4.addWidget(self.lblID, 0, 0, 1, 1)
        self.txtExeID = QtGui.QLabel(self.frmID)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.txtExeID.setFont(font)
        self.txtExeID.setObjectName(_fromUtf8("txtExeID"))
        self.gridLayout_4.addWidget(self.txtExeID, 0, 1, 1, 1)
        self.lblDesc = QtGui.QLabel(self.frmID)
        self.lblDesc.setObjectName(_fromUtf8("lblDesc"))
        self.gridLayout_4.addWidget(self.lblDesc, 1, 0, 1, 1)
        self.txtExeDesc = QtGui.QLabel(self.frmID)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.txtExeDesc.setFont(font)
        self.txtExeDesc.setObjectName(_fromUtf8("txtExeDesc"))
        self.gridLayout_4.addWidget(self.txtExeDesc, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.frmID, 1, 1, 1, 1)
        self.lblImg = QtGui.QLabel(WPagConfigExe)
        self.lblImg.setMinimumSize(QtCore.QSize(0, 0))
        self.lblImg.setMaximumSize(QtCore.QSize(240, 16777215))
        self.lblImg.setText(_fromUtf8(""))
        self.lblImg.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/wpgConfigExe.jpg")))
        self.lblImg.setScaledContents(True)
        self.lblImg.setObjectName(_fromUtf8("lblImg"))
        self.gridLayout.addWidget(self.lblImg, 0, 0, 4, 1)
        self.txtTitle = QtGui.QLabel(WPagConfigExe)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.txtTitle.setFont(font)
        self.txtTitle.setStyleSheet(_fromUtf8("color:rgb(0, 0, 255);\n"
"font: 26pt \"Sans Serif\";\n"
""))
        self.txtTitle.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.txtTitle.setScaledContents(False)
        self.txtTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.txtTitle.setObjectName(_fromUtf8("txtTitle"))
        self.gridLayout.addWidget(self.txtTitle, 0, 1, 1, 1)
        self.qtwExeTab = QtGui.QTableWidget(WPagConfigExe)
        self.qtwExeTab.setObjectName(_fromUtf8("qtwExeTab"))
        self.qtwExeTab.setColumnCount(0)
        self.qtwExeTab.setRowCount(0)
        self.gridLayout.addWidget(self.qtwExeTab, 2, 1, 1, 1)

        self.retranslateUi(WPagConfigExe)
        QtCore.QMetaObject.connectSlotsByName(WPagConfigExe)

    def retranslateUi(self, WPagConfigExe):
        WPagConfigExe.setWindowTitle(_translate("WPagConfigExe", "Form", None))
        self.lblID.setText(_translate("WPagConfigExe", "Exercício:", None))
        self.txtExeID.setText(_translate("WPagConfigExe", "SBRJ001", None))
        self.lblDesc.setText(_translate("WPagConfigExe", "Descrição:", None))
        self.txtExeDesc.setText(_translate("WPagConfigExe", "exercício teste", None))
        self.txtTitle.setText(_translate("WPagConfigExe", "Escolha do Exercício", None))

import qrc_resources_rc
