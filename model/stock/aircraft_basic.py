#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
aircraft_basic

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
from .. import tMath as tmath

from ..coords import pos_lat_lng as pll
from . import aircraft as sanv

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CAircraftBasic >-------------------------------------------------------------------------

class CAircraftBasic(sanv.CAircraft):
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
        super(CAircraftBasic, self).__init__()

        # herdado de CAircraft
        # self.adiru          # air data inertial reference unit
        # self.s_callsign     # callsign
        # self.s_icao_addr    # icao address
        # self.pos            # posição lat/lng

        # herdado de CADIRU
        # self.adiru.f_alt             # altitude
        # self.adiru.f_ias             # instrument air speed
        # self.adiru.f_proa            # proa em relação ao norte magnético
        # self.adiru.f_true_heading    # proa em relação ao norte verdadeiro
        # self.adiru.f_vel             # velocidade

        # import foreign objects
        self.__airspace = f_emula.model.airspace
        # assert self.__airspace
        
        # create vectors
        self.__lst_trail = []
        self.__lst_instructions = []

        self.__v_uninitialized = True

        # recebeu dados ?
        if f_data is not None:
                
            # recebeu uma lista ?
            if isinstance(f_data, list):
                                        
                # cria uma aeronave com os dados da lista
                self.make_aircraft(f_data, True)
                                                                                        
            # recebeu uma aeronave ?
            elif isinstance(f_data, CAircraftBasic):
                                                                                                                
                # copia a aeronave
                # self.copy_aircraft(f_data)
                pass
                                                                                                                                                                
            # senão, inicia os dados locais
            else:
                # set initial values
                self.adiru.f_alt = 10000.
                self.adiru.f_ias = 230.
                self.adiru.f_vel = 230.
                self.adiru.f_proa = 0.
                self.adiru.f_true_heading = 0.

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def init_position(self, f_oPos):
        """
        set initial position and radar position
        """
        # logger
        # M_LOG.info("init_position:>>")

        # verifica parâmetros de entrada
        # assert f_control

        # logger
        # M_LOG.info("init_position:<<")

    # ---------------------------------------------------------------------------------------------

    def isClimbing(self):
        """
        is the aircraft climbing ?
        """
        # logger
        # M_LOG.info("isClimbing:><")

        # TODO
        return False

    # ---------------------------------------------------------------------------------------------

    def isDescending(self):
        """
        is the aircraft descending ?
        """
        # logger
        # M_LOG.info("isDescending:><")

        # TODO
        return False

    # ---------------------------------------------------------------------------------------------
    # @public
    
    def make_aircraft(self, f_data, fv_initial=False):
        """
        create an aircraft from list
        """
        # logger
        # M_LOG.info("__make_aircraft:>>")

        # verifica parâmetros de entrada
        assert f_data is not None

        # inicia o índice de dados
        li_ndx = 0

        # identificacao da aeronave
        self.s_icao_addr = str(f_data[li_ndx])
        li_ndx += 1

        # M_LOG.debug("s_icao:[{}]".format(self.s_icao_addr))

        # código transponder (ssr)
        self.__i_ssr = int(f_data[li_ndx])
        li_ndx += 1

        # M_LOG.debug("i_ssr:[{}]".format(self.__i_ssr))

        # spi
        li_spi = int(f_data[li_ndx])
        li_ndx += 1

        # M_LOG.debug("li_spi:[{}]".format(li_spi))

        # altitude (m)
        self.adiru.f_alt = float(f_data[li_ndx])
        li_ndx += 1

        M_LOG.debug("f_alt:[{}]".format(self.adiru.f_alt))

        # latitude
        lf_lat = float(f_data[li_ndx])
        li_ndx += 1

        # M_LOG.debug("f_lat:[{}]".format(lf_lat))

        # longitude
        lf_lng = float(f_data[li_ndx])
        li_ndx += 1

        # M_LOG.debug("f_lng:[{}]".format(lf_lng))

        self.pos = pll.CPosLatLng(lf_lat, lf_lng)
        assert self.pos

        # if fv_initial:
            # self.pos = pll.CPosLatLng(lf_lat, lf_lng)
            # assert self.pos
        
        # velocidade (kt)
        lf_vel = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_ias = lf_vel
        self.adiru.f_vel = lf_vel

        M_LOG.debug("f_vel:[{}]".format(lf_vel))

        # razão de subida
        self.__f_raz = float(f_data[li_ndx])
        li_ndx += 1

        M_LOG.debug("f_raz:[{}]".format(self.__f_raz))

        # proa
        lf_pro = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_proa = lf_pro
        self.adiru.f_true_heading = lf_pro

        M_LOG.debug("f_pro:[{}]".format(lf_pro))

        # callsign
        self.s_callsign = str(f_data[li_ndx])
        li_ndx += 1

        M_LOG.debug("s_callsign:[{}]".format(self.s_callsign))

        # performance
        self.__s_prf = str(f_data[li_ndx])
        li_ndx += 1

        M_LOG.debug("s_prf:[{}]".format(self.__s_prf))

        # hora
        self.__i_hora = float(f_data[li_ndx])
        li_ndx += 1

        # M_LOG.debug("i_hora:[{}]".format(self.__i_hora))

        # logger
        # M_LOG.info("__make_aircraft:<<")

    # ---------------------------------------------------------------------------------------------

    def radar_ground_speed(self):
        """
        determine groundspeed from radar history
        """
        # logger
        # M_LOG.info("radar_ground_speed:>>")

        if len(self.__lst_trail) < 3:

            # logger
            # M_LOG.info("radar_ground_speed:<E01")

            # return
            return 0

        # calculate ground speed
        l_gs = tmath.distLL(self.__lst_trail[-1], self.pos) / (self.__f_trail_interval / 1000.) * 3600.

        # logger
        # M_LOG.info("radar_ground_speed:<<")

        # return
        return l_gs

    # ---------------------------------------------------------------------------------------------

    def radar_magnetic_track(self):
        """
        determine magnetic track from radar history
        """
        # logger
        # M_LOG.info("radar_magnetic_track:>>")

        if len(self.__lst_trail) < 3:

            # logger
            # M_LOG.info("radar_magnetic_track:<E01")

            # return
            return 0

        # determine magnetic track
        l_tr = round(tmath.track(self.__lst_trail[-1], self.pos) + self.__airspace.f_variation, 0)

        # need normalize ?
        if l_tr < 0:
            # normalize angle
            l_tr += 360

        # logger
        # M_LOG.info("radar_magnetic_track:<<")

        # return
        return l_tr

    # ---------------------------------------------------------------------------------------------

    def trail(self, fi_ndx):
        """
        get position of radar history point #n
        """
        # logger
        # M_LOG.info("trail:>>")

        # exists trail ?
        if not self.__lst_trail:

            # logger
            # M_LOG.info("trail:<E01")

            # return
            return None

        # index out of range ?
        if fi_ndx >= len(self.__lst_trail):

            # logger
            # M_LOG.info("trail:<E02")

            # return
            return None

        # logger
        # M_LOG.info("trail:<<")

        # return
        return self.__lst_trail[len(self.__lst_trail) - 1 - fi_ndx]

    # ---------------------------------------------------------------------------------------------

    def update_data(self, f_data):
        """
        update data
        """
        # logger
        # M_LOG.info("update_data:>>")

        # update aircraft data
        self.make_aircraft(f_data)
        
        # logger
        # M_LOG.info("update_data:<<")

    # ---------------------------------------------------------------------------------------------

    def update_radar_position(self, ff_tim):
        """
        get new radar position, and push old one into history
        """
        # logger
        # M_LOG.info("update_radar_position:>>")

        # verifica parâmetros de entrada
        # assert f_control

        # obtém a última posção conhecida
        l_last_pos = pll.CPosLatLng(self.pos)
        assert l_last_pos is not None

        # coloca no rastro
        self.__lst_trail.append(l_last_pos)

        # atualiza a posição da aeronave
        # self.pos = self.pos

        # salva o intervalo do rastro
        self.__f_trail_interval = ff_tim

        # logger
        # M_LOG.info("update_radar_position:<<")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def i_hora(self):
        """
        get hora
        """
        return self.__i_hora

    @i_hora.setter
    def i_hora(self, f_val):
        """
        set hora
        """
        self.__i_hora = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def s_prf(self):
        """
        get performance
        """
        return self.__s_prf

    @s_prf.setter
    def s_prf(self, f_val):
        """
        set performance
        """
        self.__s_prf = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_raz(self):
        """
        get razão de descida/subida
        """
        return self.__f_raz

    @f_raz.setter
    def f_raz(self, f_val):
        """
        set razão de descida/subida
        """
        self.__f_raz = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def i_ssr(self):
        """
        get transponder code
        """
        return self.__i_ssr

    @i_ssr.setter
    def i_ssr(self, f_val):
        """
        set transponder code
        """
        self.__i_ssr = f_val

# < the end >--------------------------------------------------------------------------------------
