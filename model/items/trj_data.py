#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
trj_data

mantém as informações sobre o dicionário de procedimento de trajetórias

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
import model.items.trj_new as model
import model.items.parser_utils as parser

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CTrjData >-------------------------------------------------------------------------------

class CTrjData(dict):
    """
    mantém as informações sobre o dicionário de procedimento de trajetória

    <trajetoria nTrj="1">
        <descricao>DEP SDJD VIA SCB</descricao>
        <star>S</star>

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

    def __init__(self, f_model, f_data=None):
        """
        @param f_model: model manager
        @param f_data: dados dos procedimento de trajetórias
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parametros de entrada
        assert f_model

        # inicia a super class
        super(CTrjData, self).__init__()

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

                # cria um procedimento de trajetória com os dados da lista
                # self.make_trj(f_data)
                pass

            # recebeu um procedimento de trajetória ?
            elif isinstance(f_data, CTrjData):

                # copia o procedimento de trajetória
                # self.copy_trj(f_data)
                pass

            # senão, recebeu o pathname de um arquivo de procedimento de trajetória
            else:
                # carrega o dicionário de procedimento de trajetória de um arquivo em disco
                self.load_file(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def load_file(self, fs_trj_pn):
        """
        carrega os dados do procedimento de trajetória de um arquivo em disco

        @param fs_trj_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("load_file:>>")

        # verifica parâmetros de entrada
        assert fs_trj_pn

        # carrega o arquivo de procedimento de trajetória
        self.parse_trj_xml(fs_trj_pn + ".xml")

        # logger
        # M_LOG.info("load_file:<<")

    # ---------------------------------------------------------------------------------------------

    def make_trj(self, fdct_root, fdct_data):
        """
        carrega os dados de procedimento de trajetória a partir de um dicionário

        @param fdct_data: dados do procedimento de trajetória

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("make_trj:>>")

        # verifica parâmetros de entrada
        assert fdct_root is not None
        assert fdct_data is not None

        # é uma procedimento de trajetória do TrackS ?
        if "trajetorias" != fdct_root["tagName"]:

            # logger
            l_log = logging.getLogger("CTrjData::make_trj")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: não é um arquivo de procedimentos de trajetória.")

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
            l_log = logging.getLogger("CTrjData::make_trj")
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
            l_log = logging.getLogger("CTrjData::make_trj")
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
        if "nTrj" in fdct_data:

            # cria procedimento de trajetória
            l_trj = model.CTrjNEW(self.__model, fdct_data, fdct_root["VERSION"])
            assert l_trj

            # coloca a procedimento de trajetória no dicionário
            self[fdct_data["nTrj"]] = l_trj

        # senão, não existe identificação
        else:
            # monta uma mensagem
            ls_msg = u"não tem identificação. Trajetória não incluída."

            # logger
            l_log = logging.getLogger("CTrjData::make_trj")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E04: {}".format(ls_msg))

            # se não for, cai fora...
            return False, ls_msg

        # logger
        # M_LOG.info("make_trj:<<")

        # retorna Ok
        return True, None

    # ---------------------------------------------------------------------------------------------

    def parse_trj_xml(self, fs_trj_pn):
        """
        carrega o arquivo de procedimentos de trajetória

        @param fs_trj_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("parse_trj_xml:>>")

        # verifica parâmetros de entrada
        assert fs_trj_pn

        # cria o QFile para o arquivo XML do procedimentos de trajetória
        l_data_file = QtCore.QFile(fs_trj_pn)
        assert l_data_file is not None

        # abre o arquivo XML do procedimentos de trajetória
        l_data_file.open(QtCore.QIODevice.ReadOnly)

        # erro na abertura do arquivo ?
        if not l_data_file.isOpen():

            # logger
            l_log = logging.getLogger("CTrjData::parse_trj_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na abertura de {}".format(fs_trj_pn))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # cria o documento XML do procedimento de trajetória
        l_xdoc_trj = QtXml.QDomDocument("trajetorias")
        assert l_xdoc_trj is not None

        # erro na carga do documento ?
        if not l_xdoc_trj.setContent(l_data_file):

            # fecha o arquivo
            l_data_file.close()

            # logger
            l_log = logging.getLogger("CTrjData::parse_trj_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: falha no parse de {}".format(fs_trj_pn))

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
        l_elem_root = l_xdoc_trj.documentElement()
        assert l_elem_root is not None

        # faz o parse dos atributos do elemento raíz
        ldct_root = parser.parse_root_element(l_elem_root)

        # cria uma lista com os elementos de procedimento de trajetória
        l_node_list = l_elem_root.elementsByTagName("trajetoria")

        # para todos os nós na lista...
        for li_ndx in xrange(l_node_list.length()):

            # inicia o dicionário de dados
            ldct_data = {}

            # inicia a lista de breakpoints
            ldct_data["breakpoints"] = []

            # obtém um nó da lista
            l_element = l_node_list.at(li_ndx).toElement()
            assert l_element is not None

            # read identification if available
            if l_element.hasAttribute("nTrj"):
                ldct_data["nTrj"] = int(l_element.attribute("nTrj"))

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
                    ldct_tmp = parser.parse_trajetoria(l_element)

                    # atualiza o dicionário com o breakpoint
                    if "breakpoint" in ldct_tmp:

                        # atualiza o dicionário com o breakpoint
                        ldct_data["breakpoints"].append(ldct_tmp["breakpoint"])

                        # apaga este elemento
                        del ldct_tmp["breakpoint"]

                    # atualiza o dicionário de dados
                    ldct_data.update(ldct_tmp)

                # próximo nó
                l_node = l_node.nextSibling()
                assert l_node is not None

            # M_LOG.debug("trajetória: " + str(ldct_data))

            # carrega os dados de procedimento de trajetória a partir de um dicionário
            self.make_trj(ldct_root, ldct_data)

        # logger
        # M_LOG.info("parse_trj_xml:<<")

    # ---------------------------------------------------------------------------------------------

    def save2disk(self, fs_trj_pn=None):
        """
        salva os dados da procedimento de trajetória em um arquivo em disco

        @param fs_trj_pn: path name do arquivo onde salvar

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
