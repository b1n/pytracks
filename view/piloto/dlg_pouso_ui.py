# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_pouso.ui'
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

class Ui_CDlgPouso(object):
    def setupUi(self, CDlgPouso):
        CDlgPouso.setObjectName(_fromUtf8("CDlgPouso"))
        CDlgPouso.resize(259, 151)
        self.verticalLayout_2 = QtGui.QVBoxLayout(CDlgPouso)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gbx_pouso = QtGui.QGroupBox(CDlgPouso)
        self.gbx_pouso.setObjectName(_fromUtf8("gbx_pouso"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbx_pouso)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cbx_pouso = QtGui.QComboBox(self.gbx_pouso)
        self.cbx_pouso.setObjectName(_fromUtf8("cbx_pouso"))
        self.verticalLayout.addWidget(self.cbx_pouso)
        self.verticalLayout_2.addWidget(self.gbx_pouso)
        self.lbl_comando = QtGui.QLabel(CDlgPouso)
        self.lbl_comando.setStyleSheet(_fromUtf8("background-color:rgb(0, 0, 0);\n"
"color:rgb(0, 190, 0)"))
        self.lbl_comando.setObjectName(_fromUtf8("lbl_comando"))
        self.verticalLayout_2.addWidget(self.lbl_comando)
        self.bbx_pouso = QtGui.QDialogButtonBox(CDlgPouso)
        self.bbx_pouso.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_pouso.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbx_pouso.setObjectName(_fromUtf8("bbx_pouso"))
        self.verticalLayout_2.addWidget(self.bbx_pouso)

        self.retranslateUi(CDlgPouso)
        QtCore.QObject.connect(self.bbx_pouso, QtCore.SIGNAL(_fromUtf8("accepted()")), CDlgPouso.accept)
        QtCore.QObject.connect(self.bbx_pouso, QtCore.SIGNAL(_fromUtf8("rejected()")), CDlgPouso.reject)
        QtCore.QMetaObject.connectSlotsByName(CDlgPouso)

    def retranslateUi(self, CDlgPouso):
        CDlgPouso.setWindowTitle(_translate("CDlgPouso", "Pousos", None))
        self.gbx_pouso.setTitle(_translate("CDlgPouso", "Pousos", None))
        self.lbl_comando.setText(_translate("CDlgPouso", "ARR SBSP/35", None))

