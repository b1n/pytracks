#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
emula_piloto.

the actual flight control

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
import json
import logging
import threading
import time

# model
import model.glb_data as gdata
import model.glb_defs as gdefs

import model.emula.emula_model as model

import model.piloto.data_piloto as ldata
import model.piloto.aircraft_piloto as canv

# control
import control.events.events_flight as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CEmulaPiloto >---------------------------------------------------------------------------

class CEmulaPiloto(model.CEmulaModel):
    """
    the flight model class generates new flights and handles their movement. It has a list of
    flight objects holding all flights that are currently active. The flights are generated when
    activation time comes, or quando ja foi ativado na confecção do exercicio. Once a flight has
    been generated it is handed by the flight engine.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_control):
        """
        @param f_model: model manager.
        @param f_control: control manager.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parametros de entrada
        assert f_control
        assert f_model

        # inicia a super classe
        super(CEmulaPiloto, self).__init__(f_model, f_control)

        # herdados de CEmulaModel
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager
        # self.dct_flight    # dictionary for active flights
        # self.model         # model manager

        # obtém o http server listener
        self.__sck_http = f_control.sck_http
        assert self.__sck_http

        # obtém o dicionário de performances
        self.__dct_prf = f_model.dct_prf
        assert self.__dct_prf is not None

        # logger
        # M_LOG.info("__init__:<<")
                                        
    # ---------------------------------------------------------------------------------------------

    def __msg_trk(self, flst_data):
        """
        checks whether it's time to created another flight.

        @param flst_data: mensagem de status
        """
        # logger
        # M_LOG.info("__msg_trk:>>")

        # check for requirements
        assert self.__sck_http is not None
        assert self.dct_config is not None
        assert self.dct_flight is not None
        assert self.__dct_prf is not None
                
        # obtém o callsign da aeronave
        ls_callsign = flst_data[10]
        M_LOG.debug("__msg_trk:callsign:[{}]".format(ls_callsign))
                            
        # trava a lista de vôos
        gdata.G_LCK_FLIGHT.acquire()

        try:
            # aeronave já está no dicionário ?
            if ls_callsign in self.dct_flight:

                # atualiza os dados da aeronave
                self.dct_flight[ls_callsign].update_data(flst_data[1:])

            # senão, aeronave nova...
            else:
                # create new aircraft
                self.dct_flight[ls_callsign] = canv.CAircraftPiloto(self, flst_data[1:])
                assert self.dct_flight[ls_callsign]
                                                                                                                                                                                                                                                            
        finally:

            # libera a lista de vôos
            gdata.G_LCK_FLIGHT.release()

        # obtém o indicativo da performance
        ls_prf_ind = flst_data[11]
        M_LOG.debug("__msg_trk:ls_prf_ind:[{}]".format(ls_prf_ind))
                            
        # performance não está no dicionário ?
        if self.__dct_prf.get(ls_prf_ind, None) is None:

            # monta o request da performance
            ls_req = "data/prf.json?{}".format(ls_prf_ind)
            M_LOG.debug("__msg_trk:ls_req:[{}]".format(ls_req))

            # get server address
            l_srv = self.dct_config.get("srv.addr", None)
            
            if l_srv is not None:

                # obtém os dados de performance do servidor
                l_prf = self.__sck_http.get_data(l_srv, ls_req)
                M_LOG.debug("__msg_trk:l_prf:[{}]".format(l_prf))

                if (l_prf is not None) and (l_prf != ""):

                    # salva a performance no dicionário
                    self.__dct_prf[ls_prf_ind] = json.loads(l_prf)
                    M_LOG.debug("__msg_trk:dct_prf:[{}]".format(self.__dct_prf))

                # senão, não achou no servidor...
                else:
                    # logger
                    l_log = logging.getLogger("CEmulaPiloto::__msg_trk")
                    l_log.setLevel(logging.WARNING)
                    l_log.error(u"<E01: performance({}) não existe no servidor.".format(ls_prf_ind))

            # senão, não achou endereço do servidor
            else:
                # logger
                l_log = logging.getLogger("CEmulaPiloto::__msg_trk")
                l_log.setLevel(logging.WARNING)
                l_log.warning(u"<E02: srv.addr não existe na configuração.")

        # cria um evento de atualização de aeronave
        l_evt = events.CFlightUpdate(ls_callsign)
        assert l_evt

        # dissemina o evento
        self.event.post(l_evt)

        # logger
        # M_LOG.info("__msg_trk:<<")

    # ---------------------------------------------------------------------------------------------

    def run(self):
        """
        checks whether it's time to created another flight.
        """
        # logger
        # M_LOG.info("run:>>")
                
        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:

            # aguarda 1 seg
            time.sleep(1)

        # cria a trava da lista de vôos
        gdata.G_LCK_FLIGHT = threading.Lock()
        assert gdata.G_LCK_FLIGHT
                        
        # obtém o data listener
        lsck_rcv_trks = self.control.sck_rcv_trks
        assert lsck_rcv_trks

        # inicia o recebimento de mensagens de pista
        lsck_rcv_trks.start()

        # obtém a queue de dados
        lq_rcv_trks = self.control.q_rcv_trks
        assert lq_rcv_trks

        # loop
        while gdata.G_KEEP_RUN:

            # obtém um item da queue de entrada
            llst_data = lq_rcv_trks.get()
            # M_LOG.debug("llst_data:[{}]".format(llst_data))

            # queue tem dados ?
            if llst_data:

                # mensagem de status de aeronave ?
                if gdefs.D_MSG_NEW == int(llst_data[0]):

                    # trata mensagem de status de aeronave
                    self.__msg_trk(llst_data)
                    
                # mensagem de eliminação de aeronave ?
                elif gdefs.D_MSG_KLL == int(llst_data[0]):

                    # coloca a mensagem na queue
                    # M_LOG.debug("Elimina:[{}]".format(ls_callsign))

                    # trava a lista de vôos
                    ldata.G_LCK_FLIGHT.acquire()

                    try:
                        # aeronave está no dicionário ?
                        if ls_callsign in self.dct_flight:

                            # retira a aeronave do dicionário
                            del self.dct_flight[ls_callsign]

                    finally:

                        # libera a lista de vôos
                        ldata.G_LCK_FLIGHT.release()

                    # cria um evento de eliminação de aeronave
                    l_evt = events.FlightKill(ls_callsign)
                    assert l_evt

                    # dissemina o evento
                    self._event.post(l_evt)

                # senão, mensagem não reconhecida ou não tratada
                else:
                    # logger
                    l_log = logging.getLogger("CEmulaPiloto::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("Mensagem não reconhecida ou não tratada !")

    # =============================================================================================
    # data
    # =============================================================================================
            
# < the end >--------------------------------------------------------------------------------------
