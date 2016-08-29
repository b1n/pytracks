#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
standard_route.
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

# python library
import logging

# < module data >----------------------------------------------------------------------------------

# logging level
# M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# < class CStandardRoute >-------------------------------------------------------------------------


class CStandardRoute(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__init__:>>")

        # inicia a super classe
        super(CStandardRoute, self).__init__()

        # route name
        self.__s_name = None

        self.__lst_items = []
        self.__lst_runways = []

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def addItem(self, f_item):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("addItem:><")

        # verifica parâmetros de entrada
        # assert f_control

        self.__lst_items.append(f_item)

    # ---------------------------------------------------------------------------------------------

    def addRunway(self, fs_rwy):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("addRunway:><")

        # verifica parâmetros de entrada
        # assert f_control

        self.__lst_runways.append(fs_rwy)
        # M_LOG.info("fs_rwy: %s added." % fs_rwy)

    # ---------------------------------------------------------------------------------------------

    def belongsToRunway(self, fs_rwy):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("belongsToRunway:><")

        # return
        return fs_rwy in self.__lst_runways

    # ---------------------------------------------------------------------------------------------

    def getItem(self, fi_ndx):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("getItem:><")

        # verifica parâmetros de entrada
        if fi_ndx >= len(self.__lst_items):
            return None

        # verifica condições de execuçao
        if not self.__lst_items:
            return None

        # return
        return self.__lst_items[fi_ndx]

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def lst_items(self):
        """
        get list items
        """
        return self.__lst_items
                                            
    @lst_items.setter
    def lst_items(self, f_val):
        """
        set list items
        """
        self.__lst_items = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def s_name(self):
        """
        get name
        """
        return self.__s_name
                                            
    @s_name.setter
    def s_name(self, f_val):
        """
        set name
        """
        self.__s_name = f_val

# < the end >--------------------------------------------------------------------------------------
