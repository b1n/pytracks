#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
get_address.

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
# import logging
import os

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------

def get_address(f_config, fs_addr_key):
    """
    @param f_config: gerente de configuração (config manager).
    @param fs_addr_key: address key.
    """
    # logger
    # M_LOG.info("get_address:>>")

    # check input parameters
    assert f_config
    assert fs_addr_key

    # obtém o dicionário de configuração
    ldct_config = f_config.dct_config
    assert ldct_config is not None

    # obtém o canal de comunicação (3)
    li_canal = int(ldct_config.get("glb.canal", 3))
    # M_LOG.debug(u"canal de comunicação: " + str(li_canal))

    assert (li_canal > 2) and (li_canal < 200)

    # monta o endereço ('235.0.0.3')
    ls_addr = "%s.%s" % (ldct_config.get(fs_addr_key, "235.0.0"), str(li_canal))
    # M_LOG.debug(u"endereço: " + ls_addr)
    assert ls_addr

    # configura a porta (1961)
    li_port = int(ldct_config.get("net.port", 1961))
    # M_LOG.debug("porta: " + str(li_port))

    # lista de interfaces disponíveis
    llst_iface = os.listdir("/sys/class/net/")
    assert llst_iface is not None

    # obtém a interface de entrada (None)
    ls_ifce_in = ldct_config.get("net.ifin", None)

    if ls_ifce_in not in llst_iface:
        ls_ifce_in = None

    # obtém a interface de saída (None)
    ls_ifce_out = ldct_config.get("net.iout", None)

    if ls_ifce_out not in llst_iface:
        ls_ifce_out = None

    # logger
    # M_LOG.info("get_address:<<")

    # return
    return (ls_ifce_in, ls_ifce_out), ls_addr, li_port
    
# < the end >--------------------------------------------------------------------------------------
