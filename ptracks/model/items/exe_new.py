#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------------------------
exe_new.

mantém as informações sobre um exercício.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
-------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import sys

# model
from . import exe_model as model

# control
from ...control.events import events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CExeNEW >--------------------------------------------------------------------------------

class CExeNEW(model.CExeModel):
    """
    mantém as informações sobre um exercício.

    <exercicio nExe="SBSP5301">
        <descricao>PBN 2013 INTEGRADO RJ E SP 17/09/15/15</descricao>
        <horainicio>06:00</horainicio>
    </exercicio>
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_data=None, fs_ver="0001"):
        """
        @param f_event: event manager.
        @param f_data: dados do exercício.
        @param fs_ver: versão do formato.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CExeNEW, self).__init__()

        # salva o model manager localmente
        self.__model = f_model
        assert self.__model
                        
        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # herdado de CExeModel
        # self.v_exe_ok      # ok (bool)
        # self.s_exe_id      # identificação
        # self.s_exe_desc    # descrição

        # horário inicial (HORA)
        self.__t_exe_hor_ini = (0, 0, 0)

        # horário atual (HORA)
        self.__i_exe_hor_atu = 0

        # estado (bool) (T = congelado / F = descongelado)
        self.__v_exe_congelado = True

        # velocidade do exercício (float)
        self.__f_exe_vel_exe = 1.

        # dicionário de tráfegos
        self.__dct_exe_trf = {}

        # recebeu dados ?
        if f_data is not None:

            # recebeu um dicionário ?
            if isinstance(f_data, dict):

                # carrega o exercício com os dados do dicionário
                self.load_exe(f_data, fs_ver)

            # recebeu um exercício ?
            elif isinstance(f_data, CExeNEW):

                # copia o exercício
                self.copy_exe(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy_exe(self, f_exe):
        """
        copy constructor.
        cria um novo exercício a partir de um outro exercício.

        @param f_exe: exercício a ser copiado.

        @return flag e mensagem.
        """
        # logger
        # M_LOG.info("copy_exe:>>")

        # copy super class attributes
        super(CExeNEW, self).copy_exe(f_exe)

        # horário inicial (HORA)
        self.__t_exe_hor_ini = f_exe.t_exe_hor_ini

        # horário atual (HORA)
        self.__i_exe_hor_atu = f_exe.i_exe_hor_atu

        # estado (bool) (T = congelado / F = descongelado)
        self.__v_exe_congelado = f_exe.v_exe_congelado

        # velocidade do exercício (float)
        self.__f_exe_vel_exe = f_exe.f_exe_vel_exe

        # logger
        # M_LOG.info("copy_exe:<<")

    # ---------------------------------------------------------------------------------------------

    def load_exe(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados do exercício a partir de um dicionário.

        @param fdct_data: dicionário de dados de exercício.
        @param fs_ver: versão do formato dos dados.
        """
        # logger
        # M_LOG.info("load_exe:>>")

        # formato versão 0.01 ?
        if "0001" == fs_ver:

            # cria o exercício
            self.make_exe(fdct_data)

        # senão, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CExeNEW::load_exe")
            l_log.setLevel(logging.NOTSET)
            l_log.critical(u"<E01: formato desconhecido [{}].".format(fs_ver))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

        # (bool)
        self.v_exe_ok = True

        # logger
        # M_LOG.info("load_exe:<<")

    # ---------------------------------------------------------------------------------------------

    def make_exe(self, fdct_data):
        """
        carrega os dados do exercício a partir de um dicionário (formato 0001).

        @param fdct_data: dicionário com os dados do exercício.
        """
        # logger
        # M_LOG.info("make_exe:>>")

        # M_LOG.debug("fdct_data: " + str(fdct_data))

        # identificação do exercício
        if "nExe" in fdct_data:
            self.s_exe_id = fdct_data["nExe"].strip()
            # M_LOG.debug("self.s_exe_id: " + str(self.s_exe_id))

        # descrição
        if "descricao" in fdct_data:
            self.s_exe_desc = fdct_data["descricao"]
            # M_LOG.debug("self.s_exe_desc: " + str(self.s_exe_desc))

        # hora inicial
        if "horainicio" in fdct_data:
            ls_hora = fdct_data["horainicio"].strip().upper()
            # M_LOG.debug("ls_hora: " + str(ls_hora))

            li_hor = int(ls_hora[:2])
            # M_LOG.debug("li_hor: " + str(li_hor))

            li_min = int(ls_hora[3:])
            # M_LOG.debug("li_min: " + str(li_min))

            # horário inicial (HORA)
            self.__t_exe_hor_ini = (li_hor, li_min, 0)
            # M_LOG.debug("self.t_exe_hor_ini: " + str(self.__t_exe_hor_ini))

            # horário atual (HORA)
            self.__i_exe_hor_atu = ((li_hor * 60) + li_min) * 60
            # M_LOG.debug("self.i_exe_hor_atu: " + str(self.__i_exe_hor_atu))

        # status ok
        self.__v_exe_congelado = True
        self.v_exe_ok = True

        # logger
        # M_LOG.info("make_exe:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def v_exe_congelado(self):
        """
        get estado do exercício
        """
        return self.__v_exe_congelado

    @v_exe_congelado.setter
    def v_exe_congelado(self, f_val):
        """
        set estado do exercício
        """
        self.__v_exe_congelado = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def i_exe_hor_atu(self):
        """
        get hora atual do exercício
        """
        return self.__i_exe_hor_atu

    @i_exe_hor_atu.setter
    def i_exe_hor_atu(self, f_val):
        """
        set hora atual do exercício
        """
        self.__i_exe_hor_atu = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def t_exe_hor_ini(self):
        """
        get hora inicial do exercício
        """
        return self.__t_exe_hor_ini

    @t_exe_hor_ini.setter
    def t_exe_hor_ini(self, f_val):
        """
        set hora inicial do exercício
        """
        self.__t_exe_hor_ini = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def i_exe_qtd_trf(self):
        """
        get quantidade de tráfegos
        """
        return len(self.__dct_exe_trf)

    # ---------------------------------------------------------------------------------------------

    @property
    def s_exe_tipo(self):
        """
        get tipo de exercício
        """
        return "newton"

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_exe_trf(self):
        """
        get tráfegos do exercício
        """
        return self.__dct_exe_trf

    @dct_exe_trf.setter
    def dct_exe_trf(self, f_val):
        """
        set tráfegos do exercício
        """
        self.__dct_exe_trf = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_exe_vel_exe(self):
        """
        get velocidade do exercício
        """
        return self.__f_exe_vel_exe

    @f_exe_vel_exe.setter
    def f_exe_vel_exe(self, f_val):
        """
        set velocidade do exercício
        """
        self.__f_exe_vel_exe = f_val

# < the end >--------------------------------------------------------------------------------------
