#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pos_lat_lng.

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
import copy
# import logging

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CPosLatLng >-----------------------------------------------------------------------------

class CPosLatLng(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, ff_pos_lat=0., ff_pos_lng=0.):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__init__:>>")

        # inicia a super classe
        super(CPosLatLng, self).__init__()

        if isinstance(ff_pos_lat, CPosLatLng):

            ff_pos_lng = ff_pos_lat.f_lng
            ff_pos_lat = ff_pos_lat.f_lat

        # verifica parâmetros de entrada
        assert -90. <= ff_pos_lat <= 90.
        assert -180. <= ff_pos_lng <= 180.

        self.__f_lat = ff_pos_lat
        # M_LOG.info("self.__f_lat: %f" % self.__f_lat)

        self.__f_lng = ff_pos_lng
        # M_LOG.info("self.__f_lng: %f" % self.__f_lng)

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
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_lat(self):
        """
        get latitude
        """
        return self.__f_lat
                                            
    @f_lat.setter
    def f_lat(self, f_val):
        """
        set latitude
        """
        # check input parameters
        assert -90. <= f_val <= 90.
        
        # save latitude
        self.__f_lat = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_lng(self):
        """
        get longitude
        """
        return self.__f_lng
                                            
    @f_lng.setter
    def f_lng(self, f_val):
        """
        set longitude
        """
        # check input parameters
        assert -180. <= f_val <= 180.
        
        # save longitude
        self.__f_lng = f_val

# < class CPosLatLngRef >--------------------------------------------------------------------------

class CPosLatLngRef(CPosLatLng):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_ref, ff_variation, ff_track, ff_dcl_mag):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        # assert f_control

        # convert difference to radians 
        lf_dif = math.radians(ff_track - ff_variation)

        # calculate lat & lng
        lf_lat = f_ref.f_lat + ff_dcl_mag / 60. * math.cos(lf_dif)
        lf_lng = f_ref.f_lng + ff_dcl_mag / 60. * math.sin(lf_dif) / math.cos(math.radians(lf_lat))

        # inicia a super classe
        super(CPosLatLngRef, self).__init__(lf_lat, lf_lng)

        # logger
        # M_LOG.info("__init__:<<")

# < the end >--------------------------------------------------------------------------------------
