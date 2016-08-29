#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_direcao
mantém as informações sobre a dialog de direção.

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
import view.piloto.dlg_direcao_ui as dlg

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CDlgDirecao >----------------------------------------------------------------------------

class CDlgDirecao(QtGui.QDialog, dlg.Ui_CDlgDirecao):
    """
    mantém as informações sobre a dialog de direção
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, ff_proa, f_parent=None):
        """
        @param f_control: control manager.
        @param f_parent: janela pai.
        """
        # logger
        M_LOG.info("__init__:>>")

        # init super class
        super(CDlgDirecao, self).__init__(f_parent)

        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Direção")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # inicia valores
        self.sbx_dir.setValue(ff_proa)

        # configura botões
        self.bbx_direcao.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_direcao.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros da direção
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

        # conecta groupBox
        self.gbx_sentido.clicked.connect(self.__on_gbx_clicked)
        self.gbx_direcao.clicked.connect(self.__on_gbx_direcao_clicked)
        self.gbx_razao.clicked.connect(self.__on_gbx_clicked)

        # conecta radioButton
        self.rbt_dir.clicked.connect(self.__on_rbt_clicked)
        self.rbt_esq.clicked.connect(self.__on_rbt_clicked)
        self.rbt_mnr.clicked.connect(self.__on_rbt_mnr_clicked)
        self.rbt_grau.clicked.connect(self.__on_rbt_clicked)
        self.rbt_proa.clicked.connect(self.__on_rbt_clicked)

        # conecta spinBox
        self.sbx_dir.valueChanged.connect(self.__on_sbx_valueChanged)
        self.sbx_raz.valueChanged.connect(self.__on_sbx_valueChanged)

        # conecta botão Ok da edição de direção
        # self.bbx_direcao.accepted.connect(self.__accept)

        # conecta botão Cancela da edição de direção
        # self.bbx_direcao.rejected.connect(self.__reject)

        # logger
        M_LOG.info("__config_connects:<<")

    # ---------------------------------------------------------------------------------------------

    def __config_texts(self):

        # logger
        M_LOG.info("__config_texts:>>")

        # configura títulos e mensagens
        self.__txt_settings = "CDlgDirecao"

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
        ls_cmd = "CURVA "

        # direita ?
        if self.rbt_dir.isChecked():
            ls_cmd += "DIR "

        # esquerda ?
        elif self.rbt_esq.isChecked():
            ls_cmd += "ESQ "

        # senão, menor...
        else:
            ls_cmd += "MNR "

        # direção ?
        if self.gbx_direcao.isChecked():

            # graus ?
            if self.rbt_grau.isChecked():
                ls_cmd += "{} GRAUS ".format(self.sbx_dir.value())

            # senão, proa...
            else:
                ls_cmd += "PROA {} ".format(self.sbx_dir.value())

        # razão ?
        if self.gbx_razao.isChecked():
            ls_cmd += "RAZ {}".format(self.sbx_raz.value())

        # coloca o comando no label
        self.lbl_comando.setText(ls_cmd)

        # logger
        M_LOG.info("__update_command:<<")

    # =============================================================================================
    # edição de campos
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSignature("bool")
    def __on_gbx_clicked(self, f_val):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("__on_gbx_clicked:>>")

        # atualiza comando
        self.__update_command()

        # logger
        M_LOG.info("__on_gbx_clicked:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSignature("bool")
    def __on_gbx_direcao_clicked(self, f_val):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("__on_gbx_direcao_clicked:>>")

        # menor ?
        if (not f_val) and self.rbt_mnr.isChecked():
            # habilita direção groupButton
            self.gbx_direcao.setChecked(True)                

        # atualiza comando
        self.__update_command()

        # logger
        M_LOG.info("__on_gbx_direcao_clicked:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSignature("bool")
    def __on_rbt_clicked(self, f_val):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("__on_rbt_clicked:>>")

        # disable graus radioButton
        self.rbt_grau.setEnabled(True)

        # atualiza comando
        self.__update_command()

        # logger
        M_LOG.info("__on_rbt_clicked:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSignature("bool")
    def __on_rbt_mnr_clicked(self, f_val):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("__on_rbt_mnr_clicked:>>")

        # check direção groupButton
        self.gbx_direcao.setChecked(True)

        # check proa radioButton
        self.rbt_proa.setChecked(True)

        # disable graus radioButton
        self.rbt_grau.setEnabled(False)

        # atualiza comando
        self.__update_command()

        # logger
        M_LOG.info("__on_rbt_mnr_clicked:<<")

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
