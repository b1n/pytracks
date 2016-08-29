#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
adiru.

represents air data inertial reference unit.

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
import copy
# import logging

# model
import model.coords.pos_lat_lng as pll

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CADIRU >---------------------------------------------------------------------------------

class CADIRU(object):
    """
    represents air data inertial reference unit
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # inicia a super classe
        super(CADIRU, self).__init__()

        # altitude
        self.__f_alt = 0.

        # instrument air speed
        self.__f_ias = 0.

        # proa em relação ao norte magnético
        self.__f_proa = 0.

        # proa em relação ao norte verdadeiro
        self.__f_true_heading = 0.

        # velocidade
        self.__f_vel = 0.

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy(self):
        """
        copy constructor.
        """
        # logger
        # M_LOG.info("copy:><")

        # return a copy
        return copy.deepcopy(self)

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_alt(self):
        """
        get altitude
        """
        return self.__f_alt
                                            
    @f_alt.setter
    def f_alt(self, f_val):
        """
        set altitude
        """
        self.__f_alt = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_ias(self):
        """
        get ias (instrument air speed)
        """
        return self.__f_ias
                                            
    @f_ias.setter
    def f_ias(self, f_val):
        """
        set ias (instrument air speed)
        """
        self.__f_ias = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_proa(self):
        """
        get proa
        """
        return self.__f_proa
                                            
    @f_proa.setter
    def f_proa(self, f_val):
        """
        set proa
        """
        # check input parameters
        assert 0. <= f_val <= 360.

        # save proa
        self.__f_proa = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_true_heading(self):
        """
        get true heading
        """
        return self.__f_true_heading
                                            
    @f_true_heading.setter
    def f_true_heading(self, f_val):
        """
        set true heading
        """
        # check input parameters
        assert 0. <= f_val <= 360.

        # save true heading
        self.__f_true_heading = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_vel(self):
        """
        get velocidade
        """
        return self.__f_vel
                                            
    @f_vel.setter
    def f_vel(self, f_val):
        """
        set velocidade
        """
        self.__f_vel = f_val

# < the end >--------------------------------------------------------------------------------------
