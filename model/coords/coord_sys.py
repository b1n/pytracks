#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
coord_sys.

mantém os detalhes de um sistema de coordenadas.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import collections
import logging
import math
import re

# model
import model.coords.coord_model as model
import model.coords.coord_conv as conv
import model.coords.coord_defs as cdefs
import model.coords.coord_geod as geod
import model.coords.coord_geog as geog

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CCoordSys >------------------------------------------------------------------------------

class CCoordSys(model.CCoordModel):
    """
    mantém os detalhes de um sistema de coordenadas.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, ff_ref_lat=cdefs.M_REF_LAT, ff_ref_lng=cdefs.M_REF_LNG, ff_dcl_mag=cdefs.M_DCL_MAG):

        # logger
        # M_LOG.info("__init__:>>")
                
        # init super class
        super(CCoordSys, self).__init__(ff_ref_lat, ff_ref_lng, ff_dcl_mag)

        # M_LOG.debug(u"latitude de referência..:[{}]".format(ff_ref_lat))
        # M_LOG.debug(u"longitude de referência.:[{}]".format(ff_ref_lng))
        # M_LOG.debug(u"declinação de referência:[{}]".format(ff_dcl_mag))

        # herdados de CCoordModel
        # self.f_ref_lat    # latitude de referência
        # self.f_ref_lng    # longitude de referência
        # self.f_dcl_mag    # declinação magnética de referência

        # coordenadas geográficas de referênica e declinação magnética
        CREF = collections.namedtuple("CREF", "lat lng decl_mag")

        self.__nt_ref = CREF(lat=ff_ref_lat, lng=ff_ref_lng, decl_mag=ff_dcl_mag)
        assert self.__nt_ref

        # coordenadas de referência
        cdefs.D_REF_LAT = ff_ref_lat
        cdefs.D_REF_LNG = ff_ref_lng
        cdefs.D_DCL_MAG = ff_dcl_mag

        # dicionário de fixos
        self.__dct_fix = None

        # dicionário de indicativos
        self.__dct_fix_indc = None

        # logger
        # M_LOG.info("__init__:<<")

    # -------------------------------------------------------------------------------------------------

    def from_dict(self, f_dict):
        """
        conversão de um dicionário em latitude e longitude.

        @param f_dict: dicionário.

        @return lat, long
        """
        # logger
        # M_LOG.info("from_dict:>>")
                
        # verifica parâmetros de entrada
        assert f_dict

        # get coords fields
        l_cpo_b = f_dict.get("campoB", None)
        l_cpo_c = f_dict.get("campoC", None)
        l_cpo_d = f_dict.get("campoD", None)

        # coordenada
        li_rc, lf_lat, lf_lng = self.new_coord(f_dict["tipo"], f_dict["campoA"], l_cpo_b, l_cpo_c, l_cpo_d)

        # logger
        # M_LOG.info("from_dict:<<")
                
        # retorna a coordenada em latitude e longitude
        return lf_lat, lf_lng

    # ------------------------------------------------------------------------------------------------

    def __geo_fixo(self, fs_cpo_a, f_dct_fix=None):
        """
        encontra coordenada geográfica do fixo pelo número

        @param fs_cpo_a: número do fixo.
        @param f_dct_fix: dicionário de fixos.

        @return 0 se Ok, senão -1 = NOk
        """
        # logger
        # M_LOG.info("__geo_fixo:>>")
                
        # verifica parâmetros de entrada
        assert fs_cpo_a

        # dicionário de fixos
        if f_dct_fix is None:
            f_dct_fix = self.__dct_fix

        # verifica condições de execução
        assert f_dct_fix is not None
        
        # número do fixo
        ln_fix = int(fs_cpo_a)
        # M_LOG.debug("ln_fix:[%d]", ln_fix)
        '''
        # check for various possible errors
        if ((( ERANGE == errno) and (( LONG_MAX == ln_fix) or (LONG_MIN == ln_fix))) or (( 0 != errno) and (0 == ln_fix)))

            # logger
            # M_LOG.error("erro na conversão do número do fixo(campoA).")

            # logger
            # M_LOG.debug("<E01: erro na conversão do número do fixo(campoA).")

            # return
            return -1, 0., 0.
        '''
        # fixo existe no dicionário ?
        if ln_fix in f_dct_fix:

            # o fixo é válido ?
            if f_dct_fix[ln_fix].v_fix_ok:

                # latitude
                lf_lat = f_dct_fix[ln_fix].f_fix_lat
                # M_LOG.debug("latitude:[%f]", lf_lat)

                # longitude
                lf_lng = f_dct_fix[ln_fix].f_fix_lng
                # M_LOG.debug("longitude:[%f]", lf_lng)

                # logger
                # M_LOG.debug("<E02: ok.")

                # return
                return 0, lf_lat, lf_lng

        # logger
        # M_LOG.warn("fixo:[%s] não existe no dicionário.", fs_cpo_a)

        # logger
        # M_LOG.info("__geo_fixo:<<")
                
        # return
        return -1, 0., 0.

    # ---------------------------------------------------------------------------------------------

    def geo2xyz(self, f_lat, f_lng, f_alt=0.):
        """
        conversão de coordenadas geográficas em (x, y, z)
        """
        # logger
        # M_LOG.info("geo2xyz:><")

        # retorna a coordenada em x, y z
        # return geog.geo2xyz(f_lat, f_lng, self.__nt_ref.lat, self.__nt_ref.lng)
        # return geod.geod2ecef(f_lat, f_lng, f_alt)
        return geog.geo2xyz_3(f_lat, f_lng, f_alt)

    # ------------------------------------------------------------------------------------------------

    def __get_fixo_by_indc(self, fs_cpo_a, f_dct_fix_indc=None):
        """
        encontra o número do fixo pelo indicativo

        @param fs_cpo_a: indicativo do fixo.
        @param f_dct_fix_indc: dicionário de indicativos de fixos.

        @return número do fixo ou -1
        """
        # logger
        # M_LOG.info("__get_fixo_by_indc:>>")
                
        # verifica parâmetros de entrada
        assert fs_cpo_a

        # dicionário de indicativos
        if f_dct_fix_indc is None:
            f_dct_fix_indc = self.__dct_fix_indc

        # verifica condições de execução
        assert f_dct_fix_indc is not None
        
        # indicativo do fixo
        ls_fix = str(fs_cpo_a).strip().upper()
        # M_LOG.debug("ls_fix:[{}]".format(ln_fix))

        # logger
        # M_LOG.info("__get_fixo_by_indc:<<")
                
        # return
        return f_dct_fix_indc.get(ls_fix, -1)

    # ---------------------------------------------------------------------------------------------

    def new_coord(self, fc_tipo, fs_cpo_a, fs_cpo_b="", fs_cpo_c="", fs_cpo_d=""):
        """
        cria uma coordenada.
        """
        # logger
        # M_LOG.info("new_coord:>>")
                
        # verifica parâmetros de entrada
        if fc_tipo not in cdefs.D_SET_COORD_VALIDAS:

            # logger
            l_log = logging.getLogger("CCoordSys::new_coord")
            l_log.setLevel(logging.NOTSET)
            l_log.critical(u"<E01: tipo de coordenada({}) inválida.".format(fc_tipo))

            # cai fora
            return -1, -90., -180.

        # inicia os valores de resposta
        lf_lat = None
        lf_lng = None

        # coordenada distância/radial
        if 'D' == fc_tipo:

            #!!TipoD(lp_ref, fp_coord)

            # obtém as coordenadas geográficas do fixo(campoA)
            li_rc, lf_lat, lf_lng = self.__geo_fixo(fs_cpo_a)
            # M_LOG.debug("new_coord:coords(1): Lat:[%f]/Lng:[%f].", lf_lat, lf_lng)

            if 0 != li_rc:

                # -1 = fixo não encontrado
                # M_LOG.warning("fixo:[%4s] inexistente no dicionário de fixos.", fs_cpo_a)

                # cai fora
                return li_rc, lf_lat, lf_lng

            # converte para cartesiana
            lf_x, lf_y, _ = self.geo2xyz(lf_lat, lf_lng)
            # M_LOG.debug("new_coord:coords(2): X:[%f]/Y:[%f]", lf_x, lf_y)

            # distância(m)
            l_vd = float(fs_cpo_b) * cdefs.D_CNV_NM2M
            # M_LOG.debug("new_coord:distância(m):[%f]", l_vd)

            # radial(radianos)
            l_vr = math.radians(conv.azm2ang(float(fs_cpo_c)))
            # M_LOG.debug("new_coord:radial(rad):[%f]", l_vr)

            # x, y do ponto
            lf_x += l_vd * math.cos(l_vr)
            lf_y += l_vd * math.sin(l_vr)
            # M_LOG.debug("new_coord:coords(3): X:[%f]/Y:[%f]", lf_x, lf_y)

            # converte para geográfica
            lf_lat, lf_lng, _ = self.xyz2geo(lf_x, lf_y)
            # M_LOG.debug("new_coord:coords(4): Lat:[%f]/Lng:[%f]", lf_lat, lf_lng)

            # ok
            return li_rc, lf_lat, lf_lng

        # coordenada fixo
        elif 'F' == fc_tipo:

            # obtém as coordenadas geográficas do fixo(campoA)
            li_rc, lf_lat, lf_lng = self.__geo_fixo(fs_cpo_a)
            # M_LOG.debug("new_coord:coords(1): Lat:[%f]/Lng:[%f].", lf_lat, lf_lng)

            if 0 != li_rc:
                # -1 = fixo não encontrado
                # M_LOG.warn("fixo:[%4s] inexistente no dicionário de fixos.", fs_cpo_a)
                pass

            # cai fora
            return li_rc, lf_lat, lf_lng

        # coordenada geográfica formato ICA ?(formato GGGMM.mmmH)
        elif 'G' == fc_tipo:

            # latitude
            lf_lat = conv.parse_ica(fs_cpo_a)
            # M_LOG.debug("new_coord:lf_lat: " + str(lf_lat))

            # longitude
            lf_lng = conv.parse_ica(fs_cpo_b)
            # M_LOG.debug("new_coord:lf_lng: " + str(lf_lng))

            # ok
            return 0, lf_lat, lf_lng

        # coordenada indicativo de fixo
        elif 'I' == fc_tipo:

            # obtém o número do fixo pelo indicativo
            li_rc = self.__get_fixo_by_indc(fs_cpo_a)
            
            if li_rc < 0:

                # cai fora
                return -1, -90., -180.

            # obtém as coordenadas geográficas do indicativo do fixo
            li_rc, lf_lat, lf_lng = self.__geo_fixo(li_rc)
            # M_LOG.debug("new_coord:coords(1): Lat:[%f]/Lng:[%f].", lf_lat, lf_lng)

            if li_rc < 0:

                # -1 = fixo não encontrado
                # M_LOG.warn("fixo:[%4s] inexistente no dicionário de fixos.", fs_cpo_a)
                pass

            # cai fora
            return li_rc, lf_lat, lf_lng

        # coordenada geográfica formato decimal ?(formato +/-999.9999)
        elif 'L' == fc_tipo:

            # latitude
            lf_lat = float(fs_cpo_a)
            # M_LOG.debug("new_coord:lf_lat: " + str(lf_lat))

            # longitude
            lf_lng = float(fs_cpo_b)
            # M_LOG.debug("new_coord:lf_lng: " + str(lf_lng))

            # ok
            return 0, lf_lat, lf_lng

        # coordenada polar
        elif 'P' == fc_tipo:

            li_rc = -1

            lf_lat = -90.
            # M_LOG.debug("new_coord:lf_lat: " + str(lf_lat))
            lf_lng = -180.
            # M_LOG.debug("new_coord:lf_lng: " + str(lf_lng))

            # cai fora
            return li_rc, lf_lat, lf_lng

        # coordenada desconhecida
        elif 'X' == fc_tipo:

            li_rc = -1

            lf_lat = -90.
            # M_LOG.debug("new_coord:lf_lat: " + str(lf_lat))
            lf_lng = -180.
            # M_LOG.debug("new_coord:lf_lng: " + str(lf_lng))

            # cai fora
            return li_rc, lf_lat, lf_lng

        # senão, coordenada inválida
        else:
            # logger
            l_log = logging.getLogger("CCoordSys::new_coord")
            l_log.setLevel(logging.NOTSET)
            l_log.critical(u"<E02: tipo de coordenada({}) inválida.".format(fc_tipo))

            # cai fora
            return -1, -90., -180.

        '''
        # coordenada geográfica em decimal ?
        elif ("G0" == fc_tipo) or ("GC" == fc_tipo) or
             ("GD" == fc_tipo) or ("GF" == fc_tipo) or
             ("GG" == fc_tipo) or ("GP" == fc_tipo):

            lf_lat = float(f_dict [ "latitude" ])
            # M_LOG.debug("new_coord:lf_lat: " + str(lf_lat))

            lf_lng = float(f_dict [ "longitude" ])
            # M_LOG.debug("new_coord:lf_lng: " + str(lf_lng))

        # coordenada geográfica formato ICA ?(formato GGGMM.mmmH)
        elif "G1" == fc_tipo:

            lf_lat = conv.parse_ica(f_dict [ "latitude" ])
            # M_LOG.debug("new_coord:lf_lat: " + str(lf_lat))
            lf_lng = conv.parse_ica(f_dict [ "longitude" ])
            # M_LOG.debug("new_coord:lf_lng: " + str(lf_lng))

        # coordenada geográfica formato ICA ?(formato GGGMM.mmmH/GGMM.mmmH)
        elif "GI" == fc_tipo:

            lf_lat = conv.parse_ica_2(f_dict [ "latitude" ])
            # M_LOG.debug("new_coord:lf_lat: " + str(lf_lat))
            lf_lng = conv.parse_ica_2(f_dict [ "longitude" ])
            # M_LOG.debug("new_coord:lf_lng: " + str(lf_lng))
        '''
        # logger
        # M_LOG.info("new_coord:<<")
                
        # return
        return -1, -90., -180.

    # ---------------------------------------------------------------------------------------------

    def xyz2geo(self, ff_x, ff_y, ff_z=0.):
        """
        conversão de coordenadas geográficas em (x, y, z)
        """
        # logger
        # M_LOG.info("xyz2geo:>>")

        # retorna a coordenada em latitude e longitude
        # return geog.xy2geo(ff_x, ff_y)
        # return geod.ecef2geod(ff_x, ff_y, ff_z)
        return geog.xyz2geo_3(ff_x, ff_y, ff_z)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_fix(self):
        """
        get dicionário de fixos
        """
        return self.__dct_fix

    @dct_fix.setter
    def dct_fix(self, f_val):
        """
        set dicionário de fixos
        """
        self.__dct_fix = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_fix_indc(self):
        """
        get dicionário de indicativos
        """
        return self.__dct_fix_indc

    @dct_fix_indc.setter
    def dct_fix_indc(self, f_val):
        """
        set dicionário de indicativos
        """
        self.__dct_fix_indc = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def nt_ref(self):
        """
        get referência
        """
        return self.__nt_ref

    @nt_ref.setter
    def nt_ref(self, f_val):
        """
        set referência
        """
        self.__nt_ref = f_val

# < the end >--------------------------------------------------------------------------------------
