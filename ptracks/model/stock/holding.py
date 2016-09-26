#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
holding.

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

# Python library
import logging

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CHolding >----------------------------------------------------------------------------

class CHolding(object):

    # ---------------------------------------------------------------------------------------------

    def __init__(self, fs_fixo=None, ff_entrada=None, fc_dir=None):
        """
        constructor
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert fc_dir in ['l', 'r']

        self._sWaypoint = fs_fixo
        # M_LOG.info("self._sWaypoint: %s" % self._sWaypoint)

        self._fInbound = ff_entrada
        # M_LOG.info("self._fInbound: %f" % self._fInbound)

        # sentido da espera 
        self._cDirection = fc_dir
        # M_LOG.info("self._cDirection: %c" % self._cDirection)

        # logger
        # M_LOG.info("__init__:<<")

# < the end >--------------------------------------------------------------------------------------
