#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
generate_prf_json.

DOCUMENT ME!

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
import json
import logging
import time

# model
import model.coords.coord_defs as cdefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# ------------------------------------------------------------------------------------------------

def generate_prf_json(fdct_prf, fs_prf):
    """
    DOCUMENT ME!
    """
    # logger
    # M_LOG.info("generate_prf_json:>>")

    # M_LOG.debug("generate_prf_json::fs_prf:[{}]".format(fs_prf))

    # performance existe no dicionário ?
    l_prf = fdct_prf.get(fs_prf, None)

    if l_prf is None:

        # logger
        l_log = logging.getLogger("generate_prf_json")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"E01: performance {} não existe no dicionário.".format(fs_prf))
                                                
        # return
        return None

    # monta um dicionário com a performance
    ldct_prf = { "teto_sv": int(l_prf.f_prf_teto_sv * cdefs.D_CNV_M2FT),                      # (m -> ft)
                 "vel_max_crz": int(l_prf.f_prf_vel_max_crz * cdefs.D_CNV_MS2KT),             # (m/s -> kt)
                 "raz_max_sub_crz": int(l_prf.f_prf_raz_max_sub_crz * cdefs.D_CNV_MS2FTMIN),  # (m/s -> ft/min)
                 "raz_max_des_crz": int(l_prf.f_prf_raz_max_des_crz * cdefs.D_CNV_MS2FTMIN),  # (m/s -> ft/min)
                 "raz_crv_rot": round(l_prf.f_prf_raz_crv_rot, 1),
               }

    ls_buf = json.dumps(ldct_prf)
    # M_LOG.debug("generate_prf_json:ls_buf:[{}]".format(ls_buf))

    # logger
    # M_LOG.info("generate_prf_json:<<")

    # return
    return ls_buf

# < the end >--------------------------------------------------------------------------------------
