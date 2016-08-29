#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wnd_main_dbedit.

janela principal do editor da base de dados.

revision 0.2  2014/nov  mlabru
inclusão de fixos, procedimentos e radares

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2014/11"

# < import >---------------------------------------------------------------------------------------

# python library
import logging
import os

# PyQt library
from PyQt4 import QtCore, QtGui

# view
import view.dbedit.dlg_aer_data_new as dlgaer
import view.dbedit.dlg_exe_data_new as dlgexe
import view.dbedit.dlg_fix_data_new as dlgfix
import view.dbedit.dlg_prf_data_new as dlgprf
# import view.dbedit.dlg_rad_data_new as dlgrad

import view.dbedit.wnd_main_dbedit_ui as wmain_ui

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CWndMainDBEdit >-------------------------------------------------------------------------

class CWndMainDBEdit(QtGui.QMainWindow, wmain_ui.Ui_wndMainDBEdit):
    """
    janela principal do editor da base de dados.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_parent=None):
        """
        @param f_control: control manager.
        @param f_parent: janela vinculada ou None.
        """
        # init super class
        super(CWndMainDBEdit, self).__init__()

        # verifica parâmetros de entrada
        assert f_control

        # salva o control manager localmente
        self._control = f_control
        assert self._control

        # obtém o event manager
        self._event = f_control.event
        assert self._event

        # registra a sí próprio como recebedor de eventos
        # self._event.register_listener(self)

        # create main menu ui
        self.setupUi(self)

        # create connections
        self.connect(self.btnAer, QtCore.SIGNAL("clicked()"), self.cbk_aerodromos)
        self.connect(self.btnExe, QtCore.SIGNAL("clicked()"), self.cbk_exercicios)
        self.connect(self.btnFix, QtCore.SIGNAL("clicked()"), self.cbk_fixos)
        self.connect(self.btnPrf, QtCore.SIGNAL("clicked()"), self.cbk_performances)
        self.connect(self.btnPrc, QtCore.SIGNAL("clicked()"), self.cbk_procedimentos)
        # self.connect(self.btnRad, QtCore.SIGNAL("clicked()"), self.cbk_radares)
        self.connect(self.btnSai, QtCore.SIGNAL("clicked()"), self.cbk_sair)

        # dialogs
        self._dlg_aer = None
        self._dlg_exe = None
        self._dlg_fix = None
        self._dlg_prf = None
        self._dlg_prc = None
        # self._dlg_rad = None

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def cbk_aerodromos(self):
        """
        callback da opção edição de aeródromos da janela principal.
        """
        # já existe a dialog de edição da tabela de aeródromos ?
        if self._dlg_aer is None:

            # cria a dialog de edição da tabela de aeródromos
            self._dlg_aer = dlgaer.CDlgAerDataNEW(self._control, self)
            assert self._dlg_aer

        # exibe a dialog de edição da tabela de aeródromos
        self._dlg_aer.show()

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def cbk_exercicios(self):
        """
        callback da opção edição de exercícios da janela principal.
        """
        # já existe a dialog de edição da tabela de exercícios ?
        if self._dlg_exe is None:

            # cria a dialog de edição da tabela de exercícios
            self._dlg_exe = dlgexe.CDlgExeDataNEW(self._control, self)
            assert self._dlg_exe

        # exibe a dialog de edição da tabela de exercícios
        self._dlg_exe.show()

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def cbk_fixos(self):
        """
        callback da opção edição de fixos da janela principal.
        """
        # já existe a dialog de edição da tabela de fixos ?
        if self._dlg_fix is None:

            # cria a dialog de edição da tabela de fixos
            self._dlg_fix = dlgfix.CDlgFixDataNEW(self._control, self)
            assert self._dlg_fix

        # exibe a dialog de edição da tabela de fixos
        self._dlg_fix.show()

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def cbk_performances(self):
        """
        callback da opção edição de performances da janela principal.
        """
        # já existe a dialog de edição da tabela de performances ?
        if self._dlg_prf is None:

            # cria a dialog de edição da tabela de performances
            self._dlg_prf = dlgprf.CDlgPrfDataNEW(self._control, self)
            assert self._dlg_prf

        # exibe a dialog de edição da tabela de performances
        self._dlg_prf.show()

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def cbk_procedimentos(self):
        """
        callback da opção edição de procedimentos da janela principal.
        """
        # já existe a dialog de edição da tabela de procedimentos ?
        # if self._dlg_prc is None:

            # cria a dialog de edição da tabela de procedimentos
            # self._dlg_prc = dlgprc.CDlgPrcDataNEW(self._control, self)
            # assert self._dlg_prc

        # exibe a dialog de edição da tabela de procedimentos
        # self._dlg_prc.show()

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def cbk_radares(self):
        """
        callback da opção edição de radares da janela principal.
        """
        # já existe a dialog de edição da tabela de radares ?
        if self._dlg_rad is None:

            # cria a dialog de edição da tabela de radares
            self._dlg_rad = dlgrad.CDlgRadDataNEW(self._control, self)
            assert self._dlg_rad

        # exibe a dialog de edição da tabela de radares
        self._dlg_rad.show()

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def cbk_sair(self):
        """
        callback da opção sair da janela principal.
        """
        # cria um evento de quit
        l_evt = events.CQuit()
        assert l_evt

        # dissemina o evento
        self._event.post(l_evt)

        # finaliza o sistema
        self.close()

# < the end>---------------------------------------------------------------------------------------
