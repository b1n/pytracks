# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_dir_fixo.ui'
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

class Ui_CDlgDirFixo(object):
    def setupUi(self, CDlgDirFixo):
        CDlgDirFixo.setObjectName(_fromUtf8("CDlgDirFixo"))
        CDlgDirFixo.resize(259, 151)
        self.verticalLayout_2 = QtGui.QVBoxLayout(CDlgDirFixo)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gbx_dir_fixo = QtGui.QGroupBox(CDlgDirFixo)
        self.gbx_dir_fixo.setObjectName(_fromUtf8("gbx_dir_fixo"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbx_dir_fixo)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cbx_fix = QtGui.QComboBox(self.gbx_dir_fixo)
        self.cbx_fix.setObjectName(_fromUtf8("cbx_fix"))
        self.verticalLayout.addWidget(self.cbx_fix)
        self.verticalLayout_2.addWidget(self.gbx_dir_fixo)
        self.lbl_comando = QtGui.QLabel(CDlgDirFixo)
        self.lbl_comando.setStyleSheet(_fromUtf8("background-color:rgb(0, 0, 0);\n"
"color:rgb(0, 190, 0)"))
        self.lbl_comando.setObjectName(_fromUtf8("lbl_comando"))
        self.verticalLayout_2.addWidget(self.lbl_comando)
        self.bbx_dir_fixo = QtGui.QDialogButtonBox(CDlgDirFixo)
        self.bbx_dir_fixo.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_dir_fixo.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbx_dir_fixo.setObjectName(_fromUtf8("bbx_dir_fixo"))
        self.verticalLayout_2.addWidget(self.bbx_dir_fixo)

        self.retranslateUi(CDlgDirFixo)
        QtCore.QObject.connect(self.bbx_dir_fixo, QtCore.SIGNAL(_fromUtf8("accepted()")), CDlgDirFixo.accept)
        QtCore.QObject.connect(self.bbx_dir_fixo, QtCore.SIGNAL(_fromUtf8("rejected()")), CDlgDirFixo.reject)
        QtCore.QMetaObject.connectSlotsByName(CDlgDirFixo)

    def retranslateUi(self, CDlgDirFixo):
        CDlgDirFixo.setWindowTitle(_translate("CDlgDirFixo", "Direção", None))
        self.gbx_dir_fixo.setTitle(_translate("CDlgDirFixo", "Fixos", None))
        self.lbl_comando.setText(_translate("CDlgDirFixo", "FIX 1001", None))

