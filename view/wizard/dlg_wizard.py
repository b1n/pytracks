#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_wizard.
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

# model
import model.glb_data as gdata

# view / wizard
import view.wizard.wizard_model as model
import view.wizard.wpg_config_canal as wcanal
import view.wizard.wpg_config_exe as wexe
import view.wizard.wpg_termina as wterm

# < module data >----------------------------------------------------------------------------------

# logging level
# M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# < class CDlgWizard >-----------------------------------------------------------------------------


class CDlgWizard(model.CWizardModel):
    """
    initializes the wizard.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_parent=None):
        """
        initializes the wizard.
        """
        # logger
        # M_LOG.info("__init__:>>")
                
        # inicia a super classe
        super(CDlgWizard, self).__init__(f_parent)

        # obtém o dicionário de configuração
        self.__dct_config = f_control.config.dct_config
        assert self.__dct_config

        # página de configuração do canal de comunicação
        self._pagCanal = wcanal.CWPagConfigCanal(f_control, self)
        assert self._pagCanal

        # página de configuração de exercício
        self._pagConfigExe = wexe.CWPagConfigExe(f_control, self)
        assert self._pagConfigExe

        # página de confirmação
        self._pagTermina = wterm.CWPagTermina(f_control, self)
        assert self._pagTermina

        # primeira página (entry-point)
        self.setFirstPage(self._pagConfigExe)

        # geometria da janela
        self.setWindowTitle(self.tr(u"Gerador de Pistas [ Configurador de Simulação ]"))
        self.resize(660, 520)

        # logger
        # M_LOG.info("__init__:<<")
                
    # ---------------------------------------------------------------------------------------------

    def accept(self):
        """
        initializes the wizard.
        """
        # logger
        # M_LOG.info("accept:>>")
                
        # finaliza o sistema
        self.close()

        # obtém o exercício
        l_exe = self.__dct_config["glb.exe"]
        assert l_exe

        # obtém o canal
        li_canal = int(self.__dct_config["glb.canal"])
        assert 2 < li_canal < 201

        # parâmetros do simulador
        l_args = ["-e", "%s" % (l_exe.s_exe_id), "-c", "%d" % (li_canal)]

        # executa o simulador
        # os.execlp("python", "python", "-OO", "newton.py", *l_args)
        os.execlp("sh", "sh", "newton", *l_args)

        # logger
        # M_LOG.info("accept:<<")
                
# < the end >--------------------------------------------------------------------------------------
