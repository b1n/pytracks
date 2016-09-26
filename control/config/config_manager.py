#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
config_manager

módulo que mantém as informações comuns de configuração

revision 0.4  2016/ago  mlabru
pequenas correções e otimizações

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do dicionário de configuração

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.4$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/08"

# < imports >--------------------------------------------------------------------------------------

# python library
import ConfigParser
# import logging
import os

# model
from ...model import glb_data as gdata
from ...model import glb_defs as gdefs
from ...model.coords import coord_defs as cdefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CConfigManager >-------------------------------------------------------------------------

class CConfigManager(object):
    """
    mantém as informações comuns de configuração
    """
    # informações comuns de configuração
    __CFG_COMMON = {"dir.air": gdefs.D_DIR_AIR,    # diretório de airspaces
                    "dir.dat": gdefs.D_DIR_DAT,    # diretório de dados
                    "dir.exe": gdefs.D_DIR_EXE,    # diretório de exercícios
                    "dir.img": gdefs.D_DIR_IMG,    # diretório de imagens
                    "dir.map": gdefs.D_DIR_MAP,    # diretório de mapas
                    "dir.prc": gdefs.D_DIR_PRC,    # diretório de procedimentos
                    "dir.snd": gdefs.D_DIR_SND,    # diretório de sons
                    "dir.tab": gdefs.D_DIR_TAB,    # diretório de tabelas
                    "dir.trf": gdefs.D_DIR_TRF,    # diretório de tráfegos

                    "glb.canal": gdata.G_CANAL,    # canal de comunicação

                    "map.lat": cdefs.M_REF_LAT,    # latitude de referência do mapa
                    "map.lng": cdefs.M_REF_LNG,    # longitude de referência do mapa
                    "map.dcl": cdefs.M_DCL_MAG,    # declinação magnética na referência

                    "net.addr": gdefs.D_NET_ADDR,    # endereço default
                    "net.cnfg": gdefs.D_NET_CNFG,    # endereço multicast de configuração
                    "net.cpil": gdefs.D_NET_CPIL,    # endereço multicast de pilotagem
                    "net.ifin": gdefs.D_NET_IFIN,    # interface de entrada
                    "net.iout": gdefs.D_NET_IOUT,    # interface de saída
                    "net.snsr": gdefs.D_NET_SNSR,    # endereço multicast de sensor
                    "net.trks": gdefs.D_NET_TRKS,    # endereço multicast de pistas
                    "net.voip": gdefs.D_NET_VOIP,    # endereço multicast de voip
                    "net.port": gdefs.D_NET_PORT,    # porta de comunicação
                    "net.vers": gdefs.D_MSG_VRS,     # versão do protocolo

                    "tim.accl": gdefs.D_TIM_ACCL,    # fast-time simulation acceleration factor (1x)
                    "tim.cnfg": gdefs.D_TIM_CNFG,    # reenvio de configuração do sistema (5s)
                    "tim.evnt": gdefs.D_TIM_EVNT,    # tratador de eventos (1/10th)
                    "tim.fgen": gdefs.D_TIM_FGEN,    # tempo de ativação das aeronaves (30s)
                    "tim.hora": gdefs.D_TIM_HORA,    # reenvia a hora do sistema (1s)
                    "tim.prox": gdefs.D_TIM_PROX,    # colisão entre aeronaves (1s)
                    "tim.rdar": gdefs.D_TIM_RDAR,    # rotação do radar (4s)
                    "tim.rfsh": gdefs.D_TIM_REFR,    # screen refresh time (1/10th)
                    "tim.rrbn": gdefs.D_TIM_RRBN,    # round robin do sistema (1s)
                    "tim.wait": gdefs.D_TIM_WAIT,    # tempo de espera de eventos (1/10th)
                   }  # __CFG_COMMON

    # ---------------------------------------------------------------------------------------------

    def __init__(self, fs_path="acme.cfg"):
        """
        inicia o gerente de configuração

        @param fs_path: full path do arquivo de configuração
        """
        # logger
        # M_LOG.info("__init__:>>")

        # load default values in dictionary
        self.__dct_config = self.__CFG_COMMON.copy()
        assert self.__dct_config is not None

        # cria o parser para o arquivo de configuração
        l_cp = ConfigParser.SafeConfigParser()
        assert l_cp

        # verfica se o arquivo de configuração existe
        if os.path.exists(os.path.expanduser(fs_path)):

            # abre o arquivo de configuração
            l_cp.readfp(open(fs_path))

            # load entire config file in dictionary
            for l_section in l_cp.sections():
                for l_option in l_cp.options(l_section):
                    self.__dct_config[str(l_section.lower() + '.' + l_option.lower())] = l_cp.get(l_section, l_option)

        # logger
        # M_LOG.info("__init__:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_config(self):
        """
        config manager data dictionary
        """
        return self.__dct_config

    @dct_config.setter
    def dct_config(self, f_val):
        """
        config manager data dictionary
        """
        # verifica parâmetros de entrada
        assert f_val is not None

        # save a shallow copy
        self.__dct_config = dict(f_val)

# < the end >--------------------------------------------------------------------------------------
