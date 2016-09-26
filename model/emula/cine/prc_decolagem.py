#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_decolagem

realizar o procedimento de decolagem

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

# model
from ...newton import defs_newton as ldefs

from ...coords import coord_defs as cdefs
from ...emula.cine import calc_proa_demanda as cpd
from ...emula.cine import trata_associado as tass

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------

def __check_ok(f_atv, f_cine_data):
    """
    preparar a aeronave para decolagem
    
    @param f_atv: ponteiro para struct aeronaves
    @param f_cine_data: dados da cinemática
    """
    # logger
    # M_LOG.info("__check_ok:>>")
        
    # verifica parâmetros de entrada
    assert f_atv

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        
        # logger
        # M_LOG.info(u"__check_ok:<E01: aeronave não ativa.")
                        
        # cai fora...
        return

    # aponta para o aeródromo planejado e valida ponteiro
    l_aer = f_cine_data.ptr_aer

    if (l_aer is None) or not l_aer.v_aer_ok:

        # força o abandono do procedimento
        f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
        f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
        f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu

        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
        f_atv.en_atv_est_atv = ldefs.E_CANCELADA

        # logger
        l_log = logging.getLogger("__check_ok")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E01: aeródromo de decolagem inexistente.")

        # return
        return

    # aponta para a pista planejada e valida ponteiro
    l_pis = f_cine_data.ptr_pis

    if (l_pis is None) or not l_pis.v_pis_ok:

        # força o abandono do procedimento
        f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
        f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
        f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu

        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
        f_atv.en_atv_est_atv = ldefs.E_CANCELADA

        # logger
        l_log = logging.getLogger("__check_ok")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E02: pista de decolagem inexistente.")

        # return
        return

    # prepara a aeronave para a decolagem
    f_atv.f_atv_acel = f_atv.ptr_trf_prf.f_prf_raz_max_var_vel * ldefs.D_FATOR_ACEL

    # velocidade atual
    f_atv.f_trf_vel_atu = 0.

    # velocidade de decolagem
    f_atv.f_atv_vel_dem = f_atv.ptr_trf_prf.f_prf_vel_dec

    # rumo da pista
    f_atv.f_trf_pro_atu = \
    f_atv.f_atv_pro_dem = l_pis.i_pis_rumo

    # elevação do aeródromo
    f_atv.f_trf_alt_atu = \
    f_atv.f_atv_alt_dem = l_aer.f_aer_elev
    # M_LOG.debug("f_trf_alt_atu:[{}]".format(f_atv.f_trf_alt_atu))

    # posiciona aeronave na pista em x/y
    f_atv.f_trf_x = l_pis.f_pis_x
    f_atv.f_trf_y = l_pis.f_pis_y

    # sinaliza a fase de processamento de decolagem
    f_atv.en_atv_fase = ldefs.E_FASE_DECOLAGEM

    # logger
    # M_LOG.info("__check_ok:<<")
        
# -------------------------------------------------------------------------------------------------

def __do_dep (f_atv, f_cine_data, fstk_context):
    """
    realizar o procedimento de decolagem
    
    @param f_atv: ponteiro para struct aeronaves
    @param f_cine_data: dados de cinemática
    @param fstk_context: ponteiro para pilha
    """
    # logger
    # M_LOG.info("__do_dep:>>")
        
    # verifica parâmetros de entrada
    assert f_atv
    assert f_cine_data
    assert fstk_context

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        
        # logger
        # M_LOG.info(u"__do_dep:<E01: aeronave não ativa.")
                        
        # cai fora...
        return

    # verifica condições para execução
    if (f_atv.ptr_trf_prf is None) or (not f_atv.ptr_trf_prf.v_prf_ok):
        
        # logger
        # M_LOG.info(u"__do_dep:<E02: performance não existe.")
                        
        # cai fora...
        return

    # obtém do contexto a função operacional anterior
    len_fnc_ope_tmp, _, _, _ = fstk_context[-1]

    # verifica se aeronave atingiu a velocidade de decolagem
    if f_atv.f_trf_vel_atu != f_atv.ptr_trf_prf.f_prf_vel_dec:

        # logger
        # M_LOG.info(u"__do_dep:<E03: não atingiu a velocidade de decolagem.")

        # return
        return

    # aponta para o aeródromo planejado
    l_aer = f_cine_data.ptr_aer

    if (l_aer is None) or not l_aer.v_aer_ok:

        # força o abandono do procedimento
        f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
        f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
        f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu
        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
        f_atv.en_atv_est_atv = ldefs.E_CANCELADA

        # logger
        l_log = logging.getLogger("__do_dep")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E01: aeródromo de decolagem inexistente.")

        # l_log.error("AnvInd.:[%s]", f_atv.sAnvInd)
        # l_log.error("AnvCodT:[%s]", f_atv.sAnvCodT)

        # return
        return

    # verifica se é uma decolagem com subida ou decolagem pura
    if (ldefs.E_SUBIDA == f_atv.en_trf_fnc_ope_ant) or (ldefs.E_SUBIDA == len_fnc_ope_tmp):

        # aponta para a subida planejada do exercício
        l_sub = f_cine_data.ptr_sub
        # M_LOG.debug("__do_dep:l_sub:[{}]".format(l_sub)) 

        if (l_sub is None) or not l_sub.v_sub_ok:

            # força abandono do procedimento
            f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
            f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
            f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu
            f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
            f_atv.en_atv_est_atv = ldefs.E_CANCELADA

            # logger
            l_log = logging.getLogger("__do_dep")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E02: decolagem/subida inexistente.")

            # l_log.error("AnvInd...:[%s]", f_atv.sAnvInd)
            # l_log.error("AnvCodT..:[%s]", f_atv.sAnvCodT)
            # l_log.error("Aeródromo:[%s]", l_aer.sAerInd)

            # return
            return

        # aponta para o primeiro breakpoint da subida
        l_brk = l_sub.lst_sub_brk[0]
        # M_LOG.debug("__do_dep:l_brk:[{}]".format(l_brk)) 

        if (l_brk is None) or not l_brk.v_brk_ok:

            # força o abandono do procedimento
            f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
            f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
            f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu
            f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
            f_atv.en_atv_est_atv = ldefs.E_CANCELADA

            # logger
            l_log = logging.getLogger("__do_dep")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E03: decolagem/subida breakpoint inexistente.")

            # l_log.error("AnvInd...:[%s]", f_atv.sAnvInd)
            # l_log.error("AnvCodT..:[%s]", f_atv.sAnvCodT)
            # l_log.error("Aeródromo:[%s]", l_aer.sAerInd)

            # return
            return

        # obtem a cabeceira da decolagem (pista)
        l_pis = f_cine_data.ptr_pis

        if (l_pis is None) or not l_pis.v_pis_ok:

            # força o abandono do procedimento
            f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
            f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
            f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu
            f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
            f_atv.en_atv_est_atv = ldefs.E_CANCELADA

            # logger
            l_log = logging.getLogger("__do_dep")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E04: pista de decolagem inexistente.")

            # l_log.error("AnvInd...:[%s]", f_atv.sAnvInd)
            # l_log.error("AnvCodT..:[%s]", f_atv.sAnvCodT)
            # l_log.error("Aerodromo:[%s]", l_aer.sAerInd)

            # return
            return

        # calcula a radial entre o 1*brk da subida e a pista
        lf_delta_x = l_brk.f_brk_x - l_pis.f_pis_x
        lf_delta_y = l_brk.f_brk_y - l_pis.f_pis_y

        lf_radial_pista_brk = cpd.calc_proa_demanda(lf_delta_x , lf_delta_y)

        # calcula o ângulo entre o rumo da pista e o 1*brk da subida
        lf_ang_pista_brk = abs(l_pis.i_pis_rumo - lf_radial_pista_brk)

        # -----------------------------------------------------------------------------------------
        # regra de cálculo da altitude na decolagem com Subida
        # objetivo: livrar obstáculos na decolagem (montanhas, prédios, ...)
        # limites: ângulo limite de 15 graus entre rumo da pista e o primeiro ponto da subida
        # se a diferença dos ângulos (fAngPistaBkp) for maior que 15 graus, então a altitude
        # de demanda será 400FT (não é nível) acima da elevação do aeródromo
        # se a diferença dos ângulos (fAngPistaBkp) for menor ou igual a 15 graus, a altitude
        # de demanda será 50ft acima da elevação do aeródromo
        # -----------------------------------------------------------------------------------------
        if lf_ang_pista_brk > 15.:

            # calcula 400ft acima da altitude da pista (converte ft -> m)
            f_atv.f_atv_alt_dem = (400. * cdefs.D_CNV_FT2M) + l_aer.f_aer_elev

        # senão,...
        else:
            # calcula 50ft acima da altitude da pista (converte ft -> m)
            f_atv.f_atv_alt_dem = (50. * cdefs.D_CNV_FT2M) + l_aer.f_aer_elev

        # -----------------------------------------------------------------------------------------
        # determina a razão máxima de subida na decolagem para todos os casos
        #
        # PBN (casos de DEP no SBGL e SBRJ)
        # Descomentado este trecho para as seguintes considerações:
        # a) aeródromos com pistas curtas (caso SBGL) as aeronaves consigam aplicar a
        #    RazMaxSubDec, porém o gradiente tem que estar zerado no primeiro ponto da Subida.
        # b) aeródromos com pistas longas, a AnvRazSub possa ser aplicada mediante o cálculo do
        #    gradiente (se houver) para atingir o primeiro ponto da Subida.
        #
        # Obs_1: Com o retorno da verificação do gradiente, evitou-se que aeronaves decolando
        #        em pistas longas chegassem a subir como se fossem foguetes devido ao uso
        #        generalizado da prf_raz_max_sub_dec para todos os casos.
        # Obs_2: Ambos casos a aceleração na DEP tem que ser 4 vezes (campo do arquivo ".ini")
        # -----------------------------------------------------------------------------------------
        if 0. == l_brk.f_brk_raz_vel:

            # obtém a razão máxima de subida da tabela de performance
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_max_sub_dec

        # senão,...
        else:
            # calcula a razão de subida em função do gradiente
            f_atv.f_atv_raz_sub = f_atv.f_trf_vel_atu * l_brk.f_brk_raz_vel

    # decolagem pura, sem subida
    else:
        # -----------------------------------------------------------------------------------------
        # regra de cálculo da altitude na decolagem pura
        # objetivo: livrar obstáculos na decolagem (montanhas, prédios, ...)
        # a altitude de demanda será igual a 50ft acima da elevação do aeródromo
        # -----------------------------------------------------------------------------------------

        # calcula 50ft acima da altitude da pista (converte ft.m)
        f_atv.f_atv_alt_dem = (50. * cdefs.D_CNV_FT2M) + l_aer.f_aer_elev

        # obtém a razão máxima de subida da tabela de performance
        f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_max_sub_dec

    # ---------------------------------------------------------------------------------------------
    # regra da velocidade na decolagem
    # objetivo: estabelecer a velocidade limite de 250KT para as aeronaves que estiverem
    # voando abaixo de 10000FT (FL100)
    # ---------------------------------------------------------------------------------------------

    # verifica a altitude atual da aeronave
    if (f_atv.f_trf_alt_atu * cdefs.D_CNV_M2FT) < ldefs.D_ALT_MAX_TMA:

        # determina a velocidade de subida na decolagem (limitada a 250kt)
        f_atv.f_atv_vel_dem = min(f_atv.ptr_trf_prf.f_prf_vel_sub_dec, ldefs.D_VEL_MAX_TMA)

    # ajusta aceleração
    f_atv.f_atv_acel = f_atv.ptr_trf_prf.f_prf_raz_var_vel

    # determina fase final da decolagem
    f_atv.en_atv_fase = ldefs.E_FASE_ESTABILIZADA

    # logger
    # M_LOG.info("__do_dep:<<")
        
# -------------------------------------------------------------------------------------------------

def prc_decolagem(f_atv, f_cine_data, fstk_context):
    """
    @param f_atv: ponteiro para struct aeronaves
    @param f_cine_data: ponteiro para pilha
    @param fstk_context: pilha de contexto
    """
    # logger
    # M_LOG.info("prc_decolagem:>>")
        
    # verifica parâmetros de entrada
    assert f_atv
    assert f_cine_data
    assert fstk_context

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        
        # logger
        # M_LOG.info(u"prc_decolagem:<E01: aeronave não ativa.")
                        
        # cai fora...
        return

    # verifica condições para execução
    if (f_atv.ptr_trf_prf is None) or (not f_atv.ptr_trf_prf.v_prf_ok):
        
        # logger
        # M_LOG.info(u"prc_decolagem:<E02: performance não existe.")
                        
        # cai fora...
        return

    # processa as fases

    # fase de preparação ?
    if ldefs.E_FASE_ZERO == f_atv.en_atv_fase:

        # verifica condição dos dados
        __check_ok(f_atv, f_cine_data)

    # fase de decolagem ?
    elif ldefs.E_FASE_DECOLAGEM == f_atv.en_atv_fase:

        # realiza o processamento
        __do_dep(f_atv, f_cine_data, fstk_context)

    # fase de estabilizada ?
    elif ldefs.E_FASE_ESTABILIZADA == f_atv.en_atv_fase:

        # verifica o término da decolagem
        if f_atv.f_trf_alt_atu == f_atv.f_atv_alt_dem:

            # obtém do contexto a função operacional anterior
            len_fnc_ope_tmp, _, _, _ = fstk_context[-1]

            # restaura a pilha de procedimento ou por comando de pilotagem
            if (ldefs.E_SUBIDA == f_atv.en_trf_fnc_ope_ant) or (ldefs.E_SUBIDA == len_fnc_ope_tmp):

                # restaura a pilha de procedimento
                tass.restaura_associado(f_atv, f_cine_data, fstk_context)

            # senão,...
            else:
                # decolagem incluida num tráfego, coloca em MANUAL
                f_atv.f_atv_alt_dem = f_atv.ptr_trf_prf.f_prf_teto_sv
                f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

    # senão,...
    else:
        # logger
        l_log = logging.getLogger("prc_decolagem")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E01: fase da decolagem não identificada.")

    # logger
    # M_LOG.info("prc_decolagem:<<")
        
# < the end >--------------------------------------------------------------------------------------
