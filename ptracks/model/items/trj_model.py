#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
trj_model.

mantém os detalhes de um procedimento de trajetória.

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

# < class CTrjModel >------------------------------------------------------------------------------

class CTrjModel(object):
    """
    mantém as informações específicas sobre procedimento de trajetória.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # flag ok (bool)
        self.__v_trj_ok = False

        # identificação do procedimento de trajetória
        self.__i_trj_id = 0

        # descrição do procedimento de trajetória
        self.__s_trj_desc = ""

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy_trj(self, f_trj):
        """
        copy constructor.
        cria uma nova procedimento de trajetória a partir de uma outra procedimento de trajetória.

        @param f_trj: procedimento de trajetória a ser copiada.
        """
        # logger
        # M_LOG.info("copy_trj:>>")

        # verifica parâmetros de entrada
        assert f_trj

        # identificação do procedimento de trajetória
        self.i_trj_id = f_trj.i_trj_id

        # descrição do procedimento de trajetória
        self.s_trj_desc = f_trj.s_trj_desc

        # flag ok (bool)
        self.v_trj_ok = f_trj.v_trj_ok

        # logger
        # M_LOG.info("copy_trj:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def s_trj_desc(self):
        """
        get descrição
        """
        return self.__s_trj_desc  # .decode ( "utf-8" )

    @s_trj_desc.setter
    def s_trj_desc(self, f_val):
        """
        set descrição
        """
        self.__s_trj_desc = f_val.strip()  # .encode ( "utf-8" )

    # ---------------------------------------------------------------------------------------------

    @property
    def i_trj_id(self):
        """
        get identificação do procedimento de trajetória (indicativo)
        """
        return self.__i_trj_id

    @i_trj_id.setter
    def i_trj_id(self, f_val):
        """
        set identificação do procedimento de trajetória (indicativo)
        """
        self.__i_trj_id = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def v_trj_ok(self):
        """
        get flag ok
        """
        return self.__v_trj_ok

    @v_trj_ok.setter
    def v_trj_ok(self, f_val):
        """
        set flag ok
        """
        self.__v_trj_ok = f_val

# < the end >--------------------------------------------------------------------------------------
