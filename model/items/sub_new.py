#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
sub_new.

mantém as informações sobre um procedimento de subida do TrackS.

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
import model.items.brk_new as brknew

# control
import control.events.events_basic as event

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CSubNEW >--------------------------------------------------------------------------------

class CSubNEW(model.CPrcModel):
    """
    mantém as informações específicas sobre procedimento de subida.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_data=None, fs_ver="0001"):
        """
        @param f_model: model manager.
        @param f_data: dados do procedimento de subida.
        @param fs_ver: versão do formato.
        """
        # init super class
        super(CSubNEW, self).__init__()

        # salva o model manager localmente
        self.__model = f_model
        assert self.__model

        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # herdados de CPrcModel
        # self.v_prc_ok      # (bool)
        # self.i_prc_id      # identificação do procedimento de subida
        # self.s_prc_desc    # descrição do procedimento de subida (nome)

        # pointer para o aeródromo da subida
        self.__ptr_sub_aer = None
        # pointer para a pista da subida
        self.__ptr_sub_pis = None

        # procedimento de decolagem associado
        self.__ptr_sub_prc_dec = None

        # lista de breakpoints da subida
        self.__lst_sub_brk = []

        # recebeu dados ?
        if f_data is not None:

            # recebeu uma lista ?
            if isinstance(f_data, dict):

                # cria uma procedimento de subida com os dados da lista
                self.__load_sub(f_data, fs_ver)

            # recebeu uma procedimento de subida ?
            elif isinstance(f_data, CSubNEW):

                # copia a procedimento de subida
                self.copy_sub(f_data)

    # ---------------------------------------------------------------------------------------------

    def copy_sub(self, f_sub):
        """
        copy constructor.
        cria um novo procedimento de subida a partir de um outro procedimento de subida.

        @param f_sub: procedimento de subida a ser copiado.
        """
        # verifica parâmetros de entrada
        assert f_sub

        # init super class
        super(CSubNEW, self).__init__()

        # pointer para o aeródromo da subida
        self.__ptr_sub_aer = f_sub.ptr_sub_aer

        # pointer para a pista da subida
        self.__ptr_sub_pis = f_sub.ptr_sub_pis

        # procedimento de decolagem associado
        self.__ptr_sub_prc_dec = f_sub.ptr_sub_prc_dec

        # lista de breakpoints da subida
        self.__lst_sub_brk = list(f_sub.lst_sub_brk)

    # ---------------------------------------------------------------------------------------------

    def __load_sub(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados de procedimento de subida a partir de um dicionário (formato 0001).

        @param fdct_data: dicionário com os dados do procedimento de subida.
        @param fs_ver:    versão do formato dos dados.
        """
        # formato versão 0.01 ?
        if "0001" == fs_ver:

            # cria a procedimento de subida
            self.__make_sub(fdct_data)

        # senão, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CSubNEW::__load_sub")
            l_log.setLevel(logging.NOTSET)
            l_log.critical(u"<E01: formato desconhecido.")

            # cria um evento de quit
            l_evt = event.Quit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------

    def __make_sub(self, fdct_data):
        """
        carrega os dados de procedimento de subida a partir de um dicionário (formato 0001).

        @param fdct_data: dicionário com os dados do procedimento de subida.
        """
        # identificação do procedimento de subida
        if "nSub" in fdct_data:
            self.i_prc_id = int(fdct_data["nSub"])
            # M_LOG.debug("self.i_prc_id: " + str(self.i_prc_id))

        # descrição
        if "nome" in fdct_data:
            self.s_prc_desc = fdct_data["nome"]
            # M_LOG.debug("self.s_prc_desc: " + str(self.s_prc_desc))

        # aeródromo da subida
        if "aerodromo" in fdct_data:

            # obtém o dicionário de aeródromos
            ldct_aer = self.__model.airspace.dct_aer

            # obtém o indicativo do aeródromo
            ls_aer_id = fdct_data["aerodromo"]
            # M_LOG.debug("ls_aer_id: " + str(ls_aer_id))

            # obtém o aeródromo do subida
            self.__ptr_sub_aer = ldct_aer.get(ls_aer_id, None)

            # não existe o aeródromo no dicionário ?
            if self.__ptr_sub_aer is None:

                # logger
                l_log = logging.getLogger("CSubNEW::__make_sub")
                l_log.setLevel(logging.NOTSET)
                l_log.warning("aerodromo:[%s] não existe no dicionário", ls_aer_id)

        # pista do subida
        if "pista" in fdct_data:

            # existe o aeródromo ?
            if self.__ptr_sub_aer is not None:

                # obtém o dicionário de pistas
                ldct_pis = self.__ptr_sub_aer.dct_aer_pistas

                # obtém o indicativo do aeródromo
                ls_pis_id = fdct_data["pista"]
                # M_LOG.debug("ls_pis_id: " + str(ls_pis_id))

                # obtém o pista do subida
                self.__ptr_sub_pis = ldct_pis.get(ls_pis_id, None)

                # não existe a pista no dicionário ?
                if self.__ptr_sub_pis is None:

                    # logger
                    l_log = logging.getLogger("CSubNEW::__make_sub")
                    l_log.setLevel(logging.NOTSET)
                    l_log.warning("pista:[%s] não existe no dicionário", ls_pis_id)

        # breakpoints da subida
        if "breakpoints" in fdct_data:

            # para todos breakpoints da subida...
            for l_brk in sorted(fdct_data["breakpoints"], key=lambda l_k: l_k["nBrk"]):

                # cria o breakpoints
                lo_brk = brknew.CBrkNEW(self.__model, self, l_brk)
                assert lo_brk

                # coloca o breakpoint na lista
                self.__lst_sub_brk.append(lo_brk)

        # (bool)
        self.v_prc_ok = True

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def ptr_sub_aer(self):
        """
        get aeródromo da subida
        """
        return self.__ptr_sub_aer

    @ptr_sub_aer.setter
    def ptr_sub_aer(self, f_val):
        """
        set aeródromo da subida
        """
        self.__ptr_sub_aer = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def lst_sub_brk(self):
        """
        get lista de breakpoints da subida
        """
        return self.__lst_sub_brk

    @lst_sub_brk.setter
    def lst_sub_brk(self, f_val):
        """
        set lista de breakpoints da subida
        """
        self.__lst_sub_brk = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def ptr_sub_pis(self):
        """
        get pista da subida
        """
        return self.__ptr_sub_pis

    @ptr_sub_pis.setter
    def ptr_sub_pis(self, f_val):
        """
        set pista da subida
        """
        self.__ptr_sub_pis = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def ptr_sub_prc_dec(self):
        """
        get procedimento de decolagem associado
        """
        return self.__ptr_sub_prc_dec

    @ptr_sub_prc_dec.setter
    def ptr_sub_prc_dec(self, f_val):
        """
        set procedimento de decolagem associado
        """
        self.__ptr_sub_prc_dec = f_val

# < the end >--------------------------------------------------------------------------------------
