#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_subida

mantém as informações sobre a dialog de subida

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
from . import dlg_subida_ui as dlg

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CDlgSubida >-----------------------------------------------------------------------------

class CDlgSubida(QtGui.QDialog, dlg.Ui_CDlgSubida):
    """
    mantém as informações sobre a dialog de subida
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, fsck_http, fdct_config, f_strip_cur, fdct_sub, f_parent=None):
        """
        @param fsck_http: socket de comunicação com o servidor
        @param fdct_config: dicionário de configuração
        @param f_strip_cur: strip selecionada
        @param fdct_sub: dicionário de subidas
        @param f_parent: janela pai
        """
        # logger
        M_LOG.info("__init__:>>")

        # init super class
        super(CDlgSubida, self).__init__(f_parent)

        # salva o control manager localmente
        # self.__control = f_control

        # salva o socket de comunicação
        self.__sck_http = fsck_http
        assert self.__sck_http
        
        # salva o dicionário de configuração
        self.__dct_config = fdct_config
        assert self.__dct_config is not None

        # salva o dicionário de subidas
        self.__dct_sub = fdct_sub
        assert self.__dct_sub is not None
                
        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Procedimento de Trajetória")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # dicionário de subidas vazio ?
        if not self.__dct_sub:

            # carrega o dicionário
            self.__load_sub()

        # inicia valores
        self.cbx_sub.addItems(self.__dct_sub.values())

        # configura botões
        self.bbx_subida.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_subida.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros da subida
        self.__update_command()

        # logger
        M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __config_connects(self):
        """
        configura as conexões slot/signal
        """
        # logger
        M_LOG.info("__config_connects:>>")

        # conecta spinBox
        self.cbx_sub.currentIndexChanged.connect(self.__on_cbx_currentIndexChanged)

        # conecta botão Ok da edição de subida
        # self.bbx_subida.accepted.connect(self.__accept)

        # conecta botão Cancela da edição de subida
        # self.bbx_subida.rejected.connect(self.__reject)

        # logger
        M_LOG.info("__config_connects:<<")

    # ---------------------------------------------------------------------------------------------

    def __config_texts(self):

        # logger
        M_LOG.info("__config_texts:>>")

        # configura títulos e mensagens
        self.__txt_settings = "CDlgSubida"

        # logger
        M_LOG.info("__config_texts:<<")

    # ---------------------------------------------------------------------------------------------

    def get_data(self):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("get_data:><")

        # return command line
        return self.lbl_comando.text()

    # ---------------------------------------------------------------------------------------------

    def __load_sub(self):
        """
        carrega o dicionário de subidas
        """
        # logger
        # M_LOG.info("__load_sub:>>")

        # check input parameters
        # assert f_strip_cur

        # check for requirements
        assert self.__sck_http is not None
        assert self.__dct_config is not None
        assert self.__dct_sub is not None
                
        # monta o request das subidas
        ls_req = "data/sub.json"
        M_LOG.debug("__load_sub:ls_req:[{}]".format(ls_req))

        # get server address
        l_srv = self.__dct_config.get("srv.addr", None)
        
        if l_srv is not None:

            # obtém os dados de subidas do servidor
            l_dict = self.__sck_http.get_data(l_srv, ls_req)
            M_LOG.debug("__load_sub:l_dict:[{}]".format(l_dict))

            if l_dict is not None:

                # salva a subidas no dicionário
                self.__dct_sub.update(json.loads(l_dict))
                M_LOG.debug("__load_sub:dct_sub:[{}]".format(self.__dct_sub))

            # senão, não achou no servidor...
            else:
                # logger
                l_log = logging.getLogger("CDlgSubida::__load_sub")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E01: tabela de subidas não existe no servidor.")

        # senão, não achou endereço do servidor
        else:
            # logger
            l_log = logging.getLogger("CDlgSubida::__load_sub")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E02: srv.addr não existe na configuração.")

        # logger
        # M_LOG.info("__load_sub:<<")

    # ---------------------------------------------------------------------------------------------

    def __restore_settings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # logger
        M_LOG.info("__restore_settings:>>")

        # obtém os settings
        l_set = QtCore.QSettings("ICEA", "piloto")
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self.__txt_settings)).toByteArray())

        # logger
        M_LOG.info("__restore_settings:<<")

    # ---------------------------------------------------------------------------------------------

    def __update_command(self):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("__update_command:>>")

        # para todas as subidas...
        for l_key, l_sub in self.__dct_sub.iteritems():

            M_LOG.debug("l_key:[{}]".format(l_key))
            M_LOG.debug("l_sub:[{}]".format(l_sub))

            # é a subida selecionada ?
            if unicode(self.cbx_sub.currentText()) == unicode(l_sub):
                break

        # inicia o comando
        ls_cmd = "SUB {}".format(l_key)

        # coloca o comando no label
        self.lbl_comando.setText(ls_cmd)

        # logger
        M_LOG.info("__update_command:<<")

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
        M_LOG.info("__on_cbx_currentIndexChanged:>>")

        # atualiza comando
        self.__update_command()

        # logger
        M_LOG.info("__on_cbx_currentIndexChanged:<<")

# < the end >--------------------------------------------------------------------------------------
