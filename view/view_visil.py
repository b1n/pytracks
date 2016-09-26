#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_visil.

DOCUMENT ME!

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging
import os
import sys

# PyQt library
from PyQt4 import QtCore, QtGui

# view
from . import view_manager as view
from .visil import wnd_main_visil as wmain

# control
from ..control.events import events_basic as event

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CViewVisil >-----------------------------------------------------------------------------

class CViewVisil(view.CViewManager):
    """
    the interface to configuration visil. Handles all interaction with user.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_model):
        """
        initializes the display
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_control
        assert f_model

        # initialize super class
        super(CViewVisil, self).__init__(f_control)

        # herdados de CViewManager
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager
        # self.model         # model manager

        # salva o model localmente
        self.model = f_model
        assert self.model

        # cria a aplicação
        self.__app = QtGui.QApplication(sys.argv)
        assert self.__app

        # configura alguns parâmetros da aplicação
        self.__app.setOrganizationName("ICEA")
        self.__app.setOrganizationDomain("icea.br")
        self.__app.setApplicationName("visil")

        self.__app.setWindowIcon(QtGui.QIcon(os.path.join(self.dct_config["dir.img"], "icon.png")))

        # carrega o logo
        l_pix_logo = QtGui.QPixmap(os.path.join(self.dct_config["dir.img"], "logo.jpg"))
        assert l_pix_logo

        # cria a tela de apresentação
        self.__splash = QtGui.QSplashScreen(l_pix_logo, QtCore.Qt.WindowStaysOnTopHint)
        assert self.__splash

        self.__splash.setMask(l_pix_logo.mask())

        # exibe a tela de apresentação
        self.__splash.show()

        # trata os eventos (antes do loop principal)
        self.__app.processEvents()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def notify(self, f_evt):
        """
        callback de recebimento de eventos

        @param f_evt: event
        """
        # logger
        # M_LOG.info("notify:>>")

        # verifica parâmetros de entrada
        assert f_evt

        # o evento recebido foi um Tick ?
        if isinstance(f_evt, event.CTick):

            # M_LOG.debug("event.CTick")
            pass

        # o evento recebido foi um aviso de término da aplicação ?
        elif isinstance(f_evt, event.CQuit):

            # M_LOG.debug("event.CQuit")
            pass

            # para todos os processos
            # glb_data.G_KEEP_RUN = False

        # logger
        # M_LOG.info("notify:<<")

    # ---------------------------------------------------------------------------------------------

    def run(self):
        """
        executa a aplicação
        """
        # logger
        # M_LOG.info("run:>>")

        # verifica condições de execução
        assert self.model
        assert self.__app
        assert self.__splash

        # obtém o airspace
        # l_airspace = self.model.airspace
        # assert l_airspace

        # obtém o landscape
        # l_landscape = self.model.landscape
        # assert l_landscape

        # cria a visualização
        l_wmain = wmain.CWndMainVisil(self.control)
        assert l_wmain

        # exibe o configurador de simulação
        l_wmain.show()

        # fecha a tela de apresentação
        self.__splash.finish(l_wmain)

        # processa a aplicação
        self.__app.exec_()

        # logger
        # M_LOG.info("run:<<")

# < the end >--------------------------------------------------------------------------------------
