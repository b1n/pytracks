#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
emula_newton

the actual flight emulator

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import Queue
import threading
import time

# model
from .. import glb_data as gdata
from .. import glb_defs as gdefs

from ..emula import emula_model as model
from ..emula import flight_engine as engine
from ..emula.cine import cine_calc as cincalc

from ..items import atv_new as atv
from ..items import trf_new as trf

from ..newton import defs_newton as ldefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CEmulaNewton >---------------------------------------------------------------------------

class CEmulaNewton(model.CEmulaModel):
    """
    the flight model class generates new flights and handles their movement.  It has a list of
    flight objects holding all flights that are currently active.  The flights are generated
    when activation time comes, or if already activated in build exercise fase.  Once a flight
    has been generated it is handled by the flight engine
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_control):
        """
        @param f_model: model manager
        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")
                
        # verifica parâmetros de entrada
        assert f_control
        assert f_model

        # inicia a super classe
        super(CEmulaNewton, self).__init__(f_model, f_control)

        # herdados de CEmulaModel
        # self.config        # config manager
        # self.dct_config    # configuration dictionary
        # self.control       # control manager
        # self.event         # event manager
        # self.dct_flight    # dictionary of active flights
        # self.model         # model manager

        # obtém o MPI Comm World
        self.__mpi_comm = f_control.mpi_comm
        assert self.__mpi_comm

        # obtém o MPI rank
        self.__mpi_rank = f_control.mpi_rank
        assert self.__mpi_rank > -1

        # obtém o MPI size
        self.__mpi_size = f_control.mpi_size
        assert self.__mpi_size > -1

        # obtém o sender de ccc
        self.__sck_snd_cnfg = f_control.sck_snd_cnfg
        assert self.__sck_snd_cnfg

        # obtém a queue de ccc
        self.__q_snd_cnfg = f_control.q_snd_cnfg
        assert self.__q_snd_cnfg

        # obtém o receiver de comandos de pilotagem
        self.__sck_rcv_cpil = f_control.sck_rcv_cpil
        assert self.__sck_rcv_cpil

        # obtém o queue de comandos de pilotagem
        self.__q_rcv_cpil = f_control.q_rcv_cpil
        assert self.__q_rcv_cpil

        # obtém o relógio da simulação
        self.__sim_time = f_control.sim_time
        assert self.__sim_time

        # obtém o exercício
        self.__exe = f_model.exe
        assert self.__exe
 
        # monta as informações do servidor
        self.__s_srv_addr = str(gdefs.D_MSG_VRS) + gdefs.D_MSG_SEP + \
                            str(gdefs.D_MSG_SRV) + gdefs.D_MSG_SEP + \
                            "{}:{}".format(self.dct_config["srv.addr"], self.dct_config["srv.port"])
        assert self.__s_srv_addr

        # cria a trava da lista de vôos
        # gdata.G_LCK_FLIGHT = threading.Lock()
        # assert gdata.G_LCK_FLIGHT  

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __ativa_trf(self, f_trf):
        """
        ativa os tráfegos
        """
        # logger
        # M_LOG.info("__ativa_trf:>>")
                
        # verifica parâmetros de entrada
        assert f_trf

        # verifica condições de execução
        assert self.control

        # cria uma nova aeronave ativa a partir de um tráfego
        l_atv = atv.CAtvNEW(self.control.model, f_trf)
        assert l_atv

        # cria o flight engine para a aeronave ativa
        l_atv.atv_fe = engine.CFlightEngine(self.control, l_atv)
        assert l_atv.atv_fe

        # coloca em modo deamon
        l_atv.atv_fe.daemon = True

        # põem a aeronave pra voar
        l_atv.atv_fe.start()

        # marca a aeronave como processada
        # f_trf.setProcessed()

        # logger
        # M_LOG.info("__ativa_trf:<<")

        # retorna a aeronave ativa
        return l_atv

    # ---------------------------------------------------------------------------------------------

    def __check_time_in(self, f_trf):
        """
        checa se já deu o tempo de ativação de uma aeronave do exercício

        @param f_trf: aeronave a verificar o tempo de ativação
        """
        # logger
        # M_LOG.info("__check_time_in:>>")
                
        # verifica parâmetros de entrada
        assert f_trf

        # verifica condições de execução
        assert self.__sim_time

        # obtém a hora da simulação
        lb_h, lb_m, lb_s, _ = self.__sim_time.obtem_hora()

        # calcula o tempo da simulação
        li_sim = (((lb_h * 60) + lb_m) * 60) + lb_s

        # obtém a hora de ativação da aeronave
        lt_hatv = f_trf.t_trf_hor_atv

        # calcula o tempo da ativação
        li_atv = (((lt_hatv[0] * 60) + lt_hatv[1]) * 60) + lt_hatv[2]

        # logger
        # M_LOG.info("__check_time_in:<<")
                
        # retorna se já deu o tempo de entrada
        return li_atv <= li_sim

    # ---------------------------------------------------------------------------------------------

    def __parse_msg_pil(self, fs_msg):
        """
        faz o parse da mensagem de pilotagem recebida

        @param fs_msg: mensagem
        """
        # logger
        # M_LOG.info("__parse_msg_pil:>>")
                
        # verifica parâmetros de entrada
        assert fs_msg

        # obtém o indicativo do tráfego (callsign)
        llst_tok = fs_msg.split(':')
        M_LOG.debug("llst_tok: " + str(llst_tok))
        
        # obtém a aeronave ativa
        l_atv = self.dct_flight.get(llst_tok[0])        
        M_LOG.debug("l_atv:[{}]".format(l_atv))

        if l_atv is None:

            # logger
            l_log = logging.getLogger("CEmulaNewton::__parse_msg_pil")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E01: tráfego {} não existe.".format(llst_tok[0]))

            # logger
            # M_LOG.info("__parse_msg_pil:<E01: callsign não existe.")
                    
            # return
            return

        # obtém o flight engine da aeronave
        l_fe = l_atv.atv_fe
        M_LOG.debug("l_fe:[{}]".format(l_fe))

        if l_fe is None:

            # logger
            l_log = logging.getLogger("CEmulaNewton::__parse_msg_pil")
            l_log.setLevel(logging.ERROR)
            l_log.error(u"<E02: flight engine de {} não existe.".format(llst_tok[0]))

            # logger
            # M_LOG.info("__parse_msg_pil:<E02: flight engine não existe.")
                    
            # return
            return

        # envia o comando a aeronave
        l_fe.instruction(llst_tok[1].strip().upper())

        # logger
        # M_LOG.info("__parse_msg_pil:<<")

    # ---------------------------------------------------------------------------------------------

    def run(self):
        """
        checks whether it's time to created another flight
        """
        # logger
        # M_LOG.info("run:>>")
                
        # verifica condições de execução
        assert self.__exe

        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:

            # aguarda 1 seg
            time.sleep(1.)

        # round robin
        lf_tim_rrbn = float(self.dct_config["tim.rrbn"])

        # init check if any new flights should be generated this iteration
        l_timer_thread_ativ = threading.Thread(target=self.__run_check_ativ)
        assert l_timer_thread_ativ

        l_timer_thread_ativ.daemon = True
        l_timer_thread_ativ.start()

        # master node ?
        if 0 == self.__mpi_rank:

            # inicia envio dos dados de configuração
            l_timer_thread_cnfg = threading.Thread(target=self.__run_check_cnfg)
            assert l_timer_thread_cnfg
            
            l_timer_thread_cnfg.daemon = True
            l_timer_thread_cnfg.start()

        # master node: hora de enviar a hora ?
        if 0 == self.__mpi_rank:

            # inicia envio dos dados do servidor e de hora
            l_timer_thread_hora = threading.Thread(target=self.__run_check_hora)
            assert l_timer_thread_hora
            
            l_timer_thread_hora.daemon = True
            l_timer_thread_hora.start()

        # inicia check de colisão
        # l_timer_thread_prox = threading.Thread(target=self.__run_check_prox)
        # assert l_timer_thread_prox
        
        # l_timer_thread_prox.daemon = True
        # l_timer_thread_prox.start()

        # inicia o recebimento de mensagens de pilotagem
        self.__sck_rcv_cpil.start()

        # inicia o timer
        lf_call_time = time.time()

        # loop de execução do simulador
        while gdata.G_KEEP_RUN:

            # exercício está congelado ?
            if 0:  # self.__exe.v_exe_congelado:

                # chegou a hora de início do exercício ?
                if 1:  # self._pSIMU.vAsmTempoPre and (self.__exe.i_exe_hora_ini == self.__exe.i_exe_hora_atu):

                    # descongela o exercício
                    # self.__exe.v_exe_congelado = False

                    # não está mais em tempo de pré-ativação
                    # self._pSIMU.v_asm_tempo_pre = False
                    pass
                    
                # permite o scheduler
                time.sleep(.1)

                # faz o loop
                continue

            try: 
                # obtém um item da queue de pilotagem (nowait)
                llst_data = self.__q_rcv_cpil.get(False)

                # queue tem dados ?
                if llst_data:
                                                            
                    # mensagem de pilotagem ?
                    if gdefs.D_MSG_PIL == int(llst_data[0]):

                        # faz o parser do comando de pilotagem recebido
                        self.__parse_msg_pil(llst_data[1])

            # em caso de não haver mensagens...
            except Queue.Empty, ls_err:

                # não faz nada...
                pass
                                
            # obtém o tempo atual em segundos
            lf_now = time.time()
                                    
            # round robin (.1s)
            lf_call_time += lf_tim_rrbn

            # está adiantado ?
            if lf_call_time >= lf_now:
                                                                                                        
                # agenda a próxima execução
                time.sleep(lf_call_time - lf_now)

            # senão, atrasou...
            else:
                # logger
                l_log = logging.getLogger("CEmulaNewton::run")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E01: atraso de {}(s).".format(lf_now - lf_call_time))

                # reinicia o timer
                lf_call_time = time.time()

        # logger
        # M_LOG.info("run:<<")
                
    # ---------------------------------------------------------------------------------------------

    def __run_check_ativ(self):
        """
        checks whether it's time to created another flight
        """
        # logger
        # M_LOG.info("__run_check_ativ:>>")
                
        # verifica condições de execução
        assert self.__exe

        # inicia o timer de check de ativação (30s)
        lf_call_time = time.time()

        # loop de execução do check
        while gdata.G_KEEP_RUN:

            # percorre os tráfegos do exercício
            for l_key, l_trf in self.__exe.dct_exe_trf.items():

                # verifica aeronave
                assert isinstance(l_trf, trf.CTrfNEW)

                # processa esta aeronave ?
                if self.__mpi_rank == l_trf.i_trf_id % self.__mpi_size:

                    # tráfego não está pendente ?
                    # if ldefs.E_PENDENTE != l_trf.en_trf_est_atv:

                        # próximo tráfego
                        # continue

                    # deu o tempo para a ativação ?
                    if self.__check_time_in(l_trf):

                        # checa estado operacional da aeronave (automática ou pilotada)
                        if ldefs.E_AUTOMATICA == l_trf.en_trf_est_ope:

                            # cria uma nova aeronave ativa
                            l_atv = self.__ativa_trf(l_trf)
                            assert l_atv

                            # trava a lista de vôos
                            # gdata.G_LCK_FLIGHT.acquire()

                            try:
                                # insere os vôos no dicionário de tráfegos ativos
                                self.dct_flight[l_atv.s_trf_ind] = l_atv

                            finally:

                                # libera a lista de vôos
                                pass  # gdata.G_LCK_FLIGHT.release()

                            # remove do dicionário de tráfegos do exercício
                            del self.__exe.dct_exe_trf[l_key]

                        # senão, aeronave pilotada
                        # else:
                            # aeronave aguardando um piloto
                            # l_trf.en_trf_est_atv = ldefs.E_QUEUED

            # obtém o tempo atual em segundos
            lf_now = time.time()
                                    
            # check de ativação (30s)
            lf_call_time += float(self.dct_config["tim.fgen"])

            # está adiantado ?
            if lf_call_time >= lf_now:
                                                                                                        
                # agenda a próxima execução
                time.sleep(lf_call_time - lf_now)

            # senão, atrasou...
            else:
                # logger
                l_log = logging.getLogger("CEmulaNewton::__run_check_ativ")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E01: atraso de {}(s).".format(lf_now - lf_call_time))

                # reinicia o timer
                lf_call_time = time.time()

        # logger
        # M_LOG.info("__run_check_ativ:<<")
                
    # ---------------------------------------------------------------------------------------------

    def __run_check_cnfg(self):
        """
        checks whether it's time to created another flight
        """
        # logger
        # M_LOG.info("__run_check_cnfg:>>")

        # verifica condições de execução
        assert self.__exe
        assert self.__sck_snd_cnfg

        # inicia o timer de check de configuração (5s)
        lf_call_time = time.time()

        # loop de execução do check
        while gdata.G_KEEP_RUN:

            # envia os dados de exercício
            self.__exe.send_exe(self.__sck_snd_cnfg)

            # obtém o tempo atual em segundos
            lf_now = time.time()
                                    
            # check de configuração (5s)
            lf_call_time += float(self.dct_config["tim.cnfg"])

            # está adiantado ?
            if lf_call_time >= lf_now:
                                                                                                        
                # agenda a próxima execução
                time.sleep(lf_call_time - lf_now)

            # senão, atrasou...
            else:
                # logger
                l_log = logging.getLogger("CEmulaNewton::__run_check_cnfg")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E01: atraso de {}(s).".format(lf_now - lf_call_time))

                # reinicia o timer
                lf_call_time = time.time()

        # logger
        # M_LOG.info("__run_check_cnfg:<<")
                
    # ---------------------------------------------------------------------------------------------

    def __run_check_hora(self):
        """
        checks whether it's time to created another flight
        """
        # logger
        # M_LOG.info("__run_check_hora:>>")

        # verifica condições de execução
        assert self.__sck_snd_cnfg
        assert self.__sim_time
        assert self.__s_srv_addr

        # inicia o timer de check de hora (1s)
        lf_call_time = time.time()

        # loop de execução do check
        while gdata.G_KEEP_RUN:

            # envia os dados do servidor
            self.__sck_snd_cnfg.send_data(self.__s_srv_addr)

            # envia os dados de hora
            self.__sim_time.send_hora(self.__sck_snd_cnfg)

            # obtém o tempo atual em segundos
            lf_now = time.time()
                                    
            # check de hora (1s)
            lf_call_time += float(self.dct_config["tim.hora"])

            # está adiantado ?
            if lf_call_time >= lf_now:
                                                                                                        
                # agenda a próxima execução
                time.sleep(lf_call_time - lf_now)

            # senão, atrasou...
            else:
                # logger
                l_log = logging.getLogger("CEmulaNewton::__run_check_hora")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E01: atraso de {}(s).".format(lf_now - lf_call_time))

                # reinicia o timer
                lf_call_time = time.time()
            
        # logger
        # M_LOG.info("__run_check_hora:<<")
                
    # ---------------------------------------------------------------------------------------------

    def __run_check_prox(self):
        """
        calculates the proximity of the flights in the flight pair

        should be run everytime new positions are calculated by the flight engine.  If two flights
        are within 5 miles horizontically and at the same level or at the same position and (above
        29000 ft) within 2000 ft or (under 29000 ft)  within 1000 ft vertically a danger situation
        has occured
        """
        # logger
        # M_LOG.info("__run_check_prox:>>")

        # inicia o timer de check de colisão (1s)
        lf_call_time = time.time()

        # loop de execução do check
        while gdata.G_KEEP_RUN:

            # percorre o dicionário de vôos ativos...
            for _, l_atv1 in self.dct_flight.iteritems():

                # verifica aeronave
                assert isinstance(l_atv1, atv.CAtvNEW)

                # obtém a posição do vôo
                lf_x1 = l_atv1.f_trf_x
                lf_y1 = l_atv1.f_trf_y

                # obtém a altitude do vôo em metros
                ld_alt1 = l_atv1.f_trf_alt_atu

                # reset proximity alert
                l_atv1.v_atv_alert = False

                # percorre o dicionário de vôos ativos...
                for _, l_atv2 in self.dct_flight.iteritems():

                    # verifica aeronave
                    assert isinstance(l_atv2, atv.CAtvNEW)

                    # é o mesmo vôo ?
                    if l_atv1 == l_atv2:

                        # vai para o próximo vôo
                        continue

                    # obtém a posição do vôo
                    lf_x2 = l_atv2.f_trf_x
                    lf_y2 = l_atv2.f_trf_y

                    # obtém a altitude do vôo em metros
                    ld_alt2 = l_atv2.f_trf_alt_atu

                    # calcula a distância euclidiana entre eles
                    lf_hrz = cincalc.distancia_entre_pontos((lf_y1, lf_x1), (lf_y2, lf_x2))

                    # calcula a separação vertical em metros entre eles
                    lf_vrt = abs(ld_alt1 - ld_alt2)

                    M_LOG.debug(u"distâncias: H[%f] V[%f]" % (lf_hrz, lf_vrt))

                    # as duas estão em vôo ?
                    if (not l_atv1.v_atv_solo) and (not l_atv2.v_atv_solo):

                        # separação horizontal menor que 300m (1s a 300 Kt) e separação vertical menor que 70m (200ft) ?
                        if (lf_hrz < 300.) and (lf_vrt < 70.):

                            # emite o aviso sonoro
                            # self._snd_explode.play()

                            # gera colisão no ar entre as tráfegos
                            # l_view.gera_colisao_ar(l_atv1, l_atv2)
                            pass

                        # separação horizontal menor que 450m (3s a 300 Kt) e separação vertical menor que 150m (300ft)?
                        elif (lf_hrz < 900.) and (lf_vrt < 150.):

                            # gera alerta de colisão no ar entre as tráfegos
                            l_atv1.v_atv_alert = True

                            # emite o aviso sonoro
                            # self._snd_alert.play()

                    # as duas estão no solo ?
                    elif l_atv1.v_atv_solo and l_atv2.v_atv_solo:

                        # separação menor que 20m (1s a 20 Kt) ?
                        if lf_hrz < 20.:

                            # nova colisão ?
                            # if 'X' != l_atv1.c_atv_status_solo:

                                # emite o aviso sonoro
                                # self._snd_explode.play()

                                # gera colisão no solo entre as tráfegos
                                # l_view.gera_colisao_solo(l_atv1, l_atv2)
                            pass
                            
                        # separação menor que 150m (5s a 30 Kt) ?
                        elif lf_hrz < 150.:

                            # gera alerta de colisão no solo entre as tráfegos
                            l_atv1.v_atv_alert = True

                            # emite o aviso sonoro
                            # self._snd_alert.play()

                    # uma no solo e a outra em vôo
                    else:
                        # separação horizontal menor que 50m (1s a 50 Kt) e separação vertical menor que 25m ?
                        if (lf_hrz < 50.) and (lf_vrt < 25.):

                            # nova colisão ?
                            # if 'X' != l_atv1.c_atv_status_solo:

                                # emite o aviso sonoro
                                # self._snd_explode.play()

                                # gera colisão no solo e ar entre as tráfegos
                                # l_view.gera_colisao_ar_solo(l_atv1, l_atv2)
                            pass
                            
                        # separação horizontal menor que 100m (2s a 50 Kt) e separacão vertical menor que 50m ?
                        elif (lf_hrz < 100.) and (lf_vrt < 50.):

                            # gera colisão no solo e ar entre as tráfegos
                            l_atv1.v_atv_alert = True

                            # emite o aviso sonoro
                            # self._snd_alert.play()

            # obtém o tempo atual em segundos
            lf_now = time.time()
                                    
            # check de colisão (1s)
            lf_call_time += float(self.dct_config["tim.prox"])

            # está adiantado ?
            if lf_call_time >= lf_now:
                                                                                                        
                # agenda a próxima execução
                time.sleep(lf_call_time - lf_now)

            # senão, atrasou...
            else:
                # logger
                l_log = logging.getLogger("CEmulaNewton::__run_check_prox")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E01: atraso de {}(s).".format(lf_now - lf_call_time))

                # reinicia o timer
                lf_call_time = time.time()

        # logger
        # M_LOG.info("__run_check_prox:<<")
                
# < the end >--------------------------------------------------------------------------------------
