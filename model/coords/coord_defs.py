#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
coord_defs.

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
import math

# < math >-----------------------------------------------------------------------------------------

# radianos
# RAD_PI = 3.141592654    # PI       
D_RAD_PI = math.pi

# D_RAD_PI_2  = 1.570796327    # PI / 2
# RAD_PI_2 = 1.570796327
D_RAD_PI_2 = math.pi / 2.

# D_RAD_PI_3  = 1.047197551    # PI / 3
# RAD_PI_3 = 1.047197551    # PI / 3   
D_RAD_PI_3 = math.pi / 3.

# D_RAD_3PI_2 = 4.712388980    # 3 PI / 2
# RAD_3PI_2 = 4.712388980    # 3 PI / 2 
D_RAD_3PI_2 = 3. * (math.pi / 2.)

# D_RAD_2PI   = 6.283185307    # 2 PI
# RAD_2PI = 6.283185307    # 2 PI     
D_RAD_2PI = 2. * math.pi

# graus
D_DEG_PI_3  =  60.    # PI / 3
D_DEG_PI_2  =  90.    # PI / 2
D_DEG_PI    = 180.    # PI
D_DEG_3PI_2 = 270.    # 3 PI / 2
D_DEG_2PI   = 360.    # 2 PI

# conversão de radianos para graus
# D_CNV_RAD2DEG = 57.29577951
D_RAD2DEG = 180. / math.pi

# conversão de graus para radianos
# D_CNV_DEG2RAD = 0.017453292
D_DEG2RAD = math.pi / 180.
D_RADIAN_PER_DEGREE = D_DEG2RAD

# < conversão >------------------------------------------------------------------------------------

# conversão de pés

# conversão de pés (ft) para metros (m)
D_CNV_FT2M = 0.30480    # pés -> metros
# D_FT2M = D_CNV_FT2M

# conversão de metros (m) para pés (ft)
# D_CNV_M2FT = 3.280839895    # metros -> pés
D_CNV_M2FT = 1. / 0.30480
# D_M2FT = D_CNV_M2FT

# conversão de milhas náuticas

# conversão de milhas náuticas (nm) para metros (m)
D_CNV_NM2M = 1852.    # milhas náuticas -> metros
# D_NM2M = D_CNV_NM2M

# conversão de milhas náuticas (nm) para kilometros (km)
D_KM_PER_NAUTICAL_MILE = D_CNV_NM2M / 1000.

# conversão de metros (m) para milhas náuticas (nm)
# D_CNV_M2NM = 0.539957E-3    # metros -> milhas náuticas
D_CNV_M2NM = 1. / D_CNV_NM2M
# D_M2NM = D_CNV_M2NM

# conversão de knots

# conversão de knots (kt) para metros por segundo (m/s)
# D_CNV_KT2MS = 0.514444444    # knots -> m/s
D_CNV_KT2MS = D_CNV_NM2M / 3600.
# D_NOS_MPS = D_CNV_KT2MS
# D_CNV_NOS_MPS = 0.514444444
# D_CNV_NOS_MPS = 1. / D_CNV_MPS_NOS

# conversão de metros por segundo (m/s) para knots (kt)
# D_CNV_MS2KT = 1.943844492    # m/s -> knots
D_CNV_MS2KT = 3600. / D_CNV_NM2M
# D_CNV_MPS_NOS = 1.943844492
# D_MPS_NOS = D_CNV_MS2KT
# D_CNV_MPS_NOS = 3600. / D_CNV_NM2M

# conversão para centímetros
# D_CNV_Knots2Mcs = 0.514444444E-2    # knots -> m/100th
# D_CNV_Mcs2Knots = 194.3844492441    # m/100th -> knots

# conversão de pés por minuto

# conversão de pés por minuto (pés/min) para metros por segundo (m/s)
D_CNV_FTMIN2MS = 0.5080E-2    # pés/min -> m/s

# conversão de metros por segundo (m/s) para pés por minuto (pés/min)
D_CNV_MS2FTMIN = 196.850393701    # m/s -> pés/min

# conversão para centímetros
# D_CNV_ftMin2Mcs = 0.5080E-4    # pés/min -> m/100th
# D_CNV_Mcs2ftMin = 19685.04    # m/100th -> pés/min

# conversão de knots por minuto

# conversão de knots por minuto (knots/min) para metros / segundo^2
D_CNV_KMIN2MS2 = 0.857407407E-2    # knots/min -> m/s^2

# conversão para centímetros
# D_CNV_KMin2Mcs2 = 0.857407407E-6  # ! knots/min -> m/100th^2

# class/static variables
D_MINUTES_PER_DEGREE = 60.0
D_SECONDS_PER_MINUTE = 60.0
D_SECONDS_PER_DEGREE = D_SECONDS_PER_MINUTE * D_MINUTES_PER_DEGREE

# < WGS84 >----------------------------------------------------------------------------------------
# parâmetros do WGS84 - ref Defense Mapping Agency Technical Report - DMA TR8350 Table 3.2

# local earth radius computed at center initialization
# raio médio aritmético da Terra em milhas náuticas, i.e.(2a + b)/3 = 6371.0087714 km(WGS84)
# fonte: FAI Sphere – Fédération Aéronautique Internationale(http://www.fai.org/distance_calculation/)

# semi-major axis in WGS-84 (m)
D_a = 6378137.0
# semi-minor axis in WGS-84 (m)
D_b = 6356752.314245

# local earth radius computed at center initialization
# raio médio aritmético da Terra (2a + b)/3 (WGS84)
# D_EARTH_RADIUS_KM = 6371.0087714
D_EARTH_RADIUS_KM = ((2. * D_a) + D_b) / 3. / 1000.
# D_EARTH_RADIUS_NM = 3440.069530994
D_EARTH_RADIUS_NM = D_EARTH_RADIUS_KM / D_KM_PER_NAUTICAL_MILE

# equatorial earth radius(raio médio da Terra(a + b)/2(WGS84))
# D_EARTH_RADIUS_KM_MED = 6367.4446571
D_EARTH_RADIUS_KM_MED = (D_a + D_b) / 2. / 1000.
# D_EARTH_RADIUS_NM_MED = 3438.145063229
D_EARTH_RADIUS_NM_MED = D_EARTH_RADIUS_KM_MED / D_CNV_NM2M * 1000.

# equatorial earth radius
D_EARTH_RADIUS_KM = 6378.160
D_EARTH_RADIUS_NM = D_EARTH_RADIUS_KM / D_KM_PER_NAUTICAL_MILE

# raio equatorial da terra em milhas náuticas (NM)
# D_RAIO_TERRA = 3443.8445

# local earth radius computed at center initialization.
D_EARTH_RADIUS_KM_LOCAL = D_EARTH_RADIUS_KM
D_EARTH_RADIUS_NM_LOCAL = D_EARTH_RADIUS_NM

# new excentricity values on 21th march 2005
D_EXCENTRICITY = 0.081819191

# metros por grau no semi-eixo maior
# D_P1 = math.radians(D_a)
# metros por grau no semi-eixo maior
# D_P2 = math.radians(D_b)

# conversão de graus (gr) para metros (m)
# D_CNV_GR2M = 111120.
# conversão de graus (gr) para metros (m) médio
D_CNV_GR2M = ((math.radians(D_a) * 2) + math.radians(D_b)) / 3.
# conversão de graus (gr) para milhas náuticas (nm)
# D_CNV_GR2NM = 60.
D_CNV_GR2NM = D_CNV_GR2M / D_CNV_NM2M

# flattening
D_f = 298.257223563

# reciprocal of flattening (1/f) in WGS-84
# D_1f = 0.00335281066474
D_1f = 1. / D_f

# flattening ao quadrado
# D_f2 = 0.000011241
D_f2 = D_1f * D_1f

# first eccentricity squared in WGS-84
# D_e2 = 0.00669437999013
D_e2 = D_1f * (2. - D_1f)    # primeira excentricidade ao quadrado

# new eccentricity values (21th march 2005)
# D_e = 0.0818191908426
D_e = math.sqrt(D_e2)    # primeira excentricidade

# D_e4 = 0.00004481472345     # primeira excentricidade à quarta
D_e4 = pow(D_e, 4.)

# D_e6 = 0.00000030000678     # primeira excentricidade à sexta
D_e6 = pow(D_e, 6.)

D_el = 0.0820944379496      # segunda excentricidade

# D_el2 = 0.00673949674227    # segunda excentricidade ao quadrado
D_el2 = pow(D_el, 2.)

# parâmetros para cálculo da latitude geográfica em função da latitude conforme
D_d2 = 0.00335655146887    # primeiro parâmetro
D_d4 = 0.00000657187270    # segundo parâmetro
D_d6 = 0.00000001764564    # terceiro parâmetro
D_d8 = 0.00000000005328    # quarto parâmetro

# parâmetros para cálculo da distância meridional no elipsóide (m)
# m -> distância medida ao longo do meridiano do equador até a latitude
# navegação: Practical Rhumb Line Calculations on the Spheroid (pg 114)
# projeção : Mercator Projections - Osborne (pg 98)
D_A0a = 6367449.14596083596946    # A0 * a
D_A2a = 16038.50833312485989      # A2 * a
D_A4a = 16.83220072494370         # A4 * a
D_A6a = 0.02180076563538          # A6 * a

# < sets >-----------------------------------------------------------------------------------------

D_SET_COORD_VALIDAS = ('D', 'F', 'G', 'I', 'L', 'P', 'X')

# < module data >----------------------------------------------------------------------------------

# latitude de referência (SBBR)
M_REF_LAT = -15.778460

# longitude de referência (SBBR)
M_REF_LNG = -47.928661

# declinação magnética (SBBR)
M_DCL_MAG = -21.37

# < the end >--------------------------------------------------------------------------------------
