#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
flight_plan_item.
DOCUMENT ME!

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# Python library
import logging

# < module data >----------------------------------------------------------------------------------

# logging level
# M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(# M_LOG_LVL)

# < class CFlightPlanItem >------------------------------------------------------------------------


class CFlightPlanItem(object):

    _EXACTLY = 0
    _OR_BELOW = 1
    _OR_ABOVE = 2

    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # logger
        # M_LOG.info("__init__:>>")

        self.__s_name = None

        self._fInbound = -1.

        self._iAltConstraint = 0
        self._iAltConstraintType = 0
        self._iSpeedConstraint = 0

        self._vFlyOver = False
        self._vApproach = False

        # logger
        # M_LOG.info("__init__:<<")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    
    @property
    def s_name(self):
        """
        get latitude
        """
        return self.__s_name
                                            
    @s_name.setter
    def s_name(self, f_val):
        """
        set latitude
        """
        self.__s_name = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_lng(self):
        """
        get longitude
        """
        return self.__f_lng
                                            
    @f_lng.setter
    def f_lng(self, f_val):
        """
        set longitude
        """
        self.__f_lng = f_val

# < the end >--------------------------------------------------------------------------------------
