#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
generate_sub_json.

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

def generate_sub_json(fdct_sub, fs_sub=None):
    """
    DOCUMENT ME!
    """
    # logger
    # M_LOG.info("generate_sub_json:>>")

    # inicia dicionário local
    ldct_sub = {}

    # subida específica ?
    if fs_sub is not None:

        # subida existe no dicionário ?
        l_sub = fdct_sub.get(fs_sub, None)

        if l_sub is None:

            # logger
            l_log = logging.getLogger("generate_sub_json")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"E01: subida {} não existe no dicionário.".format(fs_sub))
                                                    
            # return
            return None

        # coloca a subida no dicionário local
        ldct_sub[fs_sub] = l_sub.s_prc_desc

    # senão, todo dicionário
    else:
        # para todas as subidas...
        for l_key, l_sub in fdct_sub.items():

            # coloca a subida no dicionário local
            ldct_sub[l_key] = l_sub.s_prc_desc

    # monta buffer
    ls_buf = json.dumps(ldct_sub)
    # M_LOG.debug("generate_sub_json:ls_buf:[{}]".format(ls_buf))

    # logger
    # M_LOG.info("generate_sub_json:<<")

    # return
    return ls_buf

# < the end >--------------------------------------------------------------------------------------
