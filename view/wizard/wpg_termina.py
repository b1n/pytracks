#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wpg_termina.
DOCUMENT ME!

revision 0.2  2015/dez  mlabru
pep8 style conventions
    
revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/01"
            
# < imports >--------------------------------------------------------------------------------------

# python library
# import logging

# PyQt library
from PyQt4 import QtCore, QtGui

# view / wizard
import view.wizard.wizard_page_model as wpm
import view.wizard.wpg_termina_ui as wterm_ui

# < module data >----------------------------------------------------------------------------------

# logging level
# M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# < class CWPagTermina >---------------------------------------------------------------------------


class CWPagTermina(wpm.CWizardPageModel, wterm_ui.Ui_WPagTermina):

    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_dlg_wizard=None):
        """
        initializes the wizard.

        @param  f_dlg_wizard : DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__init__:>>")

        # inicia super classe
        super(CWPagTermina, self).__init__(f_dlg_wizard)

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
        verifica se a form está aceitável.
        """
        # logger
        # M_LOG.info("is_complete:><")

        # verifica condições de execução
        assert self.ckbAgree
        return self.ckbAgree.isChecked()

    # ---------------------------------------------------------------------------------------------

    def is_last_page(self):

        # logger
        # M_LOG.info("is_last_page:><")

        return True

    # ---------------------------------------------------------------------------------------------

    def reset_page(self):
        """
        reseta os campos da form.
        """
        # logger
        # M_LOG.info("reset_page:>>")

        # exercício
        self.txtExe.setText(str(self.dct_config["glb.exe"].s_exe_id))

        # canal de comunicação
        self.txtCanal.setText(str(self.dct_config["glb.canal"]))

        # check box
        self.ckbAgree.setChecked(False)

        # logger
        # M_LOG.info("reset_page:<<")

    # ---------------------------------------------------------------------------------------------

    def setup_connects(self):
        """
        configura as conexões slot/signal.
        """
        # logger
        # M_LOG.info("setup_connects:>>")

        self.connect(self.ckbAgree, QtCore.SIGNAL("toggled(bool)"),
                     self, QtCore.SIGNAL("completeStateChanged()"))

        # logger
        # M_LOG.info("setup_connects:<<")

# < the end >--------------------------------------------------------------------------------------
