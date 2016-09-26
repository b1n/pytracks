#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
coord_trk.
mantém os detalhes de uma coordenada.

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
# import re

# TrackS / model
from .. import glb_defs as gdefs

# TrackS / model / coord
import model.coord.coord_base as coord

# < module data >----------------------------------------------------------------------------------

# logging level
M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# < class CoordTRK >----------------------------------------------------------------------------


class CoordTRK(coord.CoordBase):

    """
    mantém os detalhes de um sistema de coordenadas.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # init super class
        super(CoordTRK, self).__init__()

        # coordenadas geográficas de referênica e declinação magnética
        tREF = collections.namedtuple("tREF", "fLat fLng fDeclMag")

        # obtém latitude 15* 47' 38" S
        l_fLat = -1 *(15. +(47. / 60.) +(38. / 3600.))
        # M_LOG.debug("latitude(ref):[%f]", l_fLat)

        # obtém longitude 47* 52' 58" W
        l_fLng = -1 *(47. +(52. / 60.) +(58. / 3600.))
        # M_LOG.debug("longitude(ref):[%f]", l_fLng)

        # obtém declinação magnética
        l_fDeclMag = 0.
        # M_LOG.debug("decl.Mag:[%f]", l_fDeclMag)

        self._tREF = tREF(fLat=l_fLat, fLng=l_fLng, fDeclMag=l_fDeclMag)
        assert self._tREF

        # dicionário de fixos
        self._dct_fix = None

    # -------------------------------------------------------------------------------------------------

    def fromDict(self, f_dict):
        """
        conversão de um dicionário em latitude e longitude.

        @param f_dict: dicionário.

        @return lat, long
        """
        # verifica parâmetros de entrada
        assert f_dict

        # campoB existe ?
        if "campoB" in f_dict:
            l_cpoB = f_dict["campoB"]

        else:
            l_cpoB = None

        # campoC existe ?
        if "campoC" in f_dict:
            l_cpoC = f_dict["campoC"]

        else:
            l_cpoC = None

        # campoD existe ?
        if "campoD" in f_dict:
            l_cpoD = f_dict["campoD"]

        else:
            l_cpoD = None

        # coordenada
        l_iRC, l_fLat, l_fLng = self.newCoord(f_dict["tipo"], f_dict["campoA"], l_cpoB, l_cpoC, l_cpoD)

        # retorna a coordenada em latitude e longitude
        return l_fLat, l_fLng

    # ------------------------------------------------------------------------------------------------

    def geoAzim(self, f_dLatPto, f_dLngPto):
        """
        cálculo do azimute entre duas coordenadas geográficas

        @param f_dLatPto: latitude  do ponto em graus
        @param f_dLngPto: longitude do ponto em graus

        @return azimute entre a referência e o ponto em radianos
        """
        # verifica parâmetros de entrada
        # assert ??

        l_dFiRefRad = math.radians(self._tREF.fLat)
        # M_LOG.debug("LatRefRad:[%f]", l_dFiRefRad)

        l_dTetaRefRad = math.radians(self._tREF.fLng)
        # M_LOG.debug("LngRefRad:[%f]", l_dTetaRefRad)

        l_iR = self.w_EARTH_RADIUS_MN * math.cos(l_dFiRefRad) * math.cos(l_dTetaRefRad)
        l_jR = self.w_EARTH_RADIUS_MN * math.cos(l_dFiRefRad) * math.sin(l_dTetaRefRad)
        l_kR = self.w_EARTH_RADIUS_MN * math.sin(l_dFiRefRad)

        # coordenadas retangulares do ponto
        # M_LOG.debug("LatPto:[%f]", f_dLatPto)
        # M_LOG.debug("LngPto:[%f]", f_dLngPto)

        l_dFiPtoRad = math.radians(f_dLatPto)
        # M_LOG.debug("LatPtoRad:[%f]", l_dFiPtoRad)

        l_dTetaPtoRad = math.radians(f_dLngPto)
        # M_LOG.debug("LngPtoRad:[%f]", l_dTetaPtoRad)

        l_iP = self.w_EARTH_RADIUS_MN * math.cos(l_dFiPtoRad) * math.cos(l_dTetaPtoRad)
        l_jP = self.w_EARTH_RADIUS_MN * math.cos(l_dFiPtoRad) * math.sin(l_dTetaPtoRad)
        l_kP = self.w_EARTH_RADIUS_MN * math.sin(l_dFiPtoRad)

        # condições especiais de retorno
        if (l_dFiRefRad == l_dFiPtoRad) and (l_dTetaRefRad == l_dTetaPtoRad):

            # return
            return 0.

        if (l_dFiRefRad == l_dFiPtoRad) and (l_dTetaRefRad > l_dTetaPtoRad):

            # return
            return math.radians(270.)

        if (l_dFiRefRad == l_dFiPtoRad) and (l_dTetaRefRad < l_dTetaPtoRad):

            # return
            return math.radians(90.)

        if (l_dFiRefRad > l_dFiPtoRad) and (l_dTetaRefRad == l_dTetaPtoRad):

            # return
            return math.pi

        if (l_dFiRefRad < l_dFiPtoRad) and (l_dTetaRefRad == l_dTetaPtoRad):

            # return
            return 0.

        # ângulo entre a referência e o ponto
        l_dGama =((l_iR * l_iP) +(l_jR * l_jP) +(l_kR * l_kP)) /(pow(self.w_EARTH_RADIUS_MN, 2))

        if 1 == int(l_dGama):
            l_dArcGama = 0.

        else:
            l_dArcGama = math.acos(l_dGama)

        # coordenadas retangulares do ponto X
        # M_LOG.debug("LatX:[%f]", f_dLatPto)
        # M_LOG.debug("LngX:[%f]", self._tREF.fLng)

        l_dFiX = math.radians(f_dLatPto)
        # M_LOG.debug("LatX:[%f]", l_dFiX)

        l_dTetaX = math.radians(self._tREF.fLng)
        # M_LOG.debug("LngX:[%f]", l_dTetaX)

        l_iX = self.w_EARTH_RADIUS_MN * math.cos(l_dFiX) * math.cos(l_dTetaX)
        l_jX = self.w_EARTH_RADIUS_MN * math.cos(l_dFiX) * math.sin(l_dTetaX)
        l_kX = self.w_EARTH_RADIUS_MN * math.sin(l_dFiX)

        # cálculo do ângulo entre X e o ponto
        l_dDelta =((l_iX * l_iP) +(l_jX * l_jP) +(l_kX * l_kP)) / pow(self.w_EARTH_RADIUS_MN, 2)

        if 1 == int(l_dDelta):
            l_dArcDelta = 0.

        else:
            l_dArcDelta = math.acos(l_dDelta)

        # cálculo do azimute básico
        l_dAux = math.sin(l_dArcDelta) / math.sin(l_dArcGama)

        if l_dAux > 1.:
            l_dAux = 1.

        else:
            if l_dAux < -1.:
                l_dAux = -1.

        l_dAzim = math.asin(l_dAux)
        # M_LOG.debug("azimute básico:[%f]", l_dAzim)

        l_iQuad = 0

        # cálculo do azimute corrigido
        if (l_dFiRefRad < l_dFiPtoRad) and (l_dTetaRefRad < l_dTetaPtoRad):
            l_iQuad = 1
        if (l_dFiRefRad < l_dFiPtoRad) and (l_dTetaRefRad > l_dTetaPtoRad):
            l_iQuad = 4
        if (l_dFiRefRad > l_dFiPtoRad) and (l_dTetaRefRad > l_dTetaPtoRad):
            l_iQuad = 3
        if (l_dFiRefRad > l_dFiPtoRad) and (l_dTetaRefRad < l_dTetaPtoRad):
            l_iQuad = 2

        # M_LOG.debug("quadrante:[%1d]", l_iQuad)

        if 2 == l_iQuad:
            l_dAzim = math.pi - l_dAzim
        if 3 == l_iQuad:
            l_dAzim = math.pi + l_dAzim
        if 4 == l_iQuad:
            l_dAzim =(2 * math.pi) - l_dAzim

        # M_LOG.debug("azim:[%f]", l_dAzim)

        # return
        return l_dAzim

    # ------------------------------------------------------------------------------------------------

    def geoDist(self, f_dLatPto, f_dLngPto):
        """
        cálculo da distância entre dois pontos geográficos

        @param f_dLatPto: latitude  do ponto em graus
        @param f_dLngPto: longitude do ponto em graus

        @return distância entre a referência e o ponto em NM
        """
        # verifica parâmetros de entrada
        # assert ??

        # coordenadas retangulares da referência
        # M_LOG.debug("LatRef:[%f]", self._tREF.fLat)
        # M_LOG.debug("LonRef:[%f]", self._tREF.fLng)

        l_dLatRefRad = math.radians(self._tREF.fLat)
        # M_LOG.debug("LatRad:[%f]", l_dLatRefRad)

        l_dLngRefRad = math.radians(self._tREF.fLng)
        # M_LOG.debug("LonRad:[%f]", l_dLngRefRad)

        l_iR = self.w_EARTH_RADIUS_MN * math.cos(l_dLatRefRad) * math.cos(l_dLngRefRad)
        l_jR = self.w_EARTH_RADIUS_MN * math.cos(l_dLatRefRad) * math.sin(l_dLngRefRad)
        l_kR = self.w_EARTH_RADIUS_MN * math.sin(l_dLatRefRad)

        # coordenadas retangulares do ponto
        # M_LOG.debug("LatPto:[%f]", f_dLatPto)
        # M_LOG.debug("LonPto:[%f]", f_dLngPto)

        l_dLatPtoRad = math.radians(f_dLatPto)
        # M_LOG.debug("LatPR:[%f]", l_dLatPtoRad)

        l_dLngPtoRad = math.radians(f_dLngPto)
        # M_LOG.debug("LonPR:[%f]", l_dLngPtoRad)

        l_iP = self.w_EARTH_RADIUS_MN * math.cos(l_dLatPtoRad) * math.cos(l_dLngPtoRad)
        l_jP = self.w_EARTH_RADIUS_MN * math.cos(l_dLatPtoRad) * math.sin(l_dLngPtoRad)
        l_kP = self.w_EARTH_RADIUS_MN * math.sin(l_dLatPtoRad)

        # l_dDist

        # cálculo da distância entre a referência e o ponto
        if (l_dLatRefRad == l_dLatPtoRad) and (l_dLngRefRad == l_dLngPtoRad):
            l_dDist = 0.

        else:

            l_dGama =((l_iR * l_iP) +(l_jR * l_jP) +(l_kR * l_kP)) /(pow(self.w_EARTH_RADIUS_MN, 2))
            l_dDist = self.w_EARTH_RADIUS_MN * math.acos(l_dGama)

        # M_LOG.debug("dist:[%f]", l_dDist)

        # return
        return l_dDist

    # ------------------------------------------------------------------------------------------------

    def geoFixo(self, f_sCpoA, f_dct_fix):
        """
        encontra coordenada geográfica do fixo pelo número

        @param f_sCpoA: número do fixo.
        @param f_dct_fix: dicionário de fixos.

        @return 0 se Ok, senão -1 = NOk
        """
        # verifica parâmetros de entrada
        assert f_sCpoA
        assert f_dct_fix

        # número do fixo
        l_nFix = int(f_sCpoA)
        # M_LOG.debug("l_nFix:[%d]", l_nFix)
        '''
        # check for various possible errors
        if ((( ERANGE == errno) and (( LONG_MAX == l_nFix) or (LONG_MIN == l_nFix))) or (( 0 != errno) and (0 == l_nFix)))

            # logger
            # M_LOG.error("erro na conversão do número do fixo(campoA).")

            # logger
            # M_LOG.debug("<E01: erro na conversão do número do fixo(campoA).")

            # return
            return -1, 0., 0.
        '''
        # fixo existe no dicionário ?
        if l_nFix in f_dct_fix:

            # o fixo é válido ?
            if f_dct_fix[l_nFix].vFixOk:

                # latitude
                l_fLat = f_dct_fix[l_nFix].fFixLat
                # M_LOG.debug("latitude:[%f]", l_fLat)

                # longitude
                l_fLng = f_dct_fix[l_nFix].fFixLng
                # M_LOG.debug("longitude:[%f]", l_fLng)

                # logger
                # M_LOG.debug("<E02: ok.")

                # return
                return 0, l_fLat, l_fLng

        # logger
        # M_LOG.warn("fixo:[%s] não existe no dicionário.", f_sCpoA)

        # return
        return -1, 0., 0.

    # ---------------------------------------------------------------------------------------------

    def newCoord(self, f_cTipo, f_sCpoA, f_sCpoB="", f_sCpoC="", f_sCpoD=""):
        """
        cria uma coordenada.
        """
        # verifica parâmetros de entrada
        assert f_cTipo

        # inicia os valores de resposta
        l_fLat = None
        l_fLng = None

        # coordenada distância/radial
        if 'D' == f_cTipo:

            #!!TipoD(l_pREF, f_pCoord)

            # obtém as coordenadas geográficas do fixo(campoA)
            l_iRC, l_fLat, l_fLng = self.geoFixo(f_sCpoA, self._dct_fix)
            # M_LOG.debug("coords(1): Lat:[%f]/Lng:[%f].", l_fLat, l_fLng)

            if 0 != l_iRC:

                # -1 = fixo não encontrado
                # M_LOG.warn("fixo:[%4s] inexistente no dicionário de fixos.", f_sCpoA)

                # cai fora
                return l_iRC, l_fLat, l_fLng

            # converte para cartesiana
            l_fX, l_fY = self.geo2xy(l_fLat, l_fLng)
            # M_LOG.debug("coords(2): X:[%f]/Y:[%f]", l_fX, l_fY)

            # distância(m)
            l_vd = float(f_sCpoB) * gdefs.D_CNV_NM2M
            # M_LOG.debug("distância(m):[%f]", l_vd)

            # radial(radianos)
            l_vr = float(f_sCpoC)
            l_vr = math.radians(self.azm2deg(l_vr))
            # M_LOG.debug("radial(rad):[%f]", l_vr)

            # X, Y do ponto
            l_fX += l_vd * math.cos(l_vr)
            l_fY += l_vd * math.sin(l_vr)
            # M_LOG.debug("coords(3): X:[%f]/Y:[%f]", l_fX, l_fY)

            # converte para geográfica
            l_fLat, l_fLng = self.xy2geo(l_fX, l_fY)
            # M_LOG.debug("coords(4): Lat:[%f]/Lng:[%f]", l_fLat, l_fLng)

            # ok
            return l_iRC, l_fLat, l_fLng

        # coordenada geográfica formato ICA ?(formato GGGMM.mmmH)
        elif 'G' == f_cTipo:

            # latitude
            l_fLat = self.parseICA(f_sCpoA)
            # M_LOG.debug("l_fLat: " + str(l_fLat))

            # longitude
            l_fLng = self.parseICA(f_sCpoB)
            # M_LOG.debug("l_fLng: " + str(l_fLng))

            # ok
            return 0, l_fLat, l_fLng

        # coordenada fixo
        elif 'F' == f_cTipo:

            # obtém as coordenadas geográficas do fixo(campoA)
            l_iRC, l_fLat, l_fLng = self.geoFixo(f_sCpoA, self._dct_fix)
            # M_LOG.debug("coords(1): Lat:[%f]/Lng:[%f].", l_fLat, l_fLng)

            if 0 != l_iRC:

                # -1 = fixo não encontrado
                # M_LOG.warn("fixo:[%4s] inexistente no dicionário de fixos.", f_sCpoA)

                pass

            # cai fora
            return l_iRC, l_fLat, l_fLng

        # coordenada polar
        elif 'P' == f_cTipo:

            l_iRC = -1

            l_fLat = 90.
            # M_LOG.debug("l_fLat: " + str(l_fLat))
            l_fLng = 180.
            # M_LOG.debug("l_fLng: " + str(l_fLng))

            # cai fora
            return l_iRC, l_fLat, l_fLng

        # coordenada desconhecida
        elif 'X' == f_cTipo:

            l_iRC = -1

            l_fLat = 90.
            # M_LOG.debug("l_fLat: " + str(l_fLat))
            l_fLng = 180.
            # M_LOG.debug("l_fLng: " + str(l_fLng))

            # cai fora
            return l_iRC, l_fLat, l_fLng

        # senão, coordenada inválida
        else:

            # logger
            # M_LOG.warning(u"Tipo de coordenada(%c) inválida." % f_cTipo)
            pass
        '''
        # coordenada geográfica em decimal ?
        elif ("G0" == f_cTipo) or ("GC" == f_cTipo) or
             ("GD" == f_cTipo) or ("GF" == f_cTipo) or
             ("GG" == f_cTipo) or ("GP" == f_cTipo):

            l_fLat = float(f_dict [ "latitude" ])
            # M_LOG.debug("l_fLat: " + str(l_fLat))

            l_fLng = float(f_dict [ "longitude" ])
            # M_LOG.debug("l_fLng: " + str(l_fLng))

        # coordenada geográfica formato ICA ?(formato GGGMM.mmmH)
        elif "G1" == f_cTipo:

            l_fLat = parseICA(f_dict [ "latitude" ])
            # M_LOG.debug("l_fLat: " + str(l_fLat))
            l_fLng = parseICA(f_dict [ "longitude" ])
            # M_LOG.debug("l_fLng: " + str(l_fLng))

        # coordenada geográfica formato ICA ?(formato GGGMM.mmmH/GGMM.mmmH)
        elif "GI" == f_cTipo:

            l_fLat = parseICA_2(f_dict [ "latitude" ])
            # M_LOG.debug("l_fLat: " + str(l_fLat))
            l_fLng = parseICA_2(f_dict [ "longitude" ])
            # M_LOG.debug("l_fLng: " + str(l_fLng))
        '''
        # return
        return -1, None, None

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_fix(self):
        """
        dicionário de fixos
        """
        return self._dct_fix

    @dct_fix.setter
    def dct_fix(self, f_dctVal):
        self._dct_fix = f_dctVal

# < the end >--------------------------------------------------------------------------------------
