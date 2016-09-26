# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wpg_config_canal.ui'
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

class Ui_WPagConfigCanal(object):
    def setupUi(self, WPagConfigCanal):
        WPagConfigCanal.setObjectName(_fromUtf8("WPagConfigCanal"))
        WPagConfigCanal.resize(524, 242)
        self.gridLayout = QtGui.QGridLayout(WPagConfigCanal)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblImg = QtGui.QLabel(WPagConfigCanal)
        self.lblImg.setMaximumSize(QtCore.QSize(240, 16777215))
        self.lblImg.setText(_fromUtf8(""))
        self.lblImg.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/wpgCanal.png")))
        self.lblImg.setScaledContents(True)
        self.lblImg.setObjectName(_fromUtf8("lblImg"))
        self.gridLayout.addWidget(self.lblImg, 0, 0, 1, 1)
        self.widCanal = QtGui.QWidget(WPagConfigCanal)
        self.widCanal.setMinimumSize(QtCore.QSize(360, 0))
        self.widCanal.setObjectName(_fromUtf8("widCanal"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widCanal)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblTitle = QtGui.QLabel(self.widCanal)
        self.lblTitle.setStyleSheet(_fromUtf8("color:rgb(0, 0, 255);\n"
"font: 20pt \"Sans Serif\";"))
        self.lblTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblTitle.setObjectName(_fromUtf8("lblTitle"))
        self.verticalLayout.addWidget(self.lblTitle)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.lblCanal = QtGui.QLabel(self.widCanal)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblCanal.setFont(font)
        self.lblCanal.setObjectName(_fromUtf8("lblCanal"))
        self.verticalLayout.addWidget(self.lblCanal)
        self.qsbCanal = QtGui.QSpinBox(self.widCanal)
        self.qsbCanal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qsbCanal.setMinimum(2)
        self.qsbCanal.setProperty("value", 2)
        self.qsbCanal.setObjectName(_fromUtf8("qsbCanal"))
        self.verticalLayout.addWidget(self.qsbCanal)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.widCanal, 0, 1, 1, 1)

        self.retranslateUi(WPagConfigCanal)
        QtCore.QMetaObject.connectSlotsByName(WPagConfigCanal)

    def retranslateUi(self, WPagConfigCanal):
        self.lblTitle.setText(_translate("WPagConfigCanal", "Canal de Comunicação", None))
        self.lblCanal.setText(_translate("WPagConfigCanal", "Selecione o canal:", None))
        self.qsbCanal.setSpecialValueText(_translate("WPagConfigCanal", "indefinido", None))

import qrc_resources_rc
