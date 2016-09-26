#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
instruction.

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

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CInstruction >----------------------------------------------------------------------------

class CInstruction(object):
    """
    DOCUMENT ME
    """
    # ---------------------------------------------------------------------------------------------

    # C_APPROACH = 0
    # C_DIRECT = 1
    # C_HDG = 2
    # C_HOLD = 3
    # C_ROUTE = 4

    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        # assert f_control

        # inicia a super classe
        super(CInstruction, self).__init__()

        # comando
        self.__en_cmd_ope = None

        # parâmetros
        self.__f_param_1 = None
        self.__f_param_2 = None
        self.__f_param_3 = None

        # texto da instrução
        self.__s_text = None
 
        # flag running
        self.__v_running = False

        # self.__i_type = 0
        # self.__f_number = 0.
        # self.__o_react_time = None

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __repr__(self):

        # logger
        # M_LOG.info("__repr__:><")
        
        # return
        return "%s(%r)" % (self.__class__, self.__s_text)

    # ---------------------------------------------------------------------------------------------

    def __str__(self):

        # logger
        # M_LOG.info("__str__:><")
        
        # return
        return "instruction:{}".format(self.__s_text)

    # =============================================================================================
    # data
    # =============================================================================================
            
    # ---------------------------------------------------------------------------------------------
                
    @property
    def en_cmd_ope(self):
        """
        get comando operacional
        """
        return self.__en_cmd_ope
                                                        
    @en_cmd_ope.setter
    def en_cmd_ope(self, f_val):
        """
        set comando operacional
        """
        self.__en_cmd_ope = f_val
                                                        
    # ---------------------------------------------------------------------------------------------
                
    @property
    def f_param_1(self):
        """
        get parâmetro 1
        """
        return self.__f_param_1
                                                        
    @f_param_1.setter
    def f_param_1(self, f_val):
        """
        set parâmetro 1
        """
        self.__f_param_1 = f_val
                                                        
    # ---------------------------------------------------------------------------------------------
                
    @property
    def f_param_2(self):
        """
        get parâmetro 2
        """
        return self.__f_param_2
                                                        
    @f_param_2.setter
    def f_param_2(self, f_val):
        """
        set parâmetro 2
        """
        self.__f_param_2 = f_val
                                                        
    # ---------------------------------------------------------------------------------------------
                
    @property
    def f_param_3(self):
        """
        get parâmetro 3
        """
        return self.__f_param_3
                                                        
    @f_param_3.setter
    def f_param_3(self, f_val):
        """
        set parâmetro 3
        """
        self.__f_param_3 = f_val
                                                        
    # ---------------------------------------------------------------------------------------------
                
    @property
    def v_running(self):
        """
        get flag running
        """
        return self.__v_running
                                                        
    @v_running.setter
    def v_running(self, f_val):
        """
        set flag running
        """
        self.__v_running = f_val
                                                        
    # ---------------------------------------------------------------------------------------------
                
    @property
    def s_text(self):
        """
        get textual
        """
        return self.__s_text
                                                        
    @s_text.setter
    def s_text(self, f_val):
        """
        set textual
        """
        self.__s_text = f_val
                                                        
# < the end >--------------------------------------------------------------------------------------
