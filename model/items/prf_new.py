#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------------------------
prf_new.
mantém as informações sobre uma performance do TrackS.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
-------------------------------------------------------------------------------------------------
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
from . import prf_model as model

# control
from ...control.events import events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.NOTSET)

# < class CPrfNEW >--------------------------------------------------------------------------------

class CPrfNEW(model.CPrfModel):
    """
    mantém as informações específicas sobre performance.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_event, f_data=None, fs_ver="0001"):
        """
        @param f_event: event manager.
        @param f_data: dados da performance.
        @param fs_ver: versão do formato dos dados.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        # M_LOG.debug("f_data: " + str(f_data))

        # init super class
        super(CPrfNEW, self).__init__()

        # salva o event manager localmente
        self.__event = f_event

        # herdados de CPrfModel
        # self.v_prf_ok      # ok (bool)
        # self.s_prf_id      # identificação da performance
        # self.s_prf_desc    # descrição da performance

        # esteira
        self._c_prf_esteira = ''

        # máximos

        # teto de serviço (DIST)
        self.__f_prf_teto_sv = 0.

        # faixa de serviço (DIST)
        self.__f_prf_faixa = 0.

        # decolagem

        # velocidade de decolagem (VELO) (knots->m/s)
        self.__f_prf_vel_dec = 0.

        # velocidade de subida na decolagem (VELO) (knots->m/s)
        self.__f_prf_vel_sub_dec = 0.

        # razão de subida na decolagem (VELO) (knots->m/s)
        self.__f_prf_raz_sub_dec = 0.

        # razão máxima subida na decolagem (VELO) (knots->m/s)
        self.__f_prf_raz_max_sub_dec = 0.

        # aproximação

        # velocidade de aproximação (VELO) (knots->m/s)
        self.__f_prf_vel_apx = 0.

        # razão de descida na aproximação (VELO) (knots->m/s)
        self.__f_prf_raz_des_apx = 0.

        # razão máxima descida na aproximação (VELO) (knots->m/s)
        self.__f_prf_raz_max_des_apx = 0.

        # cruzeiro

        # velocidade de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_vel_crz = 0.

        # velocidade máxima de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_vel_max_crz = 0.

        # razão de subida de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_raz_sub_crz = 0.

        # razão máxima de subida de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_raz_max_sub_crz = 0.

        # razão de descida de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_raz_des_crz = 0.

        # razão máxima descida de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_raz_max_des_crz = 0.

        # aceleração

        # razão de variação de velocidade (aceleração) (ACEL)
        self.__f_prf_raz_var_vel = 0.

        # razão máxima variação de velocidade (aceleração) (ACEL)
        self.__f_prf_raz_max_var_vel = 0.

        # desaceleração de vôo
        # self.__f_prf_desacel_crz = 0.

        # aceleração mínima de decolagem
        # self.__f_prf_AcelMinDep = 0.

        # desaceleração máxima de pouso
        # self.__f_prf_DesacelMaxArr = 0.

        # razão de curva

        # razão de curva em rota (graus/s)
        self.__f_prf_raz_crv_rot = 3.

        # razão de curva no solo (graus/s)
        # self.__f_prf_raz_crv_slo = 0.

        # razão de curva no tráfego (graus/s)
        # self.__f_prf_raz_crv_trf = 3.

        # recebeu dados ?
        if f_data is not None:

            # recebeu uma lista ?
            if isinstance(f_data, dict):

                # cria uma performance com os dados da lista
                self.load_prf(f_data, fs_ver)

            # recebeu uma performance ?
            elif isinstance(f_data, CPrfNEW):

                # copia a performance
                self.copy_prf(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy_prf(self, f_prf):
        """
        copy constructor.
        cria uma nova performance a partir de uma outra performance.

        @param f_prf: performance a ser copiada.
        """
        # logger
        # M_LOG.info("copy_prf:>>")

        # verifica parâmetros de entrada
        assert f_prf

        # copy super class attributes
        super(CPrfNEW, self).copy_prf(f_prf)

        # esteira
        self._c_prf_esteira = f_prf.c_prf_esteira

        # máximos

        # teto de serviço (DIST)
        self.__f_prf_teto_sv = f_prf.f_prf_teto_sv

        # faixa (DIST)
        self.__f_prf_faixa = f_prf.f_prf_faixa

        # decolagem

        # velocidade de decolagem (VELO) (knots->m/s)
        self.__f_prf_vel_dec = f_prf.f_prf_vel_dec

        # velocidade de subida na decolagem (VELO) (knots->m/s)
        self.__f_prf_vel_sub_dec = f_prf.f_prf_vel_sub_dec

        # razão de subida na decolagem (VELO) (knots->m/s)
        self.__f_prf_raz_sub_dec = f_prf.f_prf_raz_sub_dec

        # razão máxima subida na decolagem (VELO) (knots->m/s)
        self.__f_prf_raz_max_sub_dec = f_prf.f_prf_raz_max_sub_dec

        # aproximação

        # velocidade de aproximação (VELO) (knots->m/s)
        self.__f_prf_vel_apx = f_prf.f_prf_vel_apx

        # razão de descida na aproximação (VELO) (knots->m/s)
        self.__f_prf_raz_des_apx = f_prf.f_prf_raz_des_apx

        # razão máxima descida na aproximação (VELO) (knots->m/s)
        self.__f_prf_raz_max_des_apx = f_prf.f_prf_raz_max_des_apx

        # cruzeiro

        # velocidade de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_vel_crz = f_prf.f_prf_vel_crz

        # velocidade máxima de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_vel_max_crz = f_prf.f_prf_vel_max_crz

        # razão de subida de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_raz_sub_crz = f_prf.f_prf_raz_sub_crz

        # razão máxima de subida de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_raz_max_sub_crz = f_prf.f_prf_raz_max_sub_crz

        # razão de descida de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_raz_des_crz = f_prf.f_prf_raz_des_crz

        # razão máxima descida de cruzeiro (VELO) (knots->m/s)
        self.__f_prf_raz_max_des_crz = f_prf.f_prf_raz_max_des_crz

        # aceleração

        # razão de variação de velocidade (aceleração) (ACEL)
        self.__f_prf_raz_var_vel = f_prf.f_prf_raz_var_vel

        # razão máxima variação de velocidade (aceleração) (ACEL)
        self.__f_prf_raz_max_var_vel = f_prf.f_prf_raz_max_var_vel

        # desaceleração de vôo
        # # self.__f_prf_desacel_crz = f_prf.f_prf_desacel_crz

        # aceleração mínima de decolagem
        # # self.__f_prf_AcelMinDep = f_prf.f_prf_AcelMinDep

        # desaceleração máxima de pouso
        # # self.__f_prf_DesacelMaxArr = f_prf.f_prf_DesacelMaxArr

        # razão de curva

        # razão de curva em rota
        self.__f_prf_raz_crv_rot = f_prf.f_prf_raz_crv_rot

        # razão de curva no solo
        # # self.__f_prf_RazCrvSlo = f_prf.f_prf_RazCrvSlo

        # razão de curva no tráfego
        # # self.__f_prf_RazCrvTrf = f_prf.f_prf_RazCrvTrf

        # logger
        # M_LOG.info("copy_prf:<<")

    # ---------------------------------------------------------------------------------------------

    def load_prf(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados de performance a partir de um dicionário (formato 0001).

        @param fdct_data: dicionário com os dados da performance.
        @param fs_ver: versão do formato dos dados.
        """
        # logger
        # M_LOG.info("load_prf:>>")

        # formato versão 0.01 ?
        if "0001" == fs_ver:

            # cria a performance
            self.make_prf(fdct_data)

        # senão, formato desconhecido
        else:

            # logger
            l_log = logging.getLogger("CPrfNEW::load_prf")
            l_log.setLevel(logging.NOTSET)
            l_log.critical(u"<E01: formato desconhecido.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # logger
        # M_LOG.info("load_prf:<<")

    # ---------------------------------------------------------------------------------------------

    def make_prf(self, fdct_data):
        """
        carrega os dados de performance a partir de um dicionário (formato 0001).

        @param fdct_data: dicionário com os dados da performance.
        """
        # logger
        # M_LOG.info("make_prf:>>")

        # identificação

        # identificação
        self.s_prf_id = fdct_data["nPrf"].strip().upper()

        # descrição
        self.s_prf_desc = fdct_data["descricao"]

        # esteira
        if "esteira" in fdct_data:
            self._c_prf_esteira = fdct_data["esteira"].strip().upper()

        # máximos

        # teto de serviço (DIST) (niv->ft->m)
        if "tetosv" in fdct_data:
            self.__f_prf_teto_sv = float(fdct_data["tetosv"]) * 100 * cdefs.D_CNV_FT2M

        # faixa (DIST) (niv->ft->m)
        if "faixa" in fdct_data:
            self.__f_prf_faixa = float(fdct_data["faixa"]) * 100 * cdefs.D_CNV_FT2M

        # decolagem

        # velocidade de decolagem (VELO) (knots->m/s)
        if "veldec" in fdct_data:
            self.__f_prf_vel_dec = float(fdct_data["veldec"]) * cdefs.D_CNV_KT2MS

        # velocidade de subida na decolagem (VELO) (knots->m/s)
        if "velsbdec" in fdct_data:
            self.__f_prf_vel_sub_dec = float(fdct_data["velsbdec"]) * cdefs.D_CNV_KT2MS

        # razão de subida na decolagem (VELO) (ft/min->m/s)
        if "rzsubdec" in fdct_data:
            self.__f_prf_raz_sub_dec = float(fdct_data["rzsubdec"]) * cdefs.D_CNV_FTMIN2MS

        # razão máxima subida na decolagem (VELO) (ft/min->m/s)
        if "rzmxsbdec" in fdct_data:
            self.__f_prf_raz_max_sub_dec = float(fdct_data["rzmxsbdec"]) * cdefs.D_CNV_FTMIN2MS

        # aproximação

        # velocidade de aproximação (VELO) (knots->m/s)
        if "velapx" in fdct_data:
            self.__f_prf_vel_apx = float(fdct_data["velapx"]) * cdefs.D_CNV_KT2MS

        # razão de descida na aproximação (VELO) (ft/min->m/s)
        if "rzdescapx" in fdct_data:
            self.__f_prf_raz_des_apx = float(fdct_data["rzdescapx"]) * cdefs.D_CNV_FTMIN2MS

        # razão máxima descida na aproximação (VELO) (ft/min->m/s)
        if "rzmxdesapx" in fdct_data:
            self.__f_prf_raz_max_des_apx = float(fdct_data["rzmxdesapx"]) * cdefs.D_CNV_FTMIN2MS

        # cruzeiro

        # velocidade de cruzeiro (VELO) (knots->m/s)
        if "velcruz" in fdct_data:
            self.__f_prf_vel_crz = float(fdct_data["velcruz"]) * cdefs.D_CNV_KT2MS

        # velocidade máxima de cruzeiro (VELO) (knots->m/s)
        if "velmxcrz" in fdct_data:
            self.__f_prf_vel_max_crz = float(fdct_data["velmxcrz"]) * cdefs.D_CNV_KT2MS

        # razão de subida de cruzeiro (VELO) (ft/min->m/s)
        if "rzsbcrz" in fdct_data:
            self.__f_prf_raz_sub_crz = float(fdct_data["rzsbcrz"]) * cdefs.D_CNV_FTMIN2MS

        # razão máxima de subida de cruzeiro (VELO) (ft/min->m/s)
        if "rzmxsbcrz" in fdct_data:
            self.__f_prf_raz_max_sub_crz = float(fdct_data["rzmxsbcrz"]) * cdefs.D_CNV_FTMIN2MS

        # razão de descida de cruzeiro (VELO) (ft/min->m/s)
        if "rzdescrz" in fdct_data:
            self.__f_prf_raz_des_crz = float(fdct_data["rzdescrz"]) * cdefs.D_CNV_FTMIN2MS

        # razão máxima descida de cruzeiro (VELO) (ft/min->m/s)
        if "rzmxdescrz" in fdct_data:
            self.__f_prf_raz_max_des_crz = float(fdct_data["rzmxdescrz"]) * cdefs.D_CNV_FTMIN2MS

        # aceleração

        # razão de variação de velocidade (aceleração) (ACEL) (knots/min->m/s²)
        if "razvarvel" in fdct_data:
            self.__f_prf_raz_var_vel = float(fdct_data["razvarvel"]) * cdefs.D_CNV_KMIN2MS2

        # razão máxima variação de velocidade (aceleração) (ACEL) (knots/min->m/s²)
        if "rzmxvarvel" in fdct_data:
            self.__f_prf_raz_max_var_vel = float(fdct_data["rzmxvarvel"]) * cdefs.D_CNV_KMIN2MS2
        '''
        # desaceleração de vôo (ACC) (knots/min -> m/s²)
        if "desacelcrz" in fdct_data:
            self.__f_prf_desacel_crz = float(fdct_data [ "desacelcrz" ]) * cdefs.D_CNV_KMIN2MS2

        # aceleração mínima de decolagem (ACC) (knots/min -> m/s²)
        if "acelmindep" in fdct_data:
            self.__f_prf_AcelMinDep = float(fdct_data [ "acelmindep" ]) * cdefs.D_CNV_KMIN2MS2

        # desaceleração máxima de pouso (ACC) (knots/min -> m/s²)
        if("desacelmaxarr" in fdct_data):
            self.__f_prf_DesacelMaxArr = float(fdct_data [ "desacelmaxarr" ]) * cdefs.D_CNV_KMIN2MS2
        '''
        # razão de curva

        # razão de curva em rota (graus/s)
        if "razcrvrot" in fdct_data:
            self.__f_prf_raz_crv_rot = float(fdct_data["razcrvrot"])
        '''
        # razão de curva no solo (graus/s)
        if "razcrvslo" in fdct_data:
            self.__f_prf_raz_crv_slo = float(fdct_data["razcrvslo"])

        # razão de curva no tráfego (graus/s)
        if "razcrvtrf" in fdct_data:
            self.__f_prf_raz_crv_trf = float(fdct_data["razcrvtrf"])
        '''
        # (bool)
        self.v_prf_ok = True

        # logger
        # M_LOG.info("make_prf:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_faixa(self):
        """
        get faixa
        """
        return self.__f_prf_faixa

    @f_prf_faixa.setter
    def f_prf_faixa(self, f_val):
        """
        set faixa
        """
        self.__f_prf_faixa = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_raz_crv_rot(self):
        """
        get razão de curva em rota (graus/s)
        """
        return self.__f_prf_raz_crv_rot

    @f_prf_raz_crv_rot.setter
    def f_prf_raz_crv_rot(self, f_val):
        """
        set razão de curva em rota (graus/s)
        """
        self.__f_prf_raz_crv_rot = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_raz_des_apx(self):
        """
        get 
        """
        return self.__f_prf_raz_des_apx

    @f_prf_raz_des_apx.setter
    def f_prf_raz_des_apx(self, f_val):
        """
        set 
        """
        self.__f_prf_raz_des_apx = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_raz_des_crz(self):
        """
        get razão de descida de cruzeiro (VELO) (m/s)
        """
        return self.__f_prf_raz_des_crz

    @f_prf_raz_des_crz.setter
    def f_prf_raz_des_crz(self, f_val):
        """
        set razão de descida de cruzeiro (VELO) (m/s)
        """
        self.__f_prf_raz_des_crz = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_raz_max_des_apx(self):
        """
        get 
        """
        return self.__f_prf_raz_max_des_apx

    @f_prf_raz_max_des_apx.setter
    def f_prf_raz_max_des_apx(self, f_val):
        """
        set 
        """
        self.__f_prf_raz_max_des_apx = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_raz_max_des_crz(self):
        """
        get 
        """
        return self.__f_prf_raz_max_des_crz

    @f_prf_raz_max_des_crz.setter
    def f_prf_raz_max_des_crz(self, f_val):
        """
        set 
        """
        self.__f_prf_raz_max_des_crz = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_raz_max_sub_crz(self):
        """
        get 
        """
        return self.__f_prf_raz_max_sub_crz

    @f_prf_raz_max_sub_crz.setter
    def f_prf_raz_max_sub_crz(self, f_val):
        """
        set 
        """
        self.__f_prf_raz_max_sub_crz = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_raz_max_sub_dec(self):
        """
        get 
        """
        return self.__f_prf_raz_max_sub_dec

    @f_prf_raz_max_sub_dec.setter
    def f_prf_raz_max_sub_dec(self, f_val):
        """
        set 
        """
        self.__f_prf_raz_max_sub_dec = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_raz_max_var_vel(self):
        """
        get 
        """
        return self.__f_prf_raz_max_var_vel

    @f_prf_raz_max_var_vel.setter
    def f_prf_raz_max_var_vel(self, f_val):
        """
        set 
        """
        self.__f_prf_raz_max_var_vel = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_raz_sub_crz(self):
        """
        get razão de subida de cruzeiro (VELO) (m/s)
        """
        return self.__f_prf_raz_sub_crz

    @f_prf_raz_sub_crz.setter
    def f_prf_raz_sub_crz(self, f_val):
        """
        set razão de subida de cruzeiro (VELO) (m/s)
        """
        self.__f_prf_raz_sub_crz = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_raz_sub_dec(self):
        """
        get 
        """
        return self.__f_prf_raz_sub_dec

    @f_prf_raz_sub_dec.setter
    def f_prf_raz_sub_dec(self, f_val):
        """
        set 
        """
        self.__f_prf_raz_sub_dec = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_raz_var_vel(self):
        """
        get razão de variação de velocidade (aceleração) (ACEL) (m/s²)
        """
        return self.__f_prf_raz_var_vel

    @f_prf_raz_var_vel.setter
    def f_prf_raz_var_vel(self, f_val):
        """
        set razão de variação de velocidade (aceleração) (ACEL) (m/s²)
        """
        self.__f_prf_raz_var_vel = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_teto_sv(self):
        """
        get teto de serviço (DIST)
        """
        return self.__f_prf_teto_sv

    @f_prf_teto_sv.setter
    def f_prf_teto_sv(self, f_val):
        """
        set teto de serviço (DIST)
        """
        self.__f_prf_teto_sv = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_vel_apx(self):
        """
        get 
        """
        return self.__f_prf_vel_apx

    @f_prf_vel_apx.setter
    def f_prf_vel_apx(self, f_val):
        """
        set 
        """
        self.__f_prf_vel_apx = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_vel_crz(self):
        """
        get 
        """
        return self.__f_prf_vel_crz

    @f_prf_vel_crz.setter
    def f_prf_vel_crz(self, f_val):
        """
        set 
        """
        self.__f_prf_vel_crz = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_vel_dec(self):
        """
        get 
        """
        return self.__f_prf_vel_dec

    @f_prf_vel_dec.setter
    def f_prf_vel_dec(self, f_val):
        """
        set 
        """
        self.__f_prf_vel_dec = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_vel_max_crz(self):
        """
        get 
        """
        return self.__f_prf_vel_max_crz

    @f_prf_vel_max_crz.setter
    def f_prf_vel_max_crz(self, f_val):
        """
        set 
        """
        self.__f_prf_vel_max_crz = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_prf_vel_sub_dec(self):
        """
        get 
        """
        return self.__f_prf_vel_sub_dec

    @f_prf_vel_sub_dec.setter
    def f_prf_vel_sub_dec(self, f_val):
        """
        set 
        """
        self.__f_prf_vel_sub_dec = f_val

# < the end >--------------------------------------------------------------------------------------
