# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_espera.ui'
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

class Ui_CDlgEspera(object):
    def setupUi(self, CDlgEspera):
        CDlgEspera.setObjectName(_fromUtf8("CDlgEspera"))
        CDlgEspera.resize(259, 151)
        self.verticalLayout_2 = QtGui.QVBoxLayout(CDlgEspera)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gbx_espera = QtGui.QGroupBox(CDlgEspera)
        self.gbx_espera.setObjectName(_fromUtf8("gbx_espera"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbx_espera)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cbx_esp = QtGui.QComboBox(self.gbx_espera)
        self.cbx_esp.setObjectName(_fromUtf8("cbx_esp"))
        self.verticalLayout.addWidget(self.cbx_esp)
        self.verticalLayout_2.addWidget(self.gbx_espera)
        self.lbl_comando = QtGui.QLabel(CDlgEspera)
        self.lbl_comando.setStyleSheet(_fromUtf8("background-color:rgb(0, 0, 0);\n"
"color:rgb(0, 190, 0)"))
        self.lbl_comando.setObjectName(_fromUtf8("lbl_comando"))
        self.verticalLayout_2.addWidget(self.lbl_comando)
        self.bbx_espera = QtGui.QDialogButtonBox(CDlgEspera)
        self.bbx_espera.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_espera.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbx_espera.setObjectName(_fromUtf8("bbx_espera"))
        self.verticalLayout_2.addWidget(self.bbx_espera)

        self.retranslateUi(CDlgEspera)
        QtCore.QObject.connect(self.bbx_espera, QtCore.SIGNAL(_fromUtf8("accepted()")), CDlgEspera.accept)
        QtCore.QObject.connect(self.bbx_espera, QtCore.SIGNAL(_fromUtf8("rejected()")), CDlgEspera.reject)
        QtCore.QMetaObject.connectSlotsByName(CDlgEspera)

    def retranslateUi(self, CDlgEspera):
        CDlgEspera.setWindowTitle(_translate("CDlgEspera", "Direção", None))
        self.gbx_espera.setTitle(_translate("CDlgEspera", "Esperas", None))
        self.lbl_comando.setText(_translate("CDlgEspera", "ESP 1001", None))

