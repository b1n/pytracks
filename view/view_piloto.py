#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_piloto

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

import sip
sip.setapi('QString', 2)

# PyQt library
from PyQt4 import QtCore, QtGui

# view
import view.view_manager as view
import view.piloto.wnd_main_piloto as wmain

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CViewPiloto >----------------------------------------------------------------------------

class CViewPiloto(view.CViewManager):
    """
    the interface to configuration piloto. Handles all interaction with user
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_model):
        """
        initializes the display
        """
        # logger
        # M_LOG.info("__init__:>>")
                
        # check input parameters
        assert f_control
        assert f_model 

        # initialize super class
        super(CViewPiloto, self).__init__(f_control)

        # herdados de CViewManager
        # self.config        # config manager
        # self.control       # control manager
        # self.dct_config    # dicionário de configuração
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
        self.__app.setOrganizationDomain("pbcp.icea.br")
        self.__app.setApplicationName("piloto")

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

        @param f_evt: evento
        """
        # logger
        # M_LOG.info("notify:>>")
                
        # check input parameters
        assert f_evt

        # o evento recebido foi um Tick ?
        if isinstance(f_evt, events.CTick):

            # M_LOG.debug("events.Tick !!")
            pass

        # o evento recebido foi um aviso de término da aplicação ?
        elif isinstance(f_evt, events.CQuit):

            # M_LOG.debug("events.Quit !!")
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
        assert self.__app
        assert self.control
        assert self.model

        # obtém o airspace
        # l_airspace = self._model.oAirspace
        # assert l_airspace

        # obtém o landscape
        # l_landscape = self._model.oLandscape
        # assert l_landscape

        # cria a visualização
        l_wmain = wmain.CWndMainPiloto(self.control)
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
