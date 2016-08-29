#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
events_config.

generic event superclass. What follows is a list of all events. None of these classes should
perform any tasks, as that could introduce vulnerabilities.

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

# control
import control.events.events_model as model

# < class CConfigExe >-----------------------------------------------------------------------------

class CConfigExe(model.CEventsModel):
    """
    CConfigExe event class.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, ls_exe):
        """
        DOCUMENT ME!
        """
        # init super class
        super(CConfigExe, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        self.s_name = "ConfigExe event"
        self.__s_exe = ls_exe

    # ---------------------------------------------------------------------------------------------
    
    @property
    def s_exe(self):
        """
        get exercício
        """
        return self.__s_exe

# < class CConfigHora >-----------------------------------------------------------------------------

class CConfigHora(model.CEventsModel):
    """
    CConfigHora event class.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, lt_hora):
        """
        DOCUMENT ME!
        """
        # init super class
        super(CConfigHora, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        self.s_name = "ConfigHora event"
        self.__t_hora = lt_hora

    # ---------------------------------------------------------------------------------------------
    
    @property
    def t_hora(self):
        """
        get horário
        """
        return self.__t_hora

# < the end >--------------------------------------------------------------------------------------
