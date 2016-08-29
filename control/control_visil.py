#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_visil

DOCUMENT ME!

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import Queue
import sys
import time

# model
import model.glb_data as gdata
import model.glb_defs as gdefs
import model.model_visil as model

# view
import view.view_visil as view

# control
import control.control_basic as control
import control.config.config_visil as config
import control.network.get_address as gaddr
import control.network.net_listener as listener
import control.simula.sim_time as stime

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CControlVisil >--------------------------------------------------------------------------

class CControlVisil(control.CControlBasic):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("__init__:>>")

        # inicia a super classe
        super(CControlVisil, self).__init__()

        # herdados de CControlManager
        # self.event     # event manager
        # self.config    # opções de configuração
        # self.model     # model manager
        # self.view      # view manager
        # self.voip      # biblioteca de VoIP

        # herdados de CControlBasic
        # self.ctr_flight    # flight control
        # self.sck_send      # net sender
        # self.sim_stat      # simulation statistics
        # self.sim_time      # simulation timer
                                        
        # carrega o arquivo com as opções de configuração
        self.config = config.CConfigVisil("tracks.cfg")
        assert self.config

        # create simulation statistics control
        # self.sim_stat = simStats.simStats()
        # assert self.sim_stat

        # create simulation time engine
        self.sim_time = stime.CSimTime(self)
        assert self.sim_time

        # cria a queue de recebimento de comando/controle/configuração
        self.__q_rcv_cnfg = multiprocessing.Queue()
        assert self.__q_rcv_cnfg

        # obtém o endereço de recebimento
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.cnfg")

        # cria o socket de recebimento de comando/controle/configuração
        self.__sck_rcv_cnfg = listener.CNetListener(lt_ifce, ls_addr, li_port, self.__q_rcv_cnfg)
        assert self.__sck_rcv_cnfg

        # cria a queue de recebimento de pistas
        self.__q_rcv_trks = multiprocessing.Queue()
        assert self.__q_rcv_trks

        # obtém o endereço de recebimento
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.trks")

        # cria o socket de recebimento de pistas
        self.__sck_rcv_trks = listener.CNetListener(lt_ifce, ls_addr, li_port, self.__q_rcv_trks)
        assert self.__sck_rcv_trks

        # instancia o modelo
        self.model = model.CModelVisil(self)
        assert self.model

        # get flight model
        self.__emula_model = self.model.emula_model
        assert self.__emula_model

        # create view manager
        self.view = view.CViewVisil(self, self.model)
        assert self.view

        # logger
        M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def run(self):
        """
        drive application.
        """
        # logger
        M_LOG.info("run:>>")

        # verifica condições de execução (I)
        assert self.__emula_model
        assert self.__q_rcv_cnfg
        assert self.__sck_rcv_cnfg

        # temporização de eventos
        lf_tim_rrbn = self.config.dct_config["tim.rrbn"]

        # ativa o relógio da simulação
        self.start_time()

        # inicia o recebimento de mensagens de configuração
        self.__sck_rcv_cnfg.start()

        # starts flight model
        self.__emula_model.start()

        # keep things running
        gdata.G_KEEP_RUN = True
                        
        # obtém o tempo inicial em segundos
        lf_now = time.time()

        # application loop
        while gdata.G_KEEP_RUN:

            try:
                # obtém um item da queue de configuração
                llst_data = self.__q_rcv_cnfg.get(False)
                M_LOG.debug("llst_data:[{}]",format(llst_data))

                # queue tem dados ?
                if llst_data:

                    # mensagem de aceleração ?
                    if gdefs.D_MSG_ACC == int(llst_data[0]):

                        # acelera/desacelera a aplicação
                        pass  # self.cbkAcelera(float(llst_data [ 1 ]))

                    # mensagem toggle call sign ?
                    elif gdefs.D_MSG_CSG == int(llst_data[0]):

                        # liga/desliga call-sign
                        pass  # self._oView.cbkToggleCallSign()

                        # M_LOG.debug("liga/desliga callsign")

                    # mensagem configuração de exercício ?
                    elif gdefs.D_MSG_EXE == int(llst_data[0]):

                        # liga/desliga call-sign
                        pass  # self._oView.cbkToggleCallSign()

                        # M_LOG.debug("configuração de exercício")

                    # mensagem de fim de execução ?
                    if gdefs.D_MSG_FIM == int(llst_data[0]):

                        # termina a aplicação
                        self.cbk_termina()

                    # mensagem de congelamento ?
                    elif gdefs.D_MSG_FRZ == int(llst_data[0]):

                        # freeze application
                        pass  # self._oView.cbkFreeze(False)

                    # mensagem toggle range mark ?
                    elif gdefs.D_MSG_RMK == int(llst_data[0]):

                        # liga/desliga range mark
                        pass  # self._oView.cbkToggleRangeMark()

                        # M_LOG.debug("liga/desliga range mark")

                    # mensagem de hora ?
                    elif gdefs.D_MSG_TIM == int(llst_data[0]):

                        M_LOG.debug("llst_data[1]:(%s)" % str(llst_data[1]))

                        # monta uma tupla com a mensagem de hora
                        lt_hora = tuple(int(l_s) for l_s in llst_data[1][1: -1].split(','))
                        M_LOG.debug("lt_hora:(%s)" % str(lt_hora))

                        # seta a hora de simulação
                        self.sim_time.set_hora(lt_hora)

                    # mensagem de descongelamento ?
                    elif gdefs.D_MSG_UFZ == int(llst_data[0]):

                        # defreeze application
                        pass  # self._oView.cbkDefreeze(False)

                    # senão, mensagem não reconhecida ou não tratavél
                    else:
                        # logger
                        l_log = logging.getLogger("CControlVisil::run")
                        l_log.setLevel(logging.NOTSET)
                        l_log.warning("<E02: mensagem não reconhecida ou não tratável.")

            # em caso de não haver mensagens...
            except Queue.Empty:
                        
                # salva o tempo anterior
                lf_ant = lf_now
                                                        
                # obtém o tempo atual em segundos
                lf_now = time.time()
                                                                                        
                # obtém o tempo final em segundos e calcula o tempo decorrido
                lf_dif = lf_now - lf_ant
                                                                                                                                        
                # está adiantado ?
                if lf_tim_rrbn > lf_dif:
                                                                                                                                                                        
                    # permite o scheduler
                    time.sleep((lf_tim_rrbn - lf_dif) * .99)

                # senão, atrasou...
                else:
                    # logger
                    l_log = logging.getLogger("CControlVisil::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E03: atrasou: {}".format(lf_dif - lf_tim_rrbn))

        # logger
        M_LOG.info("run:<<")

    # ---------------------------------------------------------------------------------------------

    def start_time(self):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("start_time:>>")

        # verifica condições de execução
        assert self.sim_time

        # inicia o relógio da simulação
        self.sim_time.set_hora((0, 0, 0))

        # logger
        M_LOG.info("start_time:<<")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def emula_model(self):
        """
        get flight model
        """
        return self.__emula_model

    @emula_model.setter
    def emula_model(self, f_val):
        """
        set flight model
        """
        # verifica parâmetros de entrada
        assert f_val

        # save flight model
        self.__emula_model = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def sck_rcv_cnfg(self):
        """
        get configuration listener
        """
        return self.__sck_rcv_cnfg

    @sck_rcv_cnfg.setter
    def sck_rcv_cnfg(self, f_val):
        """
        set configuration listener
        """
        # verifica parâmetros de entrada
        assert f_val

        # save configuration listener
        self.__sck_rcv_cnfg = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def q_rcv_trks(self):
        """
        get tracks queue
        """
        return self.__q_rcv_trks
                                            
    @q_rcv_trks.setter
    def q_rcv_trks(self, f_val):
        """
        set tracks queue
        """
        self.__q_rcv_trks = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def sck_rcv_trks(self):
        """
        get data listener
        """
        return self.__sck_rcv_trks

    @sck_rcv_trks.setter
    def sck_rcv_trks(self, f_val):
        """
        set data listener
        """
        # verifica parâmetros de entrada
        assert f_val

        # save data listener
        self.__sck_rcv_trks = f_val

# < the end >--------------------------------------------------------------------------------------
