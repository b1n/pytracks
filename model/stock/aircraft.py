#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
aircraft.

mantém os detalhes de uma aeronave.

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
import copy
# import logging

# model
import model.coords.pos_lat_lng as pll
import model.stock.adiru as cadi

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CAircraft >------------------------------------------------------------------------------

class CAircraft(object):
    """
    mantém as informações específicas sobre uma aeronave.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, fs_id="ABCDEF"):
        """
        @param  fs_id: identificação da aeronave
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input parameters
        assert fs_id

        # air data inertial reference unit
        self.__adiru = cadi.CADIRU()
        assert self.__adiru

        # callsign
        self.__s_callsign = "NONAME"

        # icao address
        self.__s_icao_addr = fs_id

        # posição lat/lng
        self.__pos = pll.CPosLatLng()
        assert self.__pos is not None

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy(self):
        """
        copy constructor.
        """
        # logger
        # M_LOG.info("copy:><")

        # return a copy
        return copy.deepcopy(self)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def adiru(self):
        """
        get air data inertial reference unit
        """
        return self.__adiru

    @adiru.setter
    def adiru(self, f_val):
        """
        set air data inertial reference unit
        """
        self.__adiru = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_alt(self):
        """
        get altitude
        """
        return self.__adiru.f_alt

    @f_alt.setter
    def f_alt(self, f_val):
        """
        set altitude
        """
        self.__adiru.f_alt = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def s_callsign(self):
        """
        get callsign
        """
        return self.__s_callsign  # .decode ( "utf-8" )

    @s_callsign.setter
    def s_callsign(self, f_val):
        """
        set callsign
        """
        self.__s_callsign = f_val.strip()  # .encode ( "utf-8" )

    # ---------------------------------------------------------------------------------------------

    @property
    def s_icao_addr(self):
        """
        get ICAO address
        """
        return self.__s_icao_addr

    @s_icao_addr.setter
    def s_icao_addr(self, f_val):
        """
        set ICAO address
        """
        self.__s_icao_addr = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_lat(self):
        """
        get latitude
        """
        return self.__pos.f_lat

    @f_lat.setter
    def f_lat(self, f_val):
        """
        set latitude
        """
        self.__pos.f_lat = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_lng(self):
        """
        get longitude
        """
        return self.__pos.f_lng

    @f_lng.setter
    def f_lng(self, f_val):
        """
        set longitude
        """
        self.__pos.f_lng = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def pos(self):
        """
        get position
        """
        return self.__pos

    @pos.setter
    def pos(self, f_val):
        """
        set position
        """
        self.__pos = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_proa(self):
        """
        get proa
        """
        return self.__adiru.f_proa

    @f_proa.setter
    def f_proa(self, f_val):
        """
        set proa
        """
        self.__adiru.f_proa = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_true_heading(self):
        """
        get true heading
        """
        return self.__adiru.f_true_heading
                                            
    @f_true_heading.setter
    def f_true_heading(self, f_val):
        """
        set true heading
        """
        self.__adiru.f_true_heading = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_vel(self):
        """
        get velocidade
        """
        return self.__adiru.f_vel

    @f_vel.setter
    def f_vel(self, f_val):
        """
        set velocidade
        """
        self.__adiru.f_vel = f_val

# < the end >--------------------------------------------------------------------------------------
