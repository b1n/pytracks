#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_manager

DOCUMENT ME!

revision 0.3  2016/ago  mlabru
pequenas correções e otimizações

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/08"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CViewManager >---------------------------------------------------------------------------

class CViewManager(object):
    """
    handles all interaction with user. This class is the interface
    It draws the scope on the screen and handles all mouse input
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control):
        """
        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")
                
        # check input parameters
        assert f_control

        # salva o control manager localmente
        self.__control = f_control

        # salva o model manager localmente
        self.__model = f_control.model
        assert self.__model
                                                        
        # obtém o event manager
        self.__event = f_control.event
        assert self.__event
                                                                                
        # registra a sí próprio como recebedor de eventos
        self.__event.register_listener(self)
                                                                                                
        # obtém o config manager
        self.__config = f_control.config
        assert self.__config

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    # @abstractmethod
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos.

        @param f_event: evento recebido.
        """
        # logger
        # M_LOG.info("notify:><")
        pass

    # ---------------------------------------------------------------------------------------------

    # @abstractmethod
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
        get config manager
        """
        return self.__control.config

    @config.setter
    def config(self, f_val):
        """
        set config manager
        """
        # check input parameters
        assert f_val

        # save config manager
        self.__control.config = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_config(self):
        """
        get configuration dictionary
        """
        return self.__control.config.dct_config

    @dct_config.setter
    def dct_config(self, f_val):
        """
        set configuration dictionary
        """
        # check input parameters
        assert f_val

        # save configuration dictionary
        self.__control.config.dct_config = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def control(self):
        """
        get control manager
        """
        return self.__control

    @control.setter
    def control(self, f_val):
        """
        set control manager
        """
        # check input parameters
        assert f_val

        # save control manager
        self.__control = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def event(self):
        """
        get event manager
        """
        return self.__control.event

    @event.setter
    def event(self, f_val):
        """
        set event manager
        """
        # check input parameters
        assert f_val

        # save event manager
        self.__control.event = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def model(self):
        """
        get model manager
        """
        return self.__control.model

    @model.setter
    def model(self, f_val):
        """
        set model manager
        """
        # check input parameters
        assert f_val

        # save model manager
        self.__control.model = f_val

# < the end >--------------------------------------------------------------------------------------
