#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_pouso

realiza o pouso das aeronaves vindas de uma aproximação ou pelo comando da pilotagem

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
import model.glb_defs as gdefs
import model.newton.defs_newton as ldefs

import model.emula.cine.calc_proa_demanda as cpd
import model.emula.cine.cine_calc as cincalc
import model.emula.cine.cine_model as cinmodel
import model.emula.cine.sentido_curva as scrv

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < variáveis locais >-----------------------------------------------------------------------------

glb_ui_ang_teta = 0.        # ângulo teta fator absoluto

glb_f_alt_rampa     = 0.    # altura da rampa de pouso
glb_f_dst_anv_ptq   = 0.    # distância da aeronave ao ponto
glb_f_dst_anv_ptq_x = 0.    # X da distância da anv ao ponto
glb_f_dst_anv_ptq_y = 0.    # Y da distância da anv ao ponto
glb_f_dst_eixo      = 0.    # distância do eixo
glb_f_dst_rampa     = 0.    # distância da rampa
glb_f_raio_curva    = 0.    # raio de curvatura

# -------------------------------------------------------------------------------------------------

def prc_pouso(f_atv):
    """
    @param f_atv: ponteiro para struct aeronaves
    """
    # globais
    global glb_ui_ang_teta, glb_f_dst_eixo, glb_f_dst_rampa, glb_f_dst_anv_ptq
    global glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y, glb_f_raio_curva

    # logger
    # M_LOG.info("prc_pouso:>>")

    # verifica parâmetros de entrada
    assert f_atv

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):

        # logger
        # M_LOG.info(u"prc_pouso:<E01: aeronave não ativa.")

        # cai fora...
        return None

    # verifica condições para execução
    if (f_atv.ptr_trf_prf is None) or (not f_atv.ptr_trf_prf.v_prf_ok):

        # logger
        # M_LOG.info(u"prc_pouso:<E02: performance não existe.")

        # cai fora...
        return

    # posição da aeronave (dir/esq) em relação ao eixo da pista
    len_pos_anv = 0

    # dados do aeródromo
    l_aer = f_atv.ptr_atv_aer

    if (l_aer is None) or (not l_aer.v_aer_ok):

        # força a abandonar o procedimento
        f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
        f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
        f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu

        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

        # logger
        l_log = logging.getLogger("prc_pouso")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E03: aeródromo inexistente. aeronave:[{}/{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind))
                                                
        # logger
        # M_LOG.info("<E03: aeródromo inexistente.")

        # return
        return

    # M_LOG.debug("prc_pouso:aerodromo:[{}]".format(l_aer.s_aer_indc))

    # dados da pista
    l_pst = f_atv.ptr_atv_pst

    if (l_pst is None) or (not l_pst.v_pst_ok):

        # força a abandonar o procedimento
        f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
        f_atv.f_atv_pro_dem = f_atv.f_trf_pro_atu
        f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu

        f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

        # logger
        l_log = logging.getLogger("prc_pouso")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E04: pista inexistente. aeronave:[{}/{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind))
                                                
        # logger
        # M_LOG.info("<E04: pista inexistente.")

        # return
        return

    # M_LOG.debug("prc_pouso:pista/rumo:[{}/{}]".format(l_pst.s_pst_indc, l_pst.i_pst_rumo))

    # fases do procedimento de pouso

    # fase de preparação para o procedimento ?
    if ldefs.E_FASE_ZERO == f_atv.en_atv_fase:

        # velocidade de aproximação
        f_atv.f_atv_vel_dem = f_atv.ptr_trf_prf.f_prf_vel_apx
        # M_LOG.debug("prc_pouso:f_atv.f_atv_vel_dem:[{}]".format(f_atv.f_atv_vel_dem))

        # estabiliza a altitude
        f_atv.f_atv_alt_dem = f_atv.f_trf_alt_atu
        # M_LOG.debug("prc_pouso:f_atv.f_atv_alt_dem:[{}]".format(f_atv.f_atv_alt_dem))

        # calcula o raio de curvatura
        assert abs(f_atv.f_atv_raz_crv) > 0
        # M_LOG.debug("prc_pouso:f_atv.f_atv_raz_crv:[{}]".format(f_atv.f_atv_raz_crv))

        glb_f_raio_curva = f_atv.f_trf_vel_atu / abs(math.radians(f_atv.f_atv_raz_crv))
        # M_LOG.debug("prc_pouso:glb_f_raio_curva:[{}]".format(glb_f_raio_curva))

        # calcula o ponto de toque
        glb_f_dst_anv_ptq_x = l_pst.f_pst_x - f_atv.f_trf_x
        # M_LOG.debug("prc_pouso:glb_f_dst_anv_ptq_x:[{}]".format(glb_f_dst_anv_ptq_x))
        glb_f_dst_anv_ptq_y = l_pst.f_pst_y - f_atv.f_trf_y
        # M_LOG.debug("prc_pouso:glb_f_dst_anv_ptq_y:[{}]".format(glb_f_dst_anv_ptq_y))

        # posição da aeronave em relação a pista (dir/esq)
        len_pos_anv = scrv.sent_crv(l_pst.i_pst_rumo, cpd.calc_proa_demanda(-glb_f_dst_anv_ptq_x, -glb_f_dst_anv_ptq_y))
        # M_LOG.debug("prc_pouso:len_pos_anv:[{}]".format(len_pos_anv))

        # calcula ângulo formado pela aeronave e a pista (teta)
        glb_ui_ang_teta = abs(l_pst.i_pst_rumo - cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y))

        if glb_ui_ang_teta > 180.:
            glb_ui_ang_teta = 360. - glb_ui_ang_teta

        # M_LOG.debug("prc_pouso:glb_ui_ang_teta:[{}]".format(glb_ui_ang_teta))

        # calcula distância da aeronave ao ponto (em linha reta)
        glb_f_dst_anv_ptq = math.sqrt((glb_f_dst_anv_ptq_x ** 2) + (glb_f_dst_anv_ptq_y ** 2))
        # M_LOG.debug("prc_pouso:glb_f_dst_anv_ptq:[{}]".format(glb_f_dst_anv_ptq))

        # calcula distância do eixo da pista
        glb_f_dst_eixo = abs(glb_f_dst_anv_ptq * math.sin(math.radians(glb_ui_ang_teta)))
        # M_LOG.debug("prc_pouso:glb_f_dst_eixo:[{}]".format(glb_f_dst_eixo))

        # calcula distância da rampa
        assert abs(math.tan(math.radians(ldefs.D_DST_RAMPA))) > 0

        glb_f_dst_rampa = (f_atv.f_trf_alt_atu - l_aer.f_aer_elev) / math.tan(math.radians(ldefs.D_DST_RAMPA))
        # M_LOG.debug("prc_pouso:glb_f_dst_rampa:[{}]".format(glb_f_dst_rampa))

        # aeronave afastada mais de 2R do eixo da pista ?
        if glb_f_dst_eixo >= (2 * glb_f_raio_curva):

            # aeronave pelo menos (3R + distância na rampa) antes da cabeceira ?
            if (glb_ui_ang_teta < 90.) and (abs(glb_f_dst_anv_ptq * math.cos(math.radians(glb_ui_ang_teta))) >= ((3 * glb_f_raio_curva) + glb_f_dst_rampa)):

                # aeronave a direita da pista ?
                if ldefs.E_DIREITA == len_pos_anv:

                    # aeronave a direita da pista
                    f_atv.f_atv_pro_dem = l_pst.i_pst_rumo - 90.

                    if f_atv.f_atv_pro_dem < 0:
                        f_atv.f_atv_pro_dem += 360.

                # senão,...
                else:
                    # aeronave a esquerda da pista
                    f_atv.f_atv_pro_dem = l_pst.i_pst_rumo + 90.

                    if f_atv.f_atv_pro_dem >= 360.:
                        f_atv.f_atv_pro_dem -= 360.

                # calcula sentido de curva pelo menor ângulo
                scrv.sentido_curva(f_atv)

                # voa para interceptar eixo da pista 
                f_atv.en_atv_fase = ldefs.E_FASE_EIXO

            # senão,...
            else:
                # aeronave após a distância que garante condição de alinhamento
                f_atv.f_atv_pro_dem = l_pst.i_pst_rumo + 180.

                if f_atv.f_atv_pro_dem >= 360.:
                    f_atv.f_atv_pro_dem -= 360.

                # aeronave a direita da pista ?
                if ldefs.E_DIREITA == len_pos_anv:

                    # aeronave a direita da pista
                    f_atv.f_atv_raz_crv = abs(f_atv.f_atv_raz_crv)

                # senão,...
                else:
                    # aeronave a esquerda da pista
                    f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)

                # define nova fase
                f_atv.en_atv_fase = ldefs.E_FASE_OPOSTA

        # senão,...
        else:
            # aeronave está no eixo da pista ? 
            if abs(glb_f_dst_eixo) <= 0.01:

                # aeronave está no rumo da pista ?
                if abs(f_atv.f_trf_pro_atu - l_pst.i_pst_rumo) <= 0.01:

                    # aeronave antes da rampa ?
                    if (glb_ui_ang_teta < 90.) and (abs(glb_f_dst_anv_ptq * math.cos(math.radians(glb_ui_ang_teta))) >= glb_f_dst_rampa):

                        # voar até iniciar rampa
                        f_atv.en_atv_fase = ldefs.E_FASE_ALINHAR

                    # senão,...
                    else:
                        # aeronave após a rampa
                        f_atv.f_atv_pro_dem = l_pst.i_pst_rumo - 90.

                        if f_atv.f_atv_pro_dem < 0:
                            f_atv.f_atv_pro_dem += 360.

                        # ajusta razão de curva para esquerda
                        f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)

                        # voar até se afastar 2R do eixo
                        f_atv.en_atv_fase = ldefs.E_FASE_AFASTA

                # senão, proas diferentes
                else:
                    # proa da aeronave oposta a da pista ?
                    if (abs(l_pst.i_pst_rumo - f_atv.f_trf_pro_atu) - 180.) <= 0.01:

                        # aeronave após a rampa
                        f_atv.f_atv_pro_dem = l_pst.i_pst_rumo + 90.

                        if f_atv.f_atv_pro_dem >= 360.:
                            f_atv.f_atv_pro_dem -= 360.

                        # ajusta razão de curva para esquerda
                        f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)

                        # voar até se afastar 2R do eixo
                        f_atv.en_atv_fase = ldefs.E_FASE_AFASTA

            # senão, distância do eixo menor 2R
            else:
                # aeronave a direita da pista ?
                if ldefs.E_DIREITA == len_pos_anv:

                    f_atv.f_atv_pro_dem = l_pst.i_pst_rumo + 90.

                    if f_atv.f_atv_pro_dem >= 360.:
                        f_atv.f_atv_pro_dem -= 360.

                # senão, aeronave a esquerda da pista
                else:
                    f_atv.f_atv_pro_dem = l_pst.i_pst_rumo - 90.

                    if f_atv.f_atv_pro_dem < 0:
                        f_atv.f_atv_pro_dem += 360.

                # força a curva pelo menor lado
                scrv.sentido_curva(f_atv)

                # voar até se afastar 2R do eixo
                f_atv.en_atv_fase = ldefs.E_FASE_AFASTA

    # fase voando até se afastar 2R do eixo da pista ?
    elif ldefs.E_FASE_AFASTA == f_atv.en_atv_fase:

        # calcula o raio de curvatura
        assert abs(f_atv.f_atv_raz_crv) > 0
        glb_f_raio_curva = f_atv.f_trf_vel_atu / abs(math.radians(f_atv.f_atv_raz_crv))

        # calcula o ponto de toque
        glb_f_dst_anv_ptq_x = l_pst.f_pst_x - f_atv.f_trf_x
        glb_f_dst_anv_ptq_y = l_pst.f_pst_y - f_atv.f_trf_y

        # calcula ângulo formado pela aeronave e a pista (teta)
        glb_ui_ang_teta = abs(l_pst.i_pst_rumo - cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y))

        if glb_ui_ang_teta > 180.:
            glb_ui_ang_teta = 360. - glb_ui_ang_teta

        # calcula a distância ao ponto de toque (em linha reta)
        glb_f_dst_anv_ptq = math.sqrt((glb_f_dst_anv_ptq_x ** 2) + (glb_f_dst_anv_ptq_y ** 2))

        # calcula a distância ao eixo
        glb_f_dst_eixo = abs(glb_f_dst_anv_ptq * math.sin(math.radians(glb_ui_ang_teta)))

        # aeronave distante pelo menos 2R do eixo da pista ?
        if glb_f_dst_eixo >= (2 * glb_f_raio_curva):

            # volta a fase inicial
            f_atv.en_atv_fase = ldefs.E_FASE_ZERO

    # fase voar na proa oposta para poder retornar a pista ?
    elif ldefs.E_FASE_OPOSTA == f_atv.en_atv_fase:

        # calcula o raio de curvatura
        assert abs(f_atv.f_atv_raz_crv) > 0.
        glb_f_raio_curva = f_atv.f_trf_vel_atu / abs(math.radians(f_atv.f_atv_raz_crv))

        # calcula o ponto de toque
        glb_f_dst_anv_ptq_x = l_pst.f_pst_x - f_atv.f_trf_x
        glb_f_dst_anv_ptq_y = l_pst.f_pst_y - f_atv.f_trf_y

        # posição da aeronave em relação a pista (direita/esquerda)
        len_pos_anv  = scrv.sent_crv(l_pst.i_pst_rumo, cpd.calc_proa_demanda(-glb_f_dst_anv_ptq_x, -glb_f_dst_anv_ptq_y))

        # calcula ângulo formado pela aeronave e a pista (teta)
        glb_ui_ang_teta = abs(l_pst.i_pst_rumo - cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y))

        if glb_ui_ang_teta > 180.:
            glb_ui_ang_teta = 360. - glb_ui_ang_teta

        # distância ao ponto de toque (em linha reta)
        glb_f_dst_anv_ptq = math.sqrt((glb_f_dst_anv_ptq_x ** 2) + (glb_f_dst_anv_ptq_y ** 2))

        # distância ao eixo da pista
        glb_f_dst_eixo = abs(glb_f_dst_anv_ptq * math.sin(math.radians(glb_ui_ang_teta)))

        # distância a rampa
        assert abs(math.tan(math.radians(ldefs.D_DST_RAMPA))) > 0.
        glb_f_dst_rampa = (f_atv.f_trf_alt_atu - l_aer.f_aer_elev) / math.tan(math.radians(ldefs.D_DST_RAMPA))

        # aeronave a 2R do eixo e mais de (glb_f_raio_curva + DistRampa) da cabeceira ?
        if (glb_ui_ang_teta < 90.) and ((abs(glb_f_dst_anv_ptq) * math.cos(math.radians(glb_ui_ang_teta))) >= (glb_f_raio_curva + glb_f_dst_rampa)):

            # aeronave a direita da pista ?
            if ldefs.E_DIREITA == len_pos_anv:

                f_atv.f_atv_pro_dem = l_pst.i_pst_rumo - 90.

                if f_atv.f_atv_pro_dem < 0:
                    f_atv.f_atv_pro_dem += 360.

            # senão, aeronave a esquerda da pista
            else:
                f_atv.f_atv_pro_dem = l_pst.i_pst_rumo + 90.

                if f_atv.f_atv_pro_dem >= 360.:
                    f_atv.f_atv_pro_dem -= 360.

            # força a curva pelo menor lado
            scrv.sentido_curva(f_atv)

            # voar para interceptar eixo da pista
            f_atv.en_atv_fase = ldefs.E_FASE_EIXO

    # fase voando para interceptar eixo da pista ?
    elif ldefs.E_FASE_EIXO == f_atv.en_atv_fase:

        # proas iguais ?
        if abs(f_atv.f_trf_pro_atu - f_atv.f_atv_pro_dem) <= 0.01:

            # calcula o raio de curvatura
            assert abs(f_atv.f_atv_raz_crv) > 0
            glb_f_raio_curva = f_atv.f_trf_vel_atu / abs(math.radians(f_atv.f_atv_raz_crv))

            # calcula a distância ao ponto de toque (componentes x e y)
            glb_f_dst_anv_ptq_x = l_pst.f_pst_x - f_atv.f_trf_x
            glb_f_dst_anv_ptq_y = l_pst.f_pst_y - f_atv.f_trf_y

            # calcula ângulo formado pela aeronave e a pista (teta)
            glb_ui_ang_teta = abs(l_pst.i_pst_rumo - cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y))

            if glb_ui_ang_teta > 180.:
                glb_ui_ang_teta = 360. - glb_ui_ang_teta

            # calcula a distância ao ponto de toque (em linha reta)
            glb_f_dst_anv_ptq = math.sqrt((glb_f_dst_anv_ptq_x ** 2) + (glb_f_dst_anv_ptq_y ** 2))

            # distância da aeronave ao eixo
            glb_f_dst_eixo = abs(glb_f_dst_anv_ptq * math.sin(math.radians(glb_ui_ang_teta)))

            # distância da aeronave ao eixo da pista > raio de curvatura ?
            if glb_f_dst_eixo <= glb_f_raio_curva:

                # curva em direção ao rumo da pista
                f_atv.f_atv_pro_dem = l_pst.i_pst_rumo

                # força a curva pelo menor lado
                scrv.sentido_curva(f_atv)

                # curva para buscar alinhamento com eixo da pista
                f_atv.en_atv_fase = ldefs.E_FASE_CURVA

    # fase curvando para buscar alinhamento inicial com eixo da pista ?
    elif ldefs.E_FASE_CURVA == f_atv.en_atv_fase:

        # aeronave alinhada com a pista ?
        if abs(f_atv.f_trf_pro_atu - f_atv.f_atv_pro_dem) <= 0.01:

            # calcula a distância ao ponto de toque (componentes x e y)
            glb_f_dst_anv_ptq_x = l_pst.f_pst_x - f_atv.f_trf_x
            glb_f_dst_anv_ptq_y = l_pst.f_pst_y - f_atv.f_trf_y

            # calcula proa de demanda
            f_atv.f_atv_pro_dem = cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y)

            # força a curva pelo menor lado
            scrv.sentido_curva(f_atv)

            # aeronave mantendo o alinhamento com a pista
            f_atv.en_atv_fase = ldefs.E_FASE_ALINHAR

    # fase aeronave mantendo o alinhamento com a pista ?
    elif ldefs.E_FASE_ALINHAR == f_atv.en_atv_fase:

        # calcula a distância ao ponto de toque (componentes x e y)
        glb_f_dst_anv_ptq_x = l_pst.f_pst_x - f_atv.f_trf_x
        glb_f_dst_anv_ptq_y = l_pst.f_pst_y - f_atv.f_trf_y

        # calcula ângulo formado pela aeronave e a pista (teta)
        glb_ui_ang_teta = abs(l_pst.i_pst_rumo - cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y))

        if glb_ui_ang_teta > 180.:
            glb_ui_ang_teta = 360. - glb_ui_ang_teta

        # calcula a distância ao ponto de toque (em linha reta)
        glb_f_dst_anv_ptq = math.sqrt((glb_f_dst_anv_ptq_x ** 2) + (glb_f_dst_anv_ptq_y ** 2))

        if glb_ui_ang_teta < 90.:

            # aeronave antes da cabeceira (considerando dt = 1s)
            glb_f_alt_rampa = glb_f_dst_anv_ptq * math.tan(math.radians(ldefs.D_DST_RAMPA))

            if ((f_atv.f_trf_alt_atu - l_aer.f_aer_elev) >= glb_f_alt_rampa - abs(f_atv.ptr_trf_prf.f_prf_raz_des_apx)) and \
               ((f_atv.f_trf_alt_atu - l_aer.f_aer_elev) <  glb_f_alt_rampa + abs(f_atv.ptr_trf_prf.f_prf_raz_des_apx)):

                # início da rampa de descida
                assert abs(glb_f_dst_anv_ptq) > 0

                # calcula a razão de descida
                f_atv.f_atv_raz_sub = ((f_atv.f_trf_alt_atu - l_aer.f_aer_elev) * f_atv.f_atv_vel_gnd) / glb_f_dst_anv_ptq

                # altitude de demanda é a elevação do aeródromo
                f_atv.f_atv_alt_dem = l_aer.f_aer_elev

                # voa aeronave na rampa
                f_atv.en_atv_fase = ldefs.E_FASE_RAMPA

            # aeronave procurando novo alinhamento ?
            if f_atv.f_trf_pro_atu != f_atv.f_atv_pro_dem:

                # aeronave procurando novo alinhamento
                f_atv.f_atv_pro_dem = cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y)

                # força a curva pelo menor lado
                scrv.sentido_curva(f_atv)

        # senão, teta >= 90.
        else:
            # aeronave após a cabeceira
            f_atv.f_atv_pro_dem = l_pst.i_pst_rumo + 180.

            if f_atv.f_atv_pro_dem >= 360.:
                f_atv.f_atv_pro_dem -= 360.

            # inicia a razão de curva
            f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)

            # voa até se afastar 2R do eixo da pista
            f_atv.en_atv_fase = ldefs.E_FASE_AFASTA

    # fase aeronave mantendo o alinhamento na aproximação com a pista ?
    elif ldefs.E_FASE_APXALINHAR == f_atv.en_atv_fase:

        # calcula o ponto de toque (componentes x e y)
        glb_f_dst_anv_ptq_x = l_pst.f_pst_x - f_atv.f_trf_x
        glb_f_dst_anv_ptq_y = l_pst.f_pst_y - f_atv.f_trf_y

        # calcula ângulo formado pela aeronave e a pista (teta)
        glb_ui_ang_teta = abs(l_pst.i_pst_rumo - cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y))

        if glb_ui_ang_teta > 180.:
            glb_ui_ang_teta = 360. - glb_ui_ang_teta

        # calcula o ponto de toque (em linha reta)
        glb_f_dst_anv_ptq = math.sqrt((glb_f_dst_anv_ptq_x ** 2) + (glb_f_dst_anv_ptq_y ** 2))

        # aeronave antes da cabeceira (considerando dt = 1s)
        if glb_ui_ang_teta < 90.:

            # início da rampa de descida
            assert abs(glb_f_dst_anv_ptq) > 0

            # calcula a razão de descida
            f_atv.f_atv_raz_sub = (f_atv.f_trf_alt_atu * f_atv.f_atv_vel_gnd) / glb_f_dst_anv_ptq

            # altitude de demanda é a elevação do aeródromo
            f_atv.f_atv_alt_dem = l_aer.f_aer_elev

            # voa aeronave na rampa
            f_atv.en_atv_fase = ldefs.E_FASE_RAMPA

            # aeronave procurando novo alinhamento ?
            if f_atv.f_trf_pro_atu != f_atv.f_atv_pro_dem:

                # aeronave procurando novo alinhamento
                f_atv.f_atv_pro_dem = cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y)

                # força a curva pelo menor lado
                scrv.sentido_curva(f_atv)

    # fase aeronave na rampa ?
    elif ldefs.E_FASE_RAMPA == f_atv.en_atv_fase:

        # inicia a aceleração
        f_atv.f_atv_acel = 0.

        # calcula o ponto de toque (componentes x e y)
        glb_f_dst_anv_ptq_x = l_pst.f_pst_x - f_atv.f_trf_x
        glb_f_dst_anv_ptq_y = l_pst.f_pst_y - f_atv.f_trf_y

        # calcula ângulo formado pela aeronave e a pista (teta)
        glb_ui_ang_teta = abs(l_pst.i_pst_rumo - cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y))

        if glb_ui_ang_teta > 180.:
            glb_ui_ang_teta = 360. - glb_ui_ang_teta

        # # calcula o ponto de toque (em linha reta)
        glb_f_dst_anv_ptq = math.sqrt((glb_f_dst_anv_ptq_x ** 2) + (glb_f_dst_anv_ptq_y ** 2))

        # verifica a cabeceira oposta
        if glb_ui_ang_teta >= 90.:

            # aeronave após cabeceira
            glb_f_dst_anv_ptq_x = l_pst.f_pst_cab_opos_x - f_atv.f_trf_x
            glb_f_dst_anv_ptq_y = l_pst.f_pst_cab_opos_y - f_atv.f_trf_y

        # aeronave procurando novo alinhamento ?
        if f_atv.f_trf_pro_atu != f_atv.f_atv_pro_dem:

            # aeronave procurando novo alinhamento
            f_atv.f_atv_pro_dem = cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y)

            # força a curva pelo menor lado
            scrv.sentido_curva(f_atv)

        # aeronave tocou a pista ?
        if abs(f_atv.f_trf_alt_atu - l_aer.f_aer_elev) <= 0.01:

            # calcula a distância ao fim da pista (componentes x e y)
            glb_f_dst_anv_ptq_x = l_pst.f_pst_cab_opos_x - f_atv.f_trf_x
            glb_f_dst_anv_ptq_y = l_pst.f_pst_cab_opos_y - f_atv.f_trf_y

            # inicia a proa de demanda
            f_atv.f_atv_pro_dem = cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y)

            # força a curva pelo menor lado
            scrv.sentido_curva(f_atv)

            # ajusta a velocidade para pouso
            f_atv.f_atv_vel_dem = 0.

            # desaceleração no pouso
            f_atv.f_atv_acel = 2 * abs(f_atv.ptr_trf_prf.f_prf_raz_max_var_vel)

            # prepara a aeronave para parada na pista
            f_atv.en_atv_fase = ldefs.E_FASE_PISTA

    # fase aeronave pára na pista ?
    elif ldefs.E_FASE_PISTA == f_atv.en_atv_fase:

        # calcula a distância da aeronave a cabeceira oposta (componentes x e y)
        glb_f_dst_anv_ptq_x = l_pst.f_pst_cab_opos_x - f_atv.f_trf_x
        glb_f_dst_anv_ptq_y = l_pst.f_pst_cab_opos_y - f_atv.f_trf_y

        # calcula a distância da aeronave a cabeceira oposta (em linha reta)
        glb_f_dst_anv_ptq = math.sqrt((glb_f_dst_anv_ptq_x ** 2) + (glb_f_dst_anv_ptq_y ** 2))

        assert abs(f_atv.f_atv_acel) > 0

        # espaço de pista menor que o necessário para frear a aeronave ?
        if glb_f_dst_anv_ptq < (f_atv.f_trf_vel_atu ** 2) / (2 * f_atv.f_atv_acel):

            # aumenta a frenagem
            f_atv.f_atv_acel = 4 * abs(f_atv.ptr_trf_prf.f_prf_raz_max_var_vel)

        # aeronave procurando novo alinhamento ?
        if f_atv.f_trf_pro_atu != f_atv.f_atv_pro_dem:

            # chegou ao fim da pista ?
            if (abs(l_pst.f_pst_cab_opos_x - f_atv.f_trf_x) <= abs(glb_f_dst_anv_ptq_x)) and \
               (abs(l_pst.f_pst_cab_opos_y - f_atv.f_trf_y) <= abs(glb_f_dst_anv_ptq_y)):

                # ajusta demanda ao rumo da pista
                f_atv.f_atv_pro_dem = l_pst.i_pst_rumo

            # senão,...
            else:
                # calcula distância ao fim da pista
                glb_f_dst_anv_ptq_x = l_pst.f_pst_cab_opos_x - f_atv.f_trf_x
                glb_f_dst_anv_ptq_y = l_pst.f_pst_cab_opos_y - f_atv.f_trf_y

                # calcula nova proa de demanda
                f_atv.f_atv_pro_dem = cpd.calc_proa_demanda(glb_f_dst_anv_ptq_x, glb_f_dst_anv_ptq_y)

            # força a curva pelo menor lado
            scrv.sentido_curva(f_atv)

        # aeronave parou ?
        if 0. == f_atv.f_trf_vel_atu:

            # ajusta os dados da aeronave no solo
            # f_atv.v_atv_visu   = False
            # f_atv.v_atv_movi   = False
            f_atv.en_trf_fnc_ope = ldefs.E_MANUAL
            f_atv.en_atv_est_atv = ldefs.E_CANCELADA

    # senão, erro no valor da fase
    else:
        # logger
        l_log = logging.getLogger("prc_pouso")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E05: fase no pouso não identificada:[{}].".format(ldefs.DCT_FASE[f_atv.en_atv_fase]))

    # logger
    # M_LOG.info("prc_pouso:<<")

# < the end >--------------------------------------------------------------------------------------
