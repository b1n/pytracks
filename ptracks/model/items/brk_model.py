#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
brk_model.

mantém os detalhes de um breakpoint.

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

# < class CBrkModel >------------------------------------------------------------------------------

class CBrkModel(object):
    """
    mantém as informações específicas sobre um breakpoint.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CBrkModel, self).__init__()

        # flag ok (bool)
        self.__v_brk_ok = False

        # identificação do breakpoint
        self.__i_brk_id = 0

        # X (m)
        self.__f_brk_x = 0.
        # Y (m)
        self.__f_brk_y = 0.
        # Z (m)
        self.__f_brk_z = 0.

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy_brk(self, f_brk):
        """
        copy constructor.
        cria um novo breakpoint a partir de um outro breakpoint.

        @param f_brk: breakpoint a ser copiado.
        """
        # logger
        # M_LOG.info("copy_brk:>>")

        # verifica parâmetros de entrada
        assert f_brk

        # identificação
        self.__i_brk_id = f_brk.i_brk_id

        # X
        self.__f_brk_x = f_brk.f_brk_x
        # Y
        self.__f_brk_y = f_brk.f_brk_y
        # Z
        self.__f_brk_z = f_brk.f_brk_z

        # flag ok (bool)
        self.__v_brk_ok = f_brk.v_brk_ok

        # logger
        # M_LOG.info("copy_brk:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def v_brk_ok(self):
        """
        get flag ok
        """
        return self.__v_brk_ok

    @v_brk_ok.setter
    def v_brk_ok(self, f_val):
        """
        set flag ok
        """
        self.__v_brk_ok = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def i_brk_id(self):
        """
        get número do breakpoint
        """
        return self.__i_brk_id

    @i_brk_id.setter
    def i_brk_id(self, f_val):
        """
        set número do breakpoint
        """
        self.__i_brk_id = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_brk_x(self):
        """
        get X/longitude
        """
        return self.__f_brk_x

    @f_brk_x.setter
    def f_brk_x(self, f_val):
        """
        set X/longitude
        """
        self.__f_brk_x = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_brk_y(self):
        """
        get Y/latitude
        """
        return self.__f_brk_y

    @f_brk_y.setter
    def f_brk_y(self, f_val):
        """
        set Y/latitude
        """
        self.__f_brk_y = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_brk_z(self):
        """
        get Z
        """
        return self.__f_brk_z

    @f_brk_z.setter
    def f_brk_z(self, f_val):
        """
        set Z
        """
        self.__f_brk_z = f_val

# < the end >--------------------------------------------------------------------------------------
