#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_piloto

DOCUMENT ME!

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/03"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import Queue
import time

# model
from ..model import glb_data as gdata
from ..model import glb_defs as gdefs
from ..model import model_piloto as model

# view
from ..view import view_piloto as view

# control
from ..control import control_basic as control
from ..control.config import config_piloto as config
from ..control.events import events_config as events
from ..control.network import get_address as gaddr
from ..control.network import net_http_get as httpsrv
from ..control.network import net_listener as listener
from ..control.network import net_sender as sender
from ..control.simula import sim_time as stime

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CControlPiloto >-------------------------------------------------------------------------

class CControlPiloto(control.CControlBasic):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")
                
        # init super class
        super(CControlPiloto, self).__init__()

        # herdados de CControlManager
        # self.event     # event manager
        # self.config    # opções de configuração
        # self.model     # model manager
        # self.view      # view manager
        # self.voip      # biblioteca de VoIP

        # herdados de CControlBasic
        # self.ctr_flight    # flight control
        # self.sim_stat      # simulation statistics
        # self.sim_time      # simulation timer

        # carrega o arquivo com as opções de configuração
        self.config = config.CConfigPiloto("tracks.cfg")
        assert self.config

        # obtém o dicionário de configuração
        self.__dct_config = self.config.dct_config
        assert self.__dct_config

        # create simulation statistics control
        # self.sim_stat = stats.SimStats()
        # assert self.sim_stat

        # create simulation time engine
        self.sim_time = stime.CSimTime(self)
        assert self.sim_time

        # cria a queue de envio
        self.__q_snd_cpil = multiprocessing.Queue()
        assert self.__q_snd_cpil

        # obtém o endereço de envio
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.cpil")

        # cria o socket de envio
        self.__sck_snd_cpil = sender.CNetSender(lt_ifce, ls_addr, li_port, self.__q_snd_cpil)
        assert self.__sck_snd_cpil

        # cria a queue de recebimento de configuração
        self.__q_rcv_cnfg = multiprocessing.Queue()
        assert self.__q_rcv_cnfg

        # obtém o endereço de envio
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.cnfg")

        # cria o socket de recebimento de configuração
        self.__sck_rcv_cnfg = listener.CNetListener(lt_ifce, ls_addr, li_port, self.__q_rcv_cnfg)
        assert self.__sck_rcv_cnfg

        # cria o socket de acesso ao servidor
        self.__sck_http = httpsrv.CNetHttpGet(self.event, self.config)
        assert self.__sck_http

        # cria a queue de recebimento de pistas
        self.__q_rcv_trks = multiprocessing.Queue()
        assert self.__q_rcv_trks

        # obtém o endereço de envio
        lt_ifce, ls_addr, li_port = gaddr.get_address(self.config, "net.trks")

        # cria o socket de recebimento de pistas
        self.__sck_rcv_trks = listener.CNetListener(lt_ifce, ls_addr, li_port, self.__q_rcv_trks)
        assert self.__sck_rcv_trks

        # instancia o modelo
        self.model = model.CModelPiloto(self)
        assert self.model

        # get flight model
        self.__emula_model = self.model.emula_model
        assert self.__emula_model

        # create view manager
        self.view = view.CViewPiloto(self, self.model)
        assert self.view

        # logger
        # M_LOG.info("__init__:<<")
                
    # ---------------------------------------------------------------------------------------------

    def run(self):
        """
        drive application
        """
        # logger
        # M_LOG.info("run:>>")

        # verifica condições de execução (I)
        if (None == self.model) or (None == self.view):

            # termina a aplicação sem confirmação e sem envio de fim
            self.cbk_termina()

        # verifica condições de execução (I)
        assert self.event
        assert self.__q_rcv_cnfg
        assert self.__sck_rcv_cnfg
        assert self.__emula_model

        # temporização de scheduler
        lf_tim_rrbn = self.config.dct_config["tim.rrbn"]

        # keep things running
        gdata.G_KEEP_RUN = True

        # ativa o relógio
        self.start_time()

        # inicia o recebimento de mensagens de configuração
        self.__sck_rcv_cnfg.start()

        # starts flight model
        self.__emula_model.start()

        # obtém o tempo inicial em segundos
        lf_now = time.time()

        # application loop
        while gdata.G_KEEP_RUN:

            try:
                # obtém um item da queue de configuração (nowait)
                llst_data = self.__q_rcv_cnfg.get(False)
                M_LOG.debug("llst_data:[{}]".format(llst_data))

                # queue tem dados ?
                if llst_data:

                    M_LOG.debug("llst_data[0]:[{}]".format(llst_data[0]))

                    # mensagem de aceleração ?
                    if gdefs.D_MSG_ACC == int(llst_data[0]):

                        # acelera/desacelera a aplicação
                        pass  # self.cbk_acelera ( float ( llst_data [ 1 ] ))

                    # mensagem toggle call sign ?
                    elif gdefs.D_MSG_CSG == int(llst_data[0]):

                        # liga/desliga callsign
                        pass  # self.view.cbk_toggle_callsign()

                    # mensagem configuração de exercício ?
                    elif gdefs.D_MSG_EXE == int(llst_data[0]):

                        # cria um evento de configuração de exercício
                        l_evt = events.CConfigExe(llst_data[1])
                        assert l_evt
                        
                        # dissemina o evento
                        self.event.post(l_evt)

                    # mensagem de fim de execução ?
                    elif gdefs.D_MSG_FIM == int(llst_data[0]):

                        # termina a aplicação
                        self.cbk_termina()

                    # mensagem de congelamento ?
                    elif gdefs.D_MSG_FRZ == int(llst_data[0]):

                        # freeze application
                        pass  # self.view.cbk_freeze ( False )

                    # mensagem de endereço do servidor ?
                    elif gdefs.D_MSG_SRV == int(llst_data[0]):

                        # salva o endereço do servidor
                        self.__dct_config["srv.addr"] = str(llst_data[1])

                    # mensagem de hora ?
                    elif gdefs.D_MSG_TIM == int(llst_data[0]):

                        # monta uma tupla com a mensagem de hora
                        lt_hora = tuple(int(s) for s in llst_data[1][1: -1].split(','))

                        # seta a hora de simulação
                        self.sim_time.set_hora(lt_hora)

                        # cria um evento de configuração de hora de simulação
                        l_evt = events.CConfigHora(self.sim_time.get_hora_format())
                        assert l_evt
                        
                        # dissemina o evento
                        self.event.post(l_evt)

                    # mensagem de descongelamento ?
                    elif gdefs.D_MSG_UFZ == int(llst_data[0]):

                        # defreeze application
                        pass  # self.view.cbk_defreeze ( False )

                    # senão, mensagem não reconhecida ou não tratavél
                    else:
                        # logger
                        l_log = logging.getLogger("CControlPiloto::run")
                        l_log.setLevel(logging.WARNING)
                        l_log.warning("Mensagem não reconhecida ou não tratável.")

            # em caso de não haver mensagens...
            except Queue.Empty, ls_err:

                # salva o tempo anterior
                lf_ant = lf_now
                                    
                # obtém o tempo atual em segundos
                lf_now = time.time()
                                                                    
                # obtém o tempo final em segundos e calcula o tempo decorrido
                lf_dif = lf_now - lf_ant
                                                                                                            
                # está adiantado ?
                if lf_tim_rrbn > lf_dif:
                                                                                                                                            
                    # permite o scheduler
                    time.sleep(lf_tim_rrbn - lf_dif)

        # logger
        # M_LOG.info("run:<<")

    # ---------------------------------------------------------------------------------------------

    def start_time(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("start_time:>>")

        # verifica condições de execução
        # assert self.sim_time

        # inicia o relógio da simulação
        # self.sim_time.set_hora_ini((0, 0, 0))
        pass

        # logger
        # M_LOG.info("start_time:<<")

    # =============================================================================================
    # data
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
        self.__emula_model = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def q_rcv_cnfg(self):
        """
        get configuration queue
        """
        return self.__q_rcv_cnfg

    @q_rcv_cnfg.setter
    def q_rcv_cnfg(self, f_val):
        """
        set configuration queue
        """
        self.__q_rcv_cnfg = f_val

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
        self.__sck_rcv_cnfg = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def q_snd_cpil(self):
        """
        get configuration queue
        """
        return self.__q_snd_cpil

    @q_snd_cpil.setter
    def q_snd_cpil(self, f_val):
        """
        set configuration queue
        """
        self.__q_snd_cpil = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def sck_snd_cpil(self):
        """
        get configuration listener
        """
        return self.__sck_snd_cpil

    @sck_snd_cpil.setter
    def sck_snd_cpil(self, f_val):
        """
        set configuration listener
        """
        self.__sck_snd_cpil = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def sck_http(self):
        """
        get http server listener
        """
        return self.__sck_http

    @sck_http.setter
    def sck_http(self, f_val):
        """
        set http server listener
        """
        self.__sck_http = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def q_rcv_trks(self):
        """
        get data queue
        """
        return self.__q_rcv_trks

    @q_rcv_trks.setter
    def q_rcv_trks(self, f_val):
        """
        set data queue
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
        self.__sck_rcv_trks = f_val

# < the end >--------------------------------------------------------------------------------------
