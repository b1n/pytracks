# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_trajetoria.ui'
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

class Ui_CDlgTrajetoria(object):
    def setupUi(self, CDlgTrajetoria):
        CDlgTrajetoria.setObjectName(_fromUtf8("CDlgTrajetoria"))
        CDlgTrajetoria.resize(259, 151)
        self.verticalLayout_2 = QtGui.QVBoxLayout(CDlgTrajetoria)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gbx_trajetoria = QtGui.QGroupBox(CDlgTrajetoria)
        self.gbx_trajetoria.setObjectName(_fromUtf8("gbx_trajetoria"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbx_trajetoria)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cbx_trj = QtGui.QComboBox(self.gbx_trajetoria)
        self.cbx_trj.setObjectName(_fromUtf8("cbx_trj"))
        self.verticalLayout.addWidget(self.cbx_trj)
        self.verticalLayout_2.addWidget(self.gbx_trajetoria)
        self.lbl_comando = QtGui.QLabel(CDlgTrajetoria)
        self.lbl_comando.setStyleSheet(_fromUtf8("background-color:rgb(0, 0, 0);\n"
"color:rgb(0, 190, 0)"))
        self.lbl_comando.setObjectName(_fromUtf8("lbl_comando"))
        self.verticalLayout_2.addWidget(self.lbl_comando)
        self.bbx_trajetoria = QtGui.QDialogButtonBox(CDlgTrajetoria)
        self.bbx_trajetoria.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_trajetoria.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbx_trajetoria.setObjectName(_fromUtf8("bbx_trajetoria"))
        self.verticalLayout_2.addWidget(self.bbx_trajetoria)

        self.retranslateUi(CDlgTrajetoria)
        QtCore.QObject.connect(self.bbx_trajetoria, QtCore.SIGNAL(_fromUtf8("accepted()")), CDlgTrajetoria.accept)
        QtCore.QObject.connect(self.bbx_trajetoria, QtCore.SIGNAL(_fromUtf8("rejected()")), CDlgTrajetoria.reject)
        QtCore.QMetaObject.connectSlotsByName(CDlgTrajetoria)

    def retranslateUi(self, CDlgTrajetoria):
        CDlgTrajetoria.setWindowTitle(_translate("CDlgTrajetoria", "Direção", None))
        self.gbx_trajetoria.setTitle(_translate("CDlgTrajetoria", "Trajetórias", None))
        self.lbl_comando.setText(_translate("CDlgTrajetoria", "TRJ 1001", None))

