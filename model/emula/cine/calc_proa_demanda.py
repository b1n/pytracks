#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
calc_proa_demanda

calcula a proa de demanda da aeronave

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
# import logging
import math

# model
import model.newton.defs_newton as ldefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------

def calc_proa_demanda(ff_pnt_delt_x, ff_pnt_delt_y):
    """
    calcula a proa de demanda da aeronave
    
    @param ff_pnt_delt_x: coordenada X da aeronave
    @param ff_pnt_delt_y: coordenada Y da aeronave
    
    @return proa de demanda
    """
    # logger
    # M_LOG.info("calc_proa_demanda:>>")
        
    # verifica coordenada x
    if ff_pnt_delt_x > 0.:

        # logger
        # M_LOG.info("calc_proa_demanda:<E01: ff_pnt_delt_x > 0.")

        # return
        return round(90. - math.degrees(math.atan(ff_pnt_delt_y / ff_pnt_delt_x)), 2)

    # verifica coordenada x
    if ff_pnt_delt_x < 0.:

        lf_ang_temp = 270. - math.degrees(math.atan(ff_pnt_delt_y / ff_pnt_delt_x))

        if lf_ang_temp >= 360.:

            # logger
            # M_LOG.info("calc_proa_demanda:<E02: lf_ang_temp >= 360.<")

            # return
            return round(lf_ang_temp - 360., 2)

        # logger
        # M_LOG.info("calc_proa_demanda:<E03: lf_ang_temp < 360.<")

        # return
        return round(lf_ang_temp, 2)

    # verifica coordenada y
    if ff_pnt_delt_y >= 0.:

        # logger
        # M_LOG.info("calc_proa_demanda:<E04: ff_pnt_delt_y > 0.")

        # return
        return 0.

    # logger
    # M_LOG.info("calc_proa_demanda:<<")

    # return
    return 180.

# < the end >--------------------------------------------------------------------------------------
