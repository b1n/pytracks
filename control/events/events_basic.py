#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
events_basic

what follows is a list of all events. None of these classes should perform any tasks, as that
could introduce vulnerabilities if and when I write the netcode

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

# events
import control.events.events_model as model

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CChange >----------------------------------------------------------------------------------

class CChange(model.CEventsModel):
    """
    data changed event class
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CChange, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        self.s_name = "Data Changed Event."

        # logger
        # M_LOG.info("__init__:<<")

# < class CQuit >----------------------------------------------------------------------------------

class CQuit(model.CEventsModel):
    """
    program quit event class
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CQuit, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        self.s_name = "Program Quit Event."

        # logger
        # M_LOG.info("__init__:<<")

# < class CSave2Disk >-----------------------------------------------------------------------------

class CSave2Disk(model.CEventsModel):
    """
    program save to disk event class
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, fs_table):

        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CSave2Disk, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        self.s_name = "Program Save2Disk Event."
        self.__s_table = fs_table

        # logger
        # M_LOG.info("__init__:<<")

# < class CTick >----------------------------------------------------------------------------------

class CTick(model.CEventsModel):
    """
    CPU tick event class
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CTick, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        self.s_name = "CPU Tick Event."

        # logger
        # M_LOG.info("__init__:<<")

# < the end >--------------------------------------------------------------------------------------
