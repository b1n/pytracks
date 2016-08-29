#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
config_dbedit.

mantém as informações de configuração do editor da base de dados.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging
import os

# model
import model.data as data

# control
import control.config.config_manager as config

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CConfigDBEdit >--------------------------------------------------------------------------

class CConfigDBEdit(config.CConfigManager):
    """
    mantém as informações de configuração do editor da base de dados
    """
    # informações comuns de configuração
    __CFG_DBEDIT = {"glb.exe": None,    # exercício

                    "tab.aer": "tabAer",    # tabela de aeródromos
                    "tab.esp": "tabEsp",    # tabela de procedimentos de espera
                    "tab.fix": "tabFix",    # tabela de fixos
                    "tab.prf": "tabPrf",    # tabela de performances
                    "tab.sub": "tabSub",    # tabela de procedimentos de subida
                    "tab.trj": "tabTrj",    # tabela de procedimentos de trajetória
                   }  # __CFG_DBEDIT

    # ---------------------------------------------------------------------------------------------

    def __init__(self, fs_path):
        """
        inicia o gerente de configuração do editor da base de dados

        @param fs_path: full path do arquivo de configuração
        """
        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CConfigDBEdit, self).__init__(fs_path)

        # herdados de CConfigManager
        # self.dct_config    # config manager data dictionary

        # carrega os atributos locais no dicionário de configuração
        for l_key in self.__CFG_DBEDIT.keys():
            if l_key not in self.dct_config:
                self.dct_config[l_key] = self.__CFG_DBEDIT[l_key]

        # load dirs section
        self.__load_dirs()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __load_dirs(self):
        """
        carrega as configurações de diretórios
        """
        # logger
        # M_LOG.info("__load_dirs:>>")

        # monta o diretório de exercícios
        self.dct_config["dir.exe"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.exe"]))

        # monta o diretório de procedimentos
        self.dct_config["dir.prc"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.prc"]))

        # monta o diretório de tabelas
        self.dct_config["dir.tab"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.tab"]))

        # monta o diretório de tráfegos
        self.dct_config["dir.trf"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.trf"]))

        # logger
        # M_LOG.info("__load_dirs:<<")

# < the end >--------------------------------------------------------------------------------------
