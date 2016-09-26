#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
model_wizard.

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
import os
import sys

# model
import model.model_manager as model

import model.items.exe_data as exedata

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CModelWizard >---------------------------------------------------------------------------

class CModelWizard(model.CModelManager):
    """
    modelo do wizard.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control):
        """
        @param f_control: control manager.
        """
        # logger
        # M_LOG.info("__init__:>>")
                
        # check input parameters
        assert f_control

        # init super class
        super(CModelWizard, self).__init__(f_control)

        # herdados de CModelManager
        # self.control       # control manager
        # self.event         # event manager
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração

        # obtém o event manager
        # self.event = f_control.event
        # assert self.event

        # inicia variáveis de instância
        self.__dct_exe = {}

        # carrega as tabelas do sistema
        lv_ok = self.__load_tables()

        # M_LOG.debug("dct_exe:[{}]".format(self.__dct_exe))

        # houve erro em alguma fase ?
        if not lv_ok:

            # logger
            l_log = logging.getLogger("CModelWizard::__init__")
            l_log.setLevel(logging.NOTSET)
            l_log.critical(u"<E01: Erro na carga da base de dados.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # logger
        # M_LOG.info("__init__:<<")
                
    # ---------------------------------------------------------------------------------------------

    def __load_tables(self):
        """
        abre/cria as tabelas do sistema.

        @return flag e mensagem.
        """
        # logger
        # M_LOG.info("__load_tables:>>")
                
        # carrega a tabela de exercícios
        lv_ok = self.load_table_exe()

        if lv_ok:

            # carrega a tabela de tráfegos
            # lv_ok = self.load_table_anv()
            pass

        # logger
        # M_LOG.info("__load_tables:<<")
                
        # return
        return True

    # ---------------------------------------------------------------------------------------------

    def load_table_exe(self):
        """
        faz a carga da tabela de exercícios.
        """
        # logger
        # M_LOG.info("load_table_exe:>>")
                
        # obtém o diretório padrão de exercícios
        ls_dir = self.dct_config["dir.exe"]
        # M_LOG.debug("ls_dir:[{}]".format(ls_dir))

        # nome do diretório vazio ?
        if ls_dir is None:

            # diretório padrão de exercícios
            ls_dir = self.dct_config["dir.exe"] = gdefs.D_DIR_EXE

        # diretório não existe ?
        if not os.path.exists(ls_dir):

            # cria o diretório
            os.mkdir(ls_dir)

        # logger
        # M_LOG.debug(u"Carregando diretório:[{}]".format(ls_dir))

        # percorre o diretório
        for ls_file in os.listdir(ls_dir):

            # monta o path completo do arquivo de exercício
            ls_path = os.path.join(ls_dir, ls_file)
            # M_LOG.debug("ls_path:[{}]".format(ls_path))

            # não é um arquivo ?
            if not os.path.isfile(ls_path):

                # passa ao próximo
                continue

            # split name and extension
            _, l_fext = os.path.splitext(ls_file)
            # M_LOG.debug("l_fext:[{}]".format(l_fext))

            # não é um arquivo XML ?
            if ".xml" != l_fext:

                # passa ao próximo
                continue

            # cria um dicionário de exercícios
            ldct_exe = exedata.CExeData(self, ls_path)
            # M_LOG.debug("ldct_exe:[{}]".format(ldct_exe))

            if ldct_exe is None:

                # logger
                l_log = logging.getLogger("CModelWizard::load_table_exe")
                l_log.setLevel(logging.NOTSET)
                l_log.warning(u"<E01: tabela de exercícios não existe.")

                # cai fora...
                return False

            # salva no dicionário
            self.__dct_exe.update(ldct_exe)

        # logger
        # M_LOG.info("load_table_exe:<<")
                
        # retorna
        return True

    # ---------------------------------------------------------------------------------------------

    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos.

        @param f_event: evento recebido.
        """
        # logger
        # M_LOG.info("notify:>>")
                
        # recebeu um evento de "save to disk" ?
        if isinstance(f_event, events.CSave2Disk):
            pass

        # logger
        # M_LOG.info("notify:<<")
                
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_exe(self):
        """
        get dicionário de exercícios
        """
        return self.__dct_exe

    @dct_exe.setter
    def dct_exe(self, f_val):
        """
        get dicionário de exercícios
        """
        self.__dct_exe = f_val

# < the end >--------------------------------------------------------------------------------------
