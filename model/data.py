#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
data

simple data loader module. Loads data files from the "data" directory shipped with application

todo:
Enhancing this to handle caching etc

revision 0.3  2016/ago  mlabru
pequenas correções e otimizações

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/08"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging
import os

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# data
M_DATA_PY = os.path.abspath(os.path.dirname(__file__))
M_DATA_DIR = os.path.normpath(os.path.join(M_DATA_PY, ".."))

# -------------------------------------------------------------------------------------------------

def filepath(f_filename):
    """
    determine the path to a file in the data directory
    """
    # logger
    # M_LOG.info("filepath:><")

    # M_LOG.debug("M_DATA_DIR: " + M_DATA_DIR)
    # M_LOG.debug("filename: " + f_filename)

    # return
    return os.path.join(M_DATA_DIR, f_filename)

# -------------------------------------------------------------------------------------------------

def load(f_filename, f_mode="rb"):
    """
    open a file in the data directory
    """
    # logger
    # M_LOG.info("load:><")

    # return
    return open(os.path.join(M_DATA_DIR, f_filename), f_mode)

# < the end >--------------------------------------------------------------------------------------
