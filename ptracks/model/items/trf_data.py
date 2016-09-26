#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
trf_data

mantém as informações sobre o dicionário de tráfegos

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

# PyQt library
from PyQt4 import QtCore, QtXml

# model
from . import trf_new as model
from . import parser_utils as parser

# control
from ...control.events import events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CTrfData >-------------------------------------------------------------------------------

class CTrfData(dict):
    """
    mantém as informações sobre o dicionário de tráfegos

    <trafego nTrf="1">
        <designador>A319</designador>
        <ssr>7001</ssr>
        <indicativo>TAM3912</indicativo>
        <origem>SBSP</origem>
        <destino>SBRJ</destino>
        <procedimento>SUB307</procedimento>
        <coord> ... </coord>
        <temptrafego>0</temptrafego>
        <rvsm>S</rvsm>
        <rota>LOPES OPREV CANO</rota>
        <niveltrj>270</niveltrj>
        <veltrj>380</veltrj>
    </trafego>
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_data=None, f_exe=None):
        """
        @param f_model: event manager
        @param f_data: dados das tráfegos
        @param f_exe: exercício
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parametros de entrada
        assert f_model
        assert f_exe

        # inicia a super class
        super(CTrfData, self).__init__()

        # salva o model manager localmente
        self.__model = f_model
        assert self.__model

        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # salva o exercício localmente
        self._exe = f_exe

        # recebeu dados ?
        if f_data is not None:

            # recebeu uma lista ?
            if isinstance(f_data, list):

                # cria uma tráfego com os dados da lista
                # self.make_trf(f_data)
                pass

            # recebeu uma tráfego ?
            elif isinstance(f_data, CTrfData):

                # copia a tráfego
                # self.copy_trf(f_data)
                pass

            # senão, recebeu o pathname de uma tráfego
            else:
                # carrega a tráfego de um arquivo em disco
                self.load_file(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def load_file(self, fs_trf_pn):
        """
        carrega os dados do tráfego de um arquivo em disco

        @param fs_trf_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("load_file:>>")

        # verifica parâmetros de entrada
        assert fs_trf_pn

        # carrega o arquivo de tráfego
        self.parse_trf_xml(fs_trf_pn + ".trf.xml")

        # logger
        # M_LOG.info("load_file:<<")

    # ---------------------------------------------------------------------------------------------

    def make_trf(self, fdct_root, fdct_data):
        """
        carrega os dados de tráfego a partir de um dicionário

        @param fdct_root: DOCUMENT ME!
        @param fdct_data: lista de dados de tráfego

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("make_trf:>>")

        # verifica parâmetros de entrada
        assert fdct_root is not None
        assert fdct_data is not None

        # return code
        lv_ok = True

        # mensagem
        ls_msg = None

        # é uma tráfego do TrackS ?
        if "trafegos" != fdct_root["tagName"]:

            # logger
            l_log = logging.getLogger("CTrfData::make_trf")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: não é um arquivo de tráfego.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # é um arquivo do TrackS ?
        if "NEWTON" != fdct_root["FORMAT"]:

            # logger
            l_log = logging.getLogger("CTrfData::make_trf")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: não está em um formato aceito.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # é a assinatura do TrackS ?
        if "1961" != fdct_root["CODE"]:

            # logger
            l_log = logging.getLogger("CTrfData::make_trf")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E03: não tem a assinatura correta.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # verifica se existe indicativo
        if "nTrf" in fdct_data:

            # cria a tráfego
            l_trf = model.CTrfNEW(self.__model, fdct_data, fdct_root["VERSION"])
            assert l_trf

            # coloca a tráfego no dicionário
            self[fdct_data["nTrf"]] = l_trf

        # senão, não existe indicativo
        else:
            # monta uma mensagem
            ls_msg = u"não tem identificação. Tráfego não incluída !"

            # logger
            l_log = logging.getLogger("CTrfData::make_trf")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E04: {}".format(ls_msg))

            # se não for, cai fora...
            return False, ls_msg

        # logger
        # M_LOG.info("make_trf:<<")

        # retorna Ok
        return lv_ok, ls_msg

    # ---------------------------------------------------------------------------------------------

    def parse_trf_xml(self, fs_trf_pn):
        """
        carrega o arquivo de tráfego

        @param fs_trf_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("parse_trf_xml:>>")

        # verifica parâmetros de entrada
        assert fs_trf_pn

        # cria o QFile para o arquivo XML do tráfego
        l_data_file = QtCore.QFile(fs_trf_pn)
        assert l_data_file is not None

        # abre o arquivo XML do tráfego
        l_data_file.open(QtCore.QIODevice.ReadOnly)

        # erro na abertura do arquivo ?
        if not l_data_file.isOpen():

            # logger
            l_log = logging.getLogger("CTrfData::parse_trf_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na abertura de {}.".format(fs_trf_pn))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # cria o documento XML do tráfego
        l_xdoc_trf = QtXml.QDomDocument("trafegos")
        assert l_xdoc_trf is not None

        # erro na carga do documento ?
        if not l_xdoc_trf.setContent(l_data_file):

            # fecha o arquivo
            l_data_file.close()

            # logger
            l_log = logging.getLogger("CTrfData::parse_trf_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: falha no parse de {}.".format(fs_trf_pn))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # fecha o arquivo
        l_data_file.close()

        # obtém o elemento raíz do documento
        l_elem_root = l_xdoc_trf.documentElement()
        assert l_elem_root is not None

        # faz o parse dos atributos do elemento raíz
        ldct_root = parser.parse_root_element(l_elem_root)

        # cria uma lista com os elementos de tráfego
        l_node_list = l_elem_root.elementsByTagName("trafego")

        # para todos os nós na lista...
        for li_ndx in xrange(l_node_list.length()):

            # inicia o dicionário de dados
            ldct_data = {}

            # obtém um nó da lista
            l_element = l_node_list.at(li_ndx).toElement()
            assert l_element is not None

            # read identification if available
            if l_element.hasAttribute("nTrf"):
                ldct_data["nTrf"] = int(l_element.attribute("nTrf"))

            # obtém o primeiro nó da sub-árvore
            l_node = l_element.firstChild()
            assert l_node is not None

            # percorre a sub-árvore
            while not l_node.isNull():

                # tenta converter o nó em um elemento
                l_element = l_node.toElement()
                assert l_element is not None

                # o nó é um elemento ?
                if not l_element.isNull():

                    # atualiza o dicionário de dados
                    ldct_data.update(parser.parse_trafego(l_element))

                # próximo nó
                l_node = l_node.nextSibling()
                assert l_node is not None

            # carrega os dados de tráfego a partir de um dicionário
            self.make_trf(ldct_root, ldct_data)

        # logger
        # M_LOG.info("parse_trf_xml:<<")

    # ---------------------------------------------------------------------------------------------

    def save2disk(self, fs_trf_pn=None):
        """
        salva os dados da tráfego em um arquivo em disco

        @param fs_trf_pn: path name do arquivo onde salvar

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("save2disk:>>")

        # return code
        lv_ok = True

        # mensagem
        ls_msg = "save ok"

        # logger
        # M_LOG.info("save2disk:<<")

        # retorna flag e mensagem
        return lv_ok, ls_msg

# < the end >--------------------------------------------------------------------------------------
