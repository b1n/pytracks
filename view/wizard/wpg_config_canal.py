#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wpg_config_canal

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

# PyQt library
from PyQt4 import QtCore, QtGui

# view / wizard
from . import wizard_page_model as wpm
from . import wpg_config_canal_ui as wcanal_ui

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CWPagConfigCanal >-----------------------------------------------------------------------


class CWPagConfigCanal(wpm.CWizardPageModel, wcanal_ui.Ui_WPagConfigCanal):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_dlg_wizard=None):
        """
        initializes the wizard
        """
        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CWPagConfigCanal, self).__init__(f_dlg_wizard)

        # herdados de CWizardPageModel
        # self.dct_config    # dicionário de configuração
        # self.dlg_wizard    # dialog wizard

        # obtém o gerente de configuração
        l_config = f_control.config
        assert l_config

        # obtém o dicionário de configuração
        self.dct_config = l_config.dct_config
        assert self.dct_config

        # monta a widget
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.setup_connects()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def is_complete(self):
        """
        verifica se a form está aceitável
        """
        # logger
        # M_LOG.info("is_complete:><")

        # retorna
        return "" != self.qsbCanal.cleanText()

    # ---------------------------------------------------------------------------------------------

    def next_page(self):
        """
        próxima página na seqüência do wizard
        """
        # logger
        # M_LOG.info("next_page:><")

        # salva os valores
        self.dct_config["glb.canal"] = str(self.qsbCanal.value())

        # retorna a próxima página
        return self.dlg_wizard._pagTermina

    # ---------------------------------------------------------------------------------------------

    def reset_page(self):
        """
        reseta os campos da form
        """
        # logger
        # M_LOG.info("reset_page:><")

        # reseta os campos da form
        self.qsbCanal.setValue(int(self.dct_config["glb.canal"]))

    # ---------------------------------------------------------------------------------------------

    def setup_connects(self):
        """
        configura as conexões slot/signal
        """
        # logger
        # M_LOG.info("setup_connects:>>")

        self.connect(self.qsbCanal, QtCore.SIGNAL("valueChanged(QString)"),
                     self, QtCore.SIGNAL("completeStateChanged()"))

        # logger
        # M_LOG.info("setup_connects:<<")

# < the end >--------------------------------------------------------------------------------------
