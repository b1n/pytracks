#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_pouso

mantém as informações sobre a dialog de pouso

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
from . import dlg_pouso_ui as dlg

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CDlgPouso >------------------------------------------------------------------------------

class CDlgPouso(QtGui.QDialog, dlg.Ui_CDlgPouso):
    """
    mantém as informações sobre a dialog de pouso
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, fsck_http, fdct_config, f_strip_cur, flst_pouso, f_parent=None):
        """
        @param fsck_http: socket de comunicação com o servidor
        @param fdct_config: dicionário de configuração
        @param f_strip_cur: strip selecionada
        @param flst_pouso: lista de pousos
        @param f_parent: janela pai
        """
        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CDlgPouso, self).__init__(f_parent)

        # salva o socket de comunicação
        self.__sck_http = fsck_http
        assert self.__sck_http
        
        # salva o dicionário de configuração
        self.__dct_config = fdct_config
        assert self.__dct_config is not None

        # salva a strip atual
        self.__strip_cur = f_strip_cur
        assert self.__strip_cur is not None

        # salva o lista de pousos
        self.__lst_pouso = flst_pouso
        assert self.__lst_pouso is not None
                
        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Procedimento de Pouso")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # lista de pousos vazia ?
        if not self.__lst_pouso:

            # carrega a lista
            self.__load_pouso()

        # inicia valores
        # self.cbx_pouso.addItems(["{}/{}".format(ldep[0], ldep[1]) for ldep in self.__lst_pouso])
        self.cbx_pouso.addItems(sorted(self.__lst_pouso))

        # configura botões
        self.bbx_pouso.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_pouso.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros do pouso
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
        self.cbx_pouso.currentIndexChanged.connect(self.__on_cbx_currentIndexChanged)

        # conecta botão Ok da edição de pouso
        # self.bbx_pouso.accepted.connect(self.__accept)

        # conecta botão Cancela da edição de pouso
        # self.bbx_pouso.rejected.connect(self.__reject)

        # logger
        # M_LOG.info("__config_connects:<<")

    # ---------------------------------------------------------------------------------------------

    def __config_texts(self):

        # logger
        # M_LOG.info("__config_texts:>>")

        # configura títulos e mensagens
        self.__txt_settings = "CDlgPouso"

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

    def __load_pouso(self):
        """
        carrega a lista de pousos
        """
        # logger
        # # M_LOG.info("__load_pouso:>>")

        # check for requirements
        assert self.__sck_http is not None
        assert self.__dct_config is not None
        assert self.__lst_pouso is not None
                
        # monta o request dos pousos
        ls_req = "data/arr.json"
        # M_LOG.debug("__load_pouso:ls_req:[{}]".format(ls_req))

        # get server address
        l_srv = self.__dct_config.get("srv.addr", None)
        
        if l_srv is not None:

            # obtém os dados de pousos do servidor
            l_data = self.__sck_http.get_data(l_srv, ls_req)
            # M_LOG.debug("__load_pouso:l_data:[{}]".format(l_data))

            if l_data is not None:

                # salva o pouso na lista
                self.__lst_pouso.update(json.loads(l_data))
                # M_LOG.debug("__load_pouso:lst_pouso:[{}]".format(self.__lst_pouso))

            # senão, não achou no servidor...
            else:
                # logger
                l_log = logging.getLogger("CDlgPouso::__load_pouso")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E01: tabela de pousos não existe no servidor.")

        # senão, não achou endereço do servidor
        else:
            # logger
            l_log = logging.getLogger("CDlgPouso::__load_pouso")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"<E02: srv.addr não existe na configuração.")

        # logger
        # # M_LOG.info("__load_pouso:<<")

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

        # para todas os pousos...
        for l_pouso in self.__lst_pouso:

            # é o pouso selecionada ?
            if unicode(self.cbx_pouso.currentText()) == unicode(l_pouso):
                break

        # pouso
        ls_cmd = "ARR {}".format(l_pouso)

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
