#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
generate_arr_dep_json

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

def generate_arr_dep_json(flst_arr_dep, fs_arr_dep=None):
    """
    DOCUMENT ME!
    """
    # logger
    # M_LOG.info("generate_arr_dep_json:>>")

    # inicia lista local
    llst_arr_dep = []

    # pouso/decolagem específica ?
    if fs_arr_dep is not None:

        # pouso/decolagem existe no lista ?
        lt_arr_dep = flst_arr_dep.get(fs_arr_dep, None)

        if lt_arr_dep is None:

            # logger
            l_log = logging.getLogger("generate_arr_dep_json")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"E01: pouso/decolagem {} não existe na lista.".format(fs_arr_dep))
                                                    
            # return
            return None

        # coloca o pouso/decolagem na lista local
        llst_arr_dep.append(fs_arr_dep)

    # senão, toda lista
    else:
        # todos os pousos/decolagens
        llst_arr_dep = flst_arr_dep

    # monta buffer
    ls_buf = json.dumps(llst_arr_dep)
    # M_LOG.debug("generate_arr_dep_json:ls_buf:[{}]".format(ls_buf))

    # logger
    # M_LOG.info("generate_arr_dep_json:<<")

    # return
    return ls_buf

# < the end >--------------------------------------------------------------------------------------
