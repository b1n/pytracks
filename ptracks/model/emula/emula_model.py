#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
emula_model

the actual flight model

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging
import threading

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CEmulaModel >----------------------------------------------------------------------------

class CEmulaModel(threading.Thread):
    """
    the emula model class generates new flights and handles their movement. It has a list of
    flight objects holding all flights that are currently active
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_control):
        """
        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input parameters
        assert f_control
        assert f_model

        # init super class
        super(CEmulaModel, self).__init__()

        # salva o control manager localmente
        self.__control = f_control
        assert self.__control

        # salva o model manager localmente
        self.__model = f_model
        assert self.__model

        # initialize the dictionary for all active flights
        self.__dct_flight = {}

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def run(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("run:><")

        # return
        return False

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def config(self):
        """
        config manager
        """
        return self.__control.config

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_config(self):
        """
        dicionário de configuração
        """
        return self.__control.config.dct_config

    # ---------------------------------------------------------------------------------------------

    @property
    def control(self):
        """
        control manager
        """
        return self.__control

    # ---------------------------------------------------------------------------------------------

    @property
    def event(self):
        """
        event manager
        """
        return self.__control.event

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_flight(self):
        """
        dicionário de vôos ativos
        """
        return self.__dct_flight

    # ---------------------------------------------------------------------------------------------

    @property
    def model(self):
        """
        model manager
        """
        return self.__model

    # ---------------------------------------------------------------------------------------------
    '''
    @property
    def sim_time(self):
        """
        relógio da simulação
        """
        return self._sim_time
    '''
# < the end >--------------------------------------------------------------------------------------
