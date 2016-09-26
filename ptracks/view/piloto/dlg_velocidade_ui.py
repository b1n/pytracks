# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_velocidade.ui'
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

class Ui_CDlgVelocidade(object):
    def setupUi(self, CDlgVelocidade):
        CDlgVelocidade.setObjectName(_fromUtf8("CDlgVelocidade"))
        CDlgVelocidade.resize(194, 151)
        self.verticalLayout_2 = QtGui.QVBoxLayout(CDlgVelocidade)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gbx_velocidade = QtGui.QGroupBox(CDlgVelocidade)
        self.gbx_velocidade.setObjectName(_fromUtf8("gbx_velocidade"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbx_velocidade)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.sbx_vel = QtGui.QSpinBox(self.gbx_velocidade)
        self.sbx_vel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbx_vel.setMinimum(1)
        self.sbx_vel.setMaximum(600)
        self.sbx_vel.setSingleStep(10)
        self.sbx_vel.setProperty("value", 212)
        self.sbx_vel.setObjectName(_fromUtf8("sbx_vel"))
        self.verticalLayout.addWidget(self.sbx_vel)
        self.verticalLayout_2.addWidget(self.gbx_velocidade)
        self.lbl_comando = QtGui.QLabel(CDlgVelocidade)
        self.lbl_comando.setStyleSheet(_fromUtf8("background-color:rgb(0, 0, 0);\n"
"color:rgb(0, 190, 0)"))
        self.lbl_comando.setObjectName(_fromUtf8("lbl_comando"))
        self.verticalLayout_2.addWidget(self.lbl_comando)
        self.bbx_velocidade = QtGui.QDialogButtonBox(CDlgVelocidade)
        self.bbx_velocidade.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_velocidade.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbx_velocidade.setObjectName(_fromUtf8("bbx_velocidade"))
        self.verticalLayout_2.addWidget(self.bbx_velocidade)

        self.retranslateUi(CDlgVelocidade)
        QtCore.QObject.connect(self.bbx_velocidade, QtCore.SIGNAL(_fromUtf8("accepted()")), CDlgVelocidade.accept)
        QtCore.QObject.connect(self.bbx_velocidade, QtCore.SIGNAL(_fromUtf8("rejected()")), CDlgVelocidade.reject)
        QtCore.QMetaObject.connectSlotsByName(CDlgVelocidade)

    def retranslateUi(self, CDlgVelocidade):
        CDlgVelocidade.setWindowTitle(_translate("CDlgVelocidade", "Direção", None))
        self.gbx_velocidade.setTitle(_translate("CDlgVelocidade", "Velocidade", None))
        self.lbl_comando.setText(_translate("CDlgVelocidade", "VEL 212", None))

