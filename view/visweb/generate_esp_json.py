#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
generate_esp_json

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

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# ------------------------------------------------------------------------------------------------

def generate_esp_json(fdct_esp, fs_esp=None):
    """
    DOCUMENT ME!
    """
    # logger
    # M_LOG.info("generate_esp_json:>>")

    # inicia dicionário local
    ldct_esp = {}

    # espera específica ?
    if fs_esp is not None:

        # espera existe no dicionário ?
        l_esp = fdct_esp.get(fs_esp, None)

        if l_esp is None:

            # logger
            l_log = logging.getLogger("generate_esp_json")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"E01: espera {} não existe no dicionário.".format(fs_esp))
                                                    
            # return
            return None

        # coloca a espera no dicionário local
        ldct_esp[fs_esp] = l_esp.s_prc_desc

    # senão, todo dicionário
    else:
        # para todas as esperas...
        for l_key, l_esp in fdct_esp.items():

            # coloca a espera no dicionário local
            ldct_esp[l_key] = l_esp.s_prc_desc

    # monta buffer
    ls_buf = json.dumps(ldct_esp)
    # M_LOG.debug("generate_esp_json:ls_buf:[{}]".format(ls_buf))

    # logger
    # M_LOG.info("generate_esp_json:<<")

    # return
    return ls_buf

# < the end >--------------------------------------------------------------------------------------
