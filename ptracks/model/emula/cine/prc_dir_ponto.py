#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_dir_ponto

DOCUMENT ME!

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
import logging
import math

# model
from ...newton import defs_newton as ldefs

from ...emula.cine import calc_proa_demanda as cpd
from ...emula.cine import calc_razao_curva as razc
from ...emula.cine import sentido_curva as scrv

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------

def prc_dir_ponto(f_atv, ff_pto_lng, ff_pto_lat, f_cine_data):
    """
    procedimento de direcionamento a ponto
    
    @param f_atv: ponteiro para struct aeronaves
    @param ff_pto_lng: longitude do ponto
    @param ff_pto_lat: latitude do ponto
    @param f_cine_data: ponteiro para pilha
    
    @return True se aeronave atingiu ponto, senão False
    """
    # logger
    # M_LOG.info("prc_dir_ponto:>>") 
                
    # verifica parâmetros de entrada
    assert f_atv
    assert f_cine_data

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
            
        # logger
        # M_LOG.info(u"prc_dir_ponto:<E01: aeronave não ativa.") 

        # cai fora...
        return None

    # calcula raio do cone de tolerância
    lf_pto_rcone = f_atv.f_trf_alt_atu * math.tan(math.radians(10))

    # calcula distância da aeronave ao ponto (x, y)
    f_cine_data.f_dst_anv_pto_x = ff_pto_lng - f_atv.f_trf_x
    f_cine_data.f_dst_anv_pto_y = ff_pto_lat - f_atv.f_trf_y

    # calcula distância euclidiana da aeronave ao ponto (linha reta)
    lf_dst_anv_pto = math.sqrt((f_cine_data.f_dst_anv_pto_x ** 2) + (f_cine_data.f_dst_anv_pto_y ** 2))

    # calcula distância euclidiana do passo da aeronave (linha reta)
    lf_passo_anv = math.sqrt((f_cine_data.f_delta_x ** 2) + (f_cine_data.f_delta_y ** 2))

    # (distância ao ponto <= raio de tolerância) ou (distância ao ponto <= passo da aeronave) ? (aeronave vai ultrapassar o ponto)
    if (lf_dst_anv_pto <= lf_pto_rcone) or (lf_dst_anv_pto <= lf_passo_anv):

        # logger
        # M_LOG.info(u"__ckeck_ok:<E02: aeronave atingiu o ponto.") 

        # sinaliza que aeronave atingiu o ponto
        return True

    # calcula nova proa de demanda
    f_atv.f_atv_pro_dem = cpd.calc_proa_demanda(f_cine_data.f_dst_anv_pto_x, f_cine_data.f_dst_anv_pto_y)
    # M_LOG.debug("__ckeck_ok:f_atv_pro_dem:[{}]".format(f_atv.f_atv_pro_dem)) 

    # em curva ?
    if f_atv.f_atv_pro_dem != f_atv.f_trf_pro_atu:

        # calcula sentido de curva pelo menor ângulo
        scrv.sentido_curva(f_atv)

        # faz o bloqueio do ponto próximo
        razc.calc_razao_curva(f_atv, ff_pto_lng, ff_pto_lat, f_cine_data)

    # logger
    # M_LOG.info("prc_dir_ponto:<<") 
                
    # sinaliza que aeronave ainda NÂO atingiu o ponto
    return False

# < the end >--------------------------------------------------------------------------------------
