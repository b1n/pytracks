# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wpg_termina.ui'
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

class Ui_WPagTermina(object):
    def setupUi(self, WPagTermina):
        WPagTermina.setObjectName(_fromUtf8("WPagTermina"))
        WPagTermina.setWindowModality(QtCore.Qt.WindowModal)
        WPagTermina.resize(669, 538)
        self.gridLayout = QtGui.QGridLayout(WPagTermina)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(WPagTermina)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(240, 16777215))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/wpgTermina.jpg")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 3, 1)
        self.widget = QtGui.QWidget(WPagTermina)
        self.widget.setMinimumSize(QtCore.QSize(360, 0))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.txtTitle = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.txtTitle.setFont(font)
        self.txtTitle.setStyleSheet(_fromUtf8("color:rgb(0, 0, 255);\n"
"font: 20pt \"Sans Serif\";"))
        self.txtTitle.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.txtTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.txtTitle.setObjectName(_fromUtf8("txtTitle"))
        self.verticalLayout.addWidget(self.txtTitle)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.widget_2 = QtGui.QWidget(self.widget)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblExe = QtGui.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lblExe.setFont(font)
        self.lblExe.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblExe.setObjectName(_fromUtf8("lblExe"))
        self.gridLayout_2.addWidget(self.lblExe, 1, 0, 1, 1)
        self.txtCanal = QtGui.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.txtCanal.setFont(font)
        self.txtCanal.setObjectName(_fromUtf8("txtCanal"))
        self.gridLayout_2.addWidget(self.txtCanal, 2, 1, 1, 1)
        self.txtExe = QtGui.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.txtExe.setFont(font)
        self.txtExe.setObjectName(_fromUtf8("txtExe"))
        self.gridLayout_2.addWidget(self.txtExe, 1, 1, 1, 1)
        self.lblCanal = QtGui.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lblCanal.setFont(font)
        self.lblCanal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblCanal.setObjectName(_fromUtf8("lblCanal"))
        self.gridLayout_2.addWidget(self.lblCanal, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.widget_2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.ckbAgree = QtGui.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.ckbAgree.setFont(font)
        self.ckbAgree.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ckbAgree.setIcon(icon)
        self.ckbAgree.setObjectName(_fromUtf8("ckbAgree"))
        self.verticalLayout.addWidget(self.ckbAgree)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.gridLayout.addWidget(self.widget, 0, 1, 3, 1)

        self.retranslateUi(WPagTermina)
        QtCore.QMetaObject.connectSlotsByName(WPagTermina)

    def retranslateUi(self, WPagTermina):
        WPagTermina.setWindowTitle(_translate("WPagTermina", "Form", None))
        self.txtTitle.setText(_translate("WPagTermina", "Parâmetros da Simulação", None))
        self.lblExe.setText(_translate("WPagTermina", "Exercício:", None))
        self.txtCanal.setText(_translate("WPagTermina", "9", None))
        self.txtExe.setText(_translate("WPagTermina", "XXXX9999", None))
        self.lblCanal.setText(_translate("WPagTermina", "Canal:", None))
        self.ckbAgree.setText(_translate("WPagTermina", "Dados corretos para simulação", None))

import qrc_resources_rc
