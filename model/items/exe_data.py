#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
exe_data

mantém as informações sobre o dicionário de exercícios

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
import model.items.exe_new as model
import model.items.parser_utils as parser

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CExeData >-------------------------------------------------------------------------------

class CExeData(dict):
    """
    mantém as informações sobre o dicionário de exercícios

    <exercicio nExe="SBSP5301">
        <descricao>PBN 2013 INTEGRADO RJ E SP 17/09/15/15</descricao>
        <horainicio>06:00</horainicio>
    </exercicio>
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_data=None):
        """
        @param f_model: model manager
        @param f_data: dados do exercício
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parametros de entrada
        assert f_model

        # inicia a super class
        super(CExeData, self).__init__()

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

                # cria um exercício com os dados da lista
                # self.make_exe(f_data)
                pass

            # recebeu um exercício ?
            elif isinstance(f_data, CExeData):

                # copia o exercício
                # self.copy_exe(f_data)
                pass

            # senão, recebeu o pathname de um arquivo de exercício
            else:
                # carrega o dicionário de exercício de um arquivo em disco
                self.load_file(f_data)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def load_file(self, fs_exe_path):
        """
        carrega os dados do exercício de um arquivo em disco

        @param fs_exe_path: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("load_file:>>")

        # check input parameters
        assert fs_exe_path

        # carrega o arquivo de exercício
        self.parse_exe_xml(fs_exe_path)

        # logger
        # M_LOG.info("load_file:<<")

    # ---------------------------------------------------------------------------------------------

    def make_exe(self, f_dct_root, f_dct_data):
        """
        carrega os dados de exercício a partir de um dicionário

        @param f_dct_data: lista de dados de exercício

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("make_exe:>>")

        # check input parameters
        assert f_dct_root is not None
        assert f_dct_data is not None

        # é uma exercício do TrackS ?
        if "exercicios" != f_dct_root["tagName"]:

            # logger
            l_log = logging.getLogger("CExeData::make_exe")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: não é um arquivo de exercício")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # é um arquivo do TrackS ?
        if "NEWTON" != f_dct_root["FORMAT"]:

            # logger
            l_log = logging.getLogger("CExeData::make_exe")
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
        if "1961" != f_dct_root["CODE"]:

            # logger
            l_log = logging.getLogger("CExeData::make_exe")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E03: não tem a assinatura correta")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # verifica se existe indicativo
        if "nExe" in f_dct_data:

            # cria exercício
            l_exe = model.CExeNEW(self.__model, f_dct_data, f_dct_root["VERSION"])
            assert l_exe

            # coloca a exercício no dicionário
            self[f_dct_data["nExe"]] = l_exe

        # senão, não existe indicativo
        else:
            # monta uma mensagem
            ls_msg = u"não tem identificação. Exercício não incluído."

            # logger
            l_log = logging.getLogger("CExeData::make_exe")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E04: {}".format(ls_msg))

            # se não for, cai fora...
            return False, ls_msg

        # logger
        # M_LOG.info("make_exe:<<")

        # retorna Ok
        return True, None

    # ---------------------------------------------------------------------------------------------

    def parse_exe_xml(self, fs_exe_path):
        """
        carrega o arquivo de exercício

        @param fs_exe_path: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("parse_exe_xml:>>")

        # check input parameters
        assert fs_exe_path

        # cria o QFile para o arquivo XML do exercício
        l_data_file = QtCore.QFile(fs_exe_path)
        assert l_data_file is not None

        # abre o arquivo XML do exercício
        l_data_file.open(QtCore.QIODevice.ReadOnly)

        # erro na abertura do arquivo ?
        if not l_data_file.isOpen():

            # logger
            l_log = logging.getLogger("CExeData::parse_exe_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: erro na abertura de {}".format(fs_exe_path))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # cria o documento XML do exercício
        l_xdoc_exe = QtXml.QDomDocument("exercicios")
        assert l_xdoc_exe is not None

        # erro na carga do documento ?
        if not l_xdoc_exe.setContent(l_data_file):

            # fecha o arquivo
            l_data_file.close()

            # logger
            l_log = logging.getLogger("CExeData::parse_exe_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E02: falha no parse de {}".format(fs_exe_path))

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
        l_elem_root = l_xdoc_exe.documentElement()
        assert l_elem_root is not None

        # faz o parse dos atributos do elemento raíz
        ldct_root = parser.parse_root_element(l_elem_root)

        # cria uma lista com os elementos de exercício
        l_node_list = l_elem_root.elementsByTagName("exercicio")

        # para todos os nós na lista...
        for li_ndx in xrange(l_node_list.length()):

            # inicia o dicionário de dados
            ldct_data = {}

            # obtém um nó da lista
            l_element = l_node_list.at(li_ndx).toElement()
            assert l_element is not None

            # read identification if available
            if l_element.hasAttribute("nExe"):
                ldct_data["nExe"] = str(l_element.attribute("nExe"))

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
                    ldct_tmp = parser.parse_exercicio(l_element)
                    # M_LOG.debug("ldct_tmp: {}".format(ldct_tmp))

                    # atualiza o dicionário de dados
                    ldct_data.update(ldct_tmp)

                # próximo nó
                l_node = l_node.nextSibling()
                assert l_node is not None

            # carrega os dados de exercício a partir de um dicionário
            self.make_exe(ldct_root, ldct_data)

        # logger
        # M_LOG.info("parse_exe_xml:<<")

    # ---------------------------------------------------------------------------------------------

    def save2disk(self, fs_exe_path=None):
        """
        salva os dados da exercício em um arquivo em disco

        @param fs_exe_path: path name do arquivo onde salvar

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
