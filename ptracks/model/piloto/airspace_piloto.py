#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
airspace_piloto

basic model manager
load from one configuration file all configured tables

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
from ..stock import airspace_basic as airs

from ..items import esp_data as espdata
from ..items import sub_data as subdata
from ..items import trj_data as trjdata

# import model.piloto.defs_piloto as ldefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CAirspacePiloto >------------------------------------------------------------------------

class CAirspacePiloto(airs.CAirspaceBasic):
    """
    piloto airspace
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model):
        """
        @param f_model: model manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input parameters
        assert f_model

        # init super class
        super(CAirspacePiloto, self).__init__(f_model)

        # herdado de CAirspaceBasic
        # self.model           # model manager 
        # self.event           # event manager
        # self.config          # config manager
        # self.dct_aer         # dicionário de aeródromos
        # self.dct_fix         # dicionário de fixos
        # self.dct_fix_indc    # dicionário de fixos por indicativo
        # self.lst_arr_dep     # lista de pousos/decolagens

        # procedimentos de espera
        self.__dct_esp = {}

        # procedimentos de subida
        self.__dct_sub = {}

        # procedimentos de trajetória
        self.__dct_trj = {}

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def load_dicts(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("load_dicts:>>")

        # monta o nome da tabela de procedimentos de espera
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.esp"])

        # carrega a tabela de procedimentos de espera em um dicionário
        self.__dct_esp = espdata.CEspData(self.model, ls_path)
        assert self.__dct_esp is not None

        # monta o nome da tabela de procedimentos de subida
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.sub"])

        # carrega a tabela de procedimentos de subida em um dicionário
        self.__dct_sub = subdata.CSubData(self.model, ls_path)
        assert self.__dct_sub is not None

        # monta o nome da tabela de procedimentos de trajetória
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.trj"])

        # carrega a tabela de procedimentos de trajetória em um dicionário
        self.__dct_trj = trjdata.CTrjData(self.model, ls_path)
        assert self.__dct_trj is not None

        # resolve os procedimentos dos break-points
        # self.resolv_procs()

        # logger
        # M_LOG.info("load_dicts:<<")

    # ---------------------------------------------------------------------------------------------

    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # logger
        # M_LOG.info("notify:><")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_esp(self):
        """
        get esperas
        """
        return self.__dct_esp

    @dct_esp.setter
    def dct_esp(self, f_val):
        """
        set esperas
        """
        self.__dct_esp = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_sub(self):
        """
        get subidas
        """
        return self.__dct_sub

    @dct_sub.setter
    def dct_sub(self, f_val):
        """
        set subidas
        """
        self.__dct_sub = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_trj(self):
        """
        get trajetórias
        """
        return self.__dct_trj

    @dct_trj.setter
    def dct_trj(self, f_val):
        """
        set trajetórias
        """
        self.__dct_trj = f_val

# < the end >--------------------------------------------------------------------------------------
