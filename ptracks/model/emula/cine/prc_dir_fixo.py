#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_dir_fixo

calculos para a aeronave se direcionar a um fixo

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import math

# model
from ...newton import defs_newton as ldefs

from ...emula.cine import abort_prc as abnd
from ...emula.cine import calc_razao_curva as razc
from ...emula.cine import calc_proa_demanda as cpd
from ...emula.cine import sentido_curva as scrv

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------

def __ckeck_ok(f_atv, f_cine_data):
    """
    verifica condições da aeronave para o direcionamento ao fixo
    
    @param f_atv: ponteiro para aeronave
    @param f_cine_data: ponteiro para pilha
    """
    # logger
    # M_LOG.info("__ckeck_ok:>>")
        
    # verifica parâmetros de entrada
    assert f_atv
    assert f_cine_data

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        
        # logger
        # M_LOG.info(u"__ckeck_ok:<E01: aeronave não ativa.")
                        
        # cai fora...
        return

    # aponta para o fixo a ser interceptado e valida ponteiro
    l_fix = f_atv.ptr_atv_fix_prc 
    M_LOG.debug("__cmd_pil_dir_fixo:ptr_atv_fix_prc:[{}/{}]".format(f_atv.ptr_atv_fix_prc.i_fix_id, f_atv.ptr_atv_fix_prc.s_fix_desc))

    if (l_fix is None) or (not l_fix.v_fix_ok):

        # logger
        l_log = logging.getLogger("prc_dir_fixo::__ckeck_ok")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E02: fixo inexistente. aeronave:[%d/%s]", f_atv.i_trf_id, f_atv.s_trf_ind)

        # não encontrou o fixo, força a aeronave abandonar o procedimento
        abnd.abort_prc(f_atv)
                
        # logger
        # M_LOG.info(u"__ckeck_ok:<E02: fixo inexistente.")

        # return
        return

    # VOR ?
    if ldefs.E_VOR == l_fix.en_fix_tipo:

        # calcula raio do cone de tolerância
        l_fix.f_fix_rcone = f_atv.f_trf_alt_atu * math.tan(math.radians(30))

    # senão, outro tipo de fixo
    else:
        # calcula raio do cone de tolerância
        l_fix.f_fix_rcone = f_atv.f_trf_alt_atu * math.tan(math.radians(40))

    # distância ao fixo <= raio do cone (ver DadosDinâmicos)
    if f_atv.f_atv_dst_fix <= l_fix.f_fix_rcone:

        # sinaliza que aeronave atingiu o ponto através raio do cone
        f_cine_data.v_interceptou_fixo = True 

        # coloca em manual
        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL 

        # volta a fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO 

        # logger
        # M_LOG.info(u"__ckeck_ok:<E03: interceptou o fixo.")

        # return
        return

    # calcula distância da aeronave ao fixo (x, y)
    lf_dst_x = f_cine_data.f_dst_anv_fix_x ** 2
    lf_dst_y = f_cine_data.f_dst_anv_fix_y ** 2

    # calcula distância do "passo" da aeronave (x, y)
    lf_dlt_x = f_cine_data.f_delta_x ** 2
    lf_dlt_y = f_cine_data.f_delta_y ** 2

    # aeronave atingiu fixo ? (distância <= passo da aeronave)
    if math.sqrt(lf_dst_x + lf_dst_y) <= math.sqrt(lf_dlt_x + lf_dlt_y):

        # considera que a aeronave atingiu o fixo pelas coordenadas x, y
        f_cine_data.v_interceptou_fixo = True 

        # coloca em manual
        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL 

        # volta a fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO 

        # logger
        # M_LOG.info(u"__ckeck_ok:<E04: interceptou o fixo.")

        # return
        return

    # calcula nova proa de demanda
    f_atv.f_atv_pro_dem = cpd.calc_proa_demanda(f_cine_data.f_dst_anv_fix_x, f_cine_data.f_dst_anv_fix_y)

    # calcula sentido de curva pelo menor ângulo
    scrv.sentido_curva(f_atv)

    # ajusta a razão de curva da aeronave
    razc.calc_razao_curva(f_atv, l_fix.f_fix_x, l_fix.f_fix_y, f_cine_data)

    # setar fase de processamento
    f_atv.en_atv_fase = ldefs.E_FASE_DIRFIXO 

    # logger
    # M_LOG.info("__ckeck_ok:<<")

# -------------------------------------------------------------------------------------------------

def __direciona(f_atv, f_cine_data):
    """
    direcionar a aeronave a um fixo específico
    
    @param f_atv: ponteiro para struct aeronaves
    @param f_cine_data: ponteiro para pilha
    """
    # logger
    # M_LOG.info("__direciona:>>")
        
    # verifica parâmetros de entrada
    assert f_atv
    assert f_cine_data

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        
        # logger
        # M_LOG.info(u"__direciona:<E01: aeronave não ativa.")
                        
        # cai fora...
        return

    # aponta para o fixo especificado e valida ponteiro
    l_fix = f_atv.ptr_atv_fix_prc 

    if (l_fix is None) or (not l_fix.v_fix_ok):

        # logger
        l_log = logging.getLogger("prc_dir_fixo::__direciona")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E02: fixo inexistente. aeronave:[%d/%s]", f_atv.i_trf_id, f_atv.s_trf_ind)

        # não encontrou o fixo, força a aeronave abandonar o procedimento
        abnd.abort_prc(f_atv)
                
        # logger
        # M_LOG.info(u"__direciona:<E02: fixo inexistente.")

        # return
        return

    # VOR ?
    if ldefs.E_VOR == l_fix.en_fix_tipo:

        # calcula raio do cone de tolerância do fixo
        l_fix.f_fix_rcone = f_atv.f_trf_alt_atu * math.tan(math.radians(30)) 

    # senão, outro tipo...
    else:
        # calcula raio do cone de tolerância do fixo
        l_fix.f_fix_rcone = f_atv.f_trf_alt_atu * math.tan(math.radians(40)) 

    # distância ao fixo <= raio do cone (ver DadosDinamicos)
    if f_atv.f_atv_dst_fix <= l_fix.f_fix_rcone:

        # sinaliza que aeronave atingiu o ponto através raio do cone
        f_cine_data.v_interceptou_fixo = True 

        # coloca em manual
        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL 

        # volta a fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO 

        # logger
        # M_LOG.info(u"__direciona:<E03: interceptou o fixo.")

        # return
        return

    # calcula distância da aeronave ao fixo (x, y)
    lf_dst_x = f_cine_data.f_dst_anv_fix_x ** 2
    lf_dst_y = f_cine_data.f_dst_anv_fix_y ** 2

    # calcula distância do "passo" da aeronave (x, y)
    lf_dlt_x = f_cine_data.f_delta_x ** 2
    lf_dlt_y = f_cine_data.f_delta_y ** 2

    # aeronave atingiu fixo ? (distância <= passo da aeronave)
    if math.sqrt(lf_dst_x + lf_dst_y) <= math.sqrt(lf_dlt_x + lf_dlt_y):

        # considera que a aeronave atingiu o fixo pelas coordenadas x, y
        f_cine_data.v_interceptou_fixo = True 

        # coloca em manual
        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL 

        # volta a fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO 

        # logger
        # M_LOG.info(u"__direciona:<E04: interceptou o fixo.")

        # return
        return

    # calcula nova proa de demanda
    f_atv.f_atv_pro_dem = cpd.calc_proa_demanda(f_cine_data.f_dst_anv_fix_x, f_cine_data.f_dst_anv_fix_y)

    # verifica se mudou a proa (curvando...)
    if f_atv.f_atv_pro_dem != f_atv.f_trf_pro_atu:

        # bloqueia o fixo
        razc.calc_razao_curva(f_atv, l_fix.f_fix_x, l_fix.f_fix_y, f_cine_data)

    # logger
    # M_LOG.info("__direciona:<<")

# -------------------------------------------------------------------------------------------------

def prc_dir_fixo(f_atv, f_cine_data):
    """
    procedimento de direcionamento a fixo
    
    @param f_atv: ponteiro para struct aeronaves
    @param f_cine_data: ponteiro para pilha
    """
    # logger
    # M_LOG.info("prc_dir_fixo:>>")
        
    # verifica parâmetros de entrada
    assert f_atv
    assert f_cine_data is not None

    # fase inicial ?
    if ldefs.E_FASE_ZERO == f_atv.en_atv_fase:

        # verifica condições de execução
        __ckeck_ok(f_atv, f_cine_data)

    # fase de processamento ?
    elif ldefs.E_FASE_DIRFIXO == f_atv.en_atv_fase:

        # faz o direcionamento ao fixo
        __direciona(f_atv, f_cine_data)

    # senão, erro de fase...
    else:
        # logger
        l_log = logging.getLogger("prc_dir_fixo::prc_dir_fixo")
        l_log.setLevel(logging.WARNING)
        l_log.warning(u"<E01: fase do direcionamento a fixo não identificada.")

    # logger
    # M_LOG.info("prc_dir_fixo:<<")

# < the end >-------------------------------------------------------------------------------------
