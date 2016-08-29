#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_altitude
mantém as informações sobre a dialog de altitude.

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

# model
import model.coords.coord_defs as cdefs

# view
import view.piloto.dlg_altitude_ui as dlg

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CDlgAltitude >---------------------------------------------------------------------------

class CDlgAltitude(QtGui.QDialog, dlg.Ui_CDlgAltitude):
    """
    mantém as informações sobre a dialog de altitude
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_strip_cur, fdct_prf, f_parent=None):
        """
        @param f_strip_cur: strip selecionada
        @param fdct_prf: dicionário de performances
        @param f_parent: janela pai
        """
        # logger
        M_LOG.info("__init__:>>")

        # check input parameters
        assert f_strip_cur

        # init super class
        super(CDlgAltitude, self).__init__(f_parent)

        # salva o dicionário de performances
        self.__dct_prf = fdct_prf

        # flag altitude 
        self.__v_flag_alt = True

        # monta a dialog
        self.setupUi(self)

        # configura título da dialog
        self.setWindowTitle(u"Altitude")

        # configurações de conexões slot/signal
        self.__config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.__config_texts()

        # restaura as configurações da janela de edição
        self.__restore_settings()

        # inicia valores
        self.sbx_alt.setValue(f_strip_cur.f_alt)
        self.sbx_raz.setValue(f_strip_cur.f_raz)

        # performance existe ?
        if fdct_prf is not None:

            # faixa de razão
            self.sbx_raz.setRange(2.0, self.__dct_prf["raz_max_sub_crz"])
            M_LOG.debug("__on_rbt_raz_clicked:raz_max:[{}]".format(self.__dct_prf["raz_max_sub_crz"]))

        # senão,...
        else:
            # faixa de razão
            self.sbx_raz.setRange(2.0, 25.)
            M_LOG.debug("__on_rbt_raz_clicked:raz_max:[25]")

        # configura botões
        self.bbx_altitude.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_altitude.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # inicia os parâmetros da altitude
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
        self.gbx_razao.clicked.connect(self.__on_gbx_clicked)

        # conecta radioButton
        self.rbt_alt.clicked.connect(self.__on_rbt_alt_clicked)
        self.rbt_niv.clicked.connect(self.__on_rbt_niv_clicked)

        # conecta spinBox
        self.sbx_alt.valueChanged.connect(self.__on_sbx_valueChanged)
        self.sbx_raz.valueChanged.connect(self.__on_sbx_valueChanged)

        # conecta botão Ok da edição de altitude
        # self.bbx_altitude.accepted.connect(self.__accept)

        # conecta botão Cancela da edição de altitude
        # self.bbx_altitude.rejected.connect(self.__reject)

        # logger
        M_LOG.info("__config_connects:<<")

    # ---------------------------------------------------------------------------------------------

    def __config_texts(self):

        # logger
        M_LOG.info("__config_texts:>>")

        # configura títulos e mensagens
        self.__txt_settings = "CDlgAltitude"

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

        # direita ?
        if self.rbt_alt.isChecked():
            ls_cmd = "ALT {} ".format(self.sbx_alt.value())

        # senão, nível...
        else:
            ls_cmd = "NIV {} ".format(self.sbx_alt.value())

        # razão ?
        if self.gbx_razao.isChecked():
            ls_cmd += "RAZ {} ".format(self.sbx_raz.value())

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
    def __on_rbt_alt_clicked(self, f_val):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("__on_rbt_alt_clicked:>>")

        # obtém o valor atual do campo
        li_val = self.sbx_alt.value()
        M_LOG.debug("__on_rbt_alt_clicked:li_val:[{}]".format(li_val))

        # performance existe ?
        if self.__dct_prf is not None:

            # altitude máxima é o teto de serviço
            self.sbx_alt.setRange(0, self.__dct_prf["teto_sv"] * cdefs.D_CNV_M2FT)
            M_LOG.debug("__on_rbt_alt_clicked:alt_max:[{}]".format(self.__dct_prf["teto_sv"] * cdefs.D_CNV_M2FT))

        # senão,...
        else:
            # altitude máxima é 50000 ft
            self.sbx_alt.setRange(0, 50000)
            M_LOG.debug("__on_rbt_alt_clicked:alt_max:[50000]")

        # config spinBox
        self.sbx_alt.setSingleStep(1000)

        # está em modo razão ?
        if not self.__v_flag_alt:

            # converte para altitude
            self.sbx_alt.setValue(li_val * 100)

            # muda o flag para altitude
            self.__v_flag_alt = True

        # atualiza comando
        self.__update_command()

        # logger
        M_LOG.info("__on_rbt_alt_clicked:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSignature("bool")
    def __on_rbt_niv_clicked(self, f_val):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("__on_rbt_niv_clicked:>>")

        # obtém o valor atual do campo
        li_val = self.sbx_alt.value()
        M_LOG.debug("__on_rbt_niv_clicked:li_val:[{}]".format(li_val))

        # performance existe ?
        if self.__dct_prf is not None:

            # calcula o nível 
            li_nivel = int((self.__dct_prf["teto_sv"] * cdefs.D_CNV_M2FT) / 100.)
            M_LOG.debug("__on_rbt_niv_clicked:niv_max:[{}]".format(li_nivel))

            # altitude máxima é o teto de serviço
            self.sbx_alt.setRange(0, li_nivel)

        # senão,...
        else:
            # nível máximo é 500
            self.sbx_alt.setRange(0, 500)
            M_LOG.debug("__on_rbt_niv_clicked:niv_max:[500]")

        # config spinBox
        self.sbx_alt.setSingleStep(10)

        # está em modo altitude ?
        if self.__v_flag_alt:

            # converte para altitude
            self.sbx_alt.setValue(int(li_val / 100.))

            # muda o flag para razão
            self.__v_flag_alt = False

        # atualiza comando
        self.__update_command()

        # logger
        M_LOG.info("__on_rbt_niv_clicked:<<")

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
