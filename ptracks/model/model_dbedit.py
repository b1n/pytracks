#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_dbedit.

model manager do editor da base de dados.

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
from . import model_manager as model
from .newton import airspace_newton as airs

from .coords import coord_sys as coords

# import model.items.aer_data as aerdata
from .items import exe_data as exedata
# import model.items.fix_data as fixdata
from .items import prf_data as prfdata
# import model.items.sen_data as sendata
from .items import trf_data as trfdata
# import model.items.trj_data as trjdata

# control
from ..control.events import events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CModelDBEdit >---------------------------------------------------------------------------

class CModelDBEdit(model.CModelManager):
    """
    DBEdit model object. Views and controllers interact with this.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control):
        """
        constructor.
        cria o model object do editor da base de dados.

        @param f_control: control manager.
        @param fs_dbname: pathname da base de dados.
        """
        # verifica parâmetros de entrada
        assert f_control

        # init super class
        super(CModelDBEdit, self).__init__(f_control)

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

        # obtém o event manager
        # self.event = f_control.event
        # assert self.event

        # exercício
        self.__exe = None

        # dicionário de exercícios
        self.__dct_exe = {}

        # dicionário de performances
        self.__dct_prf = {}

        # dicionário de sensores
        self.__dct_sen = {}

        # dicionário de tráfegos
        self.__dct_trf = {}

        # carrega as tabelas do sistema
        self.__load_airs()

        # carrega as tabelas do sistema
        lv_ok = self.__load_tables()

        # houve erro em alguma fase ?
        if not lv_ok:

            # logger
            l_log = logging.getLogger("CModelDBEdit::__init__")
            l_log.setLevel(logging.NOTSET)
            l_log.critical(u"<E01: Erro na carga da base de dados.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self._event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------

    def get_ptr_prc(self, fs_prc):
        """
        DOCUMENT ME!
        """
        return None, 0

    # ---------------------------------------------------------------------------------------------

    def __load_airs(self):
        """
        faz a carga do airspace.

        @return flag e mensagem.
        """
        # logger
        # M_LOG.info("__load_airs:>>")

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

        # carrega os dicionários
        self.__airspace.load_dicts()

        # logger
        # M_LOG.info("__load_airs:<<")

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------

    def __load_tables(self):
        """
        abre/cria as tabelas do sistema.

        @return flag e mensagem.
        """
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

        # M_LOG.debug("QtdTrf: " + str(self.exe.iExeQtdTrf))
        '''
        # carrega a tabela de aeródromos
        lv_ok = self.load_aers()

        if lv_ok:
            # carrega a tabela de fixos
            lv_ok = self.load_fixs()

            if lv_ok:
                # carrega a tabela de performances
                lv_ok = self.load_prfs()

                if lv_ok:
                    # carrega a tabela de sensores
                    lv_ok = self.load_rads()

                    if lv_ok:
                        # carrega a tabela de exercícios
                        lv_ok = self.load_exes()
        '''
        # retorna
        return True  # lv_ok

    # ---------------------------------------------------------------------------------------------

    def load_exes(self):
        """
        faz a carga da tabela de exercícios.
        """
        # obtém o diretório padrão de exercícios
        ls_dir = self.dct_config["dir.exe"]
        # M_LOG.debug("ls_dir: " + str(ls_dir))

        # nome do diretório vazio ?
        if ls_dir is None:

            # diretório padrão de tabelas
            ls_dir = self.dct_config["dir.exe"] = "exes"

        # diretório não existe ?
        if not os.path.exists(ls_dir):

            # cria o diretório
            os.mkdir(ls_dir)

        # logger
        # M_LOG.debug(u"Carregando diretório: " + str(ls_dir))

        # percorre o diretório
        for ls_file in os.listdir(ls_dir):

            # monta o path completo do arquivo de exercício
            ls_path = os.path.join(ls_dir, ls_file)
            # M_LOG.debug("ls_path: " + str(ls_path))

            # não é um arquivo ?
            if not os.path.isfile(ls_path):

                # passa ao próximo
                continue

            # split name and extension
            _, l_fext = os.path.splitext(ls_file)
            # M_LOG.debug("l_fn...: " + str(l_fn))
            # M_LOG.debug("l_fext.: " + str(l_fext))

            # não é um arquivo XML ?
            if ".xml" != l_fext:

                # passa ao próximo
                continue

            # cria um dicionário de exercícios
            ldct_exe = exedata.CExeData(self, ls_path)
            # M_LOG.debug("dct_exe: " + str(ldct_exe))

            if ldct_exe is None:

                # logger
                l_log = logging.getLogger("CModelDBEdit::load_exes")
                l_log.setLevel(logging.NOTSET)
                l_log.warning("<E01: tabela de exercícios:[{}] não existe.".format(ls_path))

                # cai fora...
                return False

            # salva no dicionário
            self.__dct_exe.update(ldct_exe)

        # retorna
        return True

    # ---------------------------------------------------------------------------------------------

    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos.

        @param f_event: evento recebido.
        """
        # recebeu um evento de "save to disk" ?
        if isinstance(f_event, events.CSave2Disk):

            # salvar tabela de aeródromos ?
            if "AER" == f_event.table.upper():

                # salva a tabela de aeródromos
                self.dct_aer.save2disk()

            # salvar tabela de fixos ?
            elif "FIX" == f_event.table.upper():

                # salva a tabela de fixos
                self.dct_fix.save2disk()

            # salvar tabela de performances ?
            elif "PRF" == f_event.table.upper():

                # salva a tabela de performances
                self.__dct_prf.save2disk()
        '''
            # salvar tabela de aeronaves ?
            elif "ANV" == f_event.table.upper():

                # salva a tabela de aeronaves
                self.dct_anv.save2disk()

            # salvar tabela de esperas ?
            elif "ESP" == f_event.table.upper():

                # salva a tabela de esperas
                self.dct_esp.save2disk()

            # salvar tabela de exercícios ?
            elif "EXE" == f_event.table.upper():

                # salva a tabela de exercícios
                self.__dct_exe.save2disk()

            # salvar tabela de figuras ?
            elif "FIG" == f_event.table.upper():

                # salva a tabela de figuras
                self.dct_fig.save2disk()

            # salvar tabela de navegações ?
            elif "NAV" == f_event.table.upper():

                # salva a tabela de navegações
                self.dct_Nav.save2disk()

            # salvar tabela de pontos no solo ?
            elif "PNS" == f_event.table.upper():

                # salva a tabela de pontos no solo
                self.dct_pNS.save2disk()

            # salvar tabela de procedimentos ?
            elif "PRC" == f_event.table.upper():

                # salva a tabela de procedimentos
                self.dct_prc.save2disk()

            # salvar tabela de pistas ?
            elif "PST" == f_event.table.upper():

                # salva a tabela de pistas
                self.dct_pst.save2disk()

            # salvar tabela de trajetórias ?
            elif "TRJ" == f_event.table.upper():

                # salva a tabela de trajetórias
                self.__dct_trj.save2disk()
        '''
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
    def exe(self):
        """
        get exercício
        """
        return self.__exe

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_esp(self):
        """
        get esperas
        """
        return self.__airspace.dct_esp

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_exe(self):
        """
        dicionário de exercícios
        """
        return self.__dct_exe

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_prf(self):
        """
        get performances
        """
        return self.__dct_prf

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_sen(self):
        """
        dicionário de sensores
        """
        return self.__dct_sen

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
