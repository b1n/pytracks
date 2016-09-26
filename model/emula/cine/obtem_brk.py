#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
obtem_brk

obtém os breakpoints para os procedimetos de Aproximação, Trajetória, Aproximação Perdida e Subida

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
from ...emula.cine import abort_prc as abnd
from ...emula.cine import sentido_curva as scrv

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------

def obtem_brk(f_atv, f_brk, f_cine_data):
    """
    @param f_atv: ponteiro para struct aeronaves
    @param f_brk: ponteiro para struct breakpoints
    @param f_cine_data: ponteiro para pilha
    """
    # logger
    # M_LOG.info("obtem_brk:>>")
                
    # verifica parâmetros de entrada
    assert f_atv
    assert f_cine_data

    # verifica condições para execução     
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
                                
        # logger
        # M_LOG.info(u"obtem_brk:<E01: aeronave não ativa.")
                                                        
        # cai fora...
        return

    # verifica condições para execução     
    if (f_atv.ptr_trf_prf is None) or (not f_atv.ptr_trf_prf.v_prf_ok):
                                
        # logger
        # M_LOG.info(u"obtem_brk:<E02: performance não existe.")
                                                        
        # cai fora...
        return

    # valida parâmetro
    if (f_brk is None) or (not f_brk.v_brk_ok):

        # logger
        l_log = logging.getLogger("obtem_brk::obtem_brk")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E03: breakpoint inexistente. aeronave:[{}/{}].".format(f_atv.i_trf_id, f_atv.s_trf_ind))

        # não encontrou o breakpoint, força a abandonar o procedimento
        abnd.abort_prc(f_atv)

        # logger
        # M_LOG.info(u"obtem_brk:<E03: breakpoint inexistente.")
                    
        # breakpoints inexistentes
        return

    # + obtém a altitude do ponto se:
    #   - nada foi alterado (velocidade e altitude) durante a trajetória ou
    #   - apenas a velocidade foi alterada durante a trajetória

    # + se a altitude foi alterada (v_atv_change_alt_vel = True)
    #   - mantém a altitude inserida pelo piloto e despreza as altitudes dos próximos pontos

    # i_atv_change_alt_vel = 0 > normal (sem alteração velocidade/altitude)
    # i_atv_change_alt_vel = 1 > mudou apenas a altitude
    # i_atv_change_alt_vel = 2 > mudou apenas a velocidade
    # i_atv_change_alt_vel = 3 > mudou ambas

    if f_atv.en_trf_fnc_ope in [ldefs.E_SUBIDA, ldefs.E_TRAJETORIA]:

        # M_LOG.debug("obtem_brk:i_atv_change_alt_vel(1):[{}]".format(f_atv.i_atv_change_alt_vel))
        
        # checa se precisa obter a altitude do ponto ou a altitude de TRJ do tráfego ou da performance da aeronave
        if (0 == f_atv.i_atv_change_alt_vel) or (2 == f_atv.i_atv_change_alt_vel):

            # é uma subida ?
            if ldefs.E_SUBIDA == f_atv.en_trf_fnc_ope:

                # altitude do ponto contém dado ?
                if f_brk.f_brk_alt > 0.:

                    # altitude do ponto maior que teto de serviço ?
                    if f_brk.f_brk_alt > f_atv.ptr_trf_prf.f_prf_teto_sv:

                        # altitude de demanda recebe teto de serviço
                        f_atv.f_atv_alt_dem = f_atv.ptr_trf_prf.f_prf_teto_sv

                    else:
                        # se altitude do ponto maior que altitude de TRJ tráfego
                        if (f_brk.f_brk_alt > f_atv.f_trf_alt_trj) and (f_atv.f_trf_alt_trj > 0.):

                            # altitude de demanda recebe altitude de TRJ do tráfego
                            f_atv.f_atv_alt_dem = f_atv.f_trf_alt_trj

                        else:
                            # altitude de demanda recebe altitude do ponto
                            f_atv.f_atv_alt_dem = f_brk.f_brk_alt

            # é uma trajetória : 
            elif ldefs.E_TRAJETORIA == f_atv.en_trf_fnc_ope:

                # M_LOG.debug("obtem_brk:f_brk_alt:[{}]".format(f_brk.f_brk_alt))

                # altitude do breakpoint contém dado ?
                if f_brk.f_brk_alt > 0.:

                    # altitude do breakpoint > teto de serviço ?
                    if f_brk.f_brk_alt > f_atv.ptr_trf_prf.f_prf_teto_sv:

                        # M_LOG.debug("obtem_brk:acima do teto de serviço")

                        # altitude de demanda recebe teto de serviço
                        f_atv.f_atv_alt_dem = f_atv.ptr_trf_prf.f_prf_teto_sv

                    # senão, abaixo do teto de serviço 
                    else:
                        # M_LOG.debug("obtem_brk:usa altitude do breakpoint")

                        # altitude de demanda recebe altitude do breakpoint
                        f_atv.f_atv_alt_dem = f_brk.f_brk_alt

                # senão, não tem altitude do breakpoint
                else:
                    # altitude de trajetória contém dado ?
                    if f_atv.f_trf_alt_trj > 0.:

                        # altitude de demanda recebe a altitude de trajetória do tráfego
                        f_atv.f_atv_alt_dem = f_atv.f_trf_alt_trj

                # M_LOG.debug("obtem_brk:f_atv_alt_dem:[{}]".format(f_atv.f_atv_alt_dem))

    # senão,...
    else:
        # altitude de demanda recebe altitude do breakpoint ou teto de serviço, quem for menor
        f_atv.f_atv_alt_dem = min(f_brk.f_brk_alt, f_atv.ptr_trf_prf.f_prf_teto_sv)

    # coordenada é do tipo 'T' (temporal)
    if f_brk.i_brk_t > 0:
        '''
        # aponta o fixo de referência
        # FIXO * l_pFix = None ; # &f_pAtm.AtmFix [ (int)f_brk.f_brk_x ] ;   # !!!REVER!!!

        # calcula a projeção do ponto
        # f_cine_data.fCoordXBkp = l_pFix.fFixX + ( f_atv.f_trf_vel_atu * f_brk.i_brk_t * sinf ( f_brk.f_brk_y ))
        # f_cine_data.fCoordYBkp = l_pFix.fFixY + ( f_atv.f_trf_vel_atu * f_brk.i_brk_t * cosf ( f_brk.f_brk_y ))
        '''
        pass 

    # coordenada é do tipo 'R' (rumo e altitude)
    elif f_brk.i_brk_t < 0:
        '''
        # é razão ou gradiente ?
        if f_brk.f_brk_x <= 0.:

            # obtém a razão de subida
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_sub_crz

        # otherwise,...
        else:
            # o gradiente é uma porcentagem e uma razão de subida um valor inteiro. O
            # gradiente nunca é maior que 10%.  A razão de subida sempre é maior que
            # 100ft/min. Assumir que valores maiores que 10 é razão de subida e valores
            # menores ou iguais a 10 é gradiente.
            # ref: Tratamento do Gradiente de Subida conforme MMA 100-31, pag.108.

            # é gradiente ?
            if f_brk.f_brk_x <= 10.:

                # aplica a forma simplificada do gradiente    !!!REVER!!!
                li_val = int(f_atv.f_trf_vel_atu * f_brk.f_brk_x)

                # calcula o módulo 50
                li_mod = li_val % 50

                if li_mod > 0:

                    # se não for múltiplo de 50, arrendondar para o múltiplo mais próximo
                    if li_mod < 26:
                        li_val -= li_mod

                    else:
                        li_val += 50 - li_mod

                # armazena o gradiente aplicado o múltiplo de 50
                f_atv.f_atv_raz_sub = float(li_val)

            # senão, é uma razão de subida
            else:
                # armazena a razão de subida (ft/min -> m/s)
                f_atv.f_atv_raz_sub = f_brk.f_brk_x * cdefs.D_CNV_FT2M / 60.

        # obtém o rumo
        f_atv.f_atv_pro_dem = math.degrees(f_brk.f_brk_y)

        # calcula a curva pelo menor lado
        scrv.sentido_curva(f_atv)
        '''
        pass
        
    # otherwise, f_brk.i_brk_t == 0
    else:
        # armazena na pilha as coordenadas cartesianas do breakpoint
        f_cine_data.f_coord_x_brk = f_brk.f_brk_x
        f_cine_data.f_coord_y_brk = f_brk.f_brk_y
        # M_LOG.debug("obtem_brk:f_cine_data.f_brk_x:[{}] f_cine_data.f_brk_y:[{}]".format(f_cine_data.f_coord_x_brk, f_cine_data.f_coord_y_brk))

    # trajetória ?
    if ldefs.E_TRAJETORIA == f_atv.en_trf_fnc_ope:

        # verifica procedimento de trajetória
        assert f_atv.ptr_trf_prc
        assert f_atv.ptr_trf_prc.v_prc_ok
        
        # + obtém a velocidade do ponto se:
        #   - nada foi alterado (vel e alt) durante a trajetória ou
        #   - apenas a altitude foi alterada durante a trajetória

        # + se a velocidade foi alterada (i_atv_change_alt_vel = 2)
        #   - mantém a velocidade inserida pelo piloto e despreza as velocidades dos próximos pontos

        # i_atv_change_alt_vel = 0 > normal (sem alteração velocidade/altitude)
        # i_atv_change_alt_vel = 1 > mudou apenas a altitude,
        # i_atv_change_alt_vel = 2 > mudou apenas a velocidade
        # i_atv_change_alt_vel = 3 > mudou ambas

        # M_LOG.debug("obtem_brk:i_atv_change_alt_vel(2):[{}]".format(f_atv.i_atv_change_alt_vel))

        # checa se precisa obter a velocidade do ponto ou a velocidade do tráfego
        if (0 == f_atv.i_atv_change_alt_vel) or (1 == f_atv.i_atv_change_alt_vel):

            # star ?
            if f_atv.ptr_trf_prc.v_trj_star:
                '''
                # velocidade do breakpoint contém dado ?
                if f_brk.f_brk_vel > 0.:

                    # converte a VelMaxCrz para IAS
                    lf_vel = f_atv.ptr_trf_prf.f_prf_vel_max_crz  # calcIAS(f_atv.ptr_trf_prf.f_prf_vel_max_crz, f_atv.f_atv_alt_dem, Exercicio.fExeVarTempISA)

                    # demanda recebe velocidade do breakpoint ou VelMaxCrz (IAS) o que for menor
                    f_atv.f_atv_vel_dem = min(f_brk.f_brk_vel, lf_vel)
                '''
                pass
                
            # senão é trajetória ACC
            else:
                # M_LOG.debug("obtem_brk:f_trf_vel_trj:[{}]".format(f_atv.f_trf_vel_trj))

                # velocidade de trajetória do tráfego contém dado ?
                if f_atv.f_trf_vel_trj > 0.:

                    # M_LOG.debug("obtem_brk:usa velocidade do tráfego")

                    # velocidade de demanda recebe a velocidade de trajetória do tráfego. (convertido para IAS na conversão)
                    f_atv.f_atv_vel_dem = f_atv.f_trf_vel_trj

                # senão, não tem velocidade de trajetória do tráfego
                else:
                    # M_LOG.debug("obtem_brk:f_brk_vel:[{}]".format(f_brk.f_brk_vel))

                    # velocidade do breakpoint contém dado ?
                    if f_brk.f_brk_vel > 0.:

                        # velocidade do ponto extrapolou o limite da performance ?
                        if f_brk.f_brk_vel > f_atv.ptr_trf_prf.f_prf_vel_max_crz:

                            # M_LOG.debug("obtem_brk:usa velocidade VelMaxCrz")

                            # velocidade de demanda recebe a VelMaxCrz convertida para IAS
                            f_atv.f_atv_vel_dem = f_atv.ptr_trf_prf.f_prf_vel_max_crz  # calcIAS ( f_atv.ptr_trf_prf.fAtrPrfVelMaxCrz, f_atv.f_atv_alt_dem, Exercicio.fExeVarTempISA )

                        else:
                            # M_LOG.debug("obtem_brk:usa velocidade do breakpoint")

                            # velocidade de demanda recebe a velocidade do breakpoint convertida para IAS
                            f_atv.f_atv_vel_dem = f_brk.f_brk_vel  # calcIAS ( f_brk.f_brk_vel, f_atv.f_atv_alt_dem, Exercicio.fExeVarTempISA )

                    # senão, não tem velocidade do breakpoint
                    else:
                        # M_LOG.debug("obtem_brk:usa velocidade atual do tráfego")

                        # velocidade de demanda recebe velocidade atual do tráfego
                        f_atv.f_atv_vel_dem = f_atv.f_trf_vel_atu

                # M_LOG.debug("obtem_brk:f_atv_vel_dem:[{}]".format(f_atv.f_atv_vel_dem))

            # força cálculo do MACH
            # f_atv.vAnvISOMACH = False

        # ajustar a razão de subida ou descida da aeronave em trajetória

        # em descida ?
        if f_atv.f_trf_alt_atu > f_atv.f_atv_alt_dem:

            # M_LOG.debug("obtem_brk:em descida")

            # aeronave descendo, aplica a razão de descida em cruzeiro
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_des_crz

        # em subida ?
        elif f_atv.f_trf_alt_atu < f_atv.f_atv_alt_dem:

            # M_LOG.debug("obtem_brk:em subida")

            # aeronave subindo, aplica a razão de subida em cruzeiro
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_sub_crz

        # nivelado ?
        elif f_atv.f_trf_alt_atu == f_atv.f_atv_alt_dem:

            # M_LOG.debug("obtem_brk:nivelado")

            # aeronave estabilizada, não aplica a razão de subida ou descida
            f_atv.f_atv_raz_sub = 0.

        # M_LOG.debug("obtem_brk:f_atv_raz_sub:[{}]".format(f_atv.f_atv_raz_sub))

    # subida ?
    elif ldefs.E_SUBIDA == f_atv.en_trf_fnc_ope:

        # teste de altimetria para corrigir o caso em que a aeronave ao cumprir pontos sem o
        # valor da "altitude", ela possa manter o valor da última altitude de demanda. Com a
        # "altitude do breakpoint sem valor", forçava a aeronave a entrar na condição de vôo
        # abaixo de 10000FT, o que não é correto, pois, a mesma já cumpriu esta etapa do vôo.

        # obtém altitude do ponto atual
        lf_brk_alt = f_brk.f_brk_alt

        # extrapolou o limite da performance ?
        if f_brk.f_brk_alt > f_atv.ptr_trf_prf.f_prf_teto_sv:
            lf_brk_alt = f_atv.ptr_trf_prf.f_prf_teto_sv

        # existe altitude do ponto atual ?
        if 0 == lf_brk_alt:

            # mantém a altitude de demanda do ponto anterior
            lf_brk_alt = f_atv.f_atv_alt_dem

            # converte a velocidade de cruzeiro da performance para IAS
            lf_vel = f_atv.ptr_trf_prf.f_prf_vel_crz  # calcIAS (f_atv.ptr_trf_prf.f_prf_vel_crz, f_atv.f_atv_alt_dem, Exercicio.fExeVarTempISA )

            # altitude do ponto é menor que altitude máxima na TMA ?
            if (lf_brk_alt * cdefs.D_CNV_M2FT) < ldefs.g_AltMaxTMA:

                # velocidade de subida na DEP é maior que 250KT ?
                if f_atv.ptr_trf_prf.f_prf_vel_sub_dec > ldefs.D_VEL_MAX_TMA:

                    # houve mudança de velocidade pelo piloto ?
                    if (0 == f_atv.i_atv_change_alt_vel) or (1 == f_atv.i_atv_change_alt_vel):

                        # valida a velocidade do ponto
                        if (f_brk.f_brk_vel > 0.) and (f_brk.f_brk_vel < ldefs.D_VEL_MAX_TMA):

                            if f_brk.f_brk_vel > lf_vel:
                                # inicia campo com a velocidade da performance
                                f_atv.f_atv_vel_dem = lf_vel

                            else:
                                # inicia campo com a velocidade do ponto
                                f_atv.f_atv_vel_dem = f_brk.f_brk_vel

                        else:
                            # inicia campo com a velocidade limite 250KT ou velocidade da performance
                            if lf_vel > ldefs.D_VEL_MAX_TMA:
                                # aeronave de alta performance
                                f_atv.f_atv_vel_dem = ldefs.D_VEL_MAX_TMA

                            elif lf_vel > f_atv.f_atv_vel_dem:
                                # aeronave de baixa performance
                                f_atv.f_atv_vel_dem = lf_vel

                # senão,...
                else:
                    # houve mudança de velocidade pelo piloto ?
                    if (0 == f_atv.i_atv_change_alt_vel) or (1 == f_atv.i_atv_change_alt_vel):

                        # valida a velocidade do ponto
                        if (f_brk.f_brk_vel > 0.) and (f_brk.f_brk_vel < ldefs.D_VEL_MAX_TMA):

                            # inicia campo com a velocidade do ponto ou com a velocidade da performance
                            if f_brk.f_brk_vel > lf_vel:
                                # inicia campo com a velocidade da performance
                                f_atv.f_atv_vel_dem = lf_vel

                            else:
                                # inicia campo com a velocidade do ponto
                                f_atv.f_atv_vel_dem = f_brk.f_brk_vel

                        else:
                            # inicia campo com a velocidade limite 250KT ou velocidade da performance
                            if lf_vel > ldefs.D_VEL_MAX_TMA:
                                # aeronave de alta performance
                                f_atv.f_atv_vel_dem = ldefs.D_VEL_MAX_TMA

                            elif lf_vel > f_atv.f_atv_vel_dem:
                                # aeronave de baixa performance
                                f_atv.f_atv_vel_dem = lf_vel

            # senão, altitude do ponto é maior que a altitude máxima na TMA!
            else:
                # houve mudança de velocidade pelo piloto ?
                if (0 == f_atv.i_atv_change_alt_vel) or (1 == f_atv.i_atv_change_alt_vel):

                    # existe velocidade do ponto ?
                    if f_brk.f_brk_vel > 0.:

                        if f_brk.f_brk_vel > lf_vel:
                            # inicia com a velocidade da performance
                            f_atv.f_atv_vel_dem = lf_vel

                        else:
                            # inicia com a velocidade do ponto
                            f_atv.f_atv_vel_dem = f_brk.f_brk_vel

                    elif lf_vel > f_atv.f_atv_vel_dem:
                        # inicia com a velocidade de cruzeiro
                        f_atv.f_atv_vel_dem = lf_vel

        # obtém a razão de subida de cruzeiro
        if f_brk.i_brk_t >= 0:

            # obtém a razão de subida de cruzeiro
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_sub_crz

        # tem gradiente entre os pontos ?
        if 0. == f_brk.f_brk_raz_vel:

            # obtém a razão de subida da performance
            f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_sub_crz

        else:
            # calcula a razão de subida em função do gradiente
            f_atv.f_atv_raz_sub += f_atv.f_trf_vel_atu * f_brk.f_brk_raz_vel

    # aproximação perdida
    # elif ldefs.E_APXPERDIDA == f_atv.en_trf_fnc_ope:
        '''
        # f_atv.f_atv_vel_dem = f_atv.ptr_trf_prf.f_prf_vel_sub_dec
        # former case, fall throught to next item
        '''
    # aproximação
    # elif ldefs.E_APROXIMACAO == f_atv.en_trf_fnc_ope:
        '''
        # if f_brk.i_brk_t >= 0:
            # if f_brk.f_brk_raz_vel <= 0.:
                # f_atv.f_atv_raz_sub = f_atv.ptr_trf_prf.f_prf_raz_des_apx

            # else:
                # f_atv.f_atv_raz_sub = f_brk.f_brk_raz_vel
        '''
    # otherwise,...
    else:
        # logger
        l_log = logging.getLogger("obtem_brk::obtem_brk")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E04: erro de função.")

    # tem cooredenada temporal ?
    if f_brk.i_brk_t < 0:
        '''
        # seleciona próxima fase
        f_atv.en_atv_fase = ldefs.E_FASE_RUMOALT
        '''
        pass

    # senão,...   
    else:
        # seleciona próxima fase
        f_atv.en_atv_fase = ldefs.E_FASE_DIRPONTO

    # M_LOG.debug("obtem_brk:next fase:[{}]".format(ldefs.DCT_FASE[f_atv.en_atv_fase]))
        
    # logger
    # M_LOG.info("obtem_brk:<<")
                
# < the end >--------------------------------------------------------------------------------------
