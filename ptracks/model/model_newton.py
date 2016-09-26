#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_newton

DOCUMENT ME!

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
import os.path

# model
from . import model_manager as model

from .coords import coord_sys as coords
from .emula import emula_newton as emula

from .items import exe_data as exedata
from .items import prf_data as prfdata
from .items import trf_data as trfdata

from .newton import airspace_newton as airs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CModelNewton >----------------------------------------------------------------------------

class CModelNewton(model.CModelManager):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control):
        """
        @param  f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CModelNewton, self).__init__(f_control)

        # herdados de CModelManager
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager

        # obtém as coordenadas de referência
        lf_ref_lat = self.dct_config["map.lat"]
        lf_ref_lng = self.dct_config["map.lng"]
        lf_dcl_mag = self.dct_config["map.dcl"]
                                
        # coordinate system
        self.__coords = coords.CCoordSys(lf_ref_lat, lf_ref_lng, lf_dcl_mag)
        assert self.__coords
                                                        
        # airspace
        self.__airspace = None

        # dicionário de performances
        self.__dct_prf = {}

        # dicionário de tráfegos
        self.__dct_trf = {}

        # exercício
        self.__exe = None

        # carrega o cenário de simulação (airspace & landscape)
        self.__load_cenario()

        # carrega as tabelas (base de dados)
        self.__load_dicts()

        # create flight emulation model
        self.__emula_model = emula.CEmulaNewton(self, f_control)
        assert self.__emula_model

        # set as daemon
        self.__emula_model.daemon = True

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
        ls_dir = os.path.expanduser(ls_dir)

        # diretório não existe ?
        if not os.path.exists(ls_dir):

            # cria o diretório
            os.mkdir(ls_dir)

        # create airspace
        self.__airspace = airs.CAirspaceNewton(self)
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
            l_log = logging.getLogger("CModelNewton::__load_cenario")
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

    def __load_dicts(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__load_dicts:>>")

        # monta o nome da tabela de performances
        ls_path = os.path.join(self.dct_config["dir.tab"], self.dct_config["tab.prf"])

        # carrega a tabela de performance em um dicionário
        self.__dct_prf = prfdata.CPrfData(self, ls_path)
        assert self.__dct_prf is not None

        # monta o nome do arquivo de exercício
        ls_path = os.path.join(self.dct_config["dir.exe"], self.dct_config["glb.exe"])

        # carrega o exercício em um dicionário
        ldct_exe = exedata.CExeData(self, ls_path + ".exe.xml")
        assert ldct_exe is not None

        # obtém o exercício
        self.__exe = ldct_exe[self.dct_config["glb.exe"]]
        assert self.__exe

        # monta o nome do arquivo de tráfegos
        ls_path = os.path.join(self.dct_config["dir.trf"], self.dct_config["glb.exe"])

        # carrega a tabela de tráfegos do exercício
        self.__dct_trf = trfdata.CTrfData(self, ls_path, self.__exe)
        assert self.__dct_trf is not None

        # coloca a tabela de tráfegos no exercício
        self.__exe.dct_exe_trf = self.__dct_trf

        # logger
        # M_LOG.info("__load_dicts:<<")

    # =============================================================================================
    # data
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
    def exe(self):
        """
        get exercício
        """
        return self.__exe

    # ---------------------------------------------------------------------------------------------

    @property
    def lst_arr_dep(self):
        """
        get pousos/decolagens
        """
        return self.__airspace.lst_arr_dep

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_esp(self):
        """
        get esperas
        """
        return self.__airspace.dct_esp

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_fix(self):
        """
        get fixos
        """
        return self.__airspace.dct_fix

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_prf(self):
        """
        get performances
        """
        return self.__dct_prf

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_sub(self):
        """
        get subidas
        """
        return self.__airspace.dct_sub

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_trf(self):
        """
        get tráfegos
        """
        return self.__dct_trf

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_trj(self):
        """
        get trajetórias
        """
        return self.__airspace.dct_trj

# < the end >--------------------------------------------------------------------------------------
