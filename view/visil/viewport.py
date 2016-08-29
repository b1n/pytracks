#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
viewport.

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
# import logging
import math
# import sys

# PyQt4 library
# from PyQt4 import QtCore, QtGui

# model
import model.coords.coord_defs as cdefs
import model.coords.pos_lat_lng as pll
import model.coords.pos_xy as pxy

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CViewport >------------------------------------------------------------------------------

class CViewport(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, fi_w, fi_h):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__init__:>>")

        # inicia a super classe
        super(CViewport, self).__init__()

        # largura e altura da viewport
        self.__f_width = float(fi_w)
        self.__f_height = float(fi_h)

        # coordenada do centro da viewport
        self.__center = pll.CPosLatLng()
        assert self.__center is not None

        self.__f_blip_size = fi_w / 220.
        self.__f_zoom = 160.

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def translate_pos(self, f_pos):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("translate_pos:>>")

        # verifica parâmetros de entrada
        if f_pos is None:

            # logger
            # M_LOG.info("translate_pos:<E01")

            # return
            return None

        # create answer
        l_xy = pxy.CPosXY()
        assert l_xy is not None

        # lat/lng
        lf_delta_lat = (f_pos.f_lat - self.__center.f_lat) * cdefs.D_CNV_GR2NM
        # M_LOG.debug("lf_delta_lat:[{:f}]".format(lf_delta_lat))

        lf_delta_lng = (f_pos.f_lng - self.__center.f_lng) * cdefs.D_CNV_GR2NM
        # M_LOG.debug("lf_delta_lng:[{:f}]".format(lf_delta_lng))

        # escala
        lf_esc = self.__f_width / self.__f_zoom
        # M_LOG.debug("lf_esc:[{:f}]".format(lf_esc))

        # convert to x/y
        l_xy.f_y = self.__f_height / 2. - lf_delta_lat * lf_esc
        # M_LOG.debug("l_xy.f_y:[{:f}]".format(l_xy.f_y))

        l_xy.f_x = self.__f_width / 2. + lf_delta_lng * math.cos(math.radians(self.__center.f_lat)) * lf_esc
        # M_LOG.debug("l_xy.f_x:[{:f}]".format(l_xy.f_x))

        # logger
        # M_LOG.info("translate_pos:<<")

        # return
        return l_xy

    # ---------------------------------------------------------------------------------------------

    def translate_xy(self, f_xy):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("translate_xy:>>")

        # verifica parâmetros de entrada
        if f_xy is None:

            # logger
            # M_LOG.info("translate_xy:<E01")

            # return
            return None

        # create answer
        l_pos = pll.CPosLatLng()
        assert l_pos is not None

        # get x/y
        lf_delta_x = (f_xy.f_x - self.__f_width / 2.) / cdefs.D_CNV_GR2NM
        # M_LOG.debug("lf_delta_x:[{:f}]".format(lf_delta_x))

        lf_delta_y = (f_xy.f_y - self.__f_height / 2.) / cdefs.D_CNV_GR2NM
        # M_LOG.debug("lf_delta_y:[{:f}]".format(lf_delta_y))

        # escala
        lf_esc = float(self.__f_zoom / self.__f_width)
        # M_LOG.debug("lf_esc:[{:f}]".format(lf_esc))

        # calculate lat/lng
        l_pos.f_lat = self.__center.f_lat - lf_delta_y * lf_esc
        # M_LOG.debug("l_pos.f_lat:[{:f}]".format(l_pos.f_lat))

        l_pos.f_lng = self.__center.f_lng + lf_delta_x / math.cos(math.radians(self.__center.f_lat)) * lf_esc
        # M_LOG.debug("l_pos.f_lng:[{:f}]".format(l_pos.f_lng))

        # logger
        # M_LOG.info("translate_xy:<<")

        # return
        return l_pos

    # ---------------------------------------------------------------------------------------------

    def update_size(self, fi_w, fi_h):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("update_size:>>")

        # set size
        self.__f_width = float(fi_w)
        self.__f_height = float(fi_h)

        # set blip size
        self.__f_blip_size = fi_h / 140.

        # logger
        # M_LOG.info("update_size:<<")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def f_blip_size(self):
        """
        get blip size
        """
        return self.__f_blip_size

    @f_blip_size.setter
    def f_blip_size(self, f_val):
        """
        set blip size
        """
        self.__f_blip_size = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def center(self):
        """
        get center
        """
        return self.__center

    @center.setter
    def center(self, f_val):
        """
        set center
        """
        self.__center = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def ppnm(self):
        """
        DOCUMENT ME!
        """
        return float(self.__f_width) / float(self.__f_zoom)

    # ---------------------------------------------------------------------------------------------

    @property
    def f_zoom(self):
        """
        get zoom (nm)
        """
        return self.__f_zoom

    @f_zoom.setter
    def f_zoom(self, f_val):
        """
        set zoom (nm)
        """
        # verifica parâmetros de entrada
        if f_val < 20:
            f_val = 20

        elif f_val > 420:
            f_val = 420

        self.__f_zoom = float(f_val)

# < the end >--------------------------------------------------------------------------------------
