#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_exe_data_new.
mantém as informações sobre a dialog de edição da tabela de exercícios.

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
import os
import sys

# PyQt library
from PyQt4 import QtCore, QtGui

# model / items
import model.items.exe_data as dctExe

# view / dialog / Qt
import view.dbedit.dlg_exe_edit_new as dlgEdit
import view.dbedit.dlg_exe_data_new_ui as dlgData_ui

# control / events
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logging level
M_LOG_LVL = logging.DEBUG

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(M_LOG_LVL)

# < class CDlgExeDataNEW >---------------------------------------------------------------------------


class CDlgExeDataNEW (QtGui.QDialog, dlgData_ui.Ui_DlgExeDataNEW):
    """
    mantém as informações sobre a dialog de edição da tabela de exercícios.
    """
    # galileu dbus service server
    # cSRV_Path = "org.documentroot.Galileu"

    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_parent=None):
        """
        constructor.
        cria a dialog de edição da tabela de exercícios.

        @param f_control: control manager do editor da base de dados
        @param f_parent: janela vinculada.
        """

        # logger
        M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_control

        # init super class
        super(CDlgExeDataNEW, self).__init__(f_parent)

        # salva o control manager localmente
        self._control = f_control

        # obtém o event manager
        self._event = f_control.event
        assert self._event

        # obtém o gerente de configuração
        self._config = f_control.config
        assert self._config

        # obtém o dicionário de configuração
        self._dctConfig = self._config.dct_config
        assert self._dctConfig

        # obtém o model manager
        self._model = f_control.model
        assert self._model

        # salva a parent window localmente
        self._parent = f_parent

        # existe uma parent window ?
        if self._parent is not None:

            # esconde a parent window
            self._parent.setVisible(False)

        # pointer para os itens correntes
        self._oExe = None

        # pointer para os dicionários a editar
        self._dctExe = None

        # monta a dialog
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.configConnects()

        # configurações de títulos e mensagens da janela de edição
        self.configTexts()

        # restaura as configurações da janela de edição
        self.restoreSettings()

        # configura título da dialog
        self.setWindowTitle(u"dbEdit [ Edição de Exercícios ]")

        # faz a carrga inicial do diretório de exercícios
        QtCore.QTimer.singleShot(0, self.loadInitial)

        # logger
        M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def accept(self):
        """
        callback de btnOk da dialog de edição.
        faz o accept da dialog.
        """
        # logger
        M_LOG.info("accept:>>")

        # ok para continuar ?
        if self.okToContinue():

            # faz o "accept"
            QtGui.QDialog.accept(self)

            # fecha a janela de edição
            self.close()

        # logger
        M_LOG.info("accept:<<")

    # ---------------------------------------------------------------------------------------------

    def closeEvent(self, event):
        """
        callback de tratamento do evento Close.

        @param  event : ...
        """
        # logger
        M_LOG.info("closeEvent:>>")

        # ok para continuar ?
        if self.okToContinue():

            # obtém os settings
            l_set = QtCore.QSettings()
            assert l_set

            # salva geometria da janela
            l_set.setValue("%s/Geometry" % (self._txtSettings),
                           QtCore.QVariant(self.saveGeometry()))

            # existe a parent window ?
            if self._parent is not None:

                # exibe a parent window
                self._parent.setVisible(True)

        # senão, ignora o request
        else:

            # ignora o evento
            event.ignore()

        # logger
        M_LOG.info("closeEvent:<<")

    # ---------------------------------------------------------------------------------------------

    def configConnects(self):
        """
        configura as conexões slot/signal.
        """
        # logger
        M_LOG.info("configConnects:>>")

        # exercício

        # conecta click a remoção de exercício
        self.connect(self.btnDel,
                     QtCore.SIGNAL("clicked()"),
                     self.exeDel)
        '''
        # conecta click a edição de exercício
        self.connect(self.btnEdit,
                       QtCore.SIGNAL("clicked()"),
                       self.exeEdit)
        '''
        # conecta click a inclusão de exercício
        self.connect(self.btnNew,
                     QtCore.SIGNAL("clicked()"),
                     self.exeNew)

        # conecta click a seleção da linha
        self.connect(self.qtwExeTab,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.exeSelect)

        # conecta botão Ok
        self.connect(self.bbxExeTab,
                     QtCore.SIGNAL("accepted()"),
                     self.accept)

        # conecta botão Cancela
        self.connect(self.bbxExeTab,
                     QtCore.SIGNAL("rejected()"),
                     self.reject)

        # configura botões
        self.bbxExeTab.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbxExeTab.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # logger
        M_LOG.info("configConnects:<<")

    # ---------------------------------------------------------------------------------------------

    def configTexts(self):
        """
        configura títulos e mensagens.
        """
        # logger
        M_LOG.info("configTexts:>>")

        self._txtSettings = "CDlgExeDataNEW"

        # self._txtContinueTit = u"TrackS - Alterações pendentes"
        # self._txtContinueMsg = u"Salva alterações pendentes ?"

        self._txtDelExeTit = u"TrackS - Apaga exercício"
        self._txtDelExeMsg = u"Apaga exercício {0} ?"

        # logger
        M_LOG.info("configTexts:<<")

    # ---------------------------------------------------------------------------------------------

    def exeDel(self):
        """
        callback de btnDel da dialog de edição.
        deleta um exercício da lista.
        """
        # logger
        M_LOG.info("exeDel:>>")

        # verifica condições de execução
        assert self.qtwExeTab is not None
        assert self._dctExe is not None

        # obtém o exercício selecionado
        self._oExe = self.getCurrentSel(self._dctExe, self.qtwExeTab)

        if self._oExe is not None:

            # apaga o exercício atual ?
            if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
               self._txtDelExeTit,
               self._txtDelExeMsg.format(self._oExe._sExeID),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No):

                # apaga o exercício
                self.exeRemove(self._oExe)

        # logger
        M_LOG.info("exeDel:<<")
    '''
    # ---------------------------------------------------------------------------------------------

    def exeEdit(self):
        """
        callback de btnEdit da dialog de edição.
        edita um exercício da QTableWidget.
        """
        # logger
        l_log.debug(">>")

        # verifica condições de execução
        assert self.qtwExeTab is not None
        assert self._dctExe is not None

        # obtém o exercício selecionado
        self._oExe = self.getCurrentSel(self._dctExe, self.qtwExeTab)

        if(self._oExe is not None):

            # cria a dialog de edição de exercícios
            l_Dlg = dlgEdit.dlgExeEditNEW(self._control, self._oExe, self)
            assert l_Dlg

            # processa a dialog de edição de exercícios (modal)
            if(l_Dlg.exec_ ()):

                # salva em disco as alterações no exercício
                # self._oExe.save2Disk(self._oExe._sPN)

                # se ok, atualiza a QTableWidget de exercícios
                self.exeUpdateWidget ()

        # logger
        l_log.debug("<<")
    '''
    # ---------------------------------------------------------------------------------------------

    def exeNew(self):
        """
        callback de btnNew da dialog de edição.
        cria um novo exercício na lista.
        """
        # logger
        M_LOG.info("exeNew:>>")

        # cria a dialog de edição de exercícios
        l_Dlg = dlgEdit.dlgExeEditNEW(self._control, None, self)
        assert l_Dlg

        # processa a dialog de edição de exercícios (modal)
        if l_Dlg.exec_():

            # obtém os dados da edição
            self._oExe = l_Dlg.getData()

            # exercício existente ?
            if (self._oExe is not None) and (self._dctExe is not None):

                # insere o exercício na lista
                self._dctExe.append(self._oExe)

                # salva o arquivo no disco
                # self._oExe.save2Disk(l_sPath)

                # se ok, atualiza a QTableWidget de exercícios
                self.exeUpdateWidget()

        # logger
        M_LOG.info("exeNew:<<")

    # ---------------------------------------------------------------------------------------------

    def exeRemove(self, f_oExe):
        """
        remove o exercício selecionado.

        @param  f_oExe : pointer para o exercício a remover.
        """
        # logger
        M_LOG.info("exeRemove:>>")

        # verifica condições de execução
        assert f_oExe is not None

        M_LOG.debug("f_oExe: " + str(f_oExe))

        # remove a linha da widget
        self.qtwExeTab.removeRow(self.qtwExeTab.currentRow())

        # remove o exercício da lista
        self._dctExe.remove(f_oExe)

        # logger
        M_LOG.info("exeRemove:<<")

    # ---------------------------------------------------------------------------------------------

    def exeSelect(self):
        """
        seleciona um exercício a editar.
        """
        # logger
        M_LOG.info("exeSelect:>>")

        # verifica condições de execução
        assert self._dctExe is not None
        assert self.qtwExeTab is not None

        # obtém o exercício selecionado
        self._oExe = self.getCurrentSel(self._dctExe, self.qtwExeTab)
        assert self._oExe

        # atualiza a área de dados do exercício selecionado
        self.exeUpdateSel()

        # logger
        M_LOG.info("exeSelect:<<")

    # ---------------------------------------------------------------------------------------------

    def exeUpdateList(self):
        """
        atualiza na tela os dados da lista de exercícios.
        """
        # logger
        M_LOG.info("exeUpdateList:>>")

        # verifica condições de execução
        assert self._dctExe is not None
        assert self.qtwExeTab is not None

        # atualiza a QTableWidget de exercícios
        self.exeUpdateWidget()

        # obtém o exercício selecionado
        self._oExe = self.getCurrentSel(self._dctExe, self.qtwExeTab)
        # assert self._oExe

        # logger
        M_LOG.info("exeUpdateList:<<")

    # ---------------------------------------------------------------------------------------------

    def exeUpdateSel(self):
        """
        atualiza na tela os dados do exercício selecionado.
        """
        # logger
        M_LOG.info("exeUpdateSel:>>")

        # exercício selecionado existe ?
        if self._oExe is not None:

            # indicativo do exercício
            l_sExeID = self._oExe.sExeID

            # atualiza a visualização do exercício
            # self._oSrv.configExe(l_sExeID, dbus_interface = self.cSRV_Path)

            # identificação
            self.txtExeID.setText(self._oExe.sExeID)
            self.qleExeDesc.setText(self._oExe.sExeDesc)

            # freqüência
            # self._oExe._fExeFrequencia = 0.

            # posição

            # posição
            # self._oExe._oExePosicao = None

            # l_iX, l_iY = self._oExe._oCentro.getPto ()

            # self.txtCntrX.setText(str(l_iX))
            # self.txtCntrY.setText(str(l_iY))

        # senão, o exercício não existe
        else:

            # posiciona cursor no início do formulário
            self.txtExeID.setFocus()

        # logger
        M_LOG.info("exeUpdateSel:<<")

    # ---------------------------------------------------------------------------------------------

    def exeUpdateWidget(self):
        """
        atualiza na tela os dados da QTableWidget de exercícios.
        """
        # logger
        M_LOG.info("exeUpdateWidget:>>")

        # verifica condições de execução
        assert self.qtwExeTab is not None
        assert self._dctExe is not None

        # limpa a QTableWidget
        self.qtwExeTab.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtwExeTab.setRowCount(len(self._dctExe))

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
        for l_iNdx, l_sExeID in enumerate(sorted(self._dctExe.keys())):

            # indicativo do exercício
            l_twiExeID = QtGui.QTableWidgetItem(l_sExeID)
            l_twiExeID.setData(QtCore.Qt.UserRole, QtCore.QVariant(l_sExeID))

            self.qtwExeTab.setItem(l_iNdx, 0, l_twiExeID)

            # é o exercício selecionado ?
            if (self._oExe is not None) and (self._oExe._sExeID == l_sExeID):

                # salva pointer para o item selecionado
                l_oSItem = l_twiExeID

            # obtém o exercício
            l_oExe = self._dctExe[l_sExeID]
            assert l_oExe

            # descrição
            l_twiExeDesc = QtGui.QTableWidgetItem(l_oExe._sExeDesc)

            self.qtwExeTab.setItem(l_iNdx, 1, l_twiExeDesc)

        # existe um exercício selecionado ?
        if self._oExe is not None:

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
            self._oExe = self.getCurrentSel(self._dctExe, self.qtwExeTab)
            # assert self._oExe

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtwExeTab.resizeColumnsToContents()

        # habilita a ordenação
        self.qtwExeTab.setSortingEnabled(True)

        # logger
        M_LOG.info("exeUpdateWidget:<<")

    # ---------------------------------------------------------------------------------------------

    def getCurrentData(self, f_qtwTab, f_iCol):
        """
        retorna os dados associados a linha selecionada.
        """
        # logger
        M_LOG.info("getCurrentData:>>")

        # verifica condições de execução
        assert f_qtwTab is not None
        M_LOG.debug("f_qtwTab: " + str(f_qtwTab))

        # o dado da linha selecionada
        l_sData = ""

        # obtém o item da linha selecionada
        l_oItem = self.getCurrentItem(f_qtwTab, f_iCol)
        M_LOG.debug("l_oItem: " + str(l_oItem))

        # existe uma linha selecionada ?
        if l_oItem is not None:

            # obtém o dado associado a linha
            l_sData = l_oItem.data(QtCore.Qt.UserRole).toString()
            M_LOG.debug("l_sData: " + str(l_sData))

        # logger
        M_LOG.info("getCurrentData:<<")

        # retorna o dado associado a linha selecionada
        return l_sData

    # ---------------------------------------------------------------------------------------------

    def getCurrentItem(self, f_qtwTab, f_iCol):
        """
        retorna o item associado a linha selecionada.
        """
        # o item selecionado
        l_oItem = None

        # logger
        M_LOG.info("getCurrentItem:>>")

        # verifica condições de execução
        assert f_qtwTab is not None
        M_LOG.debug("f_qtwTab: " + str(f_qtwTab))

        # obtém o número da linha selecionada
        l_iRow = f_qtwTab.currentRow()
        M_LOG.debug("l_iRow: " + str(l_iRow))

        # existe uma linha selecionada ?
        if l_iRow > -1:

            # obtém o item associado
            l_oItem = f_qtwTab.item(l_iRow, f_iCol)
            M_LOG.debug("l_oItem: " + str(l_oItem))
            assert l_oItem

        # logger
        M_LOG.info("getCurrentItem:<<")

        # retorna o item selecionado na lista
        return l_oItem

    # ---------------------------------------------------------------------------------------------

    def getCurrentSel(self, f_dct, f_qtw):
        """
        retorna o elemento associado a linha selecionada na lista.
        """
        # logger
        M_LOG.info("getCurrentSel:>>")

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
        M_LOG.info("getCurrentSel:<<")

        # retorna o elemento da linha selecionada na lista
        return l_oSel

    # ---------------------------------------------------------------------------------------------

    def loadInitial(self):
        """
        faz a carga inicial da tabela de exercícios.
        """
        # logger
        M_LOG.info("loadInitial:>>")

        # obtém o dicionário de exercícios
        self._dctExe = self._model.dct_exe

        # o dicionário de exercícios não existe ?
        if self._dctExe is None:

            # logger
            l_log.critical(u"<E01: Tabela de exercícios não carregada !")

            # cria um evento de quit
            l_evtQuit = events.CQuit()
            assert l_evtQuit

            # dissemina o evento
            self._event.post(l_evtQuit)

            # cai fora...
            sys.exit(1)

        # atualiza na tela os dados da tabela de exercícios
        self.exeUpdateList()

        # logger
        M_LOG.info("loadInitial:<<")

    # ---------------------------------------------------------------------------------------------

    def okToContinue(self):
        """
        cria uma messageBox.

        @return True se tratou a resposta, senão False.
        """
        # logger
        M_LOG.info("okToContinue:>>")

        # resposta
        l_bAns = True
        '''
        M_LOG.debug("self._bChanged: " + str(self._bChanged))

        # flag de alterações setado ?
        if(self._bChanged):

            # questiona sobre alterações pendentes
            l_Resp = QtGui.QMessageBox.question(self, self._txtContinueTit,
                                                        self._txtContinueMsg,
                                                        QtGui.QMessageBox.Yes |
                                                        QtGui.QMessageBox.No |
                                                        QtGui.QMessageBox.Cancel)

            # cancela ?
            if(QtGui.QMessageBox.Cancel == l_Resp):

                # não sai
                l_bAns = False

            # salva ?
            elif(QtGui.QMessageBox.Yes == l_Resp):

                # salva as pendências e sai
                l_bAns = True

            # não salva ?
           else:

               # reseta o flag de alterações...
               self._bChanged = False
               M_LOG.debug("self._bChanged: " + str(self._bChanged))

               # ...e sai
               l_bAns = True
        '''
        # logger
        M_LOG.info("okToContinue:<<")

        # retorna a resposta
        return l_bAns

    # ---------------------------------------------------------------------------------------------

    def reject(self):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("reject:>>")

        self._oExe = None

        # faz o "reject"
        QtGui.QDialog.reject(self)

        self.close()

        # logger
        M_LOG.info("reject:<<")

    # ---------------------------------------------------------------------------------------------

    def restoreSettings(self):
        """
        restaura as configurações salvas para esta janela.
        """
        # logger
        M_LOG.info("restoreSettings:>>")

        # obtém os settings
        l_set = QtCore.QSettings("ICEA", "dbEdit")
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self._txtSettings)).toByteArray())

        # logger
        M_LOG.info("restoreSettings:<<")

        return True

# < the end >--------------------------------------------------------------------------------------
