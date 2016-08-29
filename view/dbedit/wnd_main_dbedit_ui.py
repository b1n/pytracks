# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './wnd_main_dbedit.ui'
#
# Created: Wed Jun  1 12:00:00 2016
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

class Ui_wndMainDBEdit(object):
    def setupUi(self, wndMainDBEdit):
        wndMainDBEdit.setObjectName(_fromUtf8("wndMainDBEdit"))
        wndMainDBEdit.resize(510, 497)
        wndMainDBEdit.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.centralwidget = QtGui.QWidget(wndMainDBEdit)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frmTitle = QtGui.QFrame(self.centralwidget)
        self.frmTitle.setGeometry(QtCore.QRect(30, 20, 451, 211))
        self.frmTitle.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);"))
        self.frmTitle.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmTitle.setFrameShadow(QtGui.QFrame.Raised)
        self.frmTitle.setObjectName(_fromUtf8("frmTitle"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frmTitle)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblLin1 = QtGui.QLabel(self.frmTitle)
        self.lblLin1.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);"))
        self.lblLin1.setAlignment(QtCore.Qt.AlignCenter)
        self.lblLin1.setObjectName(_fromUtf8("lblLin1"))
        self.verticalLayout.addWidget(self.lblLin1)
        self.lblLin3 = QtGui.QLabel(self.frmTitle)
        self.lblLin3.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);"))
        self.lblLin3.setAlignment(QtCore.Qt.AlignCenter)
        self.lblLin3.setObjectName(_fromUtf8("lblLin3"))
        self.verticalLayout.addWidget(self.lblLin3)
        self.lblLin4 = QtGui.QLabel(self.frmTitle)
        self.lblLin4.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);"))
        self.lblLin4.setObjectName(_fromUtf8("lblLin4"))
        self.verticalLayout.addWidget(self.lblLin4)
        self.gbxBtn = QtGui.QGroupBox(self.centralwidget)
        self.gbxBtn.setGeometry(QtCore.QRect(20, 240, 471, 241))
        self.gbxBtn.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.gbxBtn.setFlat(False)
        self.gbxBtn.setCheckable(False)
        self.gbxBtn.setObjectName(_fromUtf8("gbxBtn"))
        self.gridLayout = QtGui.QGridLayout(self.gbxBtn)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnAer = QtGui.QPushButton(self.gbxBtn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAer.sizePolicy().hasHeightForWidth())
        self.btnAer.setSizePolicy(sizePolicy)
        self.btnAer.setObjectName(_fromUtf8("btnAer"))
        self.gridLayout.addWidget(self.btnAer, 0, 1, 1, 1)
        self.btnPrf = QtGui.QPushButton(self.gbxBtn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPrf.sizePolicy().hasHeightForWidth())
        self.btnPrf.setSizePolicy(sizePolicy)
        self.btnPrf.setObjectName(_fromUtf8("btnPrf"))
        self.gridLayout.addWidget(self.btnPrf, 2, 0, 1, 1)
        self.btnPrc = QtGui.QPushButton(self.gbxBtn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPrc.sizePolicy().hasHeightForWidth())
        self.btnPrc.setSizePolicy(sizePolicy)
        self.btnPrc.setObjectName(_fromUtf8("btnPrc"))
        self.gridLayout.addWidget(self.btnPrc, 3, 0, 1, 1)
        self.btnExe = QtGui.QPushButton(self.gbxBtn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnExe.sizePolicy().hasHeightForWidth())
        self.btnExe.setSizePolicy(sizePolicy)
        self.btnExe.setObjectName(_fromUtf8("btnExe"))
        self.gridLayout.addWidget(self.btnExe, 0, 0, 1, 1)
        self.btnFix = QtGui.QPushButton(self.gbxBtn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnFix.sizePolicy().hasHeightForWidth())
        self.btnFix.setSizePolicy(sizePolicy)
        self.btnFix.setObjectName(_fromUtf8("btnFix"))
        self.gridLayout.addWidget(self.btnFix, 2, 1, 1, 1)
        self.btnRad = QtGui.QPushButton(self.gbxBtn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRad.sizePolicy().hasHeightForWidth())
        self.btnRad.setSizePolicy(sizePolicy)
        self.btnRad.setObjectName(_fromUtf8("btnRad"))
        self.gridLayout.addWidget(self.btnRad, 3, 1, 1, 1)
        self.btnSai = QtGui.QPushButton(self.gbxBtn)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSai.sizePolicy().hasHeightForWidth())
        self.btnSai.setSizePolicy(sizePolicy)
        self.btnSai.setObjectName(_fromUtf8("btnSai"))
        self.gridLayout.addWidget(self.btnSai, 4, 0, 1, 1)
        wndMainDBEdit.setCentralWidget(self.centralwidget)

        self.retranslateUi(wndMainDBEdit)
        QtCore.QMetaObject.connectSlotsByName(wndMainDBEdit)

    def retranslateUi(self, wndMainDBEdit):
        wndMainDBEdit.setWindowTitle(_translate("wndMainDBEdit", "TrackS 0.01 [Edicão da Base de Dados]", None))
        self.lblLin1.setText(_translate("wndMainDBEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\'; font-size:16pt; font-weight:600; color:#ffff00;\">TrackS</span></p></body></html>", None))
        self.lblLin3.setText(_translate("wndMainDBEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\'; font-size:16pt; font-weight:600; color:#ffff00;\">Gerador de Pistas</span></p></body></html>", None))
        self.lblLin4.setText(_translate("wndMainDBEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\'; font-size:16pt; font-weight:600; color:#00007f;\">(C) 2014  ICEA - GMU </span></p></body></html>", None))
        self.btnAer.setText(_translate("wndMainDBEdit", "Aeródromos", None))
        self.btnPrf.setText(_translate("wndMainDBEdit", "Performances", None))
        self.btnPrc.setText(_translate("wndMainDBEdit", "Procedimentos", None))
        self.btnExe.setText(_translate("wndMainDBEdit", "Exercícios", None))
        self.btnFix.setText(_translate("wndMainDBEdit", "Fixos", None))
        self.btnRad.setText(_translate("wndMainDBEdit", "Radares", None))
        self.btnSai.setText(_translate("wndMainDBEdit", "Sair", None))

