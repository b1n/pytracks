#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
trata_associado.

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

# model
import model.newton.defs_newton as ldefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------------------------

def restaura_associado(f_atv, f_cine_data, f_stk_context):
    """
    restaura procedimentos associados e o contexto da pilha.
    """
    # logger
    # M_LOG.info("restaura_associado:>>")

    # verifica condições para execução
    assert f_atv

    # verifica condições de execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):

        # cai fora...
        return False

    # verifica se existe algo na pilha
    if len(f_stk_context) > 0:

        # se existe, desempilha o contexto
        # f_atv.en_atv_brk_ptr = f_stk_context.pop()
        f_atv.en_trf_fnc_ope, f_atv.en_atv_fase, f_atv.ptr_trf_prc, f_cine_data.i_brk_ndx = f_stk_context.pop()
        M_LOG.debug("restaura_associado:fnc_ope/fase:[{}]/[{}]".format(ldefs.DCT_FNC_OPE[f_atv.en_trf_fnc_ope], ldefs.DCT_FASE[f_atv.en_atv_fase]))
        M_LOG.debug("restaura_associado:ptr_trf_prc:[{}]".format(f_atv.ptr_trf_prc))
        M_LOG.debug("restaura_associado:i_brk_ndx:[{}]".format(f_cine_data.i_brk_ndx))

        # cai fora...
        return True

    # coloca a aeronave em manual
    f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

    # volta a fase de verificar condições
    f_atv.en_atv_fase = ldefs.E_FASE_ZERO

    # logger
    # M_LOG.info("restaura_associado:<<")

    # cai fora...
    return False

# -------------------------------------------------------------------------------------------------

def trata_associado(f_atv, f_brk, fi_brk_ndx, f_stk_context):
    """
    armazena na pilha os procedimentos associados.
    
    @param f_atv: ponteiro para struct aeronaves
    @param f_brk: ponteiro para struct breakpoints
    @param fi_brk_ndx: índice do breakpoint atual
    @param f_stk_context: ponteiro para pilha
    
    @return True se armazenou dados da aeronave na pilha, senão False.
    """
    # logger
    # M_LOG.info("trata_associado:>>")

    # verifica parâmetros de entrada
    assert f_atv

    # verifica condições de execução
    if not f_atv.v_atv_ok or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):

        # cai fora...
        return False

    # existe um procedimento associado ?
    if (f_brk.ptr_brk_prc is not None):  # (ldefs.E_NOPROC != f_brk.ptr_brk_prc) and (0 != f_brk.BkpNumProc):

        # se existe, empilha o contexto atual
        f_stk_context.append((f_atv.en_trf_fnc_ope, f_atv.en_atv_fase, f_atv.ptr_trf_prc, fi_brk_ndx))

        # carrega o novo contexto
        f_atv.en_trf_fnc_ope = f_brk.ptr_brk_prc
        f_atv.en_anv_fase = ldefs.E_FASE_ZERO

        # cai fora...
        return True

    # logger
    # M_LOG.info("trata_associado:<<")

    # retorna
    return False

# < the end >--------------------------------------------------------------------------------------
