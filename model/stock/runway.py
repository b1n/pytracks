#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
runway.

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

# model
import model.stock.fix as CFix

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CRunway >--------------------------------------------------------------------------------

class CRunway(CFix.CFix):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, fs_rwy_name, ff_rwy_lat, ff_rwy_lng, ff_rwy_track, ff_rwy_gp):
        """
        define uma aerovia

        @param fs_rwy_name: nome
        @param ff_rwy_lat: latitude
        @param ff_rwy_lng: longitude
        @param ff_rwy_track: path
        @param ff_rwy_gp: glide path
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        # assert f_control

        # inicia a super classe
        super(CRunway, self).__init__(fs_rwy_name, ff_rwy_lat, ff_rwy_lng)

        # herdados de CFix
        # self.s_name      # nome
        # self.position    # posição

        self.__f_track = ff_rwy_track
        # M_LOG.info("self.__f_track: %f" % self.__f_track)

        self.__f_app_angle = ff_rwy_gp
        # M_LOG.info("self.__f_app_angle: %f" % self.__f_app_angle)

        # logger
        # M_LOG.info("__init__:<<")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_app_angle(self):
        """
        get glide path
        """
        return self.__f_app_angle
                                            
    @f_app_angle.setter
    def f_app_angle(self, f_val):
        """
        set glide path
        """
        self.__f_app_angle = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_track(self):
        """
        get track
        """
        return self.__f_track
                                            
    @f_track.setter
    def f_track(self, f_val):
        """
        set track
        """
        self.__f_track = f_val

# < the end >--------------------------------------------------------------------------------------
