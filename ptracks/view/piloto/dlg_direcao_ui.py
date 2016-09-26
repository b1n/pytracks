# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_direcao.ui'
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

class Ui_CDlgDirecao(object):
    def setupUi(self, CDlgDirecao):
        CDlgDirecao.setObjectName(_fromUtf8("CDlgDirecao"))
        CDlgDirecao.resize(497, 235)
        self.verticalLayout_2 = QtGui.QVBoxLayout(CDlgDirecao)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frame = QtGui.QFrame(CDlgDirecao)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gbx_sentido = QtGui.QGroupBox(self.frame)
        self.gbx_sentido.setFlat(False)
        self.gbx_sentido.setCheckable(False)
        self.gbx_sentido.setObjectName(_fromUtf8("gbx_sentido"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbx_sentido)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.rbt_dir = QtGui.QRadioButton(self.gbx_sentido)
        self.rbt_dir.setChecked(True)
        self.rbt_dir.setObjectName(_fromUtf8("rbt_dir"))
        self.verticalLayout.addWidget(self.rbt_dir)
        self.rbt_esq = QtGui.QRadioButton(self.gbx_sentido)
        self.rbt_esq.setObjectName(_fromUtf8("rbt_esq"))
        self.verticalLayout.addWidget(self.rbt_esq)
        self.rbt_mnr = QtGui.QRadioButton(self.gbx_sentido)
        self.rbt_mnr.setObjectName(_fromUtf8("rbt_mnr"))
        self.verticalLayout.addWidget(self.rbt_mnr)
        self.horizontalLayout.addWidget(self.gbx_sentido)
        self.gbx_direcao = QtGui.QGroupBox(self.frame)
        self.gbx_direcao.setFlat(False)
        self.gbx_direcao.setCheckable(True)
        self.gbx_direcao.setObjectName(_fromUtf8("gbx_direcao"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbx_direcao)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.rbt_grau = QtGui.QRadioButton(self.gbx_direcao)
        self.rbt_grau.setChecked(True)
        self.rbt_grau.setObjectName(_fromUtf8("rbt_grau"))
        self.verticalLayout_3.addWidget(self.rbt_grau)
        self.rbt_proa = QtGui.QRadioButton(self.gbx_direcao)
        self.rbt_proa.setObjectName(_fromUtf8("rbt_proa"))
        self.verticalLayout_3.addWidget(self.rbt_proa)
        self.sbx_dir = QtGui.QSpinBox(self.gbx_direcao)
        self.sbx_dir.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbx_dir.setMinimum(0)
        self.sbx_dir.setMaximum(360)
        self.sbx_dir.setProperty("value", 212)
        self.sbx_dir.setObjectName(_fromUtf8("sbx_dir"))
        self.verticalLayout_3.addWidget(self.sbx_dir)
        self.horizontalLayout.addWidget(self.gbx_direcao)
        self.gbx_razao = QtGui.QGroupBox(self.frame)
        self.gbx_razao.setCheckable(True)
        self.gbx_razao.setObjectName(_fromUtf8("gbx_razao"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gbx_razao)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.sbx_raz = QtGui.QDoubleSpinBox(self.gbx_razao)
        self.sbx_raz.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbx_raz.setDecimals(1)
        self.sbx_raz.setMinimum(3.0)
        self.sbx_raz.setMaximum(4.5)
        self.sbx_raz.setSingleStep(0.1)
        self.sbx_raz.setProperty("value", 3.5)
        self.sbx_raz.setObjectName(_fromUtf8("sbx_raz"))
        self.verticalLayout_4.addWidget(self.sbx_raz)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.gbx_razao)
        self.verticalLayout_2.addWidget(self.frame)
        self.lbl_comando = QtGui.QLabel(CDlgDirecao)
        self.lbl_comando.setStyleSheet(_fromUtf8("background-color:rgb(0, 0, 0);\n"
"color:rgb(0, 190, 0)"))
        self.lbl_comando.setObjectName(_fromUtf8("lbl_comando"))
        self.verticalLayout_2.addWidget(self.lbl_comando)
        self.bbx_direcao = QtGui.QDialogButtonBox(CDlgDirecao)
        self.bbx_direcao.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_direcao.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbx_direcao.setObjectName(_fromUtf8("bbx_direcao"))
        self.verticalLayout_2.addWidget(self.bbx_direcao)

        self.retranslateUi(CDlgDirecao)
        QtCore.QObject.connect(self.bbx_direcao, QtCore.SIGNAL(_fromUtf8("accepted()")), CDlgDirecao.accept)
        QtCore.QObject.connect(self.bbx_direcao, QtCore.SIGNAL(_fromUtf8("rejected()")), CDlgDirecao.reject)
        QtCore.QMetaObject.connectSlotsByName(CDlgDirecao)

    def retranslateUi(self, CDlgDirecao):
        CDlgDirecao.setWindowTitle(_translate("CDlgDirecao", "Direção", None))
        self.gbx_sentido.setTitle(_translate("CDlgDirecao", "Sentido", None))
        self.rbt_dir.setText(_translate("CDlgDirecao", "Direita", None))
        self.rbt_esq.setText(_translate("CDlgDirecao", "Esquerda", None))
        self.rbt_mnr.setText(_translate("CDlgDirecao", "Menor", None))
        self.gbx_direcao.setTitle(_translate("CDlgDirecao", "Direção", None))
        self.rbt_grau.setText(_translate("CDlgDirecao", "Graus", None))
        self.rbt_proa.setText(_translate("CDlgDirecao", "Proa", None))
        self.gbx_razao.setTitle(_translate("CDlgDirecao", "Razão de Curva", None))
        self.lbl_comando.setText(_translate("CDlgDirecao", "CURVA DIR 207 GRAUS RAZ 3.5", None))

