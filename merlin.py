#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
merlin

configurador de simulação

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
import sys

import sip
sip.setapi('QString', 2)

# control
from .control import control_wizard as control

# -------------------------------------------------------------------------------------------------


def main():
    """
    initalize and kick off the main loop
    """
    # instancia o controller
    l_control = control.CControlWizard()
    assert l_control

    # ativa o controller
    l_control.start()

    # obtém o view manager
    l_view = l_control.view
    assert l_view

    # ativa a viewer
    sys.exit(l_view.run())

# -------------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:

    # logger
    logging.basicConfig()

    # run application
    main()

# < the end >--------------------------------------------------------------------------------------
