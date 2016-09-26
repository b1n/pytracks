#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_wizard

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
import time

import sip
sip.setapi('QString', 2)

# PyQt library
from PyQt4 import QtCore, QtGui

# view
from . import view_manager as view
from . .wizard import dlg_wizard as wizard

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CViewWizard >-----------------------------------------------------------------------------

class CViewWizard(view.CViewManager):
    """
    the interface to configuration wizard. Handles all interaction with user
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control):
        """
        initializes the display
        """
        # logger
        # M_LOG.info("__init__:>>")
                
        # check input parameters
        assert f_control

        # initialize super class
        super(CViewWizard, self).__init__(f_control)

        # herdados de CViewManager
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager
        # self.model         # model manager

        # salva o control manager localmente
        self.control = f_control
        assert self.control

        # salva o model manager localmente
        # self.model = f_control.model
        # assert self._model

        # obtém o event manager
        self.event = f_control.event
        assert self.event

        # registra a sí próprio como recebedor de eventos
        # self._event.register_listener(self)

        # obtém o config manager
        self.config = f_control.config
        assert self.config

        # obtém o dicionário de configuração
        self.dct_config = self.config.dct_config
        assert self.dct_config

        # cria a aplicação
        self._app = QtGui.QApplication(sys.argv)
        assert self._app

        # configura alguns parâmetros da aplicação
        self._app.setOrganizationName("ICEA")
        self._app.setOrganizationDomain("icea.br")
        self._app.setApplicationName("Merlin")

        self._app.setWindowIcon(QtGui.QIcon(os.path.join(self.dct_config["dir.img"], "icon.png")))

        # logger
        # M_LOG.info("__init__:<<")
                
    # ---------------------------------------------------------------------------------------------

    def notify(self, f_event):
        """
        callback de recebimento de eventos

        @param f_event: event
        """
        # logger
        # M_LOG.info("notify:>>")
                
        # check input parameters
        assert f_event

        if isinstance(f_event, events.CTick):
            pass

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
        assert self._app

        # get start time
        ll_start = time.time()

        # carrega o logo
        l_pix_logo = QtGui.QPixmap(os.path.join(self.dct_config["dir.img"], "merlinLogo_2.png"))
        assert l_pix_logo

        # cria a tela de apresentação
        l_splash = QtGui.QSplashScreen(l_pix_logo, QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)
        assert l_splash

        # cria a tela de apresentação
        l_splash.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # aplica a máscara
        l_splash.setMask(l_pix_logo.mask())

        # cria a fonte das mensagens
        l_font = QtGui.QFont(l_splash.font())
        assert l_font

        # ajusta tamanho da fonte
        l_font.setPointSize(l_font.pointSize() + 5)

        # configura a fonte
        l_splash.setFont(l_font)

        # exibe a tela de apresentação
        l_splash.show()

        # inicia o contador
        # l_count = 0

        # simulate something that takes time
        while (time.time() - ll_start) < 2:

            # trata os eventos(antes do loop principal)
            self._app.processEvents()

            # exibe a mensagem
            # l_splash.showMessage(l_splash.tr(u"Carregando as páginas %1...").arg(l_count),
            #     QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft, QtCore.Qt.white)

            # incrementa o contador
            # l_count += 1

            # simulate something that takes time
            time.sleep(0.001)

        # cria o configurador de simulação
        l_wzd = wizard.CDlgWizard(self.control)
        assert l_wzd

        # exibe o configurador de simulação
        l_wzd.show()

        # fecha a tela de apresentação
        l_splash.finish(l_wzd)

        # processa a aplicação
        self._app.exec_()

        # logger
        # M_LOG.info("run:<<")
                
# < the end >--------------------------------------------------------------------------------------
