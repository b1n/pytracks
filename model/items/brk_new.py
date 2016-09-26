#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
brk_new.

mantém as informações sobre um breakpoint.

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

# model
from ..coords import coord_defs as cdefs
from . import brk_model as model

# control
from ...control.events import events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CBrkNEW >--------------------------------------------------------------------------------

class CBrkNEW(model.CBrkModel):
    """
    mantém as informações específicas sobre breakpoint.

    <breakpoint nBrk="1">
        <coord>
            <tipo>D</tipo>
            <campoA>0964</campoA>
            <campoB>06</campoB>
            <campoC>247</campoC>
        </coord>
        <altitude>3500</altitude>
        <velocidade>160</velocidade>
    </breakpoint>
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_prc, f_data=None, fs_ver="0001"):
        """
        @param f_model: event manager
        @param f_prc: pointer para o procedimento
        @param f_data: dados do breakpoint
        @param fs_ver: versão do formato
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_prc

        # M_LOG.debug("f_data: " + str(f_data))

        # init super class
        super(CBrkNEW, self).__init__()

        # salva o model manager localmente
        self.__model = f_model
        assert self.__model

        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # herdado de CBrkModel
        # self.v_brk_ok    # (bool)
        # self.i_brk_id    # identificação do breakpoint
        # self.f_brk_x     # x (m)
        # self.f_brk_y     # y (m)
        # self.f_brk_z     # z (m)

        # latitude (gr)
        self.__f_brk_lat = 0.
        # longitude (gr)
        self.__f_brk_lng = 0.
        # elevação (m)
        # self.__f_brk_elev = 0.

        # altitude
        self.__f_brk_alt = 0.
        # velocidade
        self.__f_brk_vel = 0.

        # razão de descida/subida
        self.__f_brk_raz_vel = 0.

        # salva o procedimento localmente
        # self.__ptr_brk_prc = f_prc
        self.__ptr_brk_prc = None

        # coordenada T
        self.__i_brk_t = 0

        # se i_brk_t = 0 implica que brk_y e brk_x são coordenadas cartesianas do breakpoint
        # se i_brk_t > 0 implica coordenadas temporais, onde:
        #      brk_y = número do fixo
        #      brk_x = azimute
        #      brk_t = tempo (em segundos).
        # se i_brk_t < 0 implica coordenadas Rumo/Azimute, onde:
        #      brk_y = 0
        #      brk_x = rumo
        #      brk_z = altitude
        #      brk_vel = razão de subida

        # recebeu dados ?
        if f_data is not None:

            # recebeu uma lista ?
            if isinstance(f_data, dict):

                # cria uma breakpoint com os dados da lista
                self.load_brk(f_data, fs_ver)

            # recebeu uma breakpoint ?
            elif isinstance(f_data, CBrkNEW):

                # copia a breakpoint
                self.copy_brk(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy_brk(self, f_brk):
        """
        copy constructor.
        cria um novo breakpoint a partir de um outro breakpoint.

        @param f_brk: breakpoint a ser copiado.
        """
        # logger
        # M_LOG.info("copy_brk:>>")

        # verifica parâmetros de entrada
        assert f_brk

        # copy super class attributes
        super(CBrkNEW, self).copy_brk(f_brk)

        # latitude (gr)
        self.__f_brk_lat = f_brk.f_brk_lat
        # longitude (gr)
        self.__f_brk_lng = f_brk.f_brk_lng

        # altitude (m)
        self.__f_brk_alt = f_brk.f_brk_alt
        # velocidade (m/s)
        self.__f_brk_vel = f_brk.f_brk_vel

        # razão de descida/subida
        self.__f_brk_raz_vel = f_brk.f_brk_raz_vel

        # procedimento
        self.__ptr_brk_prc = f_brk.ptr_brk_prc

        # coordenada T
        self.__i_brk_t = f_brk.i_brk_t

        # logger
        # M_LOG.info("copy_brk:<<")

    # ---------------------------------------------------------------------------------------------

    def load_brk(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados de breakpoint a partir de um dicionário.

        @param fdct_data: dicionário com os dados do breakpoint.
        @param fs_ver: versão do formato dos dados.
        """
        # logger
        # M_LOG.info("load_brk:>>")

        # formato versão 0.01 ?
        if "0001" == fs_ver:

            # cria a breakpoint
            self.make_brk(fdct_data)

        # senão, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CBrkNEW::load_brk")
            l_log.setLevel(logging.NOTSET)
            l_log.critical(u"E01: formato desconhecido.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

        # logger
        # M_LOG.info("load_brk:<<")

    # ---------------------------------------------------------------------------------------------

    def make_brk(self, fdct_data):
        """
        carrega os dados de breakpoint a partir de um dicionário (formato 0001).

        @param fdct_data: dicionário com os dados do breakpoint.
        """
        # logger
        # M_LOG.info("make_brk:>>")

        # identificação do breakpoint
        if "nBrk" in fdct_data:
            self.i_brk_id = int(fdct_data["nBrk"])
            # M_LOG.debug("self.i_brk_id: " + str(self.i_brk_id))

        # posição (lat, lng)
        if "coord" in fdct_data:
            self.__f_brk_lat, self.__f_brk_lng = self.__model.coords.from_dict(fdct_data["coord"])
            # M_LOG.debug("brk_lat:[{}] brk_lng:[{}]".format(self.__f_brk_lat, self.__f_brk_lng))

            # converte para xyz
            self.f_brk_x, self.f_brk_y, self.f_brk_z = self.__model.coords.geo2xyz(self.__f_brk_lat, self.__f_brk_lng, 0.)
            # M_LOG.debug("brk_x:[{}] brk_y:[{}] brk_z:[{}]"format(self.f_brk_x, self.f_brk_y, self.f_brk_z))

        # altitude
        if "altitude" in fdct_data:
            self.__f_brk_alt = float(fdct_data["altitude"]) * cdefs.D_CNV_FT2M
            # M_LOG.debug("self.__f_brk_alt: " + str(self.__f_brk_alt))

        # velocidade
        if "velocidade" in fdct_data:
            self.__f_brk_vel = float(fdct_data["velocidade"]) * cdefs.D_CNV_KT2MS
            # M_LOG.debug("self.__f_brk_vel: " + str(self.__f_brk_vel))

        # razão de descida
        if "razdes" in fdct_data:
            self.__f_brk_raz_vel = float(fdct_data["razdes"]) * cdefs.D_CNV_FTMIN2MS
            # M_LOG.debug("self.__f_brk_raz_vel: " + str(self.__f_brk_raz_vel))

        # razão de subida
        if "razsub" in fdct_data:
            self.__f_brk_raz_vel = float(fdct_data["razsub"]) * cdefs.D_CNV_FTMIN2MS
            # M_LOG.debug("self.__f_brk_raz_vel: " + str(self.__f_brk_raz_vel))

        # (bool)
        self.v_brk_ok = True

        # logger
        # M_LOG.info("make_brk:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def f_brk_alt(self):
        """
        get altitude
        """
        return self.__f_brk_alt

    @f_brk_alt.setter
    def f_brk_alt(self, f_val):
        """
        set altitude
        """
        self.__f_brk_alt = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_brk_lat(self):
        """
        get latitude
        """
        return self.__f_brk_lat

    @f_brk_lat.setter
    def f_brk_lat(self, f_val):
        """
        set latitude
        """
        self.__f_brk_lat = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_brk_lng(self):
        """
        get longitude
        """
        return self.__f_brk_lng

    @f_brk_lng.setter
    def f_brk_lng(self, f_val):
        """
        set longitude
        """
        self.__f_brk_lng = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def ptr_brk_prc(self):
        """
        get procedimento
        """
        return None  # self.__ptr_brk_prc

    @ptr_brk_prc.setter
    def ptr_brk_prc(self, f_val):
        """
        set procedimento
        """
        self.__ptr_brk_prc = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_brk_raz_vel(self):
        """
        get razão de subida
        """
        return self.__f_brk_raz_vel

    @f_brk_raz_vel.setter
    def f_brk_raz_vel(self, f_val):
        """
        set razão de subida
        """
        self.__f_brk_raz_vel = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def i_brk_t(self):
        """
        get coordenada T
        """
        return 0  # self.__i_brk_t

    @i_brk_t.setter
    def i_brk_t(self, f_val):
        """
        set coordenada T
        """
        self.__i_brk_t = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_brk_vel(self):
        """
        get velocidade
        """
        return self.__f_brk_vel

    @f_brk_vel.setter
    def f_brk_vel(self, f_val):
        """
        set velocidade
        """
        self.__f_brk_vel = f_val

# < the end >--------------------------------------------------------------------------------------
