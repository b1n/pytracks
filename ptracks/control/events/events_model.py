#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
events_model.

generic event super class.

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

# < module data >----------------------------------------------------------------------------------

# logging level
# M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# < class CEventsModel >---------------------------------------------------------------------------

class CEventsModel(object):
    """
    generic event super class.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CEventsModel, self).__init__()

        # event name
        self.__s_name = "Generic Event"

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __str__(self):
        """
        DOCUMENT ME!
        """
        return "<%s %s>" % (self.__class__.__name__, id(self))

    # ---------------------------------------------------------------------------------------------

    @property
    def s_name(self):
        """
        get event name
        """
        return self.__s_name

    @s_name.setter
    def s_name(self, f_val):
        """
        set event name
        """
        self.__s_name = f_val

# < the end >--------------------------------------------------------------------------------------
