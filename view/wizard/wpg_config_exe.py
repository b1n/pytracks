#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wpg_config_exe.
DOCUMENT ME!

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
import sys

# PyQt library
from PyQt4 import QtCore, QtGui

# control / events
import control.events.events_basic as events

# view / wizard
import view.wizard.wizard_page_model as wpm
import view.wizard.wpg_config_exe_ui as wexe_ui

# < module data >----------------------------------------------------------------------------------

# logging level
M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# < class CWPagConfigExe >---------------------------------------------------------------------------


class CWPagConfigExe (wpm.CWizardPageModel, wexe_ui.Ui_WPagConfigExe):
    """
    mantém as informações sobre a dialog de seleção do exercício.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, fdlg_wizard=None):

        # logger
        # M_LOG.info("__init__:>>")

        # inicia a super classe
        super(CWPagConfigExe, self).__init__(fdlg_wizard)

        # herdados de CWizardPageModel
        # self.dct_config    # dicionário de configuração
        # self.dlg_wizard    # dialog wizard

        # salva o control manager localmente
        self.__control = f_control

        # obtém o event manager
        self.__event = f_control.event
        assert self.__event

        # obtém o gerente de configuração
        l_config = f_control.config
        assert l_config

        # obtém o dicionário de configuração
        self.dct_config = l_config.dct_config
        assert self.dct_config

        # obtém o model manager
        self.__model = f_control.model
        assert self.__model

        # pointer para os itens correntes
        self.__exe = None

        # pointer para os dicionários a editar
        self.__dct_exe = None

        # monta a dialog
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.config_connects()

        # text settings
        self.__txt_settings = "CWPagConfigExe"

        # restaura as configurações da janela de edição
        self.restore_settings()

        # faz a carrga inicial do diretório de exercícios
        QtCore.QTimer.singleShot(0, self.load_initial)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def closeEvent(self, event):
        """
        callback de tratamento do evento Close.

        @param  event : ...
        """
        # logger
        # M_LOG.info("closeEvent:>>")

        # obtém os settings
        l_set = QtCore.QSettings("ICEA", "Merlin")
        assert l_set

        # salva geometria da janela
        l_set.setValue("%s/Geometry" % (self.__txt_settings),
                       QtCore.QVariant(self.saveGeometry()))

        # logger
        # M_LOG.info("closeEvent:<<")

    # ---------------------------------------------------------------------------------------------

    def config_connects(self):
        """
        configura as conexões slot/signal.
        """
        # logger
        # M_LOG.info("config_connects:>>")

        # conecta click a seleção da linha
        self.connect(self.qtwExeTab,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.exeSelect)

        # logger
        # M_LOG.info("config_connects:<<")

    # ---------------------------------------------------------------------------------------------

    def exeSelect(self):
        """
        seleciona um exercício a editar.
        """
        # logger
        # M_LOG.info("exeSelect:>>")

        # verifica condições de execução
        assert self.__dct_exe is not None
        assert self.qtwExeTab is not None

        # obtém o número da linha selecionada da tabela
        l_iRow = self.qtwExeTab.currentRow()
        # M_LOG.debug("l_iRow: " + str(l_iRow))

        # existe uma linha selecionada ?
        if l_iRow > -1:

            # obtém o exercício selecionado
            self.__exe = self.getCurrentSel(self.__dct_exe, self.qtwExeTab)
            assert self.__exe

            # atualiza a área de dados do exercício selecionado
            self.exeUpdateSel()

            # salva o exercício selecionado
            self.dct_config["glb.exe"] = self.__exe

            # ok para prosseguir
            self.dlg_wizard.completeStateChanged()

        # logger
        # M_LOG.info("exeSelect:<<")

    # ---------------------------------------------------------------------------------------------

    def exeUpdateList(self):
        """
        atualiza na tela os dados da lista de exercícios.
        """
        # logger
        # M_LOG.info("exeUpdateList:>>")

        # verifica condições de execução
        assert self.__dct_exe is not None
        assert self.qtwExeTab is not None

        # atualiza a QTableWidget de exercícios
        self.exeUpdateWidget()

        # obtém o exercício selecionado
        self.__exe = self.getCurrentSel(self.__dct_exe, self.qtwExeTab)
        # assert(self.__exe)

        # logger
        # M_LOG.info("exeUpdateList:<<")

    # ---------------------------------------------------------------------------------------------

    def exeUpdateSel(self):
        """
        atualiza na tela os dados do exercício selecionado.
        """
        # logger
        # M_LOG.info("exeUpdateSel:>>")

        # exercício selecionado existe ?
        if self.__exe is not None:

            # identificação
            self.txtExeID.setText(self.__exe.s_exe_id)
            self.txtExeDesc.setText(self.__exe.s_exe_desc)

        # senão, o exercício não existe
        else:

            # posiciona cursor no início do formulário
            self.txtExeID.setFocus()

        # logger
        # M_LOG.info("exeUpdateSel:<<")

    # ---------------------------------------------------------------------------------------------

    def exeUpdateWidget(self):
        """
        atualiza na tela os dados da QTableWidget de exercícios.
        """
        # logger
        # M_LOG.info("exeUpdateWidget:>>")

        # verifica condições de execução
        assert self.qtwExeTab is not None
        assert self.__dct_exe is not None

        # limpa a QTableWidget
        self.qtwExeTab.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtwExeTab.setRowCount(len(self.__dct_exe))

        # seta número de colunas e cabeçalho das colunas
        self.qtwExeTab.setColumnCount(2)
        self.qtwExeTab.setHorizontalHeaderLabels([u"Indicativo", u"Descrição"])

        # seta QTableWidget
        self.qtwExeTab.setAlternatingRowColors(True)
        self.qtwExeTab.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtwExeTab.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtwExeTab.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtwExeTab.setSortingEnabled(False)

        # linha 0 (objeto exercício)
        l_oA0 = None

        # linha selecionada (objeto exercício)
        l_oSItem = None

        # para cada exercício no dicionário...
        for l_iNdx, l_sExeID in enumerate(sorted(self.__dct_exe.keys())):

            # indicativo do exercício
            l_twiExeID = QtGui.QTableWidgetItem(l_sExeID)
            l_twiExeID.setData(QtCore.Qt.UserRole, QtCore.QVariant(l_sExeID))

            self.qtwExeTab.setItem(l_iNdx, 0, l_twiExeID)

            # é o exercício selecionado ?
            if (self.__exe is not None) and (self.__exe.s_exe_id == l_sExeID):

                # salva pointer para o item selecionado
                l_oSItem = l_twiExeID

            # obtém o exercício
            l_oExe = self.__dct_exe[l_sExeID]
            assert l_oExe

            # descrição
            l_twiExeDesc = QtGui.QTableWidgetItem(l_oExe.s_exe_desc)

            self.qtwExeTab.setItem(l_iNdx, 1, l_twiExeDesc)

        # existe um exercício selecionado ?
        if self.__exe is not None:

            # seleciona o item
            self.qtwExeTab.setCurrentItem(l_oSItem)

            # posiciona no item selecionado
            self.qtwExeTab.scrollToItem(l_oSItem)

            # marca que existe seleção
            l_oSItem.setSelected(True)

        # senão, não existe um exercício selecionado
        else:

            # seleciona a primeira linha
            self.qtwExeTab.selectRow(0)

            # obtém o exercício atual
            self.__exe = self.getCurrentSel(self.__dct_exe, self.qtwExeTab)
            # assertself.__exe

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtwExeTab.resizeColumnsToContents()

        # habilita a ordenação
        self.qtwExeTab.setSortingEnabled(True)

        # logger
        # M_LOG.info("exeUpdateWidget:<<")

    # ---------------------------------------------------------------------------------------------

    def getCurrentData(self, f_qtwTab, f_iCol):
        """
        retorna os dados associados a linha selecionada.
        """
        # logger
        # M_LOG.info("getCurrentData:>>")

        # verifica condições de execução
        assert f_qtwTab is not None
        # M_LOG.debug("f_qtwTab: " + str(f_qtwTab))

        # o dado da linha selecionada
        l_sData = ""

        # obtém o item da linha selecionada
        l_oItem = self.getCurrentItem(f_qtwTab, f_iCol)
        # M_LOG.debug("l_oItem: " + str(l_oItem))

        # existe uma linha selecionada ?
        if l_oItem is not None:

            # obtém o dado associado a linha
            l_sData = l_oItem.data(QtCore.Qt.UserRole).toString()
            # M_LOG.debug("l_sData: " + str(l_sData))

        # logger
        # M_LOG.info("getCurrentData:<<")

        # retorna o dado associado a linha selecionada
        return l_sData

    # ---------------------------------------------------------------------------------------------

    def getCurrentItem(self, f_qtwTab, f_iCol):
        """
        retorna o item associado a linha selecionada.
        """
        # logger
        # M_LOG.info("getCurrentItem:>>")

        # verifica condições de execução
        assert f_qtwTab is not None
        # M_LOG.debug("f_qtwTab: " + str(f_qtwTab))

        # o item selecionado
        l_oItem = None

        # obtém o número da linha selecionada
        l_iRow = f_qtwTab.currentRow()
        # M_LOG.debug("l_iRow: " + str(l_iRow))

        # existe uma linha selecionada ?
        if l_iRow > -1:

            # obtém o item associado
            l_oItem = f_qtwTab.item(l_iRow, f_iCol)
            # M_LOG.debug("l_oItem: " + str(l_oItem))
            assert l_oItem

        # logger
        # M_LOG.info("getCurrentItem:<<")

        # retorna o item selecionado na lista
        return l_oItem

    # ---------------------------------------------------------------------------------------------

    def getCurrentSel(self, f_dct, f_qtw):
        """
        retorna o elemento associado a linha selecionada na lista.
        """
        # logger
        # M_LOG.info("getCurrentSel:>>")

        # verifica condições de execução
        assert f_dct is not None
        assert f_qtw is not None
        # M_LOG.debug("f_dct: " + str(f_dct))

        # obtém o index da linha selecionada
        l_sID = self.getCurrentData(f_qtw, 0)
        # M_LOG.debug("l_sID: " + str(l_sID))

        # indice válido ?
        if str(l_sID) in f_dct:

            # obtém o elemento selecionado se existir uma linha selecionada
            l_oSel = f_dct[str(l_sID)]
            assert l_oSel
            # M_LOG.debug("l_oSel: " + str(l_oSel))

        # senão, índice inválido
        else:

            # não há elemento selecionado
            l_oSel = None

        # logger
        # M_LOG.info("getCurrentSel:<<")

        # retorna o elemento da linha selecionada na lista
        return l_oSel

    # ---------------------------------------------------------------------------------------------

    def is_complete(self):

        # logger
        # M_LOG.info("is_complete:><")

        # retorna flag
        return self.dct_config["glb.exe"] is not None

    # ---------------------------------------------------------------------------------------------

    def load_initial(self):
        """
        faz a carga inicial da tabela de exercícios.
        """
        # logger
        # M_LOG.info("load_initial:>>")

        # obtém o dicionário de exercícios
        self.__dct_exe = self.__model.dct_exe

        # o dicionário de exercícios não existe ?
        if self.__dct_exe is None:

            # logger
            l_log = logging.getLogger("CWPagConfigExe::load_initial")
            l_log.setLevel(M_LOG_LVL)
            l_log.critical(u"<E01: Tabela de exercícios não carregada !")

            # cria um evento de quit
            l_evtQuit = events.CQuit()
            assert l_evtQuit

            # dissemina o evento
            self.__event.post(l_evtQuit)

            # cai fora...
            sys.exit(1)

        # atualiza na tela os dados da tabela de exercícios
        self.exeUpdateList()

        # logger
        # M_LOG.info("load_initial:<<")

    # ---------------------------------------------------------------------------------------------

    def next_page(self):

        # logger
        # M_LOG.info("next_page:><")

        # retorna a próxima página
        return self.dlg_wizard._pagCanal

    # ---------------------------------------------------------------------------------------------

    def restore_settings(self):
        """
        restaura as configurações salvas para esta janela.
        """
        # logger
        # M_LOG.info("restore_settings:>>")

        # obtém os settings
        l_set = QtCore.QSettings("ICEA", "Merlin")
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self.__txt_settings)).toByteArray())

        # logger
        # M_LOG.info("restore_settings:<<")

# < the end >--------------------------------------------------------------------------------------
