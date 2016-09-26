#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
piloto

DOCUMENT ME!

revision 0.2  2016/mar  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/03"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import os
import sys
import threading

import sip
sip.setapi('QString', 2)

# control
from .control import control_piloto as control
from .model import glb_defs as gdefs

# -------------------------------------------------------------------------------------------------


def main():
    f_cfg = find_cfg_file()

    if f_cfg is None:
        sys.exit(1)

    # Alterando variável global
    gdefs.D_CFG_FILE = f_cfg

    print "Loading configuration file %s" % gdefs.D_CFG_FILE

    # instancia o controller
    l_control = control.CControlPiloto(gdefs.D_CFG_FILE)
    assert l_control

    # ativa o controller
    l_control.start()

    # obtém a view
    l_view = l_control.view
    assert l_view

    # ativa a viewer
    l_view.run()

    print "threadings:", threading.enumerate ()

    import traceback

    for thread_id, frame in sys._current_frames ().iteritems ():
        name = thread_id
        for thread in threading.enumerate ():
            if thread.ident == thread_id:
                name = thread.name

        traceback.print_stack ( frame )

    # termina
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
