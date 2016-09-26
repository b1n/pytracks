#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pos_xy.

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

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CPosXY >---------------------------------------------------------------------------------

class CPosXY(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, ff_x=0., ff_y=0.):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        # assert f_control

        # inicia a super classe
        super(CPosXY, self).__init__()

        self.__f_x = ff_x
        # M_LOG.info("self._f_x:[%f]" % self._f_x)

        self.__f_y = ff_y
        # M_LOG.info("self._f_y:[%f]" % self._f_y)

        # logger
        # M_LOG.info("__init__:<<")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_x(self):
        """
        get X
        """
        return self.__f_x
                                            
    @f_x.setter
    def f_x(self, f_val):
        """
        set X
        """
        self.__f_x = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_y(self):
        """
        get Y
        """
        return self.__f_y
                                            
    @f_y.setter
    def f_y(self, f_val):
        """
        set Y
        """
        self.__f_y = f_val

# < the end >--------------------------------------------------------------------------------------
