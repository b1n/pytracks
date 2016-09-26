#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
aircraft_piloto.

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
import random
import sys
import time

# model
# import model.tMath as tmath

# import model.coords.pos_lat_lng as pll
from ..stock import aircraft_basic as sanv
from ..piloto import strip_model as mstp

#import model.visadsb.auto_pilot as CAutoPilot
#import model.visadsb.fms as CFMS
#import model.visadsb.instruction as CInstruction
#import model.visadsb.mcp as CMCP
#import model.visadsb.pilot as CPilot

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CAircraftPiloto >------------------------------------------------------------------------

class CAircraftPiloto(sanv.CAircraftBasic):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_emula, f_data=None):
        """
        constructor
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_emula

        # inicia a super classe
        super(CAircraftPiloto, self).__init__(f_emula, f_data)

        # herdado de CAircraft
        # self.adiru          # air data inertial reference unit
        # self.s_callsign     # callsign
        # self.s_icao_addr    # icao address
        # self.pos            # posição lat/lng

        # herdado de CAircraftBasic
        # self.airspace            # airspace
        # self.lst_trail           # trail list
        # self.lst_instructions    # instructions list
        # self.v_uninitialized     # flag uninitialized
                                                        
        # import foreign objects
        self.airspace = f_emula.model.airspace
        # assert self.airspace
        
        # self.__weather = f_emula.model.weather
        # assert self.__weather

        # create vectors
        self.__lst_trail = []
        self.__lst_instructions = []

        self.__v_uninitialized = True

        # create aircraft components

        #self._mcp = CMCP.CMCP(self.airspace.f_variation)
        #assert self._mcp is not None

        #self._fms = CFMS.CFMS(self, self.airspace, self.__weather, self.adiru, self._mcp)
        #assert self._fms is not None

        #self._auto_pilot = CAutoPilot.CAutoPilot(self.adiru, self._fms, self._mcp)
        #assert self._auto_pilot is not None

        #self._fms.setAutoPilot(self._auto_pilot)

        #self._pilot = CPilot.CPilot(self, self.airspace, self.__weather, self._fms, self._mcp)
        #assert self._pilot is not None

        # recebeu dados ?
        if f_data is not None:
                
            # recebeu uma lista ?
            if isinstance(f_data, list):
                                        
                # cria uma aeronave com os dados da lista
                self.make_aircraft(f_data, True)
                                                                                        
            # recebeu uma aeronave ?
            elif isinstance(f_data, CAircraftPiloto):
                                                                                                                
                # copia a aeronave
                # self.copy_aircraft(f_data)
                pass
                                                                                                                                                                
            # senão, inicia os dados locais
            else:
                # set initial values
                self.adiru.f_altitude = 10000.
                self.adiru.f_ias = 230.
                self.adiru.f_true_heading = 0.

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def get_strip(self):
        """
        return flight strip
        """
        # logger
        # M_LOG.info("get_strip:>>")

        # TODO

        # logger
        # M_LOG.info("get_strip:<<")

        # return
        return mstp.CStripModel()

    # ---------------------------------------------------------------------------------------------

    def instructAltitude(self, f_fAlt):
        """
        give instruction for an altitude
        TODO: FL/ALT
        """
        # logger
        # M_LOG.info("instructAltitude:><")

        # TODO

    # ---------------------------------------------------------------------------------------------

    def instructApproach(self, f_appName):
        """
        give instruction for an approach procedure
        """
        # logger
        # M_LOG.info("instructApproach:>>")

        # verifica parâmetros de entrada
        # assert f_control
        '''
        if (f_appName == ""):

            # logger
            # M_LOG.info("<E01")

            return

        l_inst = CInstruction.CInstruction()
        assert l_inst is not None

        l_inst._iType = CInstruction.CInstruction._APPROACH
        l_inst._oReactTime = time.time() + 2 + (random.random() * 9)

        if self.__v_uninitialized:
            l_inst._oReactTime = 0
            self.__v_uninitialized = False

        l_inst._sText = f_appName
        self.__lst_instructions.append(l_inst)
        '''
        # logger
        # M_LOG.info("instructApproach:<<")

    # ---------------------------------------------------------------------------------------------

    def instructDirect(self, f_ptName):
        """
        give instruction for a direct (or shortcut)
        """
        # logger
        # M_LOG.info("instructDirect:>>")

        # verifica parâmetros de entrada
        # assert f_control
        '''
        if (f_ptName == ""):

            # logger
            # M_LOG.info("<E01")

            return

        l_inst = CInstruction.CInstruction()
        assert l_inst is not None

        l_inst._iType = CInstruction.CInstruction._DIRECT
        l_inst._oReactTime = time.time() + 2 + (random.random() * 9)

        if self.__v_uninitialized:
            l_inst._oReactTime = 0
            self.__v_uninitialized = False

        l_inst._sText = f_ptName

        self.__lst_instructions.append(l_inst)
        '''
        # logger
        # M_LOG.info("instructDirect:<<")

    # ---------------------------------------------------------------------------------------------

    def instructHeading(self, f_hdg):
        """
        give instruction for a heading
        """
        # logger
        # M_LOG.info("instructHeading:>>")

        # verifica parâmetros de entrada
        # assert f_control
        '''
        if (f_hdg == 360):
            f_hdg = 0

        l_inst = CInstruction.CInstruction()
        assert l_inst is not None

        l_inst._iType = CInstruction.CInstruction._HDG
        l_inst._oReactTime = time.time() + 2 + (random.random() * 9)

        if self.__v_uninitialized:
            l_inst._oReactTime = 0
            self.__v_uninitialized = False

        l_inst._fNumber = f_hdg

        self.__lst_instructions.append(l_inst)
        '''
        # logger
        # M_LOG.info("instructHeading:<<")

    # ---------------------------------------------------------------------------------------------

    def instructRoute(self, f_sRtName):
        """
        give instruction for a standard route
        """
        # logger
        # M_LOG.info("instructRoute:>>")

        # verifica parâmetros de entrada
        # assert f_control
        '''
        if (f_sRtName == ""):

            # logger
            # M_LOG.info("<E01")

            return

        l_inst = CInstruction.CInstruction()
        assert l_inst is not None

        l_inst._iType = CInstruction.CInstruction._ROUTE
        l_inst._oReactTime = time.time() + 2 + (random.random() * 9)

        if self.__v_uninitialized:
            l_inst._oReactTime = 0
            self.__v_uninitialized = False

        l_inst._sText = f_sRtName

        self.__lst_instructions.append(l_inst)
        '''
        # logger
        # M_LOG.info("instructRoute:<<")

    # ---------------------------------------------------------------------------------------------

    def instructSpeed(self, ff_ias):
        """
        give instruction for a speed
        """
        # logger
        # M_LOG.info("instructSpeed:><")

        # TODO

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def f_altitude(self):
        """
        TODO
        """
        return self.adiru.f_alt

    @f_altitude.setter
    def f_altitude(self, f_val):
        """
        set initial altitude
        """
        self.adiru.f_alt = f_val

# < the end >--------------------------------------------------------------------------------------
