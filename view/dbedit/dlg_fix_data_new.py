#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_fix_data_new

mantém as informações sobre a dialog de edição da tabela de fixos

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "mlabru, ICEA"
__date__ = "2014/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os
import sys

# PyQt library
from PyQt4 import QtCore, QtGui

# model
import model.items.fix_data as dctFix

# view
import view.dbedit.dlg_fix_edit_new as dlgFixEditNEW
import view.dbedit.dlg_fix_data_new_ui as dlgFixDataNEW_ui

# control
import control.events.events_basic as events

# < variáveis globais >----------------------------------------------------------------------------

# logging level
w_logLvl = logging.DEBUG

# < class CDlgFixDataNEW >---------------------------------------------------------------------------

class CDlgFixDataNEW (QtGui.QDialog, dlgFixDataNEW_ui.Ui_dlgFixDataNEW):
    """
    mantém as informações sobre a dialog de edição da tabela de fixos
    """
    # galileu dbus service server
    # cSRV_Path = "org.documentroot.Galileu"

    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_parent=None):
        """
        constructor
        cria a dialog de edição da tabela de fixos

        @param  f_control: control manager do editor da base de dados
        @param  f_parent: janela vinculada
        """
        # logger
        l_log.info("__init__:>>")

        # verifica parâmetros de entrada
        assert (f_control)

        # init super class
        super(CDlgFixDataNEW, self).__init__(f_parent)

        # salva o control manager localmente
        self._control = f_control

        # obtém o event manager
        self._event = f_control.oEvent
        assert (self._event)

        # obtém o gerente de configuração
        self._config = f_control.oConfig
        assert (self._config)

        # obtém o dicionário de configuração
        self._dctConfig = self._config.dctConfig
        assert (self._dctConfig)

        # obtém o model manager
        self._model = f_control.oModel
        assert (self._model)

        # salva a parent window localmente
        self._parent = f_parent

        # existe uma parent window ?
        if (self._parent is not None):

            # esconde a parent window
            self._parent.setVisible(False)

        # pointer para os itens correntes
        self._oFix = None

        # pointer para os dicionários a editar
        self._dctFix = None

        # monta a dialog
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.configConnects()

        # configurações de títulos e mensagens da janela de edição
        self.configTexts()

        # restaura as configurações da janela de edição
        self.restoreSettings()

        # configura título da dialog
        self.setWindowTitle(u"TrackS [ Edição de Fixos ]")

        # faz a carrga inicial do diretório de fixos
        QtCore.QTimer.singleShot(0, self.loadInitial)

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        callback de btnOk da dialog de edição
        faz o accept da dialog
        """
        # logger
        l_log.info("__init__:>>")

        # ok para continuar ?
        if (self.okToContinue()):

            # faz o "accept"
            QtGui.QDialog.accept(self)

            # fecha a janela de edição
            self.close()

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def closeEvent(self, event):
        """
        callback de tratamento do evento Close

        @param  event : ...
        """
        # logger
        l_log.info("__init__:>>")

        # ok para continuar ?
        if (self.okToContinue()):

            # obtém os settings
            l_set = QtCore.QSettings()
            assert (l_set)

            # salva geometria da janela
            l_set.setValue("%s/Geometry" % (self._txtSettings),
                           QtCore.QVariant(self.saveGeometry()))

            # existe a parent window ?
            if (self._parent is not None):

                # exibe a parent window
                self._parent.setVisible(True)

        # senão, ignora o request
        else:

            # ignora o evento
            event.ignore()

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def configConnects(self):
        """
        configura as conexões slot/signal
        """
        # logger
        l_log.info("__init__:>>")

        # fixo

        # conecta click a remoção de fixo
        self.connect(self.btnDel,
                     QtCore.SIGNAL("clicked()"),
                     self.fixDel)
        '''
        # conecta click a edição de fixo
        self.connect ( self.btnEdit,
                       QtCore.SIGNAL ( "clicked()" ),
                       self.fixEdit )
        '''
        # conecta click a inclusão de fixo
        self.connect(self.btnNew,
                     QtCore.SIGNAL("clicked()"),
                     self.fixNew)

        # conecta click a seleção da linha
        self.connect(self.qtwFixTab,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.fixSelect)

        # conecta botão Ok
        self.connect(self.bbxFixTab,
                     QtCore.SIGNAL("accepted()"),
                     self.accept)

        # conecta botão Cancela
        self.connect(self.bbxFixTab,
                     QtCore.SIGNAL("rejected()"),
                     self.reject)

        # configura botões
        self.bbxFixTab.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbxFixTab.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def configTexts(self):
        """
        configura títulos e mensagens
        """
        # logger
        l_log.info("__init__:>>")

        self._txtSettings = "CDlgFixDataNEW"

        # self._txtContinueTit = u"TrackS - Alterações pendentes"
        # self._txtContinueMsg = u"Salva alterações pendentes ?"

        self._txtDelFixTit = u"TrackS - Apaga fixo"
        self._txtDelFixMsg = u"Apaga fixo {0} ?"

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def fixDel(self):
        """
        callback de btnDel da dialog de edição
        deleta um fixo da lista
        """
        # logger
        l_log.info("__init__:>>")

        # verifica condições de execução
        assert (self.qtwFixTab is not None)
        assert (self._dctFix is not None)

        # obtém o fixo selecionado
        self._oFix = self.getCurrentSel(self._dctFix, self.qtwFixTab)

        if (self._oFix is not None):

            # apaga o fixo atual ?
            if (QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
               self._txtDelFixTit,
               self._txtDelFixMsg.format(self._oFix.sFixID),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)):

                # apaga o fixo
                self.fixRemove(self._oFix)

        # logger
        l_log.info("__init__:<<")
    '''
    # ---------------------------------------------------------------------------------------------
    def fixEdit ( self ):
        """
        callback de btnEdit da dialog de edição
        edita um fixo da QTableWidget
        """
        # logger
        l_log.debug ( ">>" )

        # verifica condições de execução
        assert ( self.qtwFixTab is not None )
        assert ( self._dctFix is not None )

        # obtém o fixo selecionado
        self._oFix = self.getCurrentSel ( self._dctFix, self.qtwFixTab )

        if ( self._oFix is not None ):

            # cria a dialog de edição de fixos
            l_Dlg = dlgFixEditNEW.dlgFixEditNEW ( self._control, self._oFix, self )
            assert ( l_Dlg )

            # processa a dialog de edição de fixos (modal)
            if ( l_Dlg.exec_ ()):

                # salva em disco as alterações no fixo
                # self._oFix.save2Disk ( self._oFix._sPN )

                # se ok, atualiza a QTableWidget de fixos
                self.fixUpdateWidget ()

        # logger
        l_log.debug ( "<<" )
    '''
    # ---------------------------------------------------------------------------------------------

    def fixNew(self):
        """
        callback de btnNew da dialog de edição
        cria um novo fixo na lista
        """
        # logger
        l_log.info("__init__:>>")

        # cria a dialog de edição de fixos
        l_Dlg = dlgFixEditNEW.dlgFixEditNEW(self._control, None, self)
        assert (l_Dlg)

        # processa a dialog de edição de fixos (modal)
        if (l_Dlg.exec_()):

            # obtém os dados da edição
            self._oFix = l_Dlg.getData()

            # fixo existente ?
            if ((self._oFix is not None) and (self._dctFix is not None)):

                # insere o fixo na lista
                self._dctFix.append(self._oFix)

                # salva o arquivo no disco
                # self._oFix.save2Disk ( l_sPath )

                # se ok, atualiza a QTableWidget de fixos
                self.fixUpdateWidget()

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def fixRemove(self, f_oFix):
        """
        remove o fixo selecionado

        @param  f_oFix : pointer para o fixo a remover
        """
        # logger
        l_log.info("__init__:>>")

        # verifica condições de execução
        assert (f_oFix is not None)

        l_log.info("f_oFix: " + str(f_oFix))

        # remove a linha da widget
        self.qtwFixTab.removeRow(self.qtwFixTab.currentRow())

        # remove o fixo da lista
        self._dctFix.remove(f_oFix)

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def fixSelect(self):
        """
        seleciona um fixo a editar
        """
        # logger
        l_log.info("__init__:>>")

        # verifica condições de execução
        assert (self._dctFix is not None)
        assert (self.qtwFixTab is not None)

        # obtém o fixo selecionado
        self._oFix = self.getCurrentSel(self._dctFix, self.qtwFixTab)
        assert (self._oFix)

        # atualiza a área de dados do fixo selecionado
        self.fixUpdateSel()

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def fixUpdateList(self):
        """
        atualiza na tela os dados da lista de fixos
        """
        # logger
        l_log.info("__init__:>>")

        # verifica condições de execução
        assert (self._dctFix is not None)
        assert (self.qtwFixTab is not None)

        # atualiza a QTableWidget de fixos
        self.fixUpdateWidget()

        # obtém o fixo selecionado
        self._oFix = self.getCurrentSel(self._dctFix, self.qtwFixTab)
        # assert ( self._oFix )

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def fixUpdateSel(self):
        """
        atualiza na tela os dados do fixo selecionado
        """
        # logger
        l_log.info("__init__:>>")

        # fixo selecionado existe ?
        if (self._oFix is not None):

            # indicativo do fixo
            l_sFixID = self._oFix.sFixID

            # atualiza a visualização do fixo
            # self._oSrv.configFix ( l_sFixID, dbus_interface = self.cSRV_Path )

            # identificação
            self.txtFixID.setText(self._oFix.sFixID)
            self.qleFixDesc.setText(self._oFix.sFixDesc)

            # tipo de fixo

            # VOR
            if (self._oFix.vFixVOR):
                self.ckxVOR.setCheckState(QtCore.Qt.Checked)
            else:
                self.ckxVOR.setCheckState(QtCore.Qt.Unchecked)

            # NDB
            if (self._oFix.vFixNDB):
                self.ckxNDB.setCheckState(QtCore.Qt.Checked)
            else:
                self.ckxNDB.setCheckState(QtCore.Qt.Unchecked)

            # DME
            if (self._oFix.vFixDME):
                self.ckxDME.setCheckState(QtCore.Qt.Checked)
            else:
                self.ckxDME.setCheckState(QtCore.Qt.Unchecked)

            # freqüência
            self.dsbFreq.setValue(self._oFix.fFixFreq)

            # posição
            self._oFix.oFixPos = None

            # l_iX, l_iY = self._oFix.oCentro.getPto ()

            # self.txtCntrX.setText ( str ( l_iX ))
            # self.txtCntrY.setText ( str ( l_iY ))

        # senão, o fixo não existe
        else:

            # posiciona cursor no início do formulário
            self.txtFixID.setFocus()

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def fixUpdateWidget(self):
        """
        atualiza na tela os dados da QTableWidget de fixos
        """
        # logger
        l_log.info("__init__:>>")

        # verifica condições de execução
        assert (self.qtwFixTab is not None)
        assert (self._dctFix is not None)

        # limpa a QTableWidget
        self.qtwFixTab.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtwFixTab.setRowCount(len(self._dctFix))

        # seta número de colunas e cabeçalho das colunas
        self.qtwFixTab.setColumnCount(2)
        self.qtwFixTab.setHorizontalHeaderLabels([u"Indicativo", u"Descrição"])

        # seta QTableWidget
        self.qtwFixTab.setAlternatingRowColors(True)
        self.qtwFixTab.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtwFixTab.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtwFixTab.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtwFixTab.setSortingEnabled(False)

        # linha 0 (objeto fixo)
        l_oA0 = None

        # linha selecionada (objeto fixo)
        l_oSItem = None

        # para cada fixo no dicionário...
        for l_iNdx, l_sFixID in enumerate(sorted(self._dctFix.keys())):

            # indicativo do fixo
            l_twiFixID = QtGui.QTableWidgetItem(l_sFixID)
            l_twiFixID.setData(QtCore.Qt.UserRole, QtCore.QVariant(l_sFixID))

            self.qtwFixTab.setItem(l_iNdx, 0, l_twiFixID)

            # é o fixo selecionado ?
            if ((self._oFix is not None) and (self._oFix.sFixID == l_sFixID)):

                # salva pointer para o item selecionado
                l_oSItem = l_twiFixID

            # obtém o fixo
            l_oFix = self._dctFix[l_sFixID]
            assert (l_oFix)

            # descrição
            l_twiFixDesc = QtGui.QTableWidgetItem(l_oFix.sFixDesc)

            self.qtwFixTab.setItem(l_iNdx, 1, l_twiFixDesc)

        # existe um fixo selecionado ?
        if (self._oFix is not None):

            # seleciona o item
            self.qtwFixTab.setCurrentItem(l_oSItem)

            # posiciona no item selecionado
            self.qtwFixTab.scrollToItem(l_oSItem)

            # marca que existe seleção
            l_oSItem.setSelected(True)

        # senão, não existe um fixo selecionado
        else:

            # seleciona a primeira linha
            self.qtwFixTab.selectRow(0)

            # obtém o fixo atual
            self._oFix = self.getCurrentSel(self._dctFix, self.qtwFixTab)
            # assert ( self._oFix )

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtwFixTab.resizeColumnsToContents()

        # habilita a ordenação
        self.qtwFixTab.setSortingEnabled(True)

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def getCurrentData(self, f_qtwTab, f_iCol):
        """
        retorna os dados associados a linha selecionada
        """
        # logger
        l_log.info("__init__:>>")

        # verifica condições de execução
        assert (f_qtwTab is not None)
        l_log.info("f_qtwTab: " + str(f_qtwTab))

        # o dado da linha selecionada
        l_sData = ""

        # obtém o item da linha selecionada
        l_oItem = self.getCurrentItem(f_qtwTab, f_iCol)
        l_log.info("l_oItem: " + str(l_oItem))

        # existe uma linha selecionada ?
        if (l_oItem is not None):

            # obtém o dado associado a linha
            l_sData = l_oItem.data(QtCore.Qt.UserRole).toString()
            l_log.info("l_sData: " + str(l_sData))

        # logger
        l_log.info("__init__:<<")

        # retorna o dado associado a linha selecionada
        return l_sData

    # ---------------------------------------------------------------------------------------------
    def getCurrentItem(self, f_qtwTab, f_iCol):
        """
        retorna o item associado a linha selecionada
        """
        # logger
        l_log.info("__init__:>>")

        # verifica condições de execução
        assert (f_qtwTab is not None)
        l_log.info("f_qtwTab: " + str(f_qtwTab))

        # o item selecionado
        l_oItem = None

        # obtém o número da linha selecionada
        l_iRow = f_qtwTab.currentRow()
        l_log.info("l_iRow: " + str(l_iRow))

        # existe uma linha selecionada ?
        if (l_iRow > -1):

            # obtém o item associado
            l_oItem = f_qtwTab.item(l_iRow, f_iCol)
            l_log.info("l_oItem: " + str(l_oItem))
            assert (l_oItem)

        # logger
        l_log.info("__init__:<<")

        # retorna o item selecionado na lista
        return l_oItem

    # ---------------------------------------------------------------------------------------------
    def getCurrentSel(self, f_dct, f_qtw):
        """
        retorna o elemento associado a linha selecionada na lista
        """
        # logger
        l_log.info("__init__:>>")

        # verifica condições de execução
        assert (f_dct is not None)
        assert (f_qtw is not None)
        # l_log.info ( "f_dct: " + str ( f_dct ))

        # obtém o index da linha selecionada
        l_sID = self.getCurrentData(f_qtw, 0)
        # l_log.info ( "l_sID: " + str ( l_sID ))

        # indice válido ?
        if (str(l_sID) in f_dct):

            # obtém o elemento selecionado se existir uma linha selecionada
            l_oSel = f_dct[str(l_sID)]
            assert (l_oSel)
            # l_log.info ( "l_oSel: " + str ( l_oSel ))

        # senão, índice inválido
        else:

            # não há elemento selecionado
            l_oSel = None

        # logger
        l_log.info("__init__:<<")

        # retorna o elemento da linha selecionada na lista
        return l_oSel

    # ---------------------------------------------------------------------------------------------
    def loadInitial(self):
        """
        faz a carga inicial da tabela de fixos
        """
        # logger
        l_log.info("__init__:>>")

        # obtém o dicionário de fixos
        self._dctFix = self._model.dctFix

        # o dicionário de fixos não existe ?
        if (self._dctFix is None):

            # logger
            l_log.critical(u"<E01: Tabela de fixos não carregada !")

            # cria um evento de quit
            l_evtQuit = events.Quit()
            assert (l_evtQuit)

            # dissemina o evento
            self._event.post(l_evtQuit)

            # cai fora...
            sys.exit(1)

        # atualiza na tela os dados da tabela de fixos
        self.fixUpdateList()

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def okToContinue(self):
        """
        cria uma messageBox

        @return True se tratou a resposta, senão False
        """
        # logger
        l_log.info("__init__:>>")

        # resposta
        l_bAns = True
        '''
        l_log.info ( "self._bChanged: " + str ( self._bChanged ))

        # flag de alterações setado ?
        if ( self._bChanged ):

            # questiona sobre alterações pendentes
            l_Resp = QtGui.QMessageBox.question ( self, self._txtContinueTit,
                                                        self._txtContinueMsg,
                                                        QtGui.QMessageBox.Yes |
                                                        QtGui.QMessageBox.No |
                                                        QtGui.QMessageBox.Cancel )

            # cancela ?
            if ( QtGui.QMessageBox.Cancel == l_Resp ):

                # não sai
                l_bAns = False

            # salva ?
            elif ( QtGui.QMessageBox.Yes == l_Resp ):

                # salva as pendências e sai
                l_bAns = True

            # não salva ?
           else:

               # reseta o flag de alterações...
               self._bChanged = False
               l_log.info ( "self._bChanged: " + str ( self._bChanged ))

               # ...e sai
               l_bAns = True
        '''
        # logger
        l_log.info("__init__:<<")

        # retorna a resposta
        return l_bAns

    # ---------------------------------------------------------------------------------------------
    def reject(self):
        """
        DOCUMENT ME!
        """
        # logger
        l_log.info("__init__:>>")

        self._oFix = None

        # faz o "reject"
        QtGui.QDialog.reject(self)

        self.close()

        # logger
        l_log.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def restoreSettings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # logger
        l_log.info("__init__:>>")

        # obtém os settings
        l_set = QtCore.QSettings()
        assert (l_set)

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self._txtSettings)).toByteArray())

        # logger
        l_log.info("__init__:<<")

        return True

# < the end >--------------------------------------------------------------------------------------
