#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
coord_geod.

manage geographical points, perform conversions, etc.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import math

import coord_conv as conv
import coord_defs as cdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------

def __calc_gama(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    cálculo do ângulo entre a referência e o ponto

    @param ff_lat_pto: latitude do ponto em graus
    @param ff_lng_pto: longitude do ponto em graus
    @param ff_lat_ref: latitude da referência em graus
    @param ff_lng_ref: longitude da referência em graus

    @return ângulo entre a referência e o ponto
    """
    # logger
    # M_LOG.info("__calc_gama:>>")

    # verifica parametros de entrada
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # verifica coincidência de pontos
    if (ff_lat_pto == ff_lat_ref) and (ff_lng_pto == ff_lng_ref):

        # pontos coincidentes
        return 0.

    # obtém as coordenadas do ponto de referência em radianos
    lf_lat_ref = math.radians(ff_lat_ref)
    lf_lng_ref = math.radians(ff_lng_ref)

    lf_ir = math.cos(lf_lat_ref) * math.cos(lf_lng_ref)
    lf_jr = math.cos(lf_lat_ref) * math.sin(lf_lng_ref)
    lf_kr = math.sin(lf_lat_ref)

    # obtém as coordenadas do ponto em radianos
    lf_lat_pto = math.radians(ff_lat_pto)
    lf_lng_pto = math.radians(ff_lng_pto)

    lf_ip = math.cos(lf_lat_pto) * math.cos(lf_lng_pto)
    lf_jp = math.cos(lf_lat_pto) * math.sin(lf_lng_pto)
    lf_kp = math.sin(lf_lat_pto)

    # logger
    # M_LOG.info("__calc_gama:<<")

    # distância entre a referência e o ponto
    return (lf_ir * lf_ip) + (lf_jr * lf_jp) + (lf_kr * lf_kp)

# -------------------------------------------------------------------------------------------------

def declinaPonto(f_oXY, f_oRef):
    """
    negativo (O/W), gira no sentido horário

    @param f_oXY: DOCUMENT ME!
    @param f_oRef: DOCUMENT ME!

    @return xsXY.
    """
    # logger
    # M_LOG.info("declinaPonto:>>")

    # verifica parametros de entrada
    assert f_oXY
    assert f_oRef

    # M_LOG.debug("_fX: [%f]" % f_oXY._fX)
    # M_LOG.debug("_fY: [%f]" % f_oXY._fY)

    # salva nas áreas de trabalho
    l_fX = f_oXY._fX
    l_fY = f_oXY._fY

    # declinação a leste ?
    if ('E' == f_oRef._cHem) or ('e' == f_oRef._cHem):

        # ajuste da coordenada com a declinação magnética da área
        f_oXY._fX = +(l_fX * math.cos(math.radians(math.fabs(f_oRef._fDcl)))) - \
                     (l_fY * math.sin(math.radians(math.fabs(f_oRef._fDcl))))

        f_oXY._fY = +(l_fX * math.sin(math.radians(math.fabs(f_oRef._fDcl)))) + \
                     (l_fY * math.cos(math.radians(math.fabs(f_oRef._fDcl))))

    # senão, declinação a oeste
    else:
        # ajuste da coordenada com a declinação magnética da área
        f_oXY._fX = +(l_fX * math.cos(math.radians(math.fabs(f_oRef._fDcl)))) + \
                     (l_fY * math.sin(math.radians(math.fabs(f_oRef._fDcl))))

        f_oXY._fY = -(l_fX * math.sin(math.radians(math.fabs(f_oRef._fDcl)))) + \
                     (l_fY * math.cos(math.radians(math.fabs(f_oRef._fDcl))))

    # M_LOG.debug("_fX: [%f]" % f_oXY._fX)
    # M_LOG.debug("_fY: [%f]" % f_oXY._fY)
    # M_LOG.debug("_fZ: [%f]" % f_oXY._fZ)

    # logger
    # M_LOG.info("declinaPonto:<<")

    # return
    return f_oXY

# -------------------------------------------------------------------------------------------------

def declina_ponto_2(_dX, _dY, f_szDclMag):
    """
    @param f_xyzP: DOCUMENT ME!
    @param f_szDclMag: DOCUMENT ME!
    """
    # logger
    # M_LOG.info("declina_ponto_2:>>")

    # quadrante
    li_quad = 0

    # declinação magnética
    lf_dec_mag = 0.

    # angulo e distância
    lf_ang = 0.
    lf_dst = 0.

    # condições marginais
    if (_dX != 0.) or (_dY != 0.):
        if 0. == _dX:
            if _dY > 0.:
                # determinacao da distancia & angulo trigonometrico
                lf_dst = _dY
                lf_ang = RAD_PI_2

            else:
                # determinacao da distancia & angulo trigonometrico
                lf_dst = abs(_dY)
                lf_ang = RAD_3PI_2

        else:
            if _dY == 0.:
                if _dX > 0.:
                    # determinacao da distancia & angulo trigonometrico
                    lf_dst = _dX
                    lf_ang = 0.

                else:
                    # determinacao da distancia & angulo trigonometrico
                    lf_dst = abs(_dX)
                    lf_ang = math.pi

            else:
                # determinacao do quadrante
                if _dX > 0.:
                    if _dY > 0.:
                        li_quad = 1

                    else:
                        li_quad = 4

                elif _dY > 0.:
                    li_quad = 2

                else:
                    li_quad = 3

                # determinacao da distancia & angulo trigonometrico
                lf_dst = math.sqrt(pow(_dX, 2) + pow(_dY, 2))
                lf_ang = math.atan(fabs(_dY) / fabs(_dX))

        # correcao do angulo trigonometrico devido ao quadrante
        if 2 == li_quad:
            lf_ang = math.pi - lf_ang

        elif 3 == li_quad:
            lf_ang += math.pi

        elif 4 == li_quad:
            lf_ang = RAD_2PI - lf_ang

        # converte o angulo trigonometrico em radial
        if lf_ang <= RAD_PI_2:
            lf_ang = RAD_PI_2 - lf_ang

        else:
            lf_ang =(RAD_PI_2 * 5) - lf_ang

        # obtem a declinacao magnetica
        # memcpy(l_szBuf, f_szDclMag, 2)
        # l_szBuf [ 2 ] = '\0'

        # converte para radianos
        lf_dec_mag = math.radians(atof(l_szBuf))

        # corrige a radial devido a declinação magnética
        if ((f_szDclMag [ 2 ] == 'W') or (f_szDclMag [ 2 ] == 'w')):
            lf_ang += lf_dec_mag

        elif ((f_szDclMag [ 2 ] == 'E') or (f_szDclMag [ 2 ] == 'e')):
            lf_ang -= lf_dec_mag

        # converte a radial em angulo trigonométrico
        if lf_ang <= RAD_PI_2:
            lf_ang = RAD_PI_2 - lf_ang

        else:
            lf_ang =(RAD_PI_2 * 5) - lf_ang

        # calcula as novas coordenadas X e Y
        _dX = lf_dst * math.cos(lf_ang)
        _dY = lf_dst * math.sin(lf_ang)

    # logger
    # M_LOG.info("declina_ponto_2:<<")

    # return
    return _dX, _dY, 0.

# -------------------------------------------------------------------------------------------------

def geo_azim(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    cálculo do azimute entre duas coordenadas geográficas

             azimute          cartesiano
               000               090
            270   090         180   000
               180               270

    @param ff_lat_pto: latitude do ponto em graus
    @param ff_lng_pto: longitude do ponto em graus
    @param ff_lat_ref: latitude da referência em graus
    @param ff_lng_ref: longitude da referência em graus

    @return azimute entre a referência e o ponto em radianos
    """
    # logger
    # M_LOG.info("geo_azim:>>")

    # verifica parametros de entrada
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # condições especiais de retorno
    if (ff_lat_ref == ff_lat_pto) and (ff_lng_ref == ff_lng_pto):

        # logger
        # M_LOG.debug("<E01:")

        # pontos coincidentes
        return 0.

    if (ff_lat_ref == ff_lat_pto) and (ff_lng_ref > ff_lng_pto):

        # logger
        # M_LOG.debug("<E02:")

        # mesma linha à esquerda
        return math.radians(270.)

    if (ff_lat_ref == ff_lat_pto) and (ff_lng_ref < ff_lng_pto):

        # logger
        # M_LOG.debug("<E03:")

        # mesma linha à direita
        return math.radians(90.)

    if (ff_lat_ref > ff_lat_pto) and (ff_lng_ref == ff_lng_pto):

        # logger
        # M_LOG.debug("<E04:")

        # mesma coluna abaixo
        return math.pi

    if (ff_lat_ref < ff_lat_pto) and (ff_lng_ref == ff_lng_pto):

        # logger
        # M_LOG.debug("<E05:")

        # mesma coluna acima
        return 0.

    # calcula o ângulo (rad)
    lf_gama = __calc_gama(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref)

    if 1 == int(lf_gama):
        lf_arc_gama = 0.

    else:
        lf_arc_gama = math.acos(lf_gama)

    # cálculo do ângulo (rad) entre X e o ponto
    lf_delta = __calc_gama(ff_lat_pto, ff_lng_pto, ff_lat_pto, ff_lng_ref)

    if 1 == int(lf_delta):
        lf_arc_delta = 0.

    else:
        lf_arc_delta = math.acos(lf_delta)

    # cálculo do azimute básico
    lf_aux = math.sin(lf_arc_delta) / math.sin(lf_arc_gama)

    if lf_aux > 1.:
        lf_aux = 1.

    elif lf_aux < -1.:
        lf_aux = -1.

    lf_azim = math.asin(lf_aux)
    # M_LOG.debug("azimute básico:[%12.5f]", lf_azim)

    li_quad = 0

    # cálculo do azimute corrigido
    if (ff_lat_ref < ff_lat_pto) and (ff_lng_ref < ff_lng_pto): li_quad = 1
    if (ff_lat_ref < ff_lat_pto) and (ff_lng_ref > ff_lng_pto): li_quad = 4
    if (ff_lat_ref > ff_lat_pto) and (ff_lng_ref > ff_lng_pto): li_quad = 3
    if (ff_lat_ref > ff_lat_pto) and (ff_lng_ref < ff_lng_pto): li_quad = 2

    # M_LOG.debug("quadrante:[%d]", li_quad)

    if (2 == li_quad): lf_azim = math.pi - lf_azim
    if (3 == li_quad): lf_azim = math.pi + lf_azim
    if (4 == li_quad): lf_azim = (2 * math.pi) - lf_azim

    # M_LOG.debug("azim:[%12.5f]" % lf_azim)

    # logger
    # M_LOG.info("geo_azim:<<")

    # return
    return lf_azim

# -------------------------------------------------------------------------------------------------

def geo_azim_bug(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    cálculo do azimute entre dois pontos geográficos
    (válido par distâncias menores que 800NM)

    @param ff_lat_pto: latitude do ponto em graus
    @param ff_lng_pto: longitude do ponto em graus
    @param ff_lat_ref: latitude da referência em graus
    @param ff_lng_ref: longitude da referência em graus

    @return azimute entre a referência e o ponto em NM
    """
    # logger
    # M_LOG.info("geo_azim_bug:>>")

    # verifica parametros de entrada
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # verifica coincidência de pontos
    if (ff_lat_pto == ff_lat_ref) and (ff_lng_pto == ff_lng_ref):

        # pontos coincidentes
        return 0.

    # calcula a distância em latitude (DLA)
    lf_lat_dst = ff_lat_pto - ff_lat_ref
    # M_LOG.debug("distância em latitude:[%f]" % lf_lat_dst)

    # calcula a distância em longitude (DLO)
    lf_lng_dst = ff_lng_pto - ff_lng_ref
    # M_LOG.debug("distância em longitude:[%f]" % lf_lng_dst)

    # logger
    # M_LOG.info("geo_azim_bug:<<")

    # retorna o azimute entre os pontos
    return conv.azm2ang(math.atan2(lf_lat_dst, lf_lng_dst))

# -------------------------------------------------------------------------------------------------

def geo_dist(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    cálculo da distância entre dois pontos geográficos

    @param ff_lat_pto: latitude do ponto em graus
    @param ff_lng_pto: longitude do ponto em graus
    @param ff_lat_ref: latitude da referência em graus
    @param ff_lng_ref: longitude da referência em graus

    @return distância entre a referência e o ponto em NM
    """
    # logger
    # M_LOG.info("geo_dist:>>")

    # verifica parametros de entrada
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # verifica coincidência de pontos
    if (ff_lat_pto == ff_lat_ref) and (ff_lng_pto == ff_lng_ref):

        # pontos coincidentes
        return 0.

    # calcula o ângulo
    lf_gama = __calc_gama(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref)
    # M_LOG.debug("gama:[%f]" % lf_gama)

    # logger
    # M_LOG.info("geo_dist:<<")

    # retorna o cálculo da distância entre a referência e o ponto
    return math.acos(lf_gama) * cdefs.D_EARTH_RADIUS_NM

# -------------------------------------------------------------------------------------------------

def geo_dist_2(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    cálculo da distância entre dois pontos geográficos
    (válido par distâncias menores que 800NM)

    @param ff_lat_pto: latitude do ponto em graus
    @param ff_lng_pto: longitude do ponto em graus
    @param ff_lat_ref: latitude da referência em graus
    @param ff_lng_ref: longitude da referência em graus

    @return distância entre a referência e o ponto em NM
    """
    # logger
    # M_LOG.info("geo_dist_2:>>")

    # verifica parametros de entrada
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # verifica coincidência de pontos
    if (ff_lat_pto == ff_lat_ref) and (ff_lng_pto == ff_lng_ref):

        # pontos coincidentes
        return 0.

    # calcula a distância em latitude
    lf_lat_dst = (ff_lat_pto - ff_lat_ref) ** 2
    # M_LOG.debug("distância em latitude:[%f]" % lf_lat_dst)

    # calcula a distância em longitude
    lf_lng_dst = (ff_lng_pto - ff_lng_ref) ** 2
    # M_LOG.debug("distância em longitude:[%f]" % lf_lng_dst)

    # logger
    # M_LOG.info("geo_dist_2:<<")

    # retorna a distância entre a referência e o ponto
    return math.sqrt(lf_lat_dst + lf_lng_dst) * cdefs.D_CNV_G2NM

# -------------------------------------------------------------------------------------------------

def geo2pol(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    transforma coordenadas geográficas em coordenadas polares

    @param ff_lat_pto: latitude em graus
    @param ff_lng_pto: longitude em graus
    @param ff_lat_ref: latitude do ponto de referência
    @param ff_lng_ref: longitude do ponto de referência

    @return coordenadas polares do ponto (azimute em graus, distância em NM)
    """
    # logger
    # M_LOG.info("geo2pol:>>")

    # verifica parametros de entrada
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # verifica se os pontos são coincidentes
    if (ff_lat_ref == ff_lat_pto) and (ff_lng_ref == ff_lng_pto):

        # ok, pontos coincidentes
        return 0., 0.

    # calcula o ângulo
    lf_gama = math.acos(__calc_gama(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref))
    # M_LOG.debug("lf_gama:[%f]", lf_gama)

    # calcula a distância
    lf_dist = lf_gama * cdefs.D_EARTH_RADIUS_NM
    # M_LOG.debug("lf_dist:[%f]", lf_dist)

    # calcula o ângulo
    lf_delta = math.acos(__calc_gama(ff_lat_pto, ff_lng_ref, ff_lat_pto, ff_lng_pto))
    # M_LOG.debug("lf_delta:[%f]", lf_delta)

    # verificação do quadrante
    li_quad = -1

    if (ff_lat_ref < ff_lat_pto) and (ff_lng_ref == ff_lng_pto):
        lf_azim = 0.

    elif (ff_lat_ref == ff_lat_pto) and (ff_lng_ref < ff_lng_pto):
        lf_azim = 90.

    elif (ff_lat_ref > ff_lat_pto) and (ff_lng_ref == ff_lng_pto):
        lf_azim = 180.

    elif (ff_lat_ref == ff_lat_pto) and (ff_lng_ref > ff_lng_pto):
        lf_azim = 270.

    elif (ff_lat_ref < ff_lat_pto) and (ff_lng_ref < ff_lng_pto):
        li_quad = 1

    elif (ff_lat_ref > ff_lat_pto) and (ff_lng_ref < ff_lng_pto):
        li_quad = 2

    elif (ff_lat_ref > ff_lat_pto) and (ff_lng_ref > ff_lng_pto):
        li_quad = 3

    elif (ff_lat_ref < ff_lat_pto) and (ff_lng_ref > ff_lng_pto):
        li_quad = 4

    if -1 != li_quad:

        # seno do azimute
        lf_sin_azm = math.sin(lf_delta) / math.sin(lf_gama)

        # calculo do azimute
        if lf_sin_azm > 1.:
            lf_sin_azm = 1.

        elif lf_sin_azm < -1.:
            lf_sin_azm = -1.

        lf_azim = math.degrees(math.asin(lf_sin_azm))

        if 2 == li_quad:
            lf_azim = 180. - lf_azim

        elif 3 == li_quad:
            lf_azim = 180. + lf_azim

        elif 4 == li_quad:
            lf_azim = 360. - lf_azim

    if lf_azim >= 360.:
        lf_azim -= 360.

    elif lf_azim < 0:
        lf_azim += 360.

    # M_LOG.debug("azimute:[%f] / distância:[%f]" % (lf_azim, lf_dist))

    # logger
    # M_LOG.info("geo2pol:<<")

    # return
    return lf_azim, lf_dist

# -------------------------------------------------------------------------------------------------

def geo2xy(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    transforma coordenadas geográficas em coordenadas cartesianas

    @param ff_lat_pto: latitude em graus
    @param ff_lng_pto: longitude em graus
    @param ff_lat_ref: latitude do ponto de referência
    @param ff_lng_ref: longitude do ponto de referência

    @return coordenadas polares do ponto (azimute, distância em NM)
    """
    # logger
    # M_LOG.info("geo2xy:>>")

    # verifica parametros de entrada
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # converte de geográfica para polar
    lf_azim, lf_dist = geo2pol(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref)
    # M_LOG.debug("azimute:[%f] / distância:[%f]" % (lf_azim, lf_dist))

    # converte de polar para cartesiana
    lf_x = lf_dist * math.sin(math.radians(lf_azim))
    lf_y = lf_dist * math.cos(math.radians(lf_azim))

    # correcao das coordenadas X e Y devido ao efeito da declinacao magnetica
    # lf_x, lf_y = declina_ponto_2(lf_x, lf_y, f_ref.f_dcl_mag)

    # logger
    # M_LOG.info("geo2xy:<<")

    # return
    return lf_x, lf_y

# -------------------------------------------------------------------------------------------------

def geo2xy_2(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    conversão de coordenadas geográficas

    @param ff_lat_pto: latitude em graus
    @param ff_lng_pto: longitude em graus
    @param ff_lat_ref: coordenadas geográficas de referênica
    @param ff_lng_ref: coordenadas geográficas de referênica

    @return coordenadas X e Y do ponto
    """
    # logger
    # M_LOG.info("geo2xy_2:>>")

    # verifica parametros de entrada
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # cálculo da distância e do azimute geográficos do ponto
    l_vd = geo_dist(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref)
    l_vr = geo_azim(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref)
    # M_LOG.debug("distância/azimute: [%12.5f][%12.5f]", l_vd, l_vr)

    # converte o azimute para ângulo em radianos
    l_vr = math.radians(conv.azm2ang(math.degrees(l_vr)))
    # M_LOG.debug("ângulo (rad): [%12.5f]", l_vr)

    # cálculo das coordenadas X & Y do ponto
    lf_x = l_vd * math.cos(l_vr)
    lf_y = l_vd * math.sin(l_vr)

    # existe declinação magnética ?
    # if 0. != f_ref.f_dcl_mag:

        # correção das coordenadas X e Y devido ao efeito da declinação magnética
        #decl_xy(f_ref.f_dcl_mag)

    # logger
    # M_LOG.info("geo2xy_2:<<")

    # return x & y
    return lf_x, lf_y

# -------------------------------------------------------------------------------------------------

def geo2xyz_3(ff_lat_pto, ff_lng_pto, ff_alt=0.):
    """
    geodetic coordinates(latitude, longitude, height) can be converted into XY.
    """
    # logger
    # M_LOG.info("geo2xyz_3:>>")

    # M_LOG.debug("ff_lat_pto:[{:f}]".format(ff_lat_pto))
    # M_LOG.debug("ff_lng_pto:[{:f}]".format(ff_lng_pto))

    # verifica parametros de entrada
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    # calcula x
    lf_x = (ff_lng_pto - cdefs.M_REF_LNG) * cdefs.D_CNV_GR2M
    # M_LOG.debug("lf_delta_lng:[{:f}]".format(lf_delta_lng))

    # calcula y
    lf_y = (ff_lat_pto - cdefs.M_REF_LAT) * cdefs.D_CNV_GR2M
    # M_LOG.debug("lf_delta_lat:[{:f}]".format(lf_delta_lat))

    # elevação
    lf_z = ff_alt

    # logger
    # M_LOG.info("geo2xyz_3:<<")

    # retorna as coordenadas xyz
    return lf_x, lf_y, lf_z

# -------------------------------------------------------------------------------------------------

def pol2xyz(ff_azim, ff_dist):
    """
    transforma coordenadas polares em coordenadas cartesianas

    @param ff_azim: azimute
    @param ff_dist: distância

    @return coordenadas cartesianas do ponto
    """
    # logger
    # M_LOG.info("pol2xyz:>>")

    # verifica parametros de entrada
    assert 0. <= ff_azim <= 360.

    # verifica parametros de entrada
    # M_LOG.debug("ff_dist:[%f]", ff_dist)
    # M_LOG.debug("ff_azim:[%f]", ff_azim)

    # converte a distância para metros
    lf_dst = ff_dist
    # M_LOG.debug("lf_dst:[%f]", lf_dst)

    # converte a radial para ângulo trigonométrico
    lf_azim = math.radians(conv.azm2ang(math.degrees(ff_azim)))
    # M_LOG.debug("lf_azim:[%f]", lf_azim)

    # converte a distância e ângulo em X e Y
    lf_x = lf_dst * math.cos(lf_azim)
    lf_y = lf_dst * math.sin(lf_azim)
    # M_LOG.debug("lf_y:[%f]", lf_y)

    # logger
    # M_LOG.info("pol2xyz:<<")

    # return
    return lf_x, lf_y, 0.

# -------------------------------------------------------------------------------------------------

def xyz2geo_3(ff_x, ff_y, ff_z=0.):
    """
    conversão de coordenadas geográficas
    geodetic coordinates (latitude, longitude, height) can be converted into xyz.

    @param ff_x: coordenada x do ponto
    @param ff_y: coordenada y do ponto
    @param ff_z: coordenada z do ponto
    """
    # logger
    # M_LOG.info("xyz2geo_3:>>")

    # calcula latitude
    lf_lat = cdefs.M_REF_LAT + (ff_y / cdefs.D_CNV_GR2M)
    # M_LOG.debug("lf_lat: " + str(lf_lat))

    # calcula longitude
    lf_lng = cdefs.M_REF_LNG + (ff_x / cdefs.D_CNV_GR2M)
    # M_LOG.debug("lf_lng: " + str(lf_lng))

    # calcula altitude
    lf_alt = ff_z
    # M_LOG.debug("lf_alt: " + str(lf_alt))

    # logger
    # M_LOG.info("xyz2geo_3:<<")

    # retorna as coordenadas lat/long
    return lf_lat, lf_lng, lf_alt

# < the end >--------------------------------------------------------------------------------------
