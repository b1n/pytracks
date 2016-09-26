# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_altitude.ui'
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

class Ui_CDlgAltitude(object):
    def setupUi(self, CDlgAltitude):
        CDlgAltitude.setObjectName(_fromUtf8("CDlgAltitude"))
        CDlgAltitude.resize(303, 235)
        self.verticalLayout_2 = QtGui.QVBoxLayout(CDlgAltitude)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frame = QtGui.QFrame(CDlgAltitude)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gbx_altitude = QtGui.QGroupBox(self.frame)
        self.gbx_altitude.setFlat(False)
        self.gbx_altitude.setCheckable(False)
        self.gbx_altitude.setObjectName(_fromUtf8("gbx_altitude"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbx_altitude)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.rbt_alt = QtGui.QRadioButton(self.gbx_altitude)
        self.rbt_alt.setChecked(True)
        self.rbt_alt.setObjectName(_fromUtf8("rbt_alt"))
        self.verticalLayout_3.addWidget(self.rbt_alt)
        self.rbt_niv = QtGui.QRadioButton(self.gbx_altitude)
        self.rbt_niv.setObjectName(_fromUtf8("rbt_niv"))
        self.verticalLayout_3.addWidget(self.rbt_niv)
        self.sbx_alt = QtGui.QSpinBox(self.gbx_altitude)
        self.sbx_alt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbx_alt.setMinimum(0)
        self.sbx_alt.setMaximum(60000)
        self.sbx_alt.setSingleStep(10)
        self.sbx_alt.setProperty("value", 1202)
        self.sbx_alt.setObjectName(_fromUtf8("sbx_alt"))
        self.verticalLayout_3.addWidget(self.sbx_alt)
        self.horizontalLayout.addWidget(self.gbx_altitude)
        self.gbx_razao = QtGui.QGroupBox(self.frame)
        self.gbx_razao.setCheckable(True)
        self.gbx_razao.setObjectName(_fromUtf8("gbx_razao"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gbx_razao)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.sbx_raz = QtGui.QDoubleSpinBox(self.gbx_razao)
        self.sbx_raz.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbx_raz.setDecimals(1)
        self.sbx_raz.setMinimum(2.0)
        self.sbx_raz.setMaximum(25.0)
        self.sbx_raz.setSingleStep(1.0)
        self.sbx_raz.setProperty("value", 7.0)
        self.sbx_raz.setObjectName(_fromUtf8("sbx_raz"))
        self.verticalLayout_4.addWidget(self.sbx_raz)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.gbx_razao)
        self.verticalLayout_2.addWidget(self.frame)
        self.lbl_comando = QtGui.QLabel(CDlgAltitude)
        self.lbl_comando.setStyleSheet(_fromUtf8("background-color:rgb(0, 0, 0);\n"
"color:rgb(0, 190, 0)"))
        self.lbl_comando.setObjectName(_fromUtf8("lbl_comando"))
        self.verticalLayout_2.addWidget(self.lbl_comando)
        self.bbx_altitude = QtGui.QDialogButtonBox(CDlgAltitude)
        self.bbx_altitude.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_altitude.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbx_altitude.setObjectName(_fromUtf8("bbx_altitude"))
        self.verticalLayout_2.addWidget(self.bbx_altitude)

        self.retranslateUi(CDlgAltitude)
        QtCore.QObject.connect(self.bbx_altitude, QtCore.SIGNAL(_fromUtf8("accepted()")), CDlgAltitude.accept)
        QtCore.QObject.connect(self.bbx_altitude, QtCore.SIGNAL(_fromUtf8("rejected()")), CDlgAltitude.reject)
        QtCore.QMetaObject.connectSlotsByName(CDlgAltitude)

    def retranslateUi(self, CDlgAltitude):
        CDlgAltitude.setWindowTitle(_translate("CDlgAltitude", "Direção", None))
        self.gbx_altitude.setTitle(_translate("CDlgAltitude", "Altitude", None))
        self.rbt_alt.setText(_translate("CDlgAltitude", "Altitude (ft)", None))
        self.rbt_niv.setText(_translate("CDlgAltitude", "Nível", None))
        self.gbx_razao.setTitle(_translate("CDlgAltitude", "Razão", None))
        self.lbl_comando.setText(_translate("CDlgAltitude", "ALT 1202 RAZ 3.5", None))

