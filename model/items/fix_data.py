#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
fix_data

mantém as informações sobre o dicionário de fixos

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
from . import fix_new as model
from . import parser_utils as parser

# control
from ...control.events import events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CFixData >------------------------------------------------------------------------------


class CFixData(dict):
    """
    mantém as informações sobre o dicionário de fixos

    <fixo nFix="1">
        <descricao>BSCW1</descricao>
        <indicativo>BSCW1</indicativo>
        <tipo>V</tipo>
        <coord>
            <tipo>G</tipo>
            <campoA>1620.120S</campoA>
            <campoB>5823.230W</campoB>
        </coord>
    </fixo>
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_data=None):
        """
        cria umo dicionário de fixos

        @param f_model: event manager
        @param f_data: dados dos fixos
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parametros de entrada
        assert f_model

        # inicia a super class
        super(CFixData, self).__init__()

        # salva o model manager localmente
        self.__model = f_model
        assert self.__model

        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # recebeu dados ?
        if f_data is not None:

            # recebeu uma lista ?
            if isinstance(f_data, list):

                # cria uma fixo com os dados da lista
                # self.make_fix li_ndxf_data)
                pass

            # recebeu uma fixo ?
            elif isinstance(f_data, CFixData):

                # copia a fixo
                # self.copy_fix(f_data)
                pass

            # senão, recebeu o pathname de um arquivo de fixos
            else:
                # carrega o dicionário de fixos de um arquivo em disco
                self.load_file(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def load_file(self, fs_fix_pn):
        """
        carrega os dados do fixo de um arquivo em disco

        @param fs_fix_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("load_file:>>")

        # verifica parâmetros de entrada
        assert fs_fix_pn

        # carrega o arquivo de fixo
        self.parse_fix_xml(fs_fix_pn + ".xml")

        # logger
        # M_LOG.info("load_file:<<")

    # ---------------------------------------------------------------------------------------------

    def make_fix(self, fdct_root, fdct_data):
        """
        carrega os dados de fixo a partir de um dicionário

        @param f_lstData: lista de dados de fixo

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("make_fix:>>")

        # verifica parâmetros de entrada
        assert fdct_root is not None
        assert fdct_data is not None

        # é uma fixo do TrackS ?
        if "fixos" != fdct_root["tagName"]:

            # logger
            l_log = logging.getLogger("CFixData::make_fix")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: não é um arquivo de fixo")

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
            l_log = logging.getLogger("CFixData::make_fix")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: não está em um formato aceito")

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
            l_log = logging.getLogger("CFixData::make_fix")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E03: não tem a assinatura correta")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # verifica se existe identificação
        if "nFix" in fdct_data:

            # cria fixo
            l_fix = model.CFixNEW(self.__model, fdct_data, fdct_root["VERSION"])
            assert l_fix

            # coloca a fixo no dicionário
            self[fdct_data["nFix"]] = l_fix

        # senão, não existe indicativo
        else:
            # monta a mensagem
            ls_msg = u"não tem identificação. Fixo não incluído."

            # logger
            l_log = logging.getLogger("CFixData::make_fix")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E04: {}".format(ls_msg))

            # se não for, cai fora...
            return False, ls_msg

        # logger
        # M_LOG.info("make_fix:<<")

        # retorna Ok
        return True, None

    # ---------------------------------------------------------------------------------------------

    def parse_fix_xml(self, fs_fix_pn):
        """
        carrega o arquivo de fixo

        @param fs_fix_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("parse_fix_xml:>>")

        # verifica parâmetros de entrada
        assert fs_fix_pn

        # cria o QFile para o arquivo XML do fixo
        l_data_file = QtCore.QFile(fs_fix_pn)
        assert l_data_file is not None

        # abre o arquivo XML do fixo
        l_data_file.open(QtCore.QIODevice.ReadOnly)

        # erro na abertura do arquivo ?
        if not l_data_file.isOpen():

            # logger
            l_log = logging.getLogger("CFixData::parse_fix_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na abertura de {}".format(fs_fix_pn))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # cria o documento XML do fixo
        l_xdoc_fix = QtXml.QDomDocument("fixos")
        assert l_xdoc_fix is not None

        # erro na carga do documento ?
        if not l_xdoc_fix.setContent(l_data_file):

            # fecha o arquivo
            l_data_file.close()

            # logger
            l_log = logging.getLogger("CFixData::parse_fix_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: falha no parse de {}".format(fs_fix_pn))

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
        l_elem_root = l_xdoc_fix.documentElement()
        assert l_elem_root is not None

        # faz o parse dos atributos do elemento raíz
        ldct_root = parser.parse_root_element(l_elem_root)

        # cria uma lista com os elementos de fixo
        l_node_list = l_elem_root.elementsByTagName("fixo")

        # para todos os nós na lista...
        for li_ndx in xrange(l_node_list.length()):

            # inicia o dicionário de dados
            ldct_data = {}

            l_element = l_node_list.at(li_ndx).toElement()
            assert l_element is not None

            # read identification if available
            if l_element.hasAttribute("nFix"):
                ldct_data["nFix"] = int(str(l_element.attribute("nFix")))

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
                    ldct_tmp = parser.parse_fixo(l_element)

                    # atualiza o dicionário de dados
                    ldct_data.update(ldct_tmp)

                # próximo nó
                l_node = l_node.nextSibling()
                assert l_node is not None

            # carrega os dados de fixo a partir de um dicionário
            self.make_fix(ldct_root, ldct_data)

        # logger
        # M_LOG.info("parse_fix_xml:<<")

    # ---------------------------------------------------------------------------------------------

    def save2disk(self, fs_fix_pn=None):
        """
        salva os dados da fixo em um arquivo em disco

        @param fs_fix_pn: path name do arquivo onde salvar

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
