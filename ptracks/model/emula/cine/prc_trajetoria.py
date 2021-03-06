#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_trajetoria

realiza a passagem da aeronave por todos os breakpoints que determinam uma trajetória

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
from ...newton import defs_newton as ldefs

from ...emula.cine import abort_prc as abnd
from ...emula.cine import obtem_brk as obrk
from ...emula.cine import prc_dir_ponto as dp
from ...emula.cine import trata_associado as tass
from ...emula.cine import sentido_curva as scrv

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------

def prc_trajetoria(f_atv, f_cine_data, f_stk_context):
    """
    @param f_atv: 
    @param f_cine_data:
    @param f_stk_context:
    """
    # logger
    # M_LOG.info("prc_trajetoria:>>")

    # verifica parâmetros de entrada
    assert f_atv
    assert f_cine_data
    assert f_stk_context is not None

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
            
        # logger
        # M_LOG.info(u"prc_trajetoria:<E01: aeronave não ativa.")

        # cai fora...
        return

    # dados da trajetória
    l_trj = f_atv.ptr_trf_prc

    if (l_trj is None) or (not l_trj.v_prc_ok):

        # logger
        l_log = logging.getLogger("prc_trajetoria")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E02: trajetória inexistente. aeronave:[{}/{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind))

        # não encontrou a trajetória, força a aeronave abandonar a trajetória
        abnd.abort_prc(f_atv)
        
        # logger
        # M_LOG.info("prc_trajetoria:<E02: trajetória inexistente.")

        # return
        return

    # M_LOG.debug("prc_trajetoria:fase(1):[{}]".format(ldefs.DCT_FASE[f_atv.en_atv_fase]))

    # fase de iniciação ?
    if ldefs.E_FASE_ZERO == f_atv.en_atv_fase:

        # reseta o flag altitude/velocidade para iniciar uma nova trajetória
        f_atv.i_atv_change_alt_vel = 0

        # inicia o contador de breakpoints
        f_cine_data.i_brk_ndx = 0

        # inicia com dados do primeiro breakpoint
        l_brk = f_atv.ptr_atv_brk = l_trj.lst_trj_brk[0]

        if (l_brk is None) or not l_brk.v_brk_ok:

            # logger
            l_log = logging.getLogger("prc_trajetoria")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E03: trajetória/breakpoint inexistente. aeronave:[{}/{}] fase:[{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind, ldefs.DCT_FASE[f_atv.en_atv_fase]))

            # não encontrou o breakpoint, força a abandonar a trajetória
            abnd.abort_prc(f_atv)

            # logger
            # M_LOG.info("prc_trajetoria:<E03: breakpoint inexistente.")

            # return
            return

        # obtém dados do breakpoint da trajetória
        obrk.obtem_brk(f_atv, l_brk, f_cine_data)

    # fase de direção ao ponto
    elif ldefs.E_FASE_DIRPONTO == f_atv.en_atv_fase:

        # obter dados do breakpoint da trajetória
        l_brk = f_atv.ptr_atv_brk

        if (l_brk is None) or not l_brk.v_brk_ok:

            # logger
            l_log = logging.getLogger("prc_trajetoria")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E04: trajetória/breakpoint inexistente. aeronave:[{}/{}] fase:[{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind, ldefs.DCT_FASE[f_atv.en_atv_fase]))

            # não encontrou o breakpoint, força a abandonar a trajetória
            abnd.abort_prc(f_atv)

            # logger
            # M_LOG.info("prc_trajetoria:<E04: breakpoint inexistente.")

            # return
            return

        # obtém as coordenadas do ponto a ser bloqueado
        lf_brk_x = f_cine_data.f_coord_x_brk
        lf_brk_y = f_cine_data.f_coord_y_brk
        # M_LOG.debug("prc_trajetoria:stk.f_brk_x:[{}] stk.f_brk_y:[{}]".format(f_cine_data.f_coord_x_brk, f_cine_data.f_coord_y_brk))

        '''# tratamento para vôo lateral

        # foi comandado na pilotagem vôo lateral ?
        if f_atv.f_atv_dst_vlat > 0.:

            lf_radial = 0.

            # calcula a radial
            if 'D' == f_atv.c_atv_dir_vlat:
                lf_radial = 180.

            else:
                lf_radial = 0.

            if lf_radial <= 90.:
                lf_radial = 90. - lf_radial

            else:
                lf_radial = 450. - lf_radial

            # converte para radianos
            lf_radial = math.radians(lf_radial)

            # calcula as coordenadas x e y relativo ao fixo
            lf_brk_x = f_atv.f_atv_dst_vlat * math.cos(lf_radial)
            lf_brk_y = f_atv.f_atv_dst_vlat * math.sin(lf_radial)

            # calcula a projeção do ponto a ser deslocado "nnn NM" à direita ou à esquerda
            lf_brk_x = lf_brk_x + l_brk.f_brk_x
            lf_brk_y = lf_brk_y + l_brk.f_brk_y
        '''
        # faz o direcionamento ao breakpoint
        if dp.prc_dir_ponto(f_atv, lf_brk_x, lf_brk_y, f_cine_data):

            # ao bloquear o ponto, verifica se tem um procedimento associado ?
            if not tass.trata_associado(f_atv, l_brk, f_cine_data.i_brk_ndx, f_stk_context):

                # não tem procedimento associado, muda de fase
                f_atv.en_atv_fase = ldefs.E_FASE_BREAKPOINT

    # fase rumo/altitude ?
    elif ldefs.E_FASE_RUMOALT == f_atv.en_atv_fase:

        # dados do breakpoint da trajetória
        l_brk = f_atv.ptr_atv_brk

        if (l_brk is None) or not l_brk.v_brk_ok:

            # logger
            l_log = logging.getLogger("prc_trajetoria")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E05: trajetória/breakpoint inexistente. aeronave:[{}/{}] fase:[{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind, ldefs.DCT_FASE[f_atv.en_atv_fase]))

            # não encontrou o breakpoint, força a abandonar a trajetória
            abnd.abort_prc(f_atv)

            # logger
            # M_LOG.info("prc_trajetoria:<E05: breakpoint inexistente.")

            # return
            return

        # proa e a altitude estão estabilizadas ?
        if (f_atv.f_trf_pro_atu == f_atv.f_atv_pro_dem) and (f_atv.f_trf_alt_atu == f_atv.f_atv_alt_dem):

            # não existe procedimento associado ?
            if not tass.trata_associado(f_atv, f_cine_data.i_brk_ndx, f_stk_context):

                # muda de fase
                f_atv.en_atv_fase = ldefs.E_FASE_BREAKPOINT

    # fase de breakpoint ?
    elif ldefs.E_FASE_BREAKPOINT == f_atv.en_atv_fase:

        # é o último breakpoint da trajetoria atual ?
        if f_atv.ptr_atv_brk == l_trj.lst_trj_brk[-1]:

            # reseta o flag altitude/velocidade
            f_atv.i_atv_change_alt_vel = 0

            # não tem dados na pilha ?
            if not tass.restaura_associado(f_atv, f_cine_data, f_stk_context):

                # qual a proa que a aeroanve deve seguir após bloquear o último breakpoint ?
                if l_trj.f_trj_proa > 0.:

                    # ajusta proa de demanda
                    f_atv.f_atv_pro_dem = l_trj.f_trj_proa

                # otherwise,... 
                else:
                    # ajusta proa de demanda
                    f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu

                # força a curva pelo menor lado
                scrv.sentido_curva(f_atv)

            # senão, tem dados na pilha !
            else:
                ''' # após o desempilhamento o procedimento restaurado na aeronave é trajetória ?
                if ldefs.E_TRAJETORIA != f_atv.en_trf_fnc_ope:

                    # logger
                    # M_LOG.info("prc_trajetoria:<E06: breakpoint inexistente.")

                    # return
                    return

                # dados da trajetória anterior
                l_trj = f_atv.ptr_trf_prc

                # é o último ponto da trajetoria anterior ?
                if f_atv.ptr_atv_brk._pNext is None:

                    # bloqueou o último ponto da trajetória anterior, força procedimento manual
                    abnd.abort_prc(f_atv)

                    if l_trj.f_trj_proa > 0.:
                        f_atv.f_atv_pro_dem = l_trj.f_trj_proa

                    else:
                        f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu

                    # força a curva pelo menor lado
                    scrv.sentido_curva(f_atv)

                # senão, não é o último breakpoint da trajetória anterior
                else:
                    # aponta para o próximo breakpoint da trajetória anterior
                    f_atv.ptr_atv_brk = f_atv.ptr_atv_brk._pNext

                    l_brk = f_atv.ptr_atv_brk

                    if (l_brk is None) or not l_brk.v_brk_ok:

                        # logger
                        l_log = logging.getLogger("prc_trajetoria")
                        l_log.setLevel(logging.ERROR)
                        l_log.error(u"<E07: trajetória anterior não é último ponto. aeronave:[{}/{}] fase:[{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind, ldefs.DCT_FASE[f_atv.en_atv_fase]))

                        # não encontrou o breakpoint, força a abandonar a trajetória
                        abnd.abort_prc(f_atv)

                        # logger
                        # M_LOG.info("prc_trajetoria:<E07: breakpoint inexistente.")

                        # return
                        return

                    # obtém dados do breakpoint da trajetória anterior
                    obrk.obtem_brk(f_atv, l_brk, f_cine_data)
                '''
                pass
                
        # senão, não é o último breakpoint
        else:
            # próximo breakpoint
            f_cine_data.i_brk_ndx += 1
                    
            # aponta para o próximo breakpoint
            l_brk = f_atv.ptr_atv_brk = l_trj.lst_trj_brk[f_cine_data.i_brk_ndx]

            if (l_brk is None) or not l_brk.v_brk_ok:

                # logger
                l_log = logging.getLogger("prc_trajetoria")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E08: trajetória/breakpoint inexistente. aeronave:[{}/{}] fase:[{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind, ldefs.DCT_FASE[f_atv.en_atv_fase]))

                # não encontrou o breakpoint, força a abandonar a trajetória
                abnd.abort_prc(f_atv)

                # logger
                # M_LOG.info(u"prc_trajetoria:<E08: breakpoint inexistente.")

                # return
                return

            # obtém dados do breakpoint atual
            obrk.obtem_brk(f_atv, l_brk, f_cine_data)

    # fase de direcionamento a um fixo ?
    elif ldefs.E_FASE_DIRFIXO == f_atv.en_atv_fase:

        # reseta o flag altitude/velocidade para iniciar uma nova trajetória
        f_atv.i_atv_change_alt_vel = 0

        # aponta para o breakpoint
        l_brk = f_atv.ptr_atv_brk

        if (l_brk is None) or not l_brk.v_brk_ok:

            # logger
            l_log = logging.getLogger("prc_trajetoria")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E09: trajetória/breakpoint inexistente. aeronave:[{}/{}] fase:[{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind, ldefs.DCT_FASE[f_atv.en_atv_fase]))

            # não encontrou o breakpoint, força a abandonar a trajetória
            abnd.abort_prc(f_atv)

            # logger
            # M_LOG.info(u"prc_trajetoria:<E09: breakpoint inexistente.")

            # return
            return

        # obtém dados do breakpoint atual
        obrk.obtem_brk(f_atv, l_brk, f_cine_data)

    # otherwise, erro na valor da fase
    else:
        # logger
        l_log = logging.getLogger("prc_trajetoria")
        l_log.setLevel(logging.WARNING)
        l_log.warning(u"<E10: fase na trajetória não identificada. fase:[{}].".format(ldefs.DCT_FASE[f_atv.en_atv_fase]))

    # M_LOG.debug("prc_trajetoria:fase(2):[{}]".format(ldefs.DCT_FASE[f_atv.en_atv_fase]))

    # logger
    # M_LOG.info("prc_trajetoria:<<")

# < the end >--------------------------------------------------------------------------------------
