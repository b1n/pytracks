#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
config_visil.

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

# < import >---------------------------------------------------------------------------------------

# python library
import argparse
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

# < class CConfigVisil >---------------------------------------------------------------------------

class CConfigVisil(config.CConfigManager):
    """
    mantém as informações de configuração
    """
    # informações comuns de configuração
    __CFG_VISIL = {"tab.aer": "tabAer",    # tabela de aeródromos
                   "tab.esp": "tabEsp",    # tabela de esperas
                   "tab.fix": "tabFix",    # tabela de fixos
                   "tab.sub": "tabSub",    # tabela de subidas
                   "tab.trj": "tabTrj",    # tabela de trajetórias
                  }  # __CFG_VISIL

    # ---------------------------------------------------------------------------------------------

    def __init__(self, fs_cnfg):
        """
        constructor.
        inicia o gerente de configuração

        @param fs_cnfg: full path do arquivo de configuração
        """
        # logger
        # M_LOG.info("__init__:>>")

        # inicia a super class
        super(CConfigVisil, self).__init__(fs_cnfg)

        # herdados de CConfigManager
        # self.dct_config    # config manager data dictionary

        # carrega os atributos locais no dicionário de configuração
        for l_key in self.__CFG_VISIL.keys():
            if l_key not in self.dct_config:
                self.dct_config[l_key] = self.__CFG_VISIL[l_key]

        # cria um parser para os argumentos
        l_parser = argparse.ArgumentParser(description="VisIL (C) ICEA 2014-2016.")
        assert l_parser

        # argumento: canal de comunicação
        l_parser.add_argument("-c", "--canal",
                              dest="canal",
                              default=self.dct_config["glb.canal"],
                              help=u"Canal de comunicação (default: %d)" % int(self.dct_config["glb.canal"]))

        # faz o parser da linha de argumentos
        l_args = l_parser.parse_args()
        assert l_args

        # salva os argumentos no dicionário
        self.dct_config["glb.canal"] = abs(int(l_args.canal))

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

        # monta o diretório de airspaces
        self.dct_config["dir.air"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.air"]))

        # monta o diretório de exercícios
        self.dct_config["dir.exe"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.exe"]))

        # monta o diretório de imagens
        self.dct_config["dir.img"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.img"]))

        # monta o diretório de landscapes
        self.dct_config["dir.map"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.map"]))

        # monta o diretório de procedimentos
        self.dct_config["dir.prc"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.prc"]))
                                                                                                                                                                
        # monta o diretório de tabelas
        self.dct_config["dir.tab"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.tab"]))

        # logger
        # M_LOG.info("__load_dirs:<<")

# < the end >--------------------------------------------------------------------------------------
