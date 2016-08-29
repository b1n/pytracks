#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prf_data

mantém as informações sobre o dicionário de performances

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
import model.items.prf_new as model
import model.items.parser_utils as parser

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# < class CPrfData >-------------------------------------------------------------------------------

class CPrfData(dict):
    """
    mantém as informações sobre o dicionário de performances

    <performance nPrf="A1">
        <descricao>AMX</descricao>
        <esteira>M</esteira>
        <tetosv>420</tetosv>
        <faixa>420</faixa>
        <veldec>125</veldec>
        <velsbdec>190</velsbdec>
        <velapx>160</velapx>
        <velcruz>440</velcruz>
        <velmxcrz>540</velmxcrz>
        <rzsubdec>1300</rzsubdec>
        <rzmxsbdec>3500</rzmxsbdec>
        <rzsbcrz>1900</rzsbcrz>
        <rzmxsbcrz>3500</rzmxsbcrz>
        <rzdescapx>2500</rzdescapx>
        <rzmxdesapx>4000</rzmxdesapx>
        <rzdescrz>2000</rzdescrz>
        <rzmxdescrz>3500</rzmxdescrz>
        <razvarvel>45</razvarvel>
        <rzmxvarvel>60</rzmxvarvel>
    </performance>
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_data=None):
        """
        @param f_model: event manager
        @param f_data: dados das performances
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parametros de entrada
        assert f_model

        # init super class
        super(CPrfData, self).__init__()

        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # recebeu dados ?
        if f_data is not None:

            # recebeu uma lista ?
            if isinstance(f_data, list):

                # cria uma performance com os dados da lista
                # self.make_prf(f_data)
                pass

            # recebeu uma performance ?
            elif isinstance(f_data, CPrfData):

                # copia a performance
                # self.copy_prf(f_data)
                pass

            # senão, recebeu o pathname de um arquivo de performances
            else:

                # carrega o dicionário de performances de um arquivo em disco
                self.load_file(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def load_file(self, fs_prf_pn):
        """
        carrega os dados do performance de um arquivo em disco

        @param fs_prf_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("load_file:>>")

        # verifica parâmetros de entrada
        assert fs_prf_pn

        # carrega o arquivo de performance
        self.parse_prf_xml(fs_prf_pn + ".xml")

        # logger
        # M_LOG.info("load_file:<<")

    # ---------------------------------------------------------------------------------------------

    def make_prf(self, fdct_root, fdct_data):
        """
        carrega os dados de performance a partir de um dicionário

        @param fdct_data: lista de dados de performance

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("make_prf:>>")

        # verifica parâmetros de entrada
        assert fdct_root is not None
        assert fdct_data is not None

        # mensagem
        ls_msg = None

        # é uma performance do TrackS ?
        if "performances" != fdct_root["tagName"]:

            # logger
            l_log = logging.getLogger("CPrfData::make_prf")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: Não é um arquivo de performance")

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
            l_log = logging.getLogger("CPrfData::make_prf")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: Não está em um formato aceito")

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
            l_log = logging.getLogger("CPrfData::make_prf")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E03: Não tem a assinatura correta")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # verifica se existe identificação
        if "nPrf" in fdct_data:

            # cria performance
            l_prf = model.CPrfNEW(self.__event, fdct_data, fdct_root["VERSION"])
            assert l_prf

            # coloca a performance no dicionário
            self[fdct_data["nPrf"]] = l_prf

        # senão, não existe designador
        else:

            # monta a mensagem
            ls_msg = u"Não tem designador. Performance não incluída !"

            # logger
            l_log = logging.getLogger("CPrfData::make_prf")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E04: {}".format(ls_msg))

            # se não for, cai fora...
            return False, ls_msg

        # logger
        # M_LOG.info("make_prf:<<")

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------

    def parse_prf_xml(self, fs_prf_pn):
        """
        carrega o arquivo de performance

        @param fs_prf_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("parse_prf_xml:>>")

        # verifica parâmetros de entrada
        assert fs_prf_pn

        # cria o QFile para o arquivo XML do performance
        l_data_file = QtCore.QFile(fs_prf_pn)
        assert l_data_file is not None

        # abre o arquivo XML do performance
        l_data_file.open(QtCore.QIODevice.ReadOnly)

        # erro na abertura do arquivo ?
        if not l_data_file.isOpen():

            # logger
            l_log = logging.getLogger("CPrfData::parse_prf_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: Erro na abertura de {}".format(fs_prf_pn))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # cria o documento XML do performance
        l_xdoc_prf = QtXml.QDomDocument("performances")
        assert l_xdoc_prf is not None

        # erro na carga do documento ?
        if not l_xdoc_prf.setContent(l_data_file):

            # fecha o arquivo
            l_data_file.close()

            # logger
            l_log = logging.getLogger("CPrfData::parse_prf_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: Falha no parse de {}".format(fs_prf_pn))

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
        l_elem_root = l_xdoc_prf.documentElement()
        assert l_elem_root is not None

        # faz o parse dos atributos do elemento raíz
        ldct_root = parser.parse_root_element(l_elem_root)

        # cria uma lista com os elementos de performance
        l_node_list = l_elem_root.elementsByTagName("performance")

        # para todos os nós na lista...
        for li_ndx in xrange(l_node_list.length()):

            # inicia o dicionário de dados
            ldct_data = {}

            # obtém um nó da lista
            l_element = l_node_list.at(li_ndx).toElement()
            assert l_element is not None

            # read identification if available
            if l_element.hasAttribute("nPrf"):
                ldct_data["nPrf"] = str(l_element.attribute("nPrf"))

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

                    # faz o parse do elemento
                    ldct_tmp = parser.parse_performance(l_element)

                    # atualiza o dicionário de dados
                    ldct_data.update(ldct_tmp)

                # próximo nó
                l_node = l_node.nextSibling()
                assert l_node is not None

            # carrega os dados de performance a partir de um dicionário
            self.make_prf(ldct_root, ldct_data)

        # logger
        # M_LOG.info("parse_prf_xml:<<")

    # ---------------------------------------------------------------------------------------------

    def save2disk(self, fs_prf_pn=None):
        """
        salva os dados da performance em um arquivo em disco

        @param fs_prf_pn: path name do arquivo onde salvar

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("save2disk:>>")

        # return code
        lv_ok = True

        # mensagem
        ls_msg = "save Ok"

        # logger
        # M_LOG.info("save2disk:<<")

        # retorna flag e mensagem
        return lv_ok, ls_msg

# < the end >--------------------------------------------------------------------------------------
