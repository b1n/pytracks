#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
newton

DOCUMENT ME!

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""

import logging
import multiprocessing
import os
import sys
import sip

sip.setapi('QString', 2)

from .control import control_newton as control
from .model import glb_defs as gdefs

__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/01"


# -------------------------------------------------------------------------------------------------

def main():

    f_cfg = find_cfg_file()

    if f_cfg is None:
        sys.exit(1)

    # Alterando variável global
    gdefs.D_CFG_FILE = f_cfg

    print "Loading configuration file %s" % gdefs.D_CFG_FILE

    # instancia o control
    l_control = control.CControlNewton()
    assert l_control

    try:
        # ativa o control
        l_control.run()

    # trata interrupções
    except KeyboardInterrupt as SystemExit:

        # termina a aplicação
        l_control.cbk_termina()

    # termina a aplicação
    sys.exit()


def find_cfg_file():

    local_path = os.getcwd() + "/" + gdefs.D_CFG_FILE
    script_path = os.path.dirname(os.path.realpath(__file__)) + "/" + gdefs.D_CFG_FILE
    etc_path = "/etc/ptracks/" + gdefs.D_CFG_FILE

    if os.path.exists(local_path):
        return local_path

    if os.path.exists(etc_path):
        return etc_path

    if os.path.exists(script_path):
        return script_path

    return None


# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:

    # logger
    logging.basicConfig()

    # multiprocessing logger
    multiprocessing.log_to_stderr()

    # run application
    main()


# < the end >--------------------------------------------------------------------------------------
