#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_decolagem

mantém as informações sobre a dialog de decolagem

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import json
import os

# PyQt library
from PyQt4 import QtCore, QtGui

# view
from . import dlg_decolagem_ui as dlg

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CDlgDecolagem >--------------------------------------------------------------------------

class CDlgDecolagem(QtGui.QDialog, dlg.Ui_CDlgDecolagem):
    """
    mantém as informações sobre a dialog de decolagem
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, fsck_http, fdct_config, f_strip_cur, flst_dep, f_parent=None):
        """
        @param fsck_http: socket de comunicação com o servidor
        @param fdct_config: dicionário de configuração
        @param f_strip_cur: strip selecionada
        @param flst_dep: lista de decolagens
        @param f_parent: janela pai
        """
        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CDlgDecolagem, self).__init__(f_parent)

        # salva o socket de comunicação
        self.__sck_http = fsck_http
        assert self.__sck_http
        
        # salva o dicionário de configuração
        self.__dct_config = fdct_config
        assert self.__dct_config is not None

        # salva a strip atual
        self.__strip_cur = f_strip_cur
        assert self.__strip_cur is not None

        # salva o lista de decolagens
        self.__lst_dep = flst_dep
        assert self.__lst_dep is not None
                
        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Procedimento de Decolagem")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # lista de decolagens vazia ?
        if not self.__lst_dep:

            # carrega a lista
            self.__load_dep()

        # inicia valores
        # self.cbx_dep.addItems(["{}/{}".format(ldep[0], ldep[1]) for ldep in self.__lst_dep])
        self.cbx_dep.addItems(sorted(self.__lst_dep))

        # configura botões
        self.bbx_dep.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_dep.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros da decolagem
        self.__update_command()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __config_connects(self):
        """
        configura as conexões slot/signal
        """
        # logger
        # M_LOG.info("__config_connects:>>")

        # conecta comboBox
        self.cbx_dep.currentIndexChanged.connect(self.__on_cbx_currentIndexChanged)

        # conecta botão Ok da edição de decolagem
        # self.bbx_dep.accepted.connect(self.__accept)

        # conecta botão Cancela da edição de decolagem
        # self.bbx_dep.rejected.connect(self.__reject)

        # logger
        # M_LOG.info("__config_connects:<<")

    # ---------------------------------------------------------------------------------------------

    def __config_texts(self):

        # logger
        # M_LOG.info("__config_texts:>>")

        # configura títulos e mensagens
        self.__txt_settings = "CDlgDecolagem"

        # logger
        # M_LOG.info("__config_texts:<<")

    # ---------------------------------------------------------------------------------------------

    def get_data(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("get_data:><")

        # return command line
        return self.lbl_comando.text()

    # ---------------------------------------------------------------------------------------------

    def __load_dep(self):
        """
        carrega a lista de decolagens
        """
        # logger
        # # M_LOG.info("__load_dep:>>")

        # check for requirements
        assert self.__sck_http is not None
        assert self.__dct_config is not None
        assert self.__lst_dep is not None
                
        # monta o request das decolagens
        ls_req = "data/dep.json"
        # M_LOG.debug("__load_dep:ls_req:[{}]".format(ls_req))

        # get server address
        l_srv = self.__dct_config.get("srv.addr", None)
        
        if l_srv is not None:

            # obtém os dados de decolagens do servidor
            l_dict = self.__sck_http.get_data(l_srv, ls_req)
            # M_LOG.debug("__load_dep:l_dict:[{}]".format(l_dict))

            if l_dict is not None:

                # salva a decolagens na lista
                self.__lst_dep.update(json.loads(l_dict))
                # M_LOG.debug("__load_dep:lst_dep:[{}]".format(self.__lst_dep))

            # senão, não achou no servidor...
            else:
                # logger
                l_log = logging.getLogger("CDlgDecolagem::__load_dep")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E01: tabela de decolagens não existe no servidor.")

        # senão, não achou endereço do servidor
        else:
            # logger
            l_log = logging.getLogger("CDlgDecolagem::__load_dep")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E02: srv.addr não existe na configuração.")

        # logger
        # # M_LOG.info("__load_dep:<<")

    # ---------------------------------------------------------------------------------------------

    def __restore_settings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # logger
        # M_LOG.info("__restore_settings:>>")

        # obtém os settings
        l_set = QtCore.QSettings("ICEA", "piloto")
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self.__txt_settings)).toByteArray())

        # logger
        # M_LOG.info("__restore_settings:<<")

    # ---------------------------------------------------------------------------------------------

    def __update_command(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__update_command:>>")

        # para todas as decolagens...
        for l_dep in self.__lst_dep:

            # é a decolagem selecionada ?
            if unicode(self.cbx_dep.currentText()) == unicode(l_dep):
                break

        # decolagem
        ls_cmd = "DEP {}".format(l_dep)

        # coloca o comando no label
        self.lbl_comando.setText(ls_cmd)

        # logger
        # M_LOG.info("__update_command:<<")

    # =============================================================================================
    # edição de campos
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSignature("int")
    def __on_cbx_currentIndexChanged(self, f_val):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__on_cbx_currentIndexChanged:>>")

        # atualiza comando
        self.__update_command()

        # logger
        # M_LOG.info("__on_cbx_currentIndexChanged:<<")

# < the end >--------------------------------------------------------------------------------------
