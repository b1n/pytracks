#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
airspace_newton.

basic model manager
load from one configuration file all configured tables

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do event manager e config manager

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os

# model
from ..stock import airspace_basic as airs

from ..items import esp_data as espdata
from ..items import sub_data as subdata
from ..items import trj_data as trjdata

from ..newton import defs_newton as ldefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CAirspaceNewton >-------------------------------------------------------------------------

class CAirspaceNewton(airs.CAirspaceBasic):
    """
    newton airspace
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
        super(CAirspaceNewton, self).__init__(f_model)

        # herdado de CAirspaceBasic
        # self.model           # model manager 
        # self.event           # event manager
        # self.config          # config manager
        # self.dct_aer         # dicionário de aeródromos
        # self.dct_fix         # dicionário de fixos
        # self.dct_fix_indc    # dicionário de fixos por indicativo

        # procedimentos de espera
        self.__dct_esp = {}

        # procedimentos de subida
        self.__dct_sub = {}

        # procedimentos de trajetória
        self.__dct_trj = {}

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def get_aer_pst(self, fs_aer, fs_pst):
        """
        obtém o pointer para o aeródromo e pista

        @param fs_aer: indicativo do aeródromo
        @param fs_pst: indicativo da pista

        @return pointer para o aeródromo e pista
        """
        # logger
        # M_LOG.info("get_aer_pst:>>")

        # obtém o aeródromo
        l_aer = self.dct_aer.get(fs_aer, None)

        if l_aer is None:

            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_aer_pst")
            l_log.setLevel(logging.ERROR)
            l_log.error("E01: não existe aeródromo {}.".format(fs_aer))

            # retorna pointers
            return None, None

        # obtém a pista
        l_pst = l_aer.dct_aer_pistas.get(fs_pst, None)

        if l_pst is None:

            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_aer_pst")
            l_log.setLevel(logging.ERROR)
            l_log.error("E02: não existe pista {} no aeródromo {}.".format(fs_pst, fs_aer))

            # retorna pointers
            return l_aer, None

        # logger
        # M_LOG.info("get_aer_pst:<<")

        # retorna pointers
        return l_aer, l_pst

    # ---------------------------------------------------------------------------------------------

    def get_ptr_prc(self, fs_prc):
        """
        obtém o pointer e a função operacional de um procedimento

        @param fs_prc: procedimento no formato XXX9999

        @return pointer e função operacional
        """
        # logger
        # M_LOG.info("get_ptr_prc:>>")

        # não existe procedimento ?
        if fs_prc is None:

            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_ptr_prc")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E01: não existe procedimento.")

            # retorna pointer & função
            return None, ldefs.E_NOPROC

        # obtém o procedimento
        ls_prc = fs_prc[:3]
        # M_LOG.debug("get_ptr_prc:ls_prc: " + str(ls_prc))

        # obtém o número do procedimento
        li_num_prc = int(fs_prc[3:])
        # M_LOG.debug("get_ptr_prc:li_num_prc: " + str(li_num_prc))

        # é uma espera ?
        if "ESP" == ls_prc:

            # obtém o dicionário de espera
            ldct_esp = self.__dct_esp
            assert ldct_esp

            # obtém o procedimento de espera pelo número
            lptr_prc = ldct_esp.get(li_num_prc, None)
            # M_LOG.debug("get_ptr_prc:lptr_prc: " + str(lptr_prc))

            # função operacional da espera
            le_fnc_ope = ldefs.E_ESPERA if lptr_prc is not None else ldefs.E_NOPROC

        # é uma subida ?
        elif "SUB" == ls_prc:

            # obtém o dicionário de subidas
            ldct_sub = self.__dct_sub
            assert ldct_sub

            # obtém o procedimento de subida pelo número
            lptr_prc = ldct_sub.get(li_num_prc, None)
            # M_LOG.debug("get_ptr_prc:lptr_prc: " + str(lptr_prc))

            # função operacional da subidas
            le_fnc_ope = ldefs.E_SUBIDA if lptr_prc is not None else ldefs.E_NOPROC

        # é uma trajetória ?
        elif "TRJ" == ls_prc:

            # obtém o dicionário de trajetórias
            ldct_trj = self.__dct_trj
            assert ldct_trj

            # obtém o procedimento de trajetória pelo número
            lptr_prc = ldct_trj.get(li_num_prc, None)
            # M_LOG.debug("get_ptr_prc:lptr_prc: " + str(lptr_prc))

            # função operacional da trajetória
            le_fnc_ope = ldefs.E_TRAJETORIA if lptr_prc is not None else ldefs.E_NOPROC

        # senão, procedimento desconhecido
        else:
            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_ptr_prc")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E02: procedimento [{}] desconhecido. fallback to noProc.!".format(fs_prc))

            # sem procedimento
            lptr_prc = None
            le_fnc_ope = ldefs.E_NOPROC

        # função operacional sem procedimento ?
        if (lptr_prc is None) and (ldefs.E_NOPROC != le_fnc_ope):

            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_ptr_prc")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E03: função operacional:[{}] sem procedimento:[{}] ? " \
                        "Tem certeza que isto está correto ???".format(ls_prc, li_num_prc))

        # logger
        # M_LOG.info("get_ptr_prc:<<")

        # retorna pointer & função
        return lptr_prc, le_fnc_ope

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
        callback de tratamento de eventos recebidos.

        @param f_event: evento recebido.
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
