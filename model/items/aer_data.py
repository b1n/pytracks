#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
aer_data

mantém as informações sobre o dicionário de aeródromos

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
import model.items.aer_new as model
import model.items.parser_utils as parser

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CAerData >-------------------------------------------------------------------------------

class CAerData(dict):
    """
    mantém as informações sobre o dicionário de aeródromos

    <aerodromo nAer="SBSP">
        <descricao>Congonhas</descricao>
        <elevacao>2189</elevacao>
        <pista> ... </pista>
    </aerodromo>
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_data=None):
        """
        @param f_model: event manager
        @param f_data: dados dos aeródromos
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parametros de entrada
        assert f_model

        # inicia a super class
        super(CAerData, self).__init__()

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

                # cria um aeródromo com os dados da lista
                # self.make_aer(f_data)
                pass

            # recebeu um aeródromo ?
            elif isinstance(f_data, CAerData):

                # copia o aeródromo
                # self.copy_aer(f_data)
                pass

            # senão, recebeu o pathname de um arquivo de aeródromo
            else:
                # carrega o dicionário de aeródromo de um arquivo em disco
                self.load_file(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def load_file(self, fs_aer_pn):
        """
        carrega os dados do aeródromo de um arquivo em disco

        @param fs_aer_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("load_file:>>")

        # verifica parâmetros de entrada
        assert fs_aer_pn

        # carrega o arquivo de aeródromo
        self.parse_aer_xml(fs_aer_pn + ".xml")

        # logger
        # M_LOG.info("load_file:<<")

    # ---------------------------------------------------------------------------------------------

    def make_aer(self, fdct_root, fdct_data):
        """
        carrega os dados de aeródromo a partir de um dicionário

        @param fdct_data: lista de dados de aeródromo

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("make_aer:>>")

        # verifica parâmetros de entrada
        assert fdct_root is not None
        assert fdct_data is not None

        # é uma aeródromo do newton ?
        if "aerodromos" != fdct_root["tagName"]:

            # logger
            l_log = logging.getLogger("CAerData::make_aer")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: não é um arquivo de aeródromo.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # é um arquivo do newton ?
        if "NEWTON" != fdct_root["FORMAT"]:

            # logger
            l_log = logging.getLogger("CAerData::make_aer")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: não está em um formato aceito.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # é a assinatura do newton ?
        if "1961" != fdct_root["CODE"]:

            # logger
            l_log = logging.getLogger("CAerData::make_aer")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E03: não tem a assinatura correta.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # verifica se existe identificação
        if "nAer" in fdct_data:

            # cria aeródromo
            l_aer = model.CAerNEW(self.__model, fdct_data, fdct_root["VERSION"])
            assert l_aer

            # coloca a aeródromo no dicionário
            self[fdct_data["nAer"]] = l_aer

        # senão, não existe indicativo
        else:
            # monta uma mensagem
            ls_msg = u"não tem identificação. Aeródromo não incluído."

            # logger
            l_log = logging.getLogger("CAerData::make_aer")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E04: {}".format(ls_msg))

            # se não for, cai fora...
            return False, ls_msg

        # logger
        # M_LOG.info("make_aer:<<")

        # retorna Ok
        return True, None

    # ---------------------------------------------------------------------------------------------

    def parse_aer_xml(self, fs_aer_pn):
        """
        carrega o arquivo de aeródromo

        @param fs_aer_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("parse_aer_xml:>>")

        # verifica parâmetros de entrada
        assert fs_aer_pn

        # cria o QFile para o arquivo XML do aeródromo
        l_data_file = QtCore.QFile(fs_aer_pn)
        assert l_data_file is not None

        # abre o arquivo XML do aeródromo
        l_data_file.open(QtCore.QIODevice.ReadOnly)

        # erro na abertura do arquivo ?
        if not l_data_file.isOpen():

            # logger
            l_log = logging.getLogger("CAerData::parse_aer_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na abertura de {}.".format(fs_aer_pn))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # cria o documento XML do aeródromo
        l_xdoc_aer = QtXml.QDomDocument("aerodromos")
        assert l_xdoc_aer is not None

        # erro na carga do documento ?
        if not l_xdoc_aer.setContent(l_data_file):

            # fecha o arquivo
            l_data_file.close()

            # logger
            l_log = logging.getLogger("CAerData::parse_aer_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: falha no parse de {}.".format(fs_aer_pn))

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
        l_elem_root = l_xdoc_aer.documentElement()
        assert l_elem_root is not None

        # faz o parse dos atributos do elemento raíz
        ldct_root = parser.parse_root_element(l_elem_root)

        # cria uma lista com os elementos de aeródromo
        l_node_list = l_elem_root.elementsByTagName("aerodromo")

        # para todos os nós na lista...
        for li_ndx in xrange(l_node_list.length()):

            # inicia o dicionário de dados
            ldct_data = {}

            # inicia a lista de pistas
            ldct_data["pistas"] = []

            l_element = l_node_list.at(li_ndx).toElement()
            assert l_element is not None

            # read identification if available
            if l_element.hasAttribute("nAer"):
                ldct_data["nAer"] = str(l_element.attribute("nAer"))

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
                    ldct_tmp = parser.parse_aerodromo(l_element)

                    # atualiza o dicionário com a pista
                    if "pista" in ldct_tmp:

                        # atualiza o dicionário com a pista
                        ldct_data["pistas"].append(ldct_tmp["pista"])

                        # apaga este elemento
                        del ldct_tmp["pista"]

                    # atualiza o dicionário de dados
                    ldct_data.update(ldct_tmp)

                # próximo nó
                l_node = l_node.nextSibling()
                assert l_node is not None

            # carrega os dados de aeródromo a partir de um dicionário
            self.make_aer(ldct_root, ldct_data)

        # logger
        # M_LOG.info("parse_aer_xml:<<")

    # ---------------------------------------------------------------------------------------------

    def save2disk(self, fs_aer_pn=None):
        """
        salva os dados da aeródromo em um arquivo em disco

        @param fs_aer_pn: path name do arquivo onde salvar

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
