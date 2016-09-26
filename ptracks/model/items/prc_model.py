#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_model.

mantém os detalhes de um procedimento.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/04"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CPrcModel >------------------------------------------------------------------------------

class CPrcModel(object):
    """
    mantém as informações específicas sobre procedimento.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # flag ok (bool)
        self.__v_prc_ok = False

        # identificação do procedimento
        self.__i_prc_id = 0

        # descrição do procedimento
        self.__s_prc_desc = ""

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy_prc(self, f_prc):
        """
        copy constructor.
        cria um novo procedimento a partir de outro procedimento.

        @param f_prc: procedimento a ser copiado.
        """
        # logger
        # M_LOG.info("copy_prc:>>")

        # verifica parâmetros de entrada
        assert f_prc

        # identificação do procedimento
        self.i_prc_id = f_prc.i_prc_id

        # descrição do procedimento
        self.s_prc_desc = f_prc.s_prc_desc

        # flag ok (bool)
        self.v_prc_ok = f_prc.v_prc_ok

        # logger
        # M_LOG.info("copy_prc:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def s_prc_desc(self):
        """
        get descrição
        """
        return self.__s_prc_desc  # .decode ( "utf-8" )

    @s_prc_desc.setter
    def s_prc_desc(self, f_val):
        """
        set descrição
        """
        self.__s_prc_desc = f_val.strip()  # .encode ( "utf-8" )

    # ---------------------------------------------------------------------------------------------

    @property
    def i_prc_id(self):
        """
        get identificação do procedimento (indicativo)
        """
        return self.__i_prc_id

    @i_prc_id.setter
    def i_prc_id(self, f_val):
        """
        set identificação do procedimento (indicativo)
        """
        self.__i_prc_id = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def v_prc_ok(self):
        """
        get flag ok
        """
        return self.__v_prc_ok

    @v_prc_ok.setter
    def v_prc_ok(self, f_val):
        """
        set flag ok
        """
        self.__v_prc_ok = f_val

# < the end >--------------------------------------------------------------------------------------
