#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model manager

DOCUMENT ME!

revision 0.4  2016/ago  mlabru
pequenas correções e otimização

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do event manager e config manager

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.4$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/08"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging

# control
import control.events.events_manager as event

import control.config.config_manager as config

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CModelManager >--------------------------------------------------------------------------

class CModelManager(object):
    """
    main model object. Views and controllers interact with this
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control):
        """
        initializes the model manager

        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input parameters
        assert f_control

        # salva o control manager localmente
        self.__control = f_control
        assert self.__control

        # salva o event manager localmente
        self.__event = f_control.event if f_control.event is not None else event.CEventsManager()
        assert self.__event

        # registra a sí próprio como recebedor de eventos
        self.__event.register_listener(self)

        # salva o config manager localmente
        self.__config = f_control.config if f_control.config is not None else config.CConfigManager()
        assert self.__config

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    # @ abstractmethod
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # logger
        # M_LOG.info("notify:><")

        # return
        pass

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def config(self):
        """
        get config manager
        """
        return self.__config

    # ---------------------------------------------------------------------------------------------

    @property
    def control(self):
        """
        get control manager
        """
        return self.__control

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_config(self):
        """
        get configuration dictionary
        """
        return self.__config.dct_config if self.__config is not None else {}

    # ---------------------------------------------------------------------------------------------

    @property
    def event(self):
        """
        get event manager
        """
        return self.__event

    @event.setter
    def event(self, f_val):
        """
        get event manager
        """
        self.__event = f_val

# < the end >--------------------------------------------------------------------------------------
