#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------------------
# TrackS
# Copyright (c) 2008-2011, Instituto de Controle do Espaço Aéreo
# -----------------------------------------------------------------------------------------------
# dlgPrfEditNEW
# mantém as informações sobre a dialog de edição de performances.
#
# revision 0.1  2014/nov  mlabru
# initial release (Linux/Python)
# -----------------------------------------------------------------------------------------------
__version__ = "$revision: 0.01$"
__author__ = "mlabru, ICEA"
__date__ = "2014/11"

# < imports >------------------------------------------------------------------------------------

# python library
import logging
import os

# PyQt library
from PyQt4 import QtCore, QtGui

# model / items
import model.items.prf_new as dctPrf

# view / dialog / Qt
import view.dbedit.dlg_prf_edit_new_ui as dlgPrfEditNEW_ui

# < variáveis globais >--------------------------------------------------------------------------

# logging level
w_logLvl = logging.DEBUG

# < class dlgPrfEditNEW >------------------------------------------------------------------------


class dlgPrfEditNEW (QtGui.QDialog, dlgPrfEditNEW_ui.Ui_dlgPrfEditNEW):
    """
    mantém as informações sobre a dialog de edição de performances.
    """
    # -------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_oPrf=None, f_parent=None):
        """
        constructor.
        cria uma dialog de edição de performances.

        @param  f_control: control manager do editor da base de dados do TrackS.
        @param  f_oPrf: performance a editar.
        @param  f_parent: janela vinculada.
        """

        # logger
        l_log.info("__init__:>>")

        # verifica parâmetros de entrada
        assert (f_control)

        # init super class
        super(dlgPrfEditNEW, self).__init__(f_parent)

        # salva o control manager localmente
        self._control = f_control

        # obtém o gerente de configuração
        self._config = f_control.oConfig
        assert (self._config)

        # obtém o dicionário de configuração
        self._dctConfig = self._config.dctConfig
        assert (self._dctConfig)

        # salva a parent window localmente
        self._wndParent = f_parent

        # salva os parâmetros localmente
        self._oPrf = f_oPrf

        # pathnames
        self._sPN = None

        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"TrackS - Edição de Performances")

        # atualiza na tela os dados da performance
        self.updatePrfData()

        # configurações de conexões slot/signal
        self.configConnects()

        # configurações de títulos e mensagens da janela de edição
        self.configTexts()

        # restaura as configurações da janela de edição
        self.restoreSettings()

        # configura botões
        self.bbxEditPrf.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbxEditPrf.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # força uma passgem pela edição de chave
        self.on_qleInd_textEdited(QtCore.QString())

        # logger
        l_log.info("__init__:<<")

    # -------------------------------------------------------------------------------------------

    def accept(self):

        # logger
        l_log.info("__init__:>>")

        # performance existe ?
        if (self._oPrf is not None):

            # salva edição da performance
            self.acceptEdit()

        # senão, performance não existe
        else:

            # salva nova performance
            self.acceptNew()

        # faz o "accept"
        QtGui.QDialog.accept(self)

        # logger
        l_log.info("__init__:<<")

    # -------------------------------------------------------------------------------------------

    def acceptEdit(self):

        # logger
        l_log.info("__init__:>>")

        # dicionário de modificações
        l_dctAlt = {}

        # identificação

        # indicativo
        l_sInd = str(self.qleInd.text()).strip().upper()

        if (self._oPrf._sInd != l_sInd):

            l_dctAlt["Ind"] = l_sInd

        l_log.info("l_sInd: " + str(l_sInd))

        # descrição
        l_sDsc = str(self.qleDsc.text()).strip()

        if (self._oPrf._sDsc != l_sDsc):

            l_dctAlt["Dsc"] = l_sDsc

        l_log.info("l_sDsc: " + str(l_sDsc))

        # área

        # comprimento
        l_fComp = self.qsbComp.value()

        if (self._oPrf._fComp != l_fComp):

            l_dctAlt["Comp"] = l_fComp

        l_log.info("_fComp: " + str(l_fComp))

        # largura
        l_fLarg = self.qsbLarg.value()

        if (self._oPrf._fLarg != l_fLarg):

            l_dctAlt["Larg"] = l_fLarg

        l_log.info("_fLarg: " + str(l_fLarg))

        # altitude
        l_uiAlt = self.qsbAlt.value()

        if (self._oPrf._uiAlt != l_uiAlt):

            l_dctAlt["Alt"] = l_uiAlt

        l_log.info("_uiAlt: " + str(l_uiAlt))

        # centro
        l_fCentroX = self.qsbCentroX.value()
        l_fCentroY = self.qsbCentroY.value()

        if ((self._oPrf._oCentro.getPto()[0] != l_fCentroX) or
                (self._oPrf._oCentro.getPto()[1] != l_fCentroY)):

            l_dctAlt["Centro"] = (l_fCentroX, l_fCentroY)

        l_log.info("_oCentro: %02d x %02d" % (l_fCentroX, l_fCentroY))

        # diferença de declinação magnética
        l_iDifDecl = self.qsbDifDecl.value()

        if (self._oPrf._iDifDecl != l_iDifDecl):

            l_dctAlt["DifDecl"] = l_iDifDecl

        l_log.info("_iDifDecl: " + str(l_iDifDecl))

        # lista de aeronaves da performance
        # self._oFigTab = None #self.qwtTabAnv.getAnvTab ()

        # atualiza a performance
        self._oPrf.updatePrf(l_dctAlt)

        l_log.info("self._oPrf (editado): " + str(self._oPrf))

        # logger
        l_log.info("__init__:<<")

    # -------------------------------------------------------------------------------------------

    def acceptNew(self):

        # logger
        l_log.info("__init__:>>")

        # cria um nova performance
        self._oPrf = dctPrf.dctPrf()
        assert (self._oPrf)

        # identificação

        # indicativo
        l_sInd = str(self.qleInd.text()).strip().upper()
        l_log.info("_sInd: " + str(l_sInd))

        # descrição
        l_sDsc = str(self.qleDsc.text()).strip()
        l_log.info("_sDsc: " + str(l_sDsc))

        # geografia

        # comprimento
        l_fComp = self.qsbComp.value()
        l_log.info("_fComp: " + str(l_fComp))

        # largura
        l_fLarg = self.qsbLarg.value()
        l_log.info("_fLarg: " + str(l_fLarg))

        # altitude
        l_uiAlt = self.qsbAlt.value()
        l_log.info("_uiAlt: " + str(l_uiAlt))

        # centro
        l_fCentroX = self.qsbCentroX.value()
        l_fCentroY = self.qsbCentroY.value()
        l_log.info("_oCentro: %02d x %02d" % (l_fCentroX, l_fCentroY))

        # diferença de declinação magnética
        l_iDifDecl = self.qsbDifDecl.value()
        l_log.info("_iDifDecl: " + str(l_iDifDecl))

        # atualiza o pathname
        if (self._sPN is not None):

            self._oPrf._sPN = self._sPN

        # atualiza a performance
        self._oPrf.updatePrf0211([None, l_sInd, l_sDsc,
                                  l_fComp, l_fLarg, l_uiAlt,
                                  (l_fCentroX, l_fCentroY), l_iDifDecl])  # , self._oFigTab )

        # logger
        l_log.info("__init__:<<")

    # -------------------------------------------------------------------------------------------

    def configConnects(self):
        """
        configura as conexões slot/signal.
        """

        # logger
        l_log.info("__init__:>>")

        # conecta botão Ok da edição de performance
        self.connect(self.bbxEditPrf,
                     QtCore.SIGNAL("accepted()"),
                     self.accept)

        # conecta botão Cancela da edição de performance
        self.connect(self.bbxEditPrf,
                     QtCore.SIGNAL("rejected()"),
                     self.reject)

        # conect fim de edição da chave
        self.connect(self.qleInd,
                     QtCore.SIGNAL("editingFinished()"),
                     self.editingFinished)

        # logger
        l_log.info("__init__:<<")

    # -------------------------------------------------------------------------------------------

    def configTexts(self):

        # logger
        l_log.info("__init__:><")

        # configura títulos e mensagens
        self._txtSettings = "dlgPrfEditNEW"

    # -------------------------------------------------------------------------------------------

    def editingFinished(self):

        # logger
        l_log.info("__init__:>>")

        # obtém a chave digitada
#       l_sInd = str ( self.qleInd.text ()).strip ().upper ()

        # checa se digitou uma chave válida para a performance
#       l_bEnable = ( l_sInd != "" )

        # habilita / desabilita os botões
#       self.bbxEditPrf.button ( QtGui.QDialogButtonBox.Ok ).setEnabled ( l_bEnable )

        # remoção de aeronave
#       self.btnDel.setEnabled ( l_bEnable )

        # edição de aeronave
#       self.btnEdit.setEnabled ( l_bEnable )

        # inserção de aeronave
#       self.btnNew.setEnabled ( l_bEnable )

        # checa se digitou uma chave válida para a performance
#       if ( l_bEnable ):

            # salva o pathname do arquivo de performance
#           self._sPN = os.path.join ( self._cfgs [ "dir.exe" ], l_sInd + ".xrc" )
#           l_log.info ( "self._sPN (Prf): " + str ( self._sPN ))

            # salva o pathname da tabela de aeronaves da performance
#           self._sTabPath = os.path.join ( self._cfgs [ "dir.anv" ], l_sInd + ".anv" )
#           l_log.info ( "self._sTabPath (Tab): " + str ( self._sTabPath ))

        # logger
        l_log.info("__init__:<<")

    # -------------------------------------------------------------------------------------------

    def getData(self):

        # logger
        l_log.info("__init__:><")

        return self._oPrf

    # -------------------------------------------------------------------------------------------

    def reject(self):

        # logger
        l_log.info("__init__:>>")

        self._oPrf = None

        # faz o "reject"
        QtGui.QDialog.reject(self)

        # logger
        l_log.info("__init__:<<")

    # -------------------------------------------------------------------------------------------

    def restoreSettings(self):
        """
        restaura as configurações salvas para esta janela
        """

        # logger
        l_log.info("__init__:>>")

        # obtém os settings
        l_set = QtCore.QSettings()
        assert (l_set)

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self._txtSettings)).toByteArray())

        # logger
        l_log.info("__init__:<<")

        return True

    # -------------------------------------------------------------------------------------------

    def updatePrfData(self):
        """
        atualiza na tela os a área de dados da performance selecionado.
        """

        # logger
        l_log.info("__init__:>>")

        # performance existe ?
        if (self._oPrf is not None):

            # identificação
            self.qleInd.setText(self._oPrf._sInd)
            self.qleDsc.setText(self._oPrf._sDsc)

            # área

            # comprimento
            self.qsbComp.setValue(self._oPrf._fComp)

            # largura
            self.qsbLarg.setValue(self._oPrf._fLarg)

            # diferença de declinação magnética
            self.qsbDifDecl.setValue(self._oPrf._iDifDecl)

            # centro
            (l_iX, l_iY) = self._oPrf._oCentro.getPto()

            self.qsbCentroX.setValue(l_iX)
            self.qsbCentroY.setValue(l_iY)

            # altitude
            self.qsbAlt.setValue(self._oPrf._uiAlt)

        # senão, é um nova performance
        else:

            # cria uma nova tabela de figuras
            # self._oFigTab = clsTabelaFig.clsTabelaFig ()
            # assert ( self._oFigTab is not None )

            # posiciona cursor no início do formulário
            self.qleInd.setFocus()

        # logger
        l_log.info("__init__:<<")

    # ===========================================================================================
    # rotinas de tratamento de edição de campos
    # ===========================================================================================

    # -------------------------------------------------------------------------------------------

    @QtCore.pyqtSignature("QString")
    def on_qleInd_textEdited(self, f_qszVal):

        # logger
        l_log.info("__init__:><")

        # habilita / desabilita os botões
        self.bbxEditPrf.button(QtGui.QDialogButtonBox.Ok).setEnabled(not self.qleInd.text().isEmpty())

# < the end >-------------------------------------------------------------------------------------- #
