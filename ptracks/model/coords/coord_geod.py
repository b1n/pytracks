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

# import coord_conv as conv
from . import coord_defs as cdefs

# < module data >----------------------------------------------------------------------------------

# logging level
M_LOG_LVL = logging.DEBUG

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(M_LOG_LVL)

# -------------------------------------------------------------------------------------------------

def ecef2geod(ff_x, ff_y, ff_z=0.):
    """
    ECEF coordinates (X,Y,Z) can be converted into geodetic coordinates (latitude, longitude, height).

    elipsoide: WGS84
    geodesia: Comparative Analysis of Solutions to the Cartesian to Geodetic Coordinate Transformation
              Comparison of Methods Used in Rectangular to Geodetic Coordinate Transformations
    http://en.wikipedia.org/wiki/Geodetic_datum#Geodetic to/from ECEF coordinates

    @param  x, y, z (m)

    @return lat e lon (graus), alt (m)
    """
    # logger
    # M_LOG.info("ecef2geod:>>")

    # calcula a long
    lf_lng = math.degrees(math.atan2(ff_y, ff_x))
    # M_LOG.debug("lon: " + str(lf_lng))

    # distância euclidiana
    lf_p = math.sqrt((ff_x * ff_x) + (ff_y * ff_y))

    # calcula a lat inicial
    lf_lat = math.atan2(ff_z, lf_p * (1. - cdefs.D_e2))
    # M_LOG.debug("lat(0): " + str(lf_lat))

    # inicia a lat anterior
    lf_lat0 = lf_lat + 1.

    # enquanto o erro não for aceitável...
    while abs(lf_lat - lf_lat0) > 1E-8:

        # calcula v
        lf_v = cdefs.D_a / math.sqrt(1. - (cdefs.D_e2 * (math.sin(lf_lat) ** 2)))
        # M_LOG.debug("lf_v(p): " + str(lf_v))

        # salva a lat anterior
        lf_lat0 = lf_lat

        # calcula a nova lat
        lf_lat = math.atan2(ff_z + (cdefs.D_e2 * lf_v * math.sin(lf_lat)), lf_p)
        # M_LOG.debug("lat: " + str(lf_lat))
        # M_LOG.debug("lat(p): " + str(math.radians(lf_lat)))

    lf_alt = (lf_p / math.cos(lf_lat)) - lf_v
    # M_LOG.debug("lf_alt: " + str(lf_alt))

    # logger
    # M_LOG.info("ecef2geod:<<")

    # retorna as coordenadas geográficas
    return math.degrees(lf_lat), lf_lng, lf_alt

# -------------------------------------------------------------------------------------------------

def ecef2geod_bow(ft_xyz):  # (x, y, z):
    """
    conversao de coordenadas ECEF para Geografica. Metodo Iterativo de Bowring.
    """
    # logger
    # M_LOG.info("ecef2geod_bow:>>")

    x = ft_xyz[0]
    y = ft_xyz[1]
    z = ft_xyz[2]
    
    iter = 5

    # cálculo da latitude
    p = math.sqrt((x * x) + (y * y))

    beta = math.atan2((z * cdefs.D_a), (p * cdefs.D_b))

    phi_ant = math.atan2((z + (cdefs.D_b * cdefs.D_el2 * pow(math.sin(beta), 3))), (p - (cdefs.D_a * cdefs.D_e2 * pow(math.cos(beta), 3))))

    beta = math.atan2(cdefs.D_b * math.tan(phi_ant), cdefs.D_a)
    phi = math.atan2((z + (cdefs.D_b * cdefs.D_el2 * pow(math.sin(beta), 3))), (p - (cdefs.D_a * cdefs.D_e2 * pow(math.cos(beta), 3))))

    # iterar equacao de tan(phi) ate precisao requerida. Ao fim temos lat = phi
    while (iter > 0) and (abs(phi - phi_ant) > 1e-7):

        # novo valor de beta:
        beta = math.atan2(cdefs.D_b * math.tan(phi), cdefs.D_a)

        # salva a lat anterior
        phi_ant = phi

        # calcula a nova lat
        phi = math.atan2((z + (cdefs.D_b * cdefs.D_el2 * pow(math.sin(beta), 3))), (p - (cdefs.D_a * cdefs.D_e2 * pow(math.cos(beta), 3))))

        # conta iteração
        iter -= 1

    lat = math.degrees(phi)

    # cálculo da longitude
    lon = math.degrees(math.atan2(y, x))

    # cálculo da altitude
    N = cdefs.D_a / (math.sqrt(1. - (cdefs.D_e2 * math.sin(phi) * math.sin(phi))))
    alt = (p / math.cos(phi)) - N

    # logger
    # M_LOG.info("ecef2geod_bow:<<")

    # return
    return lat, lon, alt

# -------------------------------------------------------------------------------------------------

def ecef2geod_sof(ft_xyz):  # (x, y, z):
    """
    conversao de coordenadas ECEF para Geografica. Metodo Fechado de I. Sofair.

    elipsoide: WGS84
    geodesia: Improved Method for Calculating Exact Geodetic Latitude and Altitude Revisited

    @param  x, y, z (m)

    @return lat e lon (graus), alt (m)
    """
    # logger
    # M_LOG.info("ecef2geod_sof:>>")

    x = ft_xyz[0]
    y = ft_xyz[1]
    z = ft_xyz[2]
    
    # cálculo da latitude
    phi = 0.
    Ne = 0.

    r0 = math.sqrt((x * x) + (y * y))
    p = abs(z) / cdefs.D_el2
    s = (r0 * r0) / (cdefs.D_e2 * cdefs.D_el2)
    q = (p * p) - (cdefs.D_b * cdefs.D_b) + s

    if q > 0:
        u = p / math.sqrt(q)
        v = (cdefs.D_b * cdefs.D_b) * (u * u) / q
        P = (27. * v * s) / q
        Q = pow(pow((math.sqrt(P + 1.) + math.sqrt(P)), 2.), (1. / 3.))
        t = (1. + Q + (1. / Q)) / 6.
        c = math.sqrt((u * u) - 1. + (2. * t))
        w = (c - u) / 2.

        sinal = -1. if z < 0 else 1.

        d = sinal * math.sqrt(q) * (w + math.sqrt(math.sqrt((t * t) + v) - (u * w) - (t / 2.) - (1. / 4.)))
        Ne = cdefs.D_a * math.sqrt(1. + ((cdefs.D_el2 * d * d) / (cdefs.D_b * cdefs.D_b)))
        phi = math.asin((cdefs.D_el2 + 1.) * (d / Ne))

        lat = math.degrees(phi)

    else:
        lat = 0.

    # cálculo da altitude
    alt = (r0 * math.cos(phi)) + (z * math.sin(phi)) - ((cdefs.D_a * cdefs.D_a) / Ne)

    # cálculo da longitude
    lon = math.degrees(math.atan2(y, x))

    # logger
    # M_LOG.info("ecef2geod_sof:<<")

    # retorna
    return lat, lon, alt

# -------------------------------------------------------------------------------------------------

def geod2ecef(ff_lat, ff_lng, ff_alt=0.):
    """
    geodetic coordinates (latitude, longitude, height) can be converted
    into ECEF (Earth-Centered Earth-Fixed).

    elipsoide: WGS84
    geodesia: Comparison of Methods Used in Rectangular to Geodetic
              Coordinate Transformations - Robert Burtch
    ref: http://en.wikipedia.org/wiki/Geodetic_datum#Geodetic to/from ECEF coordinates

    @param ff_lat: latitude (graus)
    @param ff_lng: longitude (graus)
    @param ff_alt: altitude (m)

    @return x, y, z (m)
    """
    # logger
    # M_LOG.info("geod2ecef:>>")

    # converte para radianos
    lf_lat = math.radians(ff_lat)
    lf_lng = math.radians(ff_lng)

    # calcula v
    lf_v = cdefs.D_a / math.sqrt(1. - (cdefs.D_e2 * (math.sin(lf_lat) ** 2)))
    # M_LOG.debug("lf_v: " + str(lf_v))
    # M_LOG.debug("RX: " + str(lf_v *(1 - cdefs.D_e2) / cdefs.D_a))

    # calcula X
    lf_x = (lf_v + ff_alt) * math.cos(lf_lat) * math.cos(lf_lng)
    # M_LOG.debug("lf_x: " + str(lf_x))

    # calcula Y
    lf_y = (lf_v + ff_alt) * math.cos(lf_lat) * math.sin(lf_lng)
    # M_LOG.debug("lf_y: " + str(lf_y))

    # calcula Z
    lf_z = ((lf_v * (1 - cdefs.D_e2)) + ff_alt) * math.sin(lf_lat)
    # M_LOG.debug("lf_z: " + str(lf_z))

    # logger
    # M_LOG.info("geod2ecef:<<")

    # retorna as coordenadas ecef
    return lf_x, lf_y, lf_z

# -------------------------------------------------------------------------------------------------

def enu2ecef(x, y, z, latrad, lonrad, altrad):
    """
    conversao de coordenadas ENU (centrado no radar) para ECEF.

    elipsoide: WGS84
    geodesia: Geodetic Datum

    @param x, y, z (m)
    @param latrad e lonrad (graus), altrad (m)

    @return X, Y, Z (m)
    """
    # logger
    # M_LOG.info("enu2ecef:>>")

    # converte para ECEF
    xrad, yrad, zrad = geo2ecef(latrad, lonrad, altrad)

    # converte para radianos
    latrad = math.radians(latrad)
    lonrad = math.radians(lonrad)

    # calcula
    # | X |   | -sin(lonrad)   -sin(latrad)cos(lonrad)   cos(latrad)cos(lonrad) | | x |   | xrad |
    # | Y | = |  cos(lonrad)   -sin(latrad)sin(lonrad)   cos(latrad)sin(lonrad) | | y | + | yrad |
    # | Z |   |       0                cos(latrad)       sin(latrad)            | | z |   | zrad |
    X = - sin(lonrad) * x - sin(latrad) * cos(lonrad) * y + cos(latrad) * cos(lonrad) * z + xrad
    Y = cos(lonrad) * x - sin(latrad) * sin(lonrad) * y + cos(latrad) * sin(lonrad) * z + yrad
    Z = cos(latrad) * y + sin(latrad) * z + zrad

    # logger
    # M_LOG.info("enu2ecef:<<")

    # retorna
    return X, Y, Z

# < the end >--------------------------------------------------------------------------------------
