#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_subida.

realiza a passagem da aeronave por todos os breakpoints que determinam uma subida.

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
# import math

# model
import model.newton.defs_newton as ldefs

import model.emula.cine.obtem_brk as obrk
import model.emula.cine.prc_dir_ponto as dp
import model.emula.cine.trata_associado as tass

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------

def prc_subida(f_atv, f_cine_data, f_stk_context):
    """
    realiza o procedimento de subida após o procedimento de decolagem
    
    @param f_atv: ponteiro para struct aeronaves
    @param f_cine_data: dados da cinemática
    @param f_stk_context: ponteiro para pilha
    """
    # logger
    M_LOG.info("prc_subida:>>")
                            
    # check input parameters
    assert f_atv

    # verifica condições de execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):

        # cai fora...
        return False

    # dados da subida
    l_sub = f_atv.ptr_trf_prc

    if (l_sub is None) or not l_sub.v_sub_ok:

        # registra a falha no arquivo de log
        l_log = logging.getLogger("prc_subida")
        l_log.setLevel(logging.NOTSET)
        l_log.error("E01: subida inexistente. aeronave:[%d/%s]" % (f_atv.i_trf_id, f_atv.s_trf_ind))

        # força a abandonar a subida
        f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
        f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
        f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu

        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

        # return
        return

    M_LOG.debug("prc_subida:fase:[{}]".format(ldefs.DCT_FASE[f_atv.en_atv_fase]))

    # testa as fases da subida
    if ldefs.E_FASE_ZERO == f_atv.en_atv_fase:

        M_LOG.debug("Fase Zero")

        # inicia o contador de breakpoints
        f_cine_data.i_brk_ndx = 0

        # empilha o contexto futuro
        f_stk_context.append((f_atv.en_trf_fnc_ope, ldefs.E_FASE_SUBIDA, l_sub, 0))

        # salva a subida
        f_cine_data.ptr_sub = l_sub
        M_LOG.debug("ptr_sub:[{}]".format(f_cine_data.ptr_sub))

        # obtém o aeródromo e pista da subida
        f_cine_data.ptr_aer = l_sub.ptr_sub_aer
        f_cine_data.ptr_pis = l_sub.ptr_sub_pis

        # carrega o contexto atual
        f_atv.ptr_trf_prc = l_sub.ptr_sub_prc_dec

        f_atv.en_trf_fnc_ope = ldefs.E_DECOLAGEM
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

    # fase subida ?
    elif ldefs.E_FASE_SUBIDA == f_atv.en_atv_fase:

        M_LOG.debug("Fase Subida")

        # inicia com o número do breakpoint atual
        l_brk = f_atv.ptr_atv_brk = l_sub.lst_sub_brk[f_cine_data.i_brk_ndx]

        if (l_brk is None) or not l_brk.v_brk_ok:

            # registra a falha no arquivo de log
            l_log = logging.getLogger("prc_subida")
            l_log.setLevel(logging.ERROR)
            l_log.error("E02: subida/breakpoint inexistente. aeronave:[%d/%s]", f_atv.i_trf_id, f_atv.s_trf_ind)

            # força a abandonar a subida
            f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
            f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
            f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu
            f_atv.f_atv_vel_mac_dem = f_atv.f_atv_vel_mac_atu

            f_atv.ptr_trf_brk = None
            f_atv.ptr_trf_prc = None

            f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
            f_atv.en_atv_fase = ldefs.E_FASE_ZERO

            # return
            return

        # obtém dados do breakpoint da subida
        obrk.obtem_brk(f_atv, l_brk, f_cine_data)

    # fase direcionamento a ponto ?
    elif ldefs.E_FASE_DIRPONTO == f_atv.en_atv_fase:

        M_LOG.debug("Fase DirPonto")

        # chegou ao breakpoint ?
        if dp.prc_dir_ponto(f_atv, f_cine_data.f_coord_x_brk, f_cine_data.f_coord_y_brk, f_cine_data):

            # próxima fase
            f_atv.en_atv_fase = ldefs.E_FASE_BREAKPOINT

            # obtém o breakpoint atual
            l_brk = f_atv.ptr_atv_brk

            if (l_brk is None) or not l_brk.v_brk_ok:

                # logger
                l_log = logging.getLogger("prc_subida")
                l_log.setLevel(logging.ERROR)
                l_log.error("E03: subida/breakpoint inexistente. aeronave:[%d/%s]", f_atv.i_atv_id, f_atv.s_atv_ind)

                # força abandonar a subida
                f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
                f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
                f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu
                f_atv.f_atv_vel_mac_dem = f_atv.f_atv_vel_mac_atu

                f_atv.ptr_trf_brk = None
                f_atv.ptr_trf_prc = None

                f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
                f_atv.en_atv_fase = ldefs.E_FASE_ZERO

                # return
                return

            # trata o procedimento associado
            tass.trata_associado(f_atv, l_brk, f_cine_data.i_brk_ndx, f_stk_context)

    # fase rumo e altitude ?
    elif ldefs.E_FASE_RUMOALT == f_atv.en_atv_fase:

        M_LOG.debug("Fase RumoAlt")

        # ajusta a velocidade de demanda em função do nível de vôo
        if (f_atv.f_atv_alt_atu * cdefs.D_CNV_M2FT) > ldefs.D_ALT_MAX_TMA:
            f_atv.f_atv_vel_dem = f_atv.f_ptr_prf.f_prf_vel_crz  # calcIAS(f_atv.f_ptr_prf.f_prf_vel_crz, f_atv.f_atv_alt_atu, ldefs.D_EXE_VAR_TEMP_ISA)

        # verifica se proa e a altitude estão estabilizadas
        if (f_atv.f_atv_pro_atu == f_atv.f_atv_pro_dem) and (f_atv.f_atv_alt_atu == f_atv.f_atv_alt_dem):

            # nova fase
            f_atv.en_atv_fase = ldefs.E_FASE_BREAKPOINT

            # trata o procedimento associado
            tass.trata_associado(f_atv, l_brk, f_cine_data.i_brk_ndx, f_stk_context)

    # fase breakpoints ?
    elif ldefs.E_FASE_BREAKPOINT == f_atv.en_atv_fase:

        M_LOG.debug("Fase Breakpoint")

        # verifica se é o último breakpoint da subida
        if f_atv.ptr_atv_brk == l_sub.lst_sub_brk[-1]:

            # reseta o flag altitude/velocidade
            f_atv.i_atv_change_alt_vel = 0

            # restaura pilha, se necessário
            tass.restaura_associado(f_atv, f_cine_data, f_stk_context)

        # otherwise,... 
        else:
            # próximo breakpoint
            f_cine_data.i_brk_ndx += 1
                                            
            # aponta para o próximo breakpoint
            l_brk = f_atv.ptr_atv_brk = l_sub.lst_sub_brk[f_cine_data.i_brk_ndx]
                                                                    
            if (l_brk is None) or not l_brk.v_brk_ok:

                # registra a falha no arquivo de log
                l_log = logging.getLogger("prc_subida")
                l_log.setLevel(logging.ERROR)
                l_log.error("E04: subida/breakpoint inexistente. aeronave:[%d/%s]", f_atv.i_atv_id, f_atv.s_atv_ind)

                # força abandonar a subida
                f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
                f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
                f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu
                f_atv.f_atv_vel_mac_dem = f_atv.f_atv_vel_mac_atu

                f_atv.ptr_trf_brk = None
                f_atv.ptr_trf_prc = None

                f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
                f_atv.en_atv_fase = ldefs.E_FASE_ZERO

                # return
                return

            # obtém dados do breakpoint atual
            obrk.obtem_brk(f_atv, l_brk, f_cine_data)

    # senão, fase não identificada
    else:
        # erro na valor da fase, registra a falha no arquivo de log
        l_log = logging.getLogger("prc_subida")
        l_log.setLevel(logging.ERROR)
        l_log.error("E05: fase na subida não identificada.")
                
    # logger
    M_LOG.info("prc_subida:<<")
                            
# < the end >--------------------------------------------------------------------------------------
