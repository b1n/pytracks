#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
trf_model.

mantém os detalhes comuns de um tráfego.

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
# import logging

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CTrfModel >------------------------------------------------------------------------------

class CTrfModel(object):
    """
    mantém os detalhes comuns de um tráfego.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_data=None):

        # logger
        # M_LOG.info("__init__:>>")

        # flag ok (bool)
        self.__v_trf_ok = False

        # identificação do tráfego
        self.__i_trf_id = 0
        # indicativo do tráfego
        self.__s_trf_ind = ""

        # performance (designador)
        self.__ptr_trf_prf = None

        # X (m)
        self.__f_trf_x = 0.
        # Y (m)
        self.__f_trf_y = 0.
        # Z (m)
        self.__f_trf_z = 0.

        # altitude atual (m)
        self.__f_trf_alt_atu = 0.
        # nível autorizado (ft/100)
        self.__i_trf_niv_aut = 0
        # proa atual (gr)
        self.__f_trf_pro_atu = 0.
        # velocidade atual (m/s)
        self.__f_trf_vel_atu = 0.

        # hora de ativação (h:m:s)
        self.__t_trf_hor_atv = (0, 0, 0)

        # status
        # self._c_trf_status = 'P'
        # flag em vôo (T) / no solo (F)
        # self._v_trf_voo = True

        # recebeu dados ?
        if f_data is not None:

            # recebeu um tráfego ?
            if isinstance(f_data, CTrfModel):

                # copia o tráfego
                self.copy_trf(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy_trf(self, f_trf):
        """
        copy constructor.
        cria um novo tráfego a partir de um outro tráfego.

        @param f_trf: tráfego a ser copiado.
        """
        # logger
        # M_LOG.info("copy_trf:>>")

        # verifica parâmetros de entrada
        assert f_trf

        # identificação do tráfego
        self.__i_trf_id = f_trf.i_trf_id
        # indicativo do tráfego
        self.__s_trf_ind = f_trf.s_trf_ind
        # performance (designador)
        self.__ptr_trf_prf = f_trf.ptr_trf_prf
        # assert self.__ptr_trf_prf
        # assert self.__ptr_trf_prf.v_prf_ok

        # posição
        self.__f_trf_x = f_trf.f_trf_x
        self.__f_trf_y = f_trf.f_trf_y
        self.__f_trf_z = f_trf.f_trf_z
        # M_LOG.debug("posição atual: " + str((self.__f_trf_x, self.__f_trf_y, self.__f_trf_z)))

        # altitude (m)
        self.__f_trf_alt_atu = f_trf.f_trf_alt_atu
        # M_LOG.debug("altitude atual: " + str(self.__f_trf_alt_atu))
        # nível autorizado (ft/100)
        self.__i_trf_niv_aut = f_trf.i_trf_niv_aut
        # proa (gr)
        self.__f_trf_pro_atu = f_trf.f_trf_pro_atu
        # velocidade (m/s)
        self.__f_trf_vel_atu = f_trf.f_trf_vel_atu

        # hora de ativação (h:m:s)
        self.__t_trf_hor_atv = f_trf.t_trf_hor_atv

        # flag ok (bool)
        self.__v_trf_ok = f_trf.v_trf_ok

        # logger
        # M_LOG.info("copy_trf:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def f_trf_alt_atu(self):
        """
        get Z/altitude
        """
        return self.__f_trf_alt_atu

    @f_trf_alt_atu.setter
    def f_trf_alt_atu(self, f_val):
        """
        set Z/altitude
        """
        self.__f_trf_alt_atu = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def t_trf_hor_atv(self):
        """
        get hora de ativação
        """
        return self.__t_trf_hor_atv

    @t_trf_hor_atv.setter
    def t_trf_hor_atv(self, f_val):
        """
        set hora de ativação
        """
        self.__t_trf_hor_atv = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def i_trf_id(self):
        """
        get identificação
        """
        return self.__i_trf_id

    @i_trf_id.setter
    def i_trf_id(self, f_val):
        """
        set identificação
        """
        self.__i_trf_id = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def s_trf_ind(self):
        """
        get indicativo
        """
        return self.__s_trf_ind.decode("utf-8")

    @s_trf_ind.setter
    def s_trf_ind(self, f_val):
        """
        set indicativo
        """
        self.__s_trf_ind = f_val.strip().upper().encode("utf-8")

    # ---------------------------------------------------------------------------------------------

    @property
    def i_trf_niv_aut(self):
        """
        get nível autorizado
        """
        return self.__i_trf_niv_aut

    @i_trf_niv_aut.setter
    def i_trf_niv_aut(self, f_val):
        """
        set nível autorizado
        """
        self.__i_trf_niv_aut = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_trf_pro_atu(self):
        """
        get proa atual
        """
        return self.__f_trf_pro_atu

    @f_trf_pro_atu.setter
    def f_trf_pro_atu(self, f_val):
        """
        set proa atual
        """
        # verifica parâmetros de entrada
        assert 0. <= f_val <= 360.

        # proa atual (gr)
        self.__f_trf_pro_atu = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def v_trf_ok(self):
        """
        get flag ok
        """
        return self.__v_trf_ok

    @v_trf_ok.setter
    def v_trf_ok(self, f_val):
        """
        set flag ok
        """
        self.__v_trf_ok = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def ptr_trf_prf(self):
        """
        get performance
        """
        return self.__ptr_trf_prf

    @ptr_trf_prf.setter
    def ptr_trf_prf(self, f_val):
        """
        set performance
        """
        self.__ptr_trf_prf = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_trf_vel_atu(self):
        """
        get velocidade atual
        """
        return self.__f_trf_vel_atu

    @f_trf_vel_atu.setter
    def f_trf_vel_atu(self, f_val):
        """
        set velocidade atual
        """
        self.__f_trf_vel_atu = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_trf_x(self):
        """
        get X
        """
        return self.__f_trf_x

    @f_trf_x.setter
    def f_trf_x(self, f_val):
        """
        set X
        """
        self.__f_trf_x = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_trf_y(self):
        """
        get Y
        """
        return self.__f_trf_y

    @f_trf_y.setter
    def f_trf_y(self, f_val):
        """
        set Y
        """
        self.__f_trf_y = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_trf_z(self):
        """
        get Z
        """
        return self.__f_trf_z

    @f_trf_z.setter
    def f_trf_z(self, f_val):
        """
        set Z
        """
        self.__f_trf_z = f_val

    # ---------------------------------------------------------------------------------------------
    # properties

    # _ptr_trf_prf = property(get_anv_prf_id, set_anv_prf_id)
    # _szTrfDesc = property(get_anv_desc, set_anv_desc)

# < the end >--------------------------------------------------------------------------------------
