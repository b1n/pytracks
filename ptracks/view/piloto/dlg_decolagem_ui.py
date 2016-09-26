# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_decolagem.ui'
#
# Created: Wed Jun 22 11:22:13 2016
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

class Ui_CDlgDecolagem(object):
    def setupUi(self, CDlgDecolagem):
        CDlgDecolagem.setObjectName(_fromUtf8("CDlgDecolagem"))
        CDlgDecolagem.resize(259, 151)
        self.verticalLayout_2 = QtGui.QVBoxLayout(CDlgDecolagem)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gbx_decolagem = QtGui.QGroupBox(CDlgDecolagem)
        self.gbx_decolagem.setObjectName(_fromUtf8("gbx_decolagem"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbx_decolagem)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cbx_decolagem = QtGui.QComboBox(self.gbx_decolagem)
        self.cbx_decolagem.setObjectName(_fromUtf8("cbx_decolagem"))
        self.verticalLayout.addWidget(self.cbx_decolagem)
        self.verticalLayout_2.addWidget(self.gbx_decolagem)
        self.lbl_comando = QtGui.QLabel(CDlgDecolagem)
        self.lbl_comando.setStyleSheet(_fromUtf8("background-color:rgb(0, 0, 0);\n"
"color:rgb(0, 190, 0)"))
        self.lbl_comando.setObjectName(_fromUtf8("lbl_comando"))
        self.verticalLayout_2.addWidget(self.lbl_comando)
        self.bbx_decolagem = QtGui.QDialogButtonBox(CDlgDecolagem)
        self.bbx_decolagem.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_decolagem.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbx_decolagem.setObjectName(_fromUtf8("bbx_decolagem"))
        self.verticalLayout_2.addWidget(self.bbx_decolagem)

        self.retranslateUi(CDlgDecolagem)
        QtCore.QObject.connect(self.bbx_decolagem, QtCore.SIGNAL(_fromUtf8("accepted()")), CDlgDecolagem.accept)
        QtCore.QObject.connect(self.bbx_decolagem, QtCore.SIGNAL(_fromUtf8("rejected()")), CDlgDecolagem.reject)
        QtCore.QMetaObject.connectSlotsByName(CDlgDecolagem)

    def retranslateUi(self, CDlgDecolagem):
        CDlgDecolagem.setWindowTitle(_translate("CDlgDecolagem", "Decolagem", None))
        self.gbx_decolagem.setTitle(_translate("CDlgDecolagem", "Decolagens", None))
        self.lbl_comando.setText(_translate("CDlgDecolagem", "DEP SBSP/35", None))

