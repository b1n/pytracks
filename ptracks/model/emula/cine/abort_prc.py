#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
abort_prc

força a aeronave abandonar o procedimento

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# model
from ...newton import defs_newton as ldefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------

def abort_prc(f_atv):
    """
    força a aeronave abandonar o procedimento
    """
    # logger
    # M_LOG.info("abort_prc:>>")

    # verifica parâmetros de entrada
    assert f_atv

    # força a aeronave abandonar o procedimento
    f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
    f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
    f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu

    # f_atv.f_atv_vel_mac_dem = f_atv.f_atv_vel_mac_atu

    f_atv.ptr_atv_brk = None
    f_atv.ptr_trf_prc = None

    f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
    f_atv.en_atv_fase    = ldefs.E_FASE_ZERO

    # logger
    # M_LOG.info("abort_prc:<<")

# < the end >--------------------------------------------------------------------------------------
