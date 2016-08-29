#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pst_model

mantém os detalhes de um pista

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

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CPstModel >------------------------------------------------------------------------------

class CPstModel(object):
    """
    mantém as informações específicas sobre pista
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # flag ok (bool)
        self.__v_pst_ok = False
        # identificação do pista (indicativo)
        self.__s_pst_indc = ""

        # rumo magnético da pista
        self.__i_pst_rumo = 0

        # X (m)
        self.__f_pst_x = 0.
        # Y (m)
        self.__f_pst_y = 0.
        # Z (m)
        self.__f_pst_z = 0.

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy_pst(self, f_pst):
        """
        copy constructor
        cria uma nova pista a partir de uma outra pista

        @param f_pst: pista a ser copiada
        """
        # logger
        # M_LOG.info("copy_pst:>>")

        # verifica parâmetros de entrada
        assert f_pst

        # identificação da pista
        self.__s_pst_indc = f_pst.s_pst_indc
        # rumo da pista
        self.__i_pst_rumo = f_pst.i_pst_rumo

        # X
        self.__f_pst_x = f_pst.f_pst_x
        # Y
        self.__f_pst_y = f_pst.f_pst_y
        # Z
        self.__f_pst_z = f_pst.f_pst_z

        # flag ok (bool)
        self.__v_pst_ok = f_pst.v_pst_ok

        # logger
        # M_LOG.info("copy_pst:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def s_pst_indc(self):
        """
        get identificação da pista (indicativo)
        """
        return self.__s_pst_indc  # .decode ( "utf-8" )

    @s_pst_indc.setter
    def s_pst_indc(self, f_val):
        """
        set identificação da pista (indicativo)
        """
        self.__s_pst_indc = f_val.strip().upper()  # .encode ( "utf-8" )

    # ---------------------------------------------------------------------------------------------

    @property
    def v_pst_ok(self):
        """
        get flag pista ok
        """
        return self.__v_pst_ok

    @v_pst_ok.setter
    def v_pst_ok(self, f_val):
        """
        set flag pista ok
        """
        self.__v_pst_ok = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def i_pst_rumo(self):
        """
        get rumo magnético da pista
        """
        return self.__i_pst_rumo

    @i_pst_rumo.setter
    def i_pst_rumo(self, f_val):
        """
        set rumo magnético da pista
        """
        self.__i_pst_rumo = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_pst_x(self):
        """
        get X
        """
        return self.__f_pst_x

    @f_pst_x.setter
    def f_pst_x(self, f_val):
        """
        set X
        """
        self.__f_pst_x = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_pst_y(self):
        """
        get Y
        """
        return self.__f_pst_y

    @f_pst_y.setter
    def f_pst_y(self, f_val):
        """
        set Y
        """
        self.__f_pst_y = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_pst_z(self):
        """
        get Z
        """
        return self.__f_pst_z

    @f_pst_z.setter
    def f_pst_z(self, f_val):
        """
        set Z
        """
        self.__f_pst_z = f_val

# < the end >--------------------------------------------------------------------------------------
