#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
trj_new

mantém as informações sobre um procedimento de trajetória

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
import sys

# model
import model.items.prc_model as model
import model.items.brk_new as brktrj

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CTrjNEW >--------------------------------------------------------------------------------

class CTrjNEW(model.CPrcModel):
    """
    mantém as informações específicas sobre procedimento de trajetória.

    <trajetoria nTrj="1">
        <descricao>DEP SDJD VIA SCB</descricao>
        <star>S</star>
        <proa>123</proa>

        <breakpoint nBrk="1">
            <coord>
                <tipo>D</tipo>
                <campoA>0964</campoA>
                <campoB>06</campoB>
                <campoC>247</campoC>
            </coord>
            <altitude>3500</altitude>
            <velocidade>160</velocidade>
        </breakpoint>
    </trajetoria>
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_data=None, fs_ver="0001"):
        """
        @param f_model: model manager
        @param f_data: dados do procedimento de trajetória
        @param fs_ver: versão do formato
        """
        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CTrjNEW, self).__init__()

        # salva o model manager localmente
        self.__model = f_model
        assert self.__model

        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # herdado de CPrcModel
        # self.v_prc_ok      # (bool)
        # self.i_prc_id      # identificação do procedimento de trajetória
        # self.s_prc_desc    # descrição do procedimento de trajetória

        # star
        self.__v_trj_star = False

        # proa a seguir após a trajetória
        self.__f_trj_proa = 0.

        # lista de breakpoints da trajetória
        self.__lst_trj_brk = []

        # recebeu dados ?
        if f_data is not None:

            # recebeu uma lista ?
            if isinstance(f_data, dict):

                # cria uma procedimento de trajetória com os dados da lista
                self.__load_trj(f_data, fs_ver)

            # recebeu uma procedimento de trajetória ?
            elif isinstance(f_data, CTrjNEW):

                # copia a procedimento de trajetória
                self.copy_trj(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def copy_trj(self, f_trj):
        """
        copy constructor.
        cria uma nova procedimento de trajetória a partir de uma outra procedimento de trajetória.

        @param f_trj: procedimento de trajetória a ser copiada.
        """
        # logger
        # M_LOG.info("copy_trj:>>")

        # verifica parâmetros de entrada
        assert f_trj

        # copy super class attributes
        super(CTrjNEW, self).copy_trj(f_trj)

        # flag star
        self.__v_trj_star = f_trj.v_trj_star

        # lista de breakpoints
        self.__lst_trj_brk = list(f_trj.lst_trj_brk)

        # logger
        # M_LOG.info("copy_trj:<<")

    # ---------------------------------------------------------------------------------------------

    def __load_trj(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados de procedimento de trajetória a partir de um dicionário (formato 0001).

        @param fdct_data: dicionário com os dados do procedimento de trajetória.
        @param fs_ver: versão do formato dos dados.
        """
        # logger
        # M_LOG.info("__load_trj:>>")

        # formato versão 0.01 ?
        if "0001" == fs_ver:

            # cria a procedimento de trajetória
            self.__make_trj(fdct_data)

        # senão, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CTrjNEW::__load_trj")
            l_log.setLevel(logging.DEBUG)
            l_log.critical(u"__load_trj:<E01: formato desconhecido.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

        # logger
        # M_LOG.info("__load_trj:<<")

    # ---------------------------------------------------------------------------------------------

    def __make_trj(self, fdct_data):
        """
        carrega os dados de procedimento de trajetória a partir de um dicionário (formato 0001).

        @param fdct_data: dicionário com os dados do procedimento de trajetória.
        """
        # logger
        # M_LOG.info("__make_trj:>>")

        # identificação do procedimento de trajetória
        if "nTrj" in fdct_data:
            self.i_prc_id = int(fdct_data["nTrj"])
            # M_LOG.debug("self.i_prc_id: " + str(self.i_prc_id))

        # descrição
        if "descricao" in fdct_data:
            self.s_prc_desc = fdct_data["descricao"]
            # M_LOG.debug("self.s_prc_desc: " + str(self.s_prc_desc))

        # star
        if "star" in fdct_data:
            self.__v_trj_star = ('S' == fdct_data["star"].strip().upper())
            # M_LOG.debug("self.__v_trj_star: " + str(self.__v_trj_star))

        # proa
        if "proa" in fdct_data:
            self.__f_trj_proa = ('S' == fdct_data["proa"].strip().upper())
            # M_LOG.debug("self.__f_trj_proa: " + str(self.__f_trj_proa))

        # breakpoints da trajetória
        if "breakpoints" in fdct_data:

            # para todos breakpoints da trajetória...
            for l_brk in sorted(fdct_data["breakpoints"], key=lambda l_k: l_k["nBrk"]):

                # cria o breakpoint
                lo_brk = brktrj.CBrkNEW(self.__model, self, l_brk)
                assert lo_brk

                # coloca o breakpoint na lista
                self.__lst_trj_brk.append(lo_brk)

        # (bool)
        self.v_prc_ok = True

        # logger
        # M_LOG.info("__make_trj:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def lst_trj_brk(self):
        """
        get lista de breakpoints da trajetória
        """
        return self.__lst_trj_brk

    @lst_trj_brk.setter
    def lst_trj_brk(self, f_val):
        """
        set lista de breakpoints da trajetória
        """
        self.__lst_trj_brk = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_trj_proa(self):
        """
        get proa a seguir após a trajetória
        """
        return self.__f_trj_proa

    @f_trj_proa.setter
    def f_trj_proa(self, f_val):
        """
        set proa a seguir após a trajetória
        """
        # verifica parâmetros de entrada
        assert 0. <= f_val <= 360.

        # salva proa
        self.__f_trj_proa = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def v_trj_star(self):
        """
        get flag star
        """
        return False  # self.__v_trj_star

    @v_trj_star.setter
    def v_trj_star(self, f_val):
        """
        set flag star
        """
        self.__v_trj_star = f_val

# < the end >--------------------------------------------------------------------------------------
