#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dbEdit

editor da base de dados

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
import logging
import sys

import sip
sip.setapi('QString', 2)

# control
import control.control_dbedit as control

# -------------------------------------------------------------------------------------------------

def main():
    """
    initalize and kick off the main loop
    """
    # instancia o controller
    l_control = control.CControlDBEdit()
    assert l_control

    # ativa o controller
    l_control.start()

    # obtém a view
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
