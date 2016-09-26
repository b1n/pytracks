# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_subida.ui'
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

class Ui_CDlgSubida(object):
    def setupUi(self, CDlgSubida):
        CDlgSubida.setObjectName(_fromUtf8("CDlgSubida"))
        CDlgSubida.resize(259, 151)
        self.verticalLayout_2 = QtGui.QVBoxLayout(CDlgSubida)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gbx_subida = QtGui.QGroupBox(CDlgSubida)
        self.gbx_subida.setObjectName(_fromUtf8("gbx_subida"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbx_subida)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cbx_sub = QtGui.QComboBox(self.gbx_subida)
        self.cbx_sub.setObjectName(_fromUtf8("cbx_sub"))
        self.verticalLayout.addWidget(self.cbx_sub)
        self.verticalLayout_2.addWidget(self.gbx_subida)
        self.lbl_comando = QtGui.QLabel(CDlgSubida)
        self.lbl_comando.setStyleSheet(_fromUtf8("background-color:rgb(0, 0, 0);\n"
"color:rgb(0, 190, 0)"))
        self.lbl_comando.setObjectName(_fromUtf8("lbl_comando"))
        self.verticalLayout_2.addWidget(self.lbl_comando)
        self.bbx_subida = QtGui.QDialogButtonBox(CDlgSubida)
        self.bbx_subida.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_subida.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbx_subida.setObjectName(_fromUtf8("bbx_subida"))
        self.verticalLayout_2.addWidget(self.bbx_subida)

        self.retranslateUi(CDlgSubida)
        QtCore.QObject.connect(self.bbx_subida, QtCore.SIGNAL(_fromUtf8("accepted()")), CDlgSubida.accept)
        QtCore.QObject.connect(self.bbx_subida, QtCore.SIGNAL(_fromUtf8("rejected()")), CDlgSubida.reject)
        QtCore.QMetaObject.connectSlotsByName(CDlgSubida)

    def retranslateUi(self, CDlgSubida):
        CDlgSubida.setWindowTitle(_translate("CDlgSubida", "Direção", None))
        self.gbx_subida.setTitle(_translate("CDlgSubida", "Trajetórias", None))
        self.lbl_comando.setText(_translate("CDlgSubida", "TRJ 1001", None))

