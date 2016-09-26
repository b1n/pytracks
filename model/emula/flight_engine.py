#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
flight_engine

the flight engine class holds information about a flight and the commands the flight has been given

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
import threading
import time

# model
from .. import glb_data as gdata
from .. import glb_defs as gdefs

from ..coords import coord_defs as cdefs

from  ..emula.cine import abort_prc as abnd
from ..emula.cine import cine_data as cindata
# import model.emula.cine.cine_solo as cinsolo
from ..emula.cine import cine_voo as cinvoo
from ..emula.cine import sentido_curva as scrv

from ..newton import defs_newton as ldefs
from ..piloto import comando_piloto as cmdpil

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CFlightEngine >--------------------------------------------------------------------------

class CFlightEngine(threading.Thread):
    """
    the object holding all information concerning a flight
    """
    # ---------------------------------------------------------------------------------------------

    # contador global de loops
    # C_COUNT = 0L

    # contador global de atrasos em loops
    # C_LATE = 0L

    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_atv):
        """
        @param f_control: control manager
        @param f_atv: aeronave ativa
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input parameters
        assert f_control
        assert f_atv

        # inicia a super classe
        super(CFlightEngine, self).__init__()

        # salva o control manager localmente
        self.__control = f_control
        assert self.__control

        # obtém o event manager
        # self.__event = f_control.event
        # assert self.__event

        # obtém o relógio da simulação
        self.__sim_time = f_control.sim_time
        assert self.__sim_time

        # obtém o model manager
        self.__model = f_control.model
        assert self.__model

        # obtém o exercício
        self.__exe = self.__model.exe
        assert self.__exe

        # salva os dados da aeronave
        self.__atv = f_atv

        # context stack
        self.__stk_context = []

        # área de dados de cinemática
        self.__cine_data = cindata.CCineData()
        assert self.__cine_data

        # cria a cinemática de solo
        # self.__cine_solo = cinsolo.CineSolo(self, self._aer)
        # assert self.__cine_solo

        # cria a cinemática de vôo
        self.__cine_voo = cinvoo.CCineVoo(self, f_control)
        assert self.__cine_voo

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_pil_altitude(self, f_atv):
        """
        comando de pilotagem de altitude
        """
        # logger
        # M_LOG.info("__cmd_pil_altitude:>>")

        # check input parameters
        assert f_atv

        # obtém o comando de pilotagem atual
        l_cmd_pil = f_atv.lst_atv_cmd_pil[0]
        assert l_cmd_pil

        # M_LOG.debug("comando de pilotagem atual:[{}]".format(l_cmd_pil))

        # obtém o comando operacional
        len_cmd_ope = l_cmd_pil.en_cmd_ope

        # comando ainda não está em execução ?
        if not l_cmd_pil.v_running:
        
            # força aeronave a abandonar qualquer procedimento
            abnd.abort_prc(f_atv)
                 
            # obtém o primeiro parâmetro (altitude/nível)
            lf_param_1 = l_cmd_pil.f_param_1
            # M_LOG.debug("__comando_pilotagem:lf_param_1:[{}]".format(lf_param_1))

            # obtém o terceiro parâmetro (razão)
            lf_param_3 = l_cmd_pil.f_param_3
            # M_LOG.debug("__comando_pilotagem:lf_param_3:[{}]".format(lf_param_3))

            # obtém a altitude desejada (demanda)
            if ldefs.E_ALT == len_cmd_ope:

                # ajusta demanda
                f_atv.f_atv_alt_dem = lf_param_1 * cdefs.D_CNV_FT2M

                # razão ?
                if (lf_param_3 is not None) and (lf_param_3 != 0.):

                    # ajusta razão de subida/descida
                    f_atv.f_atv_raz_sub = lf_param_3

            # obtém a altitude desejada (demanda)
            elif ldefs.E_NIV == len_cmd_ope:

                # ajusta demanda
                f_atv.f_atv_alt_dem = lf_param_1 * 100 * cdefs.D_CNV_FT2M

                # razão ?
                if (lf_param_3 is not None) and (lf_param_3 != 0.):

                    # ajusta razão de subida/descida
                    f_atv.f_atv_raz_sub = lf_param_3

            # senão,...
            else:
                # ajusta demanda
                pass  # f_atv.f_atv_alt_dem = lf_param_1 * cdefs.D_CNV_FT2M

            # M_LOG.debug("__comando_pilotagem:atv_alt_dem:[{}/{}]".format(f_atv.f_atv_alt_dem, f_atv.f_atv_raz_sub))

            # comando em execução
            l_cmd_pil.v_running = True

        # M_LOG.debug("__comando_pilotagem:alt:[{} ==> {}]".format(f_atv.f_trf_alt_atu, f_atv.f_atv_alt_dem))

        # atingiu a altitude desejada ?
        if f_atv.f_trf_alt_atu == f_atv.f_atv_alt_dem:

            # aponta para o próximo comando
            del f_atv.lst_atv_cmd_pil[0]

        # logger
        # M_LOG.info("__cmd_pil_altitude:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_pil_curva(self, f_atv):
        """
        comando de pilotagem de curva
        """
        # logger
        # M_LOG.info("__cmd_pil_curva:>>")

        # check input parameters
        assert f_atv

        # obtém o comando de pilotagem atual
        l_cmd_pil = f_atv.lst_atv_cmd_pil[0]
        assert l_cmd_pil

        # M_LOG.debug("comando de pilotagem atual:[{}]".format(l_cmd_pil))

        # obtém o comando operacional
        len_cmd_ope = l_cmd_pil.en_cmd_ope

        # comando ainda não está em execução ?
        if not l_cmd_pil.v_running:
        
            # força aeronave a abandonar qualquer procedimento
            abnd.abort_prc(f_atv)
                 
            # obtém o primeiro parâmetro (graus)
            lf_param_1 = l_cmd_pil.f_param_1
            # M_LOG.debug("__cmd_pil_curva:lf_param_1:[{}]".format(lf_param_1))

            # obtém o segundo parâmetro (proa)
            lf_param_2 = l_cmd_pil.f_param_2
            # M_LOG.debug("__cmd_pil_curva:lf_param_2:[{}]".format(lf_param_2))

            # obtém o terceiro parâmetro (razão)
            lf_param_3 = l_cmd_pil.f_param_3
            # M_LOG.debug("__cmd_pil_curva:lf_param_3:[{}]".format(lf_param_3))

            # coloca a aeronave em manual
            f_atv.en_trf_fnc_ope = ldefs.E_MANUAL

            # curva a direita ?
            if ldefs.E_CDIR == len_cmd_ope:

                # graus ?
                if lf_param_1 is not None:

                    # obtém a proa desejada (demanda)
                    f_atv.f_atv_pro_dem = (360. + f_atv.f_trf_pro_atu + lf_param_1) % 360.

                # proa ?
                elif lf_param_2 is not None:

                    # obtém a proa desejada (demanda)
                    f_atv.f_atv_pro_dem = lf_param_2 % 360.
                
                # senão, curva indefinida... !!!REVER!!!
                else:
                    # proa negativa
                    f_atv.f_atv_pro_dem *= -1

                # razão ?
                if lf_param_3 is not None:

                    # curva direita (razão positiva)
                    f_atv.f_atv_raz_crv = abs(lf_param_3)

                else:
                    # curva direita (razão positiva)
                    f_atv.f_atv_raz_crv = abs(f_atv.f_atv_raz_crv)
                        
            # curva a esquerda ?
            elif ldefs.E_CESQ == len_cmd_ope:

                # graus ?
                if lf_param_1 is not None:

                    # obtém a proa desejada (demanda)
                    f_atv.f_atv_pro_dem = (360. + f_atv.f_trf_pro_atu - lf_param_1) % 360.

                # proa ?
                elif lf_param_2 is not None:

                    # obtém a proa desejada (demanda)
                    f_atv.f_atv_pro_dem = lf_param_2 % 360.
                
                # senão, curva indefinida...  !!!REVER!!!
                else:
                    # proa negativa
                    f_atv.f_atv_pro_dem *= -1

                # razão ?
                if lf_param_3 is not None:

                    # curva esquerda (razão negativa)
                    f_atv.f_atv_raz_crv = -abs(lf_param_3)

                else:
                    # curva esquerda (razão negativa)
                    f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)
                        
            # curva pelo menor ângulo ?
            elif ldefs.E_CMNR == len_cmd_ope:

                # obtém a proa desejada (demanda)
                f_atv.f_atv_pro_dem = lf_param_2

                # força a curva pelo menor ângulo
                scrv.sentido_curva(f_atv)

            # proa ?
            elif ldefs.E_PROA == len_cmd_ope:

                # obtém a proa desejada (demanda)
                f_atv.f_atv_pro_dem = lf_param_2

                # força a curva pelo menor ângulo
                scrv.sentido_curva(f_atv)

            # M_LOG.debug("__cmd_pil_curva:atv_pro_dem:[{}]".format(f_atv.f_atv_pro_dem))

            # comando em execução
            l_cmd_pil.v_running = True

        # M_LOG.debug("__cmd_pil_curva:proa:[{} ==> {}]".format(f_atv.f_trf_pro_atu, f_atv.f_atv_pro_dem))

        # atingiu a proa desejada ?
        if f_atv.f_trf_pro_atu == f_atv.f_atv_pro_dem:

            # aponta para o próximo comando
            del f_atv.lst_atv_cmd_pil[0]

        # logger
        # M_LOG.info("__cmd_pil_curva:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_pil_decolagem(self, f_atv):
        """
        comando de pilotagem de decolagem
        """
        # logger
        # M_LOG.info("__cmd_pil_decolagem:>>")

        # check input parameters
        assert f_atv

        # obtém o comando de pilotagem atual
        l_cmd_pil = f_atv.lst_atv_cmd_pil[0]
        assert l_cmd_pil

        # M_LOG.debug("comando de pilotagem atual:[{}]".format(l_cmd_pil))

        # obtém o primeiro parâmetro (aeródromo)
        lf_aer = l_cmd_pil.f_param_1
        M_LOG.debug("__cmd_pil_decolagem:lf_aer:[{}]".format(lf_aer))

        # obtém o segundo parâmetro (pista)
        lf_pst = l_cmd_pil.f_param_2
        M_LOG.debug("__cmd_pil_decolagem:lf_pst:[{}]".format(lf_pst))

        # aeródromo e pista da decolagem
        f_atv.ptr_atv_aer, f_atv.ptr_atv_pst = self.__model.airspace.get_aer_pst(lf_aer, lf_pst)

        # função operacional
        f_atv.en_trf_fnc_ope = ldefs.E_DECOLAGEM
        
        # fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

        # aponta para o próximo comando
        del f_atv.lst_atv_cmd_pil[0]

        # logger
        # M_LOG.info("__cmd_pil_decolagem:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_pil_dir_fixo(self, f_atv):
        """
        comando de pilotagem de dir_fixo
        """
        # logger
        # M_LOG.info("__cmd_pil_dir_fixo:>>")

        # check input parameters
        assert f_atv

        # verifica condições para execução (I)
        assert self.__cine_data

        # obtém o comando de pilotagem atual
        l_cmd_pil = f_atv.lst_atv_cmd_pil[0]
        assert l_cmd_pil

        M_LOG.debug("comando de pilotagem atual:[{}]".format(l_cmd_pil))

        # obtém o dicionário de fixos
        ldct_fix = self.__cine_voo.dct_fix
        assert ldct_fix is not None

        # obtém fixo a bloquear
        f_atv.ptr_atv_fix_prc = ldct_fix.get(l_cmd_pil.f_param_1, None)
        M_LOG.debug("__cmd_pil_dir_fixo:ptr_atv_fix_prc:[{}/{}]".format(f_atv.ptr_atv_fix_prc.i_fix_id, f_atv.ptr_atv_fix_prc.s_fix_desc))

        # status da interceptação ao fixo
        self.__cine_data.v_interceptou_fixo = False

        # função operacional
        f_atv.en_trf_fnc_ope = ldefs.E_DIRFIXO

        # fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

        # aponta para o próximo comando
        del f_atv.lst_atv_cmd_pil[0]

        # logger
        # M_LOG.info("__cmd_pil_dir_fixo:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_pil_espera(self, f_atv):
        """
        comando de pilotagem de espera
        """
        # logger
        # M_LOG.info("__cmd_pil_espera:>>")

        # check input parameters
        assert f_atv

        # verifica condições para execução (I)
        assert self.__model

        # obtém o comando de pilotagem atual
        l_cmd_pil = f_atv.lst_atv_cmd_pil[0]
        assert l_cmd_pil

        # M_LOG.debug("comando de pilotagem atual:[{}]".format(l_cmd_pil))

        # obtém o primeiro parâmetro (número da espera)
        lf_param_1 = int(l_cmd_pil.f_param_1)
        # M_LOG.debug("__comando_pilotagem:lf_param_1:[{}]".format(lf_param_1))

        # procedimento e função operacional
        f_atv.ptr_trf_prc, f_atv.en_trf_fnc_ope = self.__model.airspace.get_ptr_prc("ESP{:03d}".format(lf_param_1))
        # M_LOG.debug("ptr_trf_prc...: " + str("ESP{:03d}".format(lf_param_1)))
        # M_LOG.debug("en_trf_fnc_ope: " + str(f_atv.en_trf_fnc_ope))

        # fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

        # aponta para o próximo comando
        del f_atv.lst_atv_cmd_pil[0]

        # logger
        # M_LOG.info("__cmd_pil_espera:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_pil_pouso(self, f_atv):
        """
        comando de pilotagem de pouso
        """
        # logger
        # M_LOG.info("__cmd_pil_pouso:>>")

        # check input parameters
        assert f_atv

        # verifica condições para execução (I)
        assert self.__model

        # obtém o comando de pilotagem atual
        l_cmd_pil = f_atv.lst_atv_cmd_pil[0]
        assert l_cmd_pil

        # M_LOG.debug("comando de pilotagem atual:[{}]".format(l_cmd_pil))

        # obtém o primeiro parâmetro (aeródromo)
        lf_aer = l_cmd_pil.f_param_1
        M_LOG.debug("__comando_pilotagem:lf_aer:[{}]".format(lf_aer))

        # obtém o segundo parâmetro (pista)
        lf_pst = l_cmd_pil.f_param_2
        M_LOG.debug("__comando_pilotagem:lf_pst:[{}]".format(lf_pst))

        # aeródromo e pista do pouso
        f_atv.ptr_atv_aer, f_atv.ptr_atv_pst = self.__model.airspace.get_aer_pst(lf_aer, lf_pst)

        # função operacional
        f_atv.en_trf_fnc_ope = ldefs.E_POUSO
        
        # fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

        # aponta para o próximo comando
        del f_atv.lst_atv_cmd_pil[0]

        # logger
        # M_LOG.info("__cmd_pil_pouso:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_pil_trajetoria(self, f_atv):
        """
        comando de pilotagem de trajetória
        """
        # logger
        # M_LOG.info("__cmd_pil_trajetoria:>>")

        # check input parameters
        assert f_atv

        # verifica condições para execução (I)
        assert self.__model

        # obtém o comando de pilotagem atual
        l_cmd_pil = f_atv.lst_atv_cmd_pil[0]
        assert l_cmd_pil

        # M_LOG.debug("comando de pilotagem atual:[{}]".format(l_cmd_pil))

        # obtém o primeiro parâmetro (número da trajetória)
        lf_param_1 = int(l_cmd_pil.f_param_1)
        # M_LOG.debug("__comando_pilotagem:lf_param_1:[{}]".format(lf_param_1))

        # procedimento e função operacional
        f_atv.ptr_trf_prc, f_atv.en_trf_fnc_ope = self.__model.airspace.get_ptr_prc("TRJ{:03d}".format(lf_param_1))
        # M_LOG.debug("ptr_trf_prc...: " + str("TRJ{:03d}".format(lf_param_1)))
        # M_LOG.debug("en_trf_fnc_ope: " + str(f_atv.en_trf_fnc_ope))

        # fase de verificar condições
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

        # aponta para o próximo comando
        del f_atv.lst_atv_cmd_pil[0]

        # logger
        # M_LOG.info("__cmd_pil_trajetoria:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_pil_velocidade(self, f_atv):
        """
        comando de pilotagem de velocidade
        """
        # logger
        # M_LOG.info("__cmd_pil_velocidade:>>")

        # check input parameters
        assert f_atv

        # verifica condições para execução (I)
        # assert self.__exe
        # assert self.__exe.v_exe_ok

        # obtém o comando de pilotagem atual
        l_cmd_pil = f_atv.lst_atv_cmd_pil[0]
        assert l_cmd_pil

        # M_LOG.debug("comando de pilotagem atual:[{}]".format(l_cmd_pil))

        # obtém o comando operacional
        len_cmd_ope = l_cmd_pil.en_cmd_ope

        # comando ainda não está em execução ?
        if not l_cmd_pil.v_running:
        
            # força aeronave a abandonar qualquer procedimento
            abnd.abort_prc(f_atv)
                 
            # obtém o primeiro parâmetro (graus)
            lf_param_1 = l_cmd_pil.f_param_1
            M_LOG.debug("__cmd_pil_velocidade:lf_param_1:[{}]".format(lf_param_1))

            # velocidade IAS ?
            if ldefs.E_IAS == len_cmd_ope:

                # obtém a velocidade desejada (demanda)
                f_atv.f_atv_vel_dem = lf_param_1 * cdefs.D_CNV_KT2MS
                M_LOG.debug("__cmd_pil_velocidade:f_atv.f_atv_vel_dem:[{}]".format(f_atv.f_atv_vel_dem))

            # velocidade MACH ?
            elif ldefs.E_MACH == len_cmd_ope:

                # if f_atv.f_trf_alt_atu >= self.__exe.f_exe_niv_apr_mac:

                    # obtém a velocidade desejada (demanda)
                    # f_atv.f_trf_vel_mac_dem = lf_param_1

                    # f_atv.f_atv_vel_dem = calcIASDemanda(f_atv.f_trf_vel_mac_dem,
                    #                                      f_atv.f_atv_alt_dem,
                    #                                      self.__exe.f_exe_var_temp_isa)

                pass

            # comando em execução
            l_cmd_pil.v_running = True

        M_LOG.debug("__cmd_pil_velocidade:f_atv.f_trf_vel_atu:[{}]".format(f_atv.f_trf_vel_atu))

        # velocidade IAS ?
        if ldefs.E_IAS == len_cmd_ope:

            # atingiu a velocidade desejada ?
            if f_atv.f_trf_vel_atu == f_atv.f_atv_vel_dem:

                # aponta para o próximo comando
                del f_atv.lst_atv_cmd_pil[0]

        # velocidade MACH ?
        elif ldefs.E_MACH == len_cmd_ope:

            # atingiu a velocidade desejada ?
            if f_atv.f_trf_vel_mac_atu == f_atv.f_trf_vel_mac_dem:

                # aponta para o próximo comando
                del f_atv.lst_atv_cmd_pil[0]

        # logger
        # M_LOG.info("__cmd_pil_velocidade:<<")

    # ---------------------------------------------------------------------------------------------

    def __comando_pilotagem(self, f_atv):
        """
        checa se a aeronave segue vários comandos de pilotagem
        """
        # logger
        # M_LOG.info("__comando_pilotagem:>>")

        # check input parameters
        assert f_atv

        # verifica condições para execução (I)
        assert self.__cine_data

        # verifica condições para execução (II)
        if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):

            # logger
            # M_LOG.info(u"__comando_pilotagem:<E01: aeronave não ativa.")

            # cai fora...
            return

        # (f_atv.en_trf_fnc_ope in [ldefs.E_NOPROC, ldefs.E_MANUAL, ldefs.E_DIRFIXO]):

        # inicializa campos referentes a procedimentos
        # f_atv.ptr_trf_bkp = None
        # f_atv.ptr_trf_prc = None

        # esvazia pilha de contexto
        self.__cine_data.i_cin_ptr = 0

        # obtém o comando de pilotagem atual
        l_cmd_pil = f_atv.lst_atv_cmd_pil[0]
        assert l_cmd_pil

        # M_LOG.debug("comando de pilotagem atual:[{}]".format(l_cmd_pil))

        # obtém o comando operacional
        len_cmd_ope = l_cmd_pil.en_cmd_ope

        # curva ou proa ?
        if len_cmd_ope in [ldefs.E_CDIR, ldefs.E_CESQ, ldefs.E_CMNR, ldefs.E_PROA]:

            # trata comando de curva ou proa
            self.__cmd_pil_curva(f_atv)

        # velocidade ou mach ?
        elif len_cmd_ope in [ldefs.E_IAS, ldefs.E_MACH]:

            # trata comando de velocidade
            self.__cmd_pil_velocidade(f_atv)

        # altitude ou nível ?
        elif len_cmd_ope in [ldefs.E_ALT, ldefs.E_DES, ldefs.E_NIV, ldefs.E_SUB]:

            # trata comando de altitude
            self.__cmd_pil_altitude(f_atv)

        # decolagem ?
        elif ldefs.E_DECOLAGEM == len_cmd_ope:

            # trata comando de decolagem
            self.__cmd_pil_decolagem(f_atv)

        # direcionamento a fixo ?
        elif ldefs.E_DIRFIXO == len_cmd_ope:

            # trata comando de direcionamento a fixo
            self.__cmd_pil_dir_fixo(f_atv)

        # espera ?
        elif ldefs.E_ESPERA == len_cmd_ope:

            # trata comando de espera
            self.__cmd_pil_espera(f_atv)

        # põem em movimento ?
        #elif ldefs.E_MOV == len_cmd_ope:

            # inicia movimentação
            #f_atv.v_atv_movi = lf_param

            # aponta para o próximo comando
            # del f_atv.lst_atv_cmd_pil[0]

        # pouso ?
        elif ldefs.E_POUSO == len_cmd_ope:

            # trata comando de pouso
            self.__cmd_pil_pouso(f_atv)

        # transponder ?
        #elif ldefs.E_SSR == len_cmd_ope:

            # inicializa campo código transponder
            #f_atv.i_trf_issr = lf_param

            # aponta para o próximo comando
            # del f_atv.lst_atv_cmd_pil[0]

        # trajetória ?
        elif ldefs.E_TRAJETORIA == len_cmd_ope:

            # trata comando de trajetória
            self.__cmd_pil_trajetoria(f_atv)

        # visualiza ?
        #elif ldefs.E_VISU == len_cmd_ope:

            # inicia visualização
            #f_atv.v_trf_visu = lf_param

            # aponta para o próximo comando
            # del f_atv.lst_atv_cmd_pil[0]

        # manual ?
        # elif ldefs.E_MANUAL == len_cmd_ope:

            # estabelece fim de comandos de pilotagem
            # pass  # f_atv.lst_atv_cmd_pil = []

        # otherwise,...
        else:
            # inicia função operacional
            f_atv.en_trf_fnc_ope = len_cmd_ope

        # logger
        # M_LOG.info("__comando_pilotagem:<<")

    # ---------------------------------------------------------------------------------------------

    def instruction(self, fs_cmd):
        """
        faz o parse da mensagem de pilotagem recebida

        @param fs_cmd: mensagem
        """
        # logger
        # M_LOG.info("instruction:>>")

        # check input parameters
        assert fs_cmd

        # verifica condições para execução
        assert self.__atv

        # coloca o comando na lista do tráfego
        self.__atv.lst_atv_cmd_pil.append(cmdpil.CComandoPil(fs_cmd))
        # M_LOG.debug("instruction:lst_atv_cmd_pil:[{}]".format(self.__atv.lst_atv_cmd_pil))

        # logger
        # M_LOG.info("instruction:<<")

    # ---------------------------------------------------------------------------------------------

    def __move_no_solo(self, f_atv):
        """
        move uma aeronave no solo
        """
        # logger
        # M_LOG.info("__move_no_solo:>>")

        # check input parameters
        assert f_atv

        # verifica condições para execução
        if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):

            # logger
            # M_LOG.info(u"__move_no_solo:<E01: aeronave não ativa.")

            # cai fora...
            return

        # muda a função operacional para decolagem
        f_atv.en_trf_fnc_ope = ldefs.E_DECOLAGEM

        # fase de preparação
        f_atv.en_atv_fase = ldefs.E_FASE_ZERO

        # logger
        # M_LOG.info("__move_no_solo:<<")

    # ---------------------------------------------------------------------------------------------

    def __procedimentos(self, f_atv):
        """
        verificar e direcionar a aeronave a um procedimento
        """
        # logger
        # M_LOG.info("__procedimentos:>>")

        # check input parameters
        assert f_atv

        # verifica condições para execução (I)
        assert self.__cine_data
        assert self.__cine_voo

        # M_LOG.debug("__procedimentos:en_trf_fnc_ope:[{}]".format(ldefs.DCT_FNC_OPE[f_atv.en_trf_fnc_ope]))

        # verifica condições para execução (II)
        if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):

            # logger
            # M_LOG.info(u"__procedimentos:<E01: aeronave não ativa.")

            # cai fora...
            return

        # função operacional é aproximação ?
        if ldefs.E_APROXIMACAO == f_atv.en_trf_fnc_ope:

            # aproximação
            self.__cine_voo.prc_aproximacao()

        # função operacional é aproximação perdida ?
        elif ldefs.E_APXPERDIDA == f_atv.en_trf_fnc_ope:

            # aproximação perdida
            self.__cine_voo.prc_apx_perdida()

        # X - arremeter em emergência ?
        # Y - "toque e arremetida" ?
        # Z - arremeter para a perna do vento ?
        # elif f_atv.c_atv_status_voo in ['X', 'Y', 'Z']:

            # procedimento de arremetida
            # self.__cine_voo.prc_arremeter ()

        # K - circuito, entrada pela perna do contra vento ?
        # V - circuito, entrada pela perna do vento ?
        # elif f_atv.c_atv_status_voo in ['K', 'V']:

            # procedimento de circuito
            # self.__cine_voo.prc_circuito ()

        # função operacional é decolagem ?
        elif ldefs.E_DECOLAGEM == f_atv.en_trf_fnc_ope:

            # decolagem
            self.__cine_voo.prc_decolagem()

        # função operacional é direcionamento a fixo ?
        elif ldefs.E_DIRFIXO == f_atv.en_trf_fnc_ope:

            # direcionamento a fixo
            self.__cine_voo.prc_dir_fixo()

        # função operacional é espera ?
        elif ldefs.E_ESPERA == f_atv.en_trf_fnc_ope:

            # espera
            self.__cine_voo.prc_espera()

        # função operacional é ILS ?
        elif ldefs.E_ILS == f_atv.en_trf_fnc_ope:

            # ILS
            pass  # self.__cine_voo.prc_ils()

        # função operacional é interceptação de radial ?
        elif ldefs.E_INTRADIAL == f_atv.en_trf_fnc_ope:

            # interceptação de radial
            pass  # self.__cine_voo.int_radial()

        # função operacional é manual ?
        elif ldefs.E_MANUAL == f_atv.en_trf_fnc_ope:

            # obtém o sentido de curva atual
            li_sinal = 1 if f_atv.f_atv_raz_crv >= 0 else -1

            # verifica qual deve ser a razão de curva (limite de 14000 pés)
            f_atv.f_atv_raz_crv = 1.5 if f_atv.f_trf_z > 4267.2 else 3.

            # ajusta o sentido de curva
            f_atv.f_atv_raz_crv *= li_sinal

        # O - peel-off ?
        # elif 'O' == f_atv.c_atv_status_voo:

            # procedimento de peel-off
            # self.__cine_voo.prc_peel_off ()

        # função operacional é pouso ?
        elif ldefs.E_POUSO == f_atv.en_trf_fnc_ope:

            # pouso
            self.__cine_voo.prc_pouso()

        # D - pouso direto ?
        # P - pousa movendo-se no circuito ?
        # elif f_atv.c_atv_status_voo in ['A', 'D', 'P']:

            # procedimento de pouso
            # self.__cine_voo.prc_pouso()

        # função operacional é subida ?
        elif ldefs.E_SUBIDA == f_atv.en_trf_fnc_ope:

            # subida
            self.__cine_voo.prc_subida()

        # função operacional é trajetória ?
        elif ldefs.E_TRAJETORIA == f_atv.en_trf_fnc_ope:

            # trajetória
            self.__cine_voo.prc_trajetoria()

        # senão, função operacional desconhecida
        else:
            # logger
            l_log = logging.getLogger("CFlightEngine::__procedimentos")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E02: função operacional {} desconhecida".format(ldefs.DCT_FNC_OPE[f_atv.en_trf_fnc_ope]))

        # logger
        # M_LOG.info("__procedimentos:<<")

    # ---------------------------------------------------------------------------------------------

    def run(self):
        """
        updates the position of all flights in the flight list
        """
        # logger
        # M_LOG.info("run:>>")

        # verifica condições para execução
        assert self.__atv
        # assert self.__cine_solo
        assert self.__cine_voo

        # tempo de espera
        lf_tim_wait = self.__control.config.dct_config["tim.wait"]

        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:

            # aguarda 1 seg
            time.sleep(1.)

        # timestamp of the last turn
        self.__atv.l_atv_time_ant = self.__sim_time.obtem_hora_sim()
        # M_LOG.debug("l_atv_time_ant:[{}]".format(self.__atv.l_atv_time_ant))

        # inicia o timer
        lf_call_time = time.time()
                
        # loop de vida da aeronave
        while gdata.G_KEEP_RUN and self.__atv.v_atv_ok and (ldefs.E_ATIVA == self.__atv.en_trf_est_atv):

            # incrementa o contador global de loops
            # CFlightEngine.C_COUNT += 1

            # aeronave em movimento ?
            if 1:  # self.__atv.v_atv_movi:

                if self.__atv.ptr_trf_prc is not None:
                    M_LOG.debug("run:en_trf_fnc_ope.:[{}/{}/{}]".format(self.__atv.s_trf_ind, ldefs.DCT_FNC_OPE[self.__atv.en_trf_fnc_ope], self.__atv.ptr_trf_prc.i_prc_id))

                else:
                    M_LOG.debug("run:en_trf_fnc_ope.:[{}/{}]".format(self.__atv.s_trf_ind, ldefs.DCT_FNC_OPE[self.__atv.en_trf_fnc_ope]))

                M_LOG.debug("run:lst_atv_cmd_pil:[{}]".format(self.__atv.lst_atv_cmd_pil))

                # existem comandos de pilotagem ?
                if len(self.__atv.lst_atv_cmd_pil) > 0:

                    # executa os comandos de pilotagem
                    self.__comando_pilotagem(self.__atv)

                # a aeronave está no solo ?
                # if self.__atv.v_atv_solo:

                    # movimenta no solo
                    # self.__move_no_solo()

                # atualiza dados dinâmicos da aeronave
                self.__cine_voo.update_cinematica()

                # M_LOG.debug("run:en_trf_fnc_ope(2):[{}]".format(ldefs.DCT_FNC_OPE[self.__atv.en_trf_fnc_ope]))

                # tem procedimento ?
                if ldefs.E_NOPROC != self.__atv.en_trf_fnc_ope:

                    # verifica qual o procedimento da aeronave
                    self.__procedimentos(self.__atv)

            # recálculo da posição (.75s)
            lf_call_time += lf_tim_wait
                        
            # obtém o tempo atual em segundos
            lf_now = time.time()

            # está adiantado ?
            if lf_call_time >= lf_now:

                # permite o scheduler
                time.sleep(lf_call_time - lf_now)

            # senão, está atrasado
            else:
                # logger
                l_log = logging.getLogger("CFlightEngine::run")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E01: atraso de {}(s).".format(lf_now - lf_call_time))

                # incrementa o contador global de atrasos
                # CFlightEngine.C_LATE += 1

                # calcula o percentual de erro
                # lf_erro = (float(CFlightEngine.C_LATE) / float(CFlightEngine.C_COUNT)) * 100.
                # M_LOG.error(">>>>>>>>>>>> ERRO GLOBAL {}/{} = {} !!!!!!!! <<<<<<<<<<<<<<<<<<".format(CFlightEngine.C_LATE, CFlightEngine.C_COUNT, lf_erro))

                # reinicia o timer
                lf_call_time = time.time()

        # logger
        # M_LOG.info("run:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def atv(self):
        """
        get pointer para a aeronave ativa
        """
        return self.__atv

    # ---------------------------------------------------------------------------------------------

    @property
    def cine_data(self):
        """
        get pointer para área de dados da cinemática
        """
        return self.__cine_data

    # ---------------------------------------------------------------------------------------------

    @property
    def cine_solo(self):
        """
        get cinemática de solo
        """
        return self.__cine_solo

    # ---------------------------------------------------------------------------------------------

    @property
    def cine_voo(self):
        """
        get cinemática de vôo
        """
        return self.__cine_voo

    # ---------------------------------------------------------------------------------------------

    @property
    def stk_context(self):
        """
        get context stack
        """
        return self.__stk_context

# < the end >--------------------------------------------------------------------------------------
