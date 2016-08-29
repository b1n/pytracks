#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
generate_trj_json.

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

def generate_trj_json(fdct_trj, fs_trj=None):
    """
    DOCUMENT ME!
    """
    # logger
    # M_LOG.info("generate_trj_json:>>")

    # inicia dicionário local
    ldct_trj = {}

    # trajetória específica ?
    if fs_trj is not None:

        # trajetória existe no dicionário ?
        l_trj = fdct_trj.get(fs_trj, None)

        if l_trj is None:

            # logger
            l_log = logging.getLogger("generate_trj_json")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"E01: trajetória {} não existe no dicionário.".format(fs_trj))
                                                    
            # return
            return None

        # coloca a trajetória no dicionário local
        ldct_trj[fs_trj] = l_trj.s_prc_desc

    # senão, todo dicionário
    else:
        # para todas as trajetórias...
        for l_key, l_trj in fdct_trj.items():

            # coloca a trajetória no dicionário local
            ldct_trj[l_key] = l_trj.s_prc_desc

    # monta buffer
    ls_buf = json.dumps(ldct_trj)
    # M_LOG.debug("generate_trj_json:ls_buf:[{}]".format(ls_buf))

    # logger
    # M_LOG.info("generate_trj_json:<<")

    # return
    return ls_buf

# < the end >--------------------------------------------------------------------------------------
