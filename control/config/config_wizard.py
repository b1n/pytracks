#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
config_wizard.

DOCUMENT ME!

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < import >---------------------------------------------------------------------------------------

# python library
# import logging
import os

# model
from ...model import data as data

# control
from ...control.config import config_manager as config

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CConfigWizard >---------------------------------------------------------------------------

class CConfigWizard(config.CConfigManager):
    """
    mantém as informações de configuração do wizard
    """
    # informações comuns de configuração
    __CFG_WIZARD = {"glb.exe": None,      # exercício
                   }  # __CFG_WIZARD

    # ---------------------------------------------------------------------------------------------

    def __init__(self, fs_config):
        """
        inicia o gerente de configuração do wizard

        @param fs_config: full path do arquivo de configuração
        """
        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CConfigWizard, self).__init__(fs_config)

        # herdados de CConfigManager
        # self.dct_config    # config manager data dictionary

        # carrega os atributos locais no dicionário de configuração
        for l_key in self.__CFG_WIZARD.keys():
            if l_key not in self.dct_config:
                self.dct_config[l_key] = self.__CFG_WIZARD[l_key]

        # load dirs section
        self.__load_dirs()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __load_dirs(self):
        """
        carrega as configurações de diretórios.
        """
        # logger
        # M_LOG.info("__load_dirs:>>")

        # monta o diretório de imagens
        self.dct_config["dir.exe"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.exe"]))

        # monta o diretório de imagens
        self.dct_config["dir.img"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.img"]))

        # logger
        # M_LOG.info("__load_dirs:<<")

# < the end >--------------------------------------------------------------------------------------
