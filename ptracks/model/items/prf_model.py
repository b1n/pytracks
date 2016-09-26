#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prf_model.
mantém os detalhes de uma família de performance.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
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
# M_LOG.setLevel(# M_LOG_LVL)

# < class CPrfModel >------------------------------------------------------------------------------


class CPrfModel(object):
    """
    mantém as informações específicas sobre performance.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # flag ok (bool)
        self.__v_prf_ok = False

        # identificação da performance
        self.__s_prf_id = ""

        # descrição da performance
        self.__s_prf_desc = ""

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy_prf(self, f_prf):
        """
        copy constructor.
        cria uma nova performance a partir de uma outra performance.

        @param f_prf: performance a ser copiada.
        """
        # logger
        # M_LOG.info("copy_prf:>>")

        # verifica parâmetros de entrada
        assert f_prf

        # identificação da performance
        self.__s_prf_id = f_prf.s_prf_id

        # descrição da performance
        self.__s_prf_desc = f_prf.s_prf_desc

        # flag ok (bool)
        self.__v_prf_ok = f_prf.v_prf_ok

        # logger
        # M_LOG.info("copy_prf:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def s_prf_desc(self):
        """
        get descrição
        """
        return self.__s_prf_desc.strip().decode("utf-8")

    @s_prf_desc.setter
    def s_prf_desc(self, f_val):
        """
        set descrição
        """
        self.__s_prf_desc = f_val.strip().encode("utf-8")

    # ---------------------------------------------------------------------------------------------

    @property
    def s_prf_id(self):
        """
        get ID
        """
        return self.__s_prf_id.strip().decode("utf-8")

    @s_prf_id.setter
    def s_prf_id(self, f_val):
        """
        set ID
        """
        self.__s_prf_id = f_val.strip().upper().encode("utf-8")

    # ---------------------------------------------------------------------------------------------

    @property
    def v_prf_ok(self):
        """
        get flag ok
        """
        return self.__v_prf_ok

    @v_prf_ok.setter
    def v_prf_ok(self, f_val):
        """
        set flag ok
        """
        self.__v_prf_ok = f_val

# < the end >--------------------------------------------------------------------------------------
