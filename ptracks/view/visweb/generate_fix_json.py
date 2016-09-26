#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
generate_fix_json.

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

def generate_fix_json(fdct_fix, fs_fix=None):
    """
    DOCUMENT ME!
    """
    # logger
    # M_LOG.info("generate_fix_json:>>")

    # inicia dicionário local
    ldct_fix = {}

    # fixo específico ?
    if fs_fix is not None:

        # converte para inteiro
        li_fix = int(fs_fix.strip())

        # fixo existe no dicionário ?
        l_fix = fdct_fix.get(li_fix, None)

        if l_fix is None:

            # logger
            l_log = logging.getLogger("generate_fix_json")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"E01: fixo {} não existe no dicionário.".format(fs_fix))
                                                    
            # return
            return None

        # coloca o fixo no dicionário local
        ldct_fix[li_fix] = l_fix.s_fix_desc

    # senão, todo dicionário
    else:
        # para todas os fixos...
        for l_key, l_fix in fdct_fix.items():

            # coloca o fixo no dicionário local
            ldct_fix[l_key] = l_fix.s_fix_desc

    # monta buffer
    ls_buf = json.dumps(ldct_fix)
    # M_LOG.debug("generate_fix_json:ls_buf:[{}]".format(ls_buf))

    # logger
    # M_LOG.info("generate_fix_json:<<")

    # return
    return ls_buf

# < the end >--------------------------------------------------------------------------------------
