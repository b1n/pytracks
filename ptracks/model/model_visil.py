#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_visil.

DOCUMENT ME!

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2015/fev  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os
import sys

# model
from . import glb_defs as gdefs
from . import model_manager as model

from .coords import coord_sys as coords
from .emula import emula_visil as emula
from .visil import airspace_visil as airs
# import model.visil.landscape as lands

# control
from ..control.events import events_basic as event

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CModelVisil >----------------------------------------------------------------------------

class CModelVisil(model.CModelManager):
    """
    visir model object.
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
        super(CModelVisil, self).__init__(f_control)

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
        self.__landscape = None

        # carrega as tabelas do sistema
        self.__load_cenario("SBSP")

        # create emula model
        self.__emula_model = emula.CEmulaVisil(self, f_control)
        assert self.__emula_model

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __load_cenario(self, fs_cena):
        """
        abre/cria as tabelas do sistema.

        @param fs_cena: cenário.

        @return flag e mensagem.
        """
        # logger
        # M_LOG.info("__load_cenario:>>")

        # carrega o landscape
        lv_ok, ls_msg = self.__load_land(fs_cena)

        # tudo Ok ?
        if lv_ok:

            # carrega o airspace
            lv_ok, ls_msg = self.__load_air(fs_cena)

        # houve erro em alguma fase ?
        if not lv_ok:

            # logger
            l_log = logging.getLogger("CModelVisil::__load_cenario")
            l_log.setLevel(logging.NOTSET)
            l_log.critical(u"<E01: Erro na carga da base de dados ({}).".format(ls_msg))

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

    def __load_air(self, fs_cena):
        """
        faz a carga do airspace.

        @param fs_cena: cenário.

        @return flag e mensagem.
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
        ls_dir = os.path.expanduser(ls_dir)

        # diretório não existe ?
        if not os.path.exists(ls_dir):

            # cria o diretório
            os.mkdir(ls_dir)

        # create airspace
        self.__airspace = airs.CAirspaceVisil(self, fs_cena)
        assert self.__airspace

        # carrega os dicionários
        self.__airspace.load_dicts()

        # logger
        # M_LOG.info("__load_air:<<")

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------

    def __load_land(self, fs_cena):
        """
        faz a carga do landscape.

        @param fs_cena: cenário.

        @return flag e mensagem.
        """
        # logger
        # M_LOG.info("__load_land:>>")

        # obtém o diretório padrão de landscapes
        ls_dir = self.dct_config["dir.map"]

        # nome do diretório vazio ?
        if ls_dir is None:

            # diretório padrão de landscapes
            self.dct_config["dir.map"] = gdefs.D_DIR_MAP

            # diretório padrão de landscapes
            ls_dir = gdefs.D_DIR_MAP

        # expand user (~)
        ls_dir = os.path.expanduser(ls_dir)

        # diretório não existe ?
        if not os.path.exists(ls_dir):

            # cria o diretório
            os.mkdir(ls_dir)

        # create landscape
        # self.__landscape = lands.CLandscape(self, ls_dir, fs_cena)
        # assert self.__landscape

        # logger
        # M_LOG.info("__load_land:<<")

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------

    def notify(self, f_evt):
        """
        callback de tratamento de eventos recebidos.

        @param f_evt: evento recebido.
        """
        # logger
        # M_LOG.info("notify:><")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def airspace(self):
        """
        get airspace
        """
        return self.__airspace

    # ---------------------------------------------------------------------------------------------

    @property
    def coords(self):
        """
        get coordinate system
        """
        return self.__coords

    @coords.setter
    def coords(self, f_val):
        """
        set coordinate system
        """
        self.__coords = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def emula_model(self):
        """
        get emula model
        """
        return self.__emula_model

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_esp(self):
        """
        get esperas
        """
        return self.__airspace.dct_esp

    # ---------------------------------------------------------------------------------------------

    @property
    def landscape(self):
        """
        get landscape
        """
        return self.__landscape

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_sub(self):
        """
        get subidas
        """
        return self.__airspace.dct_sub

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_trj(self):
        """
        get trajetórias
        """
        return self.__airspace.dct_trj

# < the end >--------------------------------------------------------------------------------------
