#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
fix.

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

# model
import model.coords.pos_lat_lng as pll

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CFix >-----------------------------------------------------------------------------------

class CFix(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, fs_fix_indc="NONAME", ff_fix_lat=0., ff_fix_lng=0.):
        """
        define um navaid
                
        @param fs_fix_indc: nome
        @param ff_fix_lat: latitude
        @param ff_fix_lng: longitude
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        # assert f_control

        # inicia a super classe
        super(CFix, self).__init__()

        self.__s_indc = fs_fix_indc
        # M_LOG.info("self.__s_indc: %s" % self.__s_indc)

        self.__position = pll.CPosLatLng(ff_fix_lat, ff_fix_lng)
        assert self.__position

        # logger
        # M_LOG.info("__init__:<<")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    
    @property
    def s_indc(self):
        """
        get indicativo
        """
        return self.__s_indc
                                            
    @s_indc.setter
    def s_indc(self, f_val):
        """
        set indicativo
        """
        self.__s_indc = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def position(self):
        """
        get posição
        """
        return self.__position
                                            
    @position.setter
    def position(self, f_val):
        """
        set posição
        """
        self.__position = f_val

# < the end >--------------------------------------------------------------------------------------
