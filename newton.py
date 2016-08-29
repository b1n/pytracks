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
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import sys

import sip
sip.setapi('QString', 2)

# control
import control.control_newton as control

# -------------------------------------------------------------------------------------------------

def main():

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
