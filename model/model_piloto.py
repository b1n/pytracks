#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_piloto

model manager da pilotagem

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
import os
import sys

# model
import model.model_manager as model
import model.coords.coord_sys as coords
import model.emula.emula_piloto as emula
import model.piloto.airspace_piloto as airs

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CModelPiloto >---------------------------------------------------------------------------

class CModelPiloto(model.CModelManager):
    """
    piloto model object.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control):
        """
        @param f_control: control manager.
        """
        # logger
        # M_LOG.info("__init__:>>")
                
        # verifica parâmetros de entrada
        assert f_control

        # init super class
        super(CModelPiloto, self).__init__(f_control)

        # herdados de CModelManager
        # self.control       # control manager
        # self.event         # event manager
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração

        # obtém as coordenadas de referência
        lf_ref_lat = self.dct_config["map.lat"]
        lf_ref_lng = self.dct_config["map.lng"]
        lf_dcl_mag = self.dct_config["map.dcl"]
                                                                
        # coordinate system
        self.__coords = coords.CCoordSys(lf_ref_lat, lf_ref_lng, lf_dcl_mag)
        assert self.__coords

        # variáveis de instância
        self.__airspace = None
        # self.__landscape = None

        # dicionário de performances
        self.__dct_prf = {}
                
        # carrega o cenário (airspace & landscape)
        self.__load_cenario()
                
        # create emula model
        self.__emula_model = emula.CEmulaPiloto(self, f_control)
        assert self.__emula_model
                        
        # logger
        # M_LOG.info("__init__:<<")
                
    # ---------------------------------------------------------------------------------------------

    def __load_air(self):
        """
        faz a carga do airspace

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("__load_air:>>")

        # obtém o diretório padrão de airspaces
        ls_dir = self.dct_config["dir.air"]

        # nome do diretório vazio ?
        if ls_dir is None:

            # diretório padrão de airspaces
            self.dct_config["dir.air"] = gdefs.D_DIR_AIR

            # diretório padrão de airspaces
            ls_dir = gdefs.D_DIR_AIR

        # expand user (~)
        # ls_dir = os.path.expanduser(ls_dir)

        # diretório não existe ?
        if not os.path.exists(ls_dir):

            # cria o diretório
            os.mkdir(ls_dir)

        # create airspace
        self.__airspace = airs.CAirspacePiloto(self)
        assert self.__airspace

        # carrega as tabelas do sistema
        self.__airspace.load_dicts()

        # logger
        # M_LOG.info("__load_air:<<")

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------

    def __load_cenario(self):
        """
        abre/cria as tabelas do sistema

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("__load_cenario:>>")

        # carrega o airspace
        lv_ok, ls_msg = self.__load_air()

        # houve erro em alguma fase ?
        if not lv_ok:

            # logger
            l_log = logging.getLogger("CModelPiloto::__load_cenario")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: Erro na carga da base de dados {}.".format(ls_msg))

            # cria um evento de quit
            l_evt = event.CQuit()
            assert l_evt

            # dissemina o evento
            self.event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # logger
        # M_LOG.info("__load_cenario:<<")

    # ---------------------------------------------------------------------------------------------
    '''
    def load_land(self, fs_land):
        """
        faz a carga do landscape.

        @param ls_cena: cenário.

        @return flag e mensagem.
        """
        # obtém o diretório padrão de landscapes
        ls_dir = self.dct_config["dir.map"]

        # nome do diretório vazio ?
        if ls_dir is None:

            # diretório padrão de landscapes
            self.dct_config["dir.map"] = "maps"

            # diretório padrão de landscapes
            ls_dir = "maps"

        # expand user (~)
        ls_dir = os.path.expanduser(ls_dir)

        # diretório não existe ?
        if not os.path.exists(ls_dir):

            # cria o diretório
            os.mkdir(ls_dir)

        # create landscape
        self.__landscape = landscape.modelLandscape(self, ls_dir, fs_land)
        assert self.__landscape

        # retorna ok
        return True, None
    '''
    # ---------------------------------------------------------------------------------------------

    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos.

        @param f_event: evento recebido.
        """
        pass

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def airspace(self):
        """
        airspace
        """
        return self.__airspace

    # ---------------------------------------------------------------------------------------------

    @property
    def lst_arr_dep(self):
        """
        get lista de pousos/decolagens
        """
        return self.__airspace.lst_arr_dep

    # ---------------------------------------------------------------------------------------------

    @property
    def coords(self):
        """
        get coordinate system
        """
        return self.__coords

    '''@coords.setter
    def coords(self, f_val):
        """
        set coordinate system
        """
        self.__coords = f_val'''

    # ---------------------------------------------------------------------------------------------

    @property
    def emula_model(self):
        """
        flight model
        """
        return self.__emula_model

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_esp(self):
        """
        get dicionário de esperas
        """
        return self.__airspace.dct_esp

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_fix(self):
        """
        get dicionário de fixos
        """
        return self.__airspace.dct_fix

    # ---------------------------------------------------------------------------------------------
    '''
    @property
    def landscape(self):
        """
        landscape
        """
        return self.__landscape
    '''
    # ---------------------------------------------------------------------------------------------

    @property
    def dct_prf(self):
        """
        get dicionário de performances
        """
        return self.__dct_prf

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_sub(self):
        """
        get dicionário de subidas
        """
        return self.__airspace.dct_sub

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_trj(self):
        """
        get dicionário de trajetórias
        """
        return self.__airspace.dct_trj

# < the end >--------------------------------------------------------------------------------------
