#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
sim_time.

simulation time engine.

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do dicionário de configuração.

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging
import threading
import time

# model
from ...model import glb_data as gdata
from ...model import glb_defs as gdefs

# control
from ...control.events import events_basic as events

# < module data >----------------------------------------------------------------------------------

# logging level
# M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# < class CSimTime >-------------------------------------------------------------------------------


class CSimTime(threading.Thread):
    """
    simulation time engine.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control):
        """
        cria o relógio da simulação.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input parameters
        assert f_control

        # init super class
        super(CSimTime, self).__init__()

        # obtém o events manager
        self.__event = f_control.event
        assert self.__event

        # obtém o config manager
        l_config = f_control.config
        assert l_config

        # obtém o dicionário de configuração
        self.__dct_config = l_config.dct_config
        assert self.__dct_config is not None

        # flag congela
        self.__v_congela = False

        # tempo anterior de execução
        # self._ulTpoAnt = 0

        # tempo atual de execução
        # self._ulTpoAtu = 0

        # hora zero da simulação
        self.__f_zero_sim = 0.

        # preenche a hora zero do sistema (seg)
        self.__f_zero_sys = time.time()
        # M_LOG.debug("self.__f_zero_sys:[{:.3f}]".format(self.__f_zero_sys))

        # hora atual do exercício
        self.__b_ha = 0
        self.__b_ma = 0
        self.__b_sa = 0

        # hora atual formatada
        self.__s_hora = "{:02d}:{:02d}:{:02d}".format(self.__b_ha, self.__b_ma, self.__b_sa)
        # M_LOG.debug("self.__s_hora:[{}]".format(self.__s_hora))

        # hora atual do exercício
        self.__f_hora_atu = 0

        # tempo de congelamento do exercício
        self.__f_hora_frz = 0

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def ajusta_hora(self, f_hora):
        """
        permite iniciar a hora do equipamento.
        """
        # logger
        # M_LOG.info("ajusta_hora:>>")

        # check input parameters
        assert f_hora

        # preenche a hora zero da simulação (seg)
        self.__f_zero_sim = f_hora
        # M_LOG.debug("self.__f_zero_sim:[{:.3f}]".format(self.__f_zero_sim))

        # preenche a hora zero do sistema (seg)
        self.__f_zero_sys = time.time()
        # M_LOG.debug("self.__f_zero_sys:[{:.3f}]".format(self.__f_zero_sys))

        # logger
        # M_LOG.info("ajusta_hora:<<")

    # ---------------------------------------------------------------------------------------------

    def cbk_congela(self):
        """
        congela o relógio da simulação.
        """
        # logger
        # M_LOG.info("cbk_congela:>>")

        # flag congela
        self.__v_congela = True

        # obtém a hora do sistema (seg)
        self.__f_hora_frz = time.time()
        # M_LOG.debug("self.__f_hora_frz:[{:.3f}]".format(self.__f_hora_frz))

        # logger
        # M_LOG.info("cbk_congela:<<")

    # ---------------------------------------------------------------------------------------------

    def cbk_descongela(self):
        """
        descongela o relógio da simulação.
        """
        # logger
        # M_LOG.info("cbk_descongela:>>")

        # obtem a hora do sistema (seg)
        lf_hora_now = time.time()
        # M_LOG.debug("lf_hora_now:[{:.3f}]".format(lf_hora_now))

        # calcula quanto tempo ficou congelado
        lf_hora_dif = lf_hora_now - self.__f_hora_frz
        # M_LOG.debug("lf_hora_dif:[{:.3f}]".format(lf_hora_dif))

        # incrementa ao tempo zero do sistema (seg)
        self.__f_zero_sys += lf_hora_dif
        # M_LOG.debug("self.__f_zero_sys:[{:.3f}]".format(self.__f_zero_sys))

        # flag congela
        self.__v_congela = False

        # logger
        # M_LOG.info("cbk_descongela:<<")

    # ---------------------------------------------------------------------------------------------

    def get_hora_format(self):
        """
        exibe o relógio da simulação.
        """
        # logger
        # M_LOG.info("get_hora_format:>>")

        # obtem a hora atual do exercício
        lb_h, lb_m, lb_s, _ = self.obtem_hora()

        # checa se mudou algo
        if (lb_h != self.__b_ha) or (lb_m != self.__b_ma) or (lb_s != self.__b_sa):

            # monta a string com a hora atual
            self.__s_hora = "{:02d}:{:02d}:{:02d}".format(lb_h, lb_m, lb_s)

            # salva os valores atuais
            self.__b_ha = lb_h
            self.__b_ma = lb_m
            self.__b_sa = lb_s

        # M_LOG.debug("Hora atual:[{}]".format(self.__s_hora))

        # logger
        # M_LOG.info("get_hora_format:<<")

        # retorna a hora da simulação formatada
        return self.__s_hora

    # ---------------------------------------------------------------------------------------------

    @staticmethod
    def notify(f_event):
        """
        callback de tratamento de eventos recebidos.

        @param f_event: event
        """
        # logger
        # M_LOG.info("notify:>>")

        # check input parameters
        assert f_event

        # logger
        # M_LOG.info("notify:<<")

    # ---------------------------------------------------------------------------------------------

    def obtem_hora(self):
        """
        obtém a hora do relógio do equipamento.
        """
        # logger
        # M_LOG.info("obtem_hora:>>")

        # obtém a hora da simulação
        lf_hora_now = self.obtem_hora_sim()

        # calcula os milésimos de segundo
        li_msg = int(round((lf_hora_now - int(lf_hora_now)) * 1000.))

        # calcula os segundos
        li_seg = int(lf_hora_now) % 60

        # calcula os minutos
        li_min = int(lf_hora_now / 60.) % 60

        # calcula as horas
        li_hor = int(lf_hora_now / 3600.)

        # M_LOG.debug("l_fHora:[{}:{}:{}.{}]".format(li_hor, li_min, li_seg, li_msg))

        # logger
        # M_LOG.info("obtem_hora:<<")

        # return
        return li_hor, li_min, li_seg, li_msg

    # ---------------------------------------------------------------------------------------------

    def obtem_hora_sim(self):
        """
        obtém a hora da simulação
        """
        # logger
        # M_LOG.info("obtem_hora_sim:>>")

        # hora descongelada ?
        if not self.__v_congela:

            # obtém a hora do sistema (seg)
            self.__f_hora_atu = time.time()
            # M_LOG.debug("self.__f_hora_atu:[{:.3f}]".format(self.__f_hora_atu))

        # calcula a diferença com a hora zero
        lf_hora_dif = self.__f_hora_atu - self.__f_zero_sys
        # M_LOG.debug("lf_hora_dif:[{:.3f}]".format(lf_hora_dif))

        # incrementa a hora zero da simulação
        lf_now = self.__f_zero_sim + (lf_hora_dif * self.__dct_config["tim.accl"])

        # logger
        # M_LOG.info("obtem_hora_sim:<<")

        # retorna a hora atual do sistema
        return lf_now

    # ---------------------------------------------------------------------------------------------

    def run(self):
        """
        executa o relógio da simulação.
        """
        # logger
        # M_LOG.info("run:>>")

        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:

            # aguarda 1 seg
            time.sleep(1)

        # loop do relógio
        while gdata.G_KEEP_RUN:

            # limit to 60 fps
            # self._clock.tick(60)

            # cria um evento de tick do clock
            l_evt_tick = events.CTick()
            assert l_evt_tick

            # dissemina o evento
            self.__event.post(l_evt_tick)

        # logger
        # M_LOG.info("run:<<")

    # ---------------------------------------------------------------------------------------------

    def send_hora(self, f_sck_scfg):
        """
        envia a hora de simulação.

        @param f_sck_scfg: net sender.
        """
        # logger
        # M_LOG.info("send_hora:>>")

        # check input parameters
        assert f_sck_scfg

        # envia a hora de simulação pela linha de configuração
        f_sck_scfg.send_data(str(gdefs.D_MSG_VRS) + gdefs.D_MSG_SEP +
                             str(gdefs.D_MSG_TIM) + gdefs.D_MSG_SEP + str(self.obtem_hora()))

        # logger
        # M_LOG.info("send_hora:<<")

    # ---------------------------------------------------------------------------------------------

    def set_hora(self, ft_hora):
        """
        configura a hora de simulação.

        @param ft_hora: tupla no formato(hor, min, seg, csg).
        """
        # logger
        # M_LOG.info("set_hora:>>")

        # check input parameters
        assert ft_hora

        assert 0 <= ft_hora[0] <= 23  # hora
        assert 0 <= ft_hora[1] <= 59  # minutos
        assert 0 <= ft_hora[2] <= 59  # segundos

        # preenche a hora zero da simulação (seg)
        self.__f_zero_sim = (((ft_hora[0] * 60) + ft_hora[1]) * 60) + ft_hora[2]
        # M_LOG.debug("self.__f_zero_sim:[{:.3f}]".format(self.__f_zero_sim))

        # preenche a hora zero do sistema (seg) em relação a simulação
        self.__f_zero_sys = time.time()
        # M_LOG.debug("self.__f_zero_sys:[{:.3f}]".format(self.__f_zero_sys))

        # logger
        # M_LOG.info("set_hora:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def v_congela(self):
        """
        get flag congela
        """
        return self.__v_congela

    @v_congela.setter
    def v_congela(self, fv_val):
        """
        set flag congela
        """
        # check input parameters
        assert isinstance(True, type(fv_val))

        # flag congela
        self.__v_congela = fv_val

# < the end >--------------------------------------------------------------------------------------
