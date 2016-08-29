#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_velocidade

mantém as informações sobre a dialog de velocidade

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
import os

# PyQt library
from PyQt4 import QtCore, QtGui

# view
import view.piloto.dlg_velocidade_ui as dlg

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CDlgVelocidade >----------------------------------------------------------------------------

class CDlgVelocidade(QtGui.QDialog, dlg.Ui_CDlgVelocidade):
    """
    mantém as informações sobre a dialog de velocidade
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_strip_cur, fdct_prf, f_parent=None):
        """
        @param f_strip_cur: strip selecionada
        @param fdct_prf: dicionário de performances
        @param f_parent: janela pai.
        """
        # logger
        M_LOG.info("__init__:>>")

        # init super class
        super(CDlgVelocidade, self).__init__(f_parent)

        # salva o control manager localmente
        # self.__control = f_control

        # salva o dicionário de performances
        self.__dct_prf = fdct_prf
                
        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Velocidade")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # inicia valores
        self.sbx_vel.setValue(f_strip_cur.f_vel)
        
        # performance existe ?
        if fdct_prf is not None:

            # faixa de velocidade
            self.sbx_vel.setRange(1., self.__dct_prf["vel_max_crz"])
            M_LOG.debug("__on_rbt_vel_clicked:vel_max:[{}]".format(self.__dct_prf["vel_max_crz"]))

        # senão,...
        else:
            # faixa de velocidade
            self.sbx_vel.setRange(1., 500.)
            M_LOG.debug("__on_rbt_vel_clicked:vel_max:[500]")

        # configura botões
        self.bbx_velocidade.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_velocidade.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros da velocidade
        self.__update_command()

        # logger
        M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __config_connects(self):
        """
        configura as conexões slot/signal.
        """
        # logger
        M_LOG.info("__config_connects:>>")

        # conecta spinBox
        self.sbx_vel.valueChanged.connect(self.__on_sbx_valueChanged)

        # conecta botão Ok da edição de velocidade
        # self.bbx_velocidade.accepted.connect(self.__accept)

        # conecta botão Cancela da edição de velocidade
        # self.bbx_velocidade.rejected.connect(self.__reject)

        # logger
        M_LOG.info("__config_connects:<<")

    # ---------------------------------------------------------------------------------------------

    def __config_texts(self):

        # logger
        M_LOG.info("__config_texts:>>")

        # configura títulos e mensagens
        self.__txt_settings = "CDlgVelocidade"

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

        # inicia o comando
        ls_cmd = "VEL {} ".format(self.sbx_vel.value())

        # coloca o comando no label
        self.lbl_comando.setText(ls_cmd)

        # logger
        M_LOG.info("__update_command:<<")

    # =============================================================================================
    # edição de campos
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSignature("int")
    def __on_sbx_valueChanged(self, f_val):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("__on_sbx_valueChanged:>>")

        # atualiza comando
        self.__update_command()

        # logger
        M_LOG.info("__on_sbx_valueChanged:<<")

# < the end >--------------------------------------------------------------------------------------
