#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_aer_data_new

mantém as informações sobre a dialog de edição da tabela de aeródromos

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
# import signal
# import subprocess
import sys
# import time
# import traceback

# DBus services
# import dbus

# PyQt library
from PyQt4 import QtCore, QtGui

# model
from ...model.coords import coord_conv as cconv
# import model.coords.coord_defs as cdefs
# import model.items.aer_data as aerdata

# import model.figuras.clsFig as clsFig

# view
from . import dlg_aer_edit_new as dlgedit
# import view.dbedit.dlgCabCAD as dlgCabCAD
# import view.dbedit.dlgFig as dlgFig
# import view.dbedit.dlgPNS as dlgPNS
# import view.dbedit.dlgPstCAD as dlgPstCAD

from . import dlg_aer_data_new_ui as dlgdata

# import view.dbedit.dlgView as dlgView

# control
from ...control.events import events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CDlgAerDataNEW >-------------------------------------------------------------------------

class CDlgAerDataNEW(QtGui.QDialog, dlgdata.Ui_dlgAerDataNEW):
    """
    mantém as informações sobre a dialog de edição de aeródromos
    """
    # galileu dbus service server
    # cSRV_Path = "org.documentroot.Galileu"

    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_parent=None):
        """
        @param f_control: control manager
        @param f_parent: janela pai
        """
        # logger
        M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_control

        # init super class
        super(CDlgAerDataNEW, self).__init__(f_parent)

        # salva o control manager localmente
        self.__control = f_control

        # obtém o dicionário de configuração
        self.__dct_config = f_control.config.dct_config
        assert self.__dct_config

        # obtém o model manager
        self.__model = f_control.model
        assert self.__model

        # salva a parent window localmente
        self.__parent = f_parent

        # existe uma parent window ?
        if self.__parent is not None:

            # esconde a parent window
            self.__parent.setVisible(False)

        # pointer para os itens correntes
        self.__obj_aer = None
        self.__obj_pst = None
        # self._oCab = None
        # self._oFig = None
        # self._oPNS = None

        # pointer para os dicionários a editar
        self.__dct_aer = None
        # self._dctCab = None
        # self._dctFig = None
        # self._dctPNS = None

        # self._lstView = [ True for _ in xrange(clsFig.clsFig.cFIG_Max + 3) ]

        # pointer para o DBus services server (Galileu)
        # self._oSrv = None
        # self._oIFace = None

        # inicia o DBus services server (Galileu)
        # self.connectDBus ()

        # monta a dialog
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.config_connects()

        # configurações de títulos e mensagens da janela de edição
        self.config_texts()

        # restaura as configurações da janela de edição
        self.restore_settings()

        # configura título da dialog
        self.setWindowTitle(u"[ Edição de Aeródromos ]")

        # faz a carrga inicial do diretório de aeródromos
        QtCore.QTimer.singleShot(0, self.__jump_start)

        # logger
        M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def accept(self):
        """
        callback de btn_ok da dialog de edição
        faz o accept da dialog
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
    '''
    # ---------------------------------------------------------------------------------------------

    def aerEdit(self):
        """
        callback de btnEdit da dialog de edição
        edita um aeródromo da QTableWidget
        """
        # logger
        M_LOG.info("aerEdit:>>")

        # verifica condições de execução
        assert self.qtw_aer is not None
        assert self.__dct_aer is not None

        # obtém o aeródromo selecionado
        self.__obj_aer = self.__get_selected_obj(self.__dct_aer, self.qtw_aer)

        if self.__obj_aer is not None:

            # cria a dialog de edição de aeródromos
            l_dlg = dlgAerEditNEW.dlgAerEditNEW(self.__control, self.__obj_aer, self)
            assert l_dlg

            # processa a dialog de edição de aeródromos (modal)
            if l_dlg.exec_ ():

                # salva em disco as alterações na aeródromo
                # self.__obj_aer.save2Disk(self.__obj_aer._sPN)

                # se ok, atualiza a QTableWidget de aeródromos
                self.__update_qtw_aer ()

        # logger
        M_LOG.info("aerEdit:<<")
    '''
    # ---------------------------------------------------------------------------------------------

    def __aer_remove(self, f_aer):
        """
        remove o aeródromo selecionado

        @param f_aer: pointer para o aeródromo a remover
        """
        # logger
        M_LOG.info("__aer_remove:>>")

        # verifica condições de execução
        assert f_aer is not None

        M_LOG.debug("f_aer: " + str(f_aer))

        # remove a linha da widget
        self.qtw_aer.removeRow(self.qtw_aer.currentRow())

        # remove o aeródromo do dicionário
        self.__dct_aer.remove(f_aer)
        '''
        # remove o arquivo de figuras associado
        ls_FN = ls_PN + ".fig"

        if (ls_FN is not None) and os.path.exists(ls_FN) and os.path.isfile(ls_FN):

            M_LOG.debug(u"removeu figuras: " + str(ls_FN))

            # remove o arquivo
            # os.remove(ls_FN)

        # remove o arquivo de pns associado
        ls_FN = ls_PN + ".pns"

        if (ls_FN is not None) and os.path.exists(ls_FN) and os.path.isfile(ls_FN):

            M_LOG.debug(u"removeu pns: " + str(ls_FN))

            # remove o arquivo
            # os.remove(ls_FN)

        # remove o arquivo de pistas associado
        ls_FN = ls_PN + ".pst"

        if (( ls_FN is not None) and os.path.exists(ls_FN) and os.path.isfile(ls_FN)):

            M_LOG.debug(u"removeu pistas: " + str(ls_FN))

            # remove o arquivo
            #os.remove(ls_FN)

        # logger
        M_LOG.info("__aer_remove:<<")
        '''
    # ---------------------------------------------------------------------------------------------

    def closeEvent(self, f_evt):
        """
        callback de tratamento do evento Close

        @param f_evt: 
        """
        # logger
        M_LOG.info("closeEvent:>>")

        # ok para continuar ?
        if self.okToContinue():

            # obtém os settings
            l_set = QtCore.QSettings()
            assert l_set

            # salva geometria da janela
            l_set.setValue("%s/Geometry" % (self.__txt_settings), QtCore.QVariant(self.saveGeometry()))

            # existe a parent window ?
            if self.__parent is not None:

                # exibe a parent window
                self.__parent.setVisible(True)

        # senão, ignora o request
        else:
            # ignora o evento
            f_evt.ignore()

        # logger
        M_LOG.info("closeEvent:<<")

    # ---------------------------------------------------------------------------------------------

    def config_connects(self):
        """
        configura as conexões slot/signal
        """
        # logger
        M_LOG.info("config_connects:>>")

        # aeródromo

        # conecta click a remoção de aeródromo
        self.btn_aer_del.clicked.connect(self.__on_btn_aer_del)

        # conecta click a edição de aeródromo
        # self.connect(self.btnEdit, QtCore.SIGNAL("clicked()"), self.aerEdit)

        # conecta click a inclusão de aeródromo
        self.btn_aer_new.clicked.connect(self.__on_btn_aer_new)

        # conecta click a seleção da linha
        self.qtw_aer.itemSelectionChanged.connect(self.__on_qtw_aer_selection_changed)

        # conecta botão Ok
        self.bbx_aer.accepted.connect(self.accept)

        # conecta botão Cancela
        self.bbx_aer.rejected.connect(self.reject)

        # configura botões
        self.bbx_aer.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbx_aer.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # pistas

        # conecta click a seleção da linha
        self.qtw_pst.itemSelectionChanged.connect(self.__on_qtw_pst_selection_changed)

        # conecta click a remoção de pista
        # self.btnPstDel.clicked.connect(self.pstDel)

        # conecta click a edição de pista
        # self.btnPstEdit.clicked.connect(self.pstEdit)

        # conecta click a inserção de pista
        # self.btnPstNew.clicked.connect(self.pstNew)

        # logger
        M_LOG.info("config_connects:<<")

    # ---------------------------------------------------------------------------------------------

    def config_texts(self):
        """
        configura títulos e mensagens
        """
        # logger
        M_LOG.info("config_texts:>>")

        self.__txt_settings = "CDlgAerDataNEW"

        # self._txtContinueTit = u"Alterações pendentes"
        # self._txtContinueMsg = u"Salva alterações pendentes ?"

        self.__txt_del_aer_Tit = u"Apaga aeródromo"
        self.__txt_del_aer_Msg = u"Apaga aeródromo {0} ?"

        self.__txt_del_pst_Tit = "Apaga pista"
        self.__txt_del_pst_Msg = "Apaga pista {0} ?"

        # logger
        M_LOG.info("config_texts:<<")

    # ---------------------------------------------------------------------------------------------

    def __get_current_data(self, f_qtw, fi_col=0):
        """
        retorna os dados associados a linha atual
        """
        # logger
        M_LOG.info("__get_current_data:>>")

        # verifica condições de execução
        assert f_qtw is not None

        # o dado da linha selecionada
        ls_data = ""

        # obtém o item da linha selecionada
        l_item = self.__get_current_item(f_qtw, fi_col)

        if l_item is not None:

            # obtém o dado associado a linha
            ls_data = l_item.data(QtCore.Qt.UserRole).toString()
            M_LOG.debug("__get_current_data:ls_data: " + str(ls_data))

        # logger
        M_LOG.info("__get_current_data:<<")

        # retorna o dado associado a linha selecionada
        return ls_data

    # ---------------------------------------------------------------------------------------------

    def __get_current_item(self, f_qtw, fi_col=0):
        """
        retorna o item associado a linha selecionada
        """
        # logger
        M_LOG.info("__get_current_item:>>")

        # o item selecionado
        l_item = None

        # verifica condições de execução
        assert f_qtw is not None

        # obtém o número da linha selecionada
        li_row = f_qtw.currentRow()
        M_LOG.debug("__get_current_item:li_row: " + str(li_row))

        # existe uma linha selecionada ?
        if li_row > -1:

            # obtém o item associado
            l_item = f_qtw.item(li_row, fi_col)
            assert l_item

        # logger
        M_LOG.info("__get_current_item:<<")

        # retorna o item selecionado na QTableWidget
        return l_item

    # ---------------------------------------------------------------------------------------------

    def __get_selected_obj(self, f_dct, f_qtw):
        """
        retorna o item associado a linha selecionada na QTableWidget
        """
        # logger
        M_LOG.info("__get_selected_obj:>>")

        # verifica condições de execução
        assert f_dct is not None
        assert f_qtw is not None

        # M_LOG.debug("__get_selected_obj:f_dct: " + str(f_dct))

        # obtém a key da linha selecionada
        ls_key = self.__get_current_data(f_qtw)
        # M_LOG.debug("__get_selected_obj:ls_key: " + str(ls_key))

        # logger
        M_LOG.info("__get_selected_obj:<<")

        # retorna o item da linha selecionada na QTableWidget
        return f_dct.get(str(ls_key), None)

    # ---------------------------------------------------------------------------------------------

    def __jump_start(self):
        """
        faz a carga inicial da tabela de aeródromos
        """
        # logger
        M_LOG.info("__jump_start:>>")

        # obtém o dicionário de aeródromos
        self.__dct_aer = self.__model.airspace.dct_aer

        # o dicionário de aeródromos não existe ?
        if self.__dct_aer is None:

            # logger
            l_log = logging.getLogger("CDlgAerDataNEW::__jump_start")
            l_log.setLevel(logging.CRITICAl)
            l_log.critical(u"<E01: Tabela de aeródromos não carregada !")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__control.event.post(l_evt)

            # cai fora
            sys.exit(1)

        # atualiza na tela os dados do aeródromo
        self.__update_aer_list()

        # logger
        M_LOG.info("__jump_start:<<")

    # ---------------------------------------------------------------------------------------------

    def okToContinue(self):
        """
        cria uma messageBox

        @return True se tratou a resposta, senão False
        """
        # logger
        M_LOG.info("okToContinue:>>")

        # resposta
        lv_ans = True
        '''
        M_LOG.debug("self.__v_changed: " + str(self.__v_changed))

        # flag de alterações setado ?
        if self.__v_changed:

            # questiona sobre alterações pendentes
            l_Resp = QtGui.QMessageBox.question(self, self._txtContinueTit,
                                                      self._txtContinueMsg,
                                                      QtGui.QMessageBox.Yes |
                                                      QtGui.QMessageBox.No |
                                                      QtGui.QMessageBox.Cancel)

            # cancela ?
            if QtGui.QMessageBox.Cancel == l_Resp:

                # não sai
                lv_ans = False

            # salva ?
            elif QtGui.QMessageBox.Yes == l_Resp:

                # salva as pendências e sai
                lv_ans = True

            # não salva ?
            else:
                # reseta o flag de alterações
                self.__v_changed = False
                M_LOG.debug("self.__v_changed: " + str(self.__v_changed))

                # ...e sai
                lv_ans = True
        '''
        # logger
        M_LOG.info("okToContinue:<<")
        
        # retorna a resposta
        return lv_ans

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_aer_del(self):
        """
        callback de btn_aer_del da dialog de edição
        remove um aeródromo da lista
        """
        # logger
        M_LOG.info("__on_btn_aer_del:>>")

        # verifica condições de execução
        assert self.qtw_aer is not None
        assert self.__dct_aer is not None

        # obtém o aeródromo selecionado
        self.__obj_aer = self.__get_selected_obj(self.__dct_aer, self.qtw_aer)

        if self.__obj_aer is not None:

            # apaga a aeródromo atual ?
            if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self,
                                                                   self.__txt_del_aer_Tit,
                                                                   self.__txt_del_aer_Msg.format(self.__obj_aer.s_aer_indc),
               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No):

                # apaga o aeródromo
                self.__aer_remove(self.__obj_aer)

        # logger
        M_LOG.info("__on_btn_aer_del:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_btn_aer_new(self):
        """
        callback de btnNew da dialog de edição
        cria um novo aeródromo na lista
        """
        # logger
        M_LOG.info("__on_btn_aer_new:>>")

        # cria a dialog de edição de aeródromos
        l_dlg = dlgedit.CDlgAerEditNEW(self.__control, None, self)
        assert l_dlg

        # processa a dialog de edição de aeródromos (modal)
        if l_dlg.exec_():

            # obtém os dados da edição
            self.__obj_aer = l_dlg.get_data()

            # aeródromo existente ?
            if (self.__obj_aer is not None) and (self.__dct_aer is not None):

                # insere a aeródromo na lista
                self.__dct_aer.append(self.__obj_aer)

                # salva o arquivo no disco
                # self.__obj_aer.save2Disk(l_sPath)

                # se ok, atualiza a QTableWidget de aeródromos
                self.__update_qtw_aer()

        # logger
        M_LOG.info("__on_btn_aer_new:<<")

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def __on_qtw_aer_selection_changed(self):
        """
        seleciona um aeródromo a editar
        """
        # logger
        M_LOG.info("__on_qtw_aer_selection_changed:>>")

        # verifica condições de execução
        assert self.__dct_aer is not None
        assert self.qtw_aer is not None

        # obtém o aeródromo selecionado
        self.__obj_aer = self.__get_selected_obj(self.__dct_aer, self.qtw_aer)

        # reseta a pista selecionada
        self.__obj_pst = None

        # atualiza a área de dados do aeródromo selecionado
        self.__update_aer_sel()

        # logger
        M_LOG.info("__on_qtw_aer_selection_changed:<<")

    # ---------------------------------------------------------------------------------------------

    def __on_qtw_pst_selection_changed(self):
        """
        seleciona uma pista a editar
        """
        # logger
        M_LOG.info("__on_qtw_pst_selection_changed:>>")

        # verifica condições de execução
        assert self.__obj_aer is not None
        assert self.__obj_aer.dct_aer_pistas is not None
        assert self.qtw_pst is not None

        # obtém a pista selecionada
        self.__obj_pst = self.__get_selected_obj(self.__obj_aer.dct_aer_pistas, self.qtw_pst)

        # logger
        M_LOG.info("__on_qtw_pst_selection_changed:<<")
    '''
    # ---------------------------------------------------------------------------------------------

    def pstDel(self):
        """
        callback de btn_pst_del da dialog de edição
        deleta uma pista da lista
        """
        # logger
        M_LOG.info("pstDel:>>")

        # verifica condições de execução
        assert self.qtw_pst is not None
        assert self.__obj_aer.dct_aer_pistas is not None

        # obtém a pista selecionada
        self.__obj_pst = self.__get_selected_obj(self.__obj_aer.dct_aer_pistas, self.qtw_pst)
        M_LOG.debug("self.__obj_pst: " + str(self.__obj_pst))

        if (self.__obj_pst is not None):

            # apaga a pista atual ?
            if (QtGui.QMessageBox.Yes == QtGui.QMessageBox.question (
                                              self, self.__txt_del_pst_Tit,
                                              self.__txt_del_pst_Msg.format(""),
                                              QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)):

                # apaga a pista
                self.__remove_pst(self.__obj_pst)

        # logger
        M_LOG.info("pstDel:<<")

    # ---------------------------------------------------------------------------------------------

    def pstEdit(self):
        """
        callback de btnEdit da dialog de edição
        edita uma pista da QTableWidget
        """
        # logger
        M_LOG.info("pstEdit:>>")

        # verifica condições de execução
        assert self.qtw_pst is not None
        assert self.__obj_aer.dct_aer_pistas is not None

        # obtém a pista selecionada
        self.__obj_pst = self.__get_selected_obj(self.__obj_aer.dct_aer_pistas, self.qtw_pst)
        M_LOG.debug("self.__obj_pst: " + str(self.__obj_pst))

        if (self.__obj_pst is not None):

            # cria a dialog de edição de pistas
            l_dlg = dlgPstCAD.dlgPstCAD(self.__control, self.__obj_pst, self)
            assert l_dlg

            # processa a dialog de edição de pistas (modal)
            if (l_dlg.exec_ ()):

                # salva em disco as alterações na pista
                #self.__obj_aer.dct_aer_pistas.save2Disk(self.__obj_aer.dct_aer_pistas._sPN)
                M_LOG.debug("Salvou pista em disco: " + self.__obj_aer.dct_aer_pistas._sPN)

                # se ok, atualiza a QTableWidget de pistas
                self.__update_qtw_pst(self.__obj_aer)

        # logger
        M_LOG.info("pstEdit:<<")

    # ---------------------------------------------------------------------------------------------

    def pstNew(self):
        """
        callback de btnNew da dialog de edição
        cria uma nova pista na lista
        """
        # logger
        M_LOG.info("pstNew:>>")

        # cria a dialog de edição de pistas
        l_dlg = dlgPstCAD.dlgPstCAD(self.__control, None, self)
        assert l_dlg

        # processa a dialog de edição de pistas (modal)
        if (l_dlg.exec_ ()):

            # obtém os dados da edição
            self.__obj_pst = l_dlg.getData ()

            # pista existente ?
            if (( self.__obj_pst is not None) and(self.__obj_aer.dct_aer_pistas is not None)):

                # insere a pista na lista
                self.__obj_aer.dct_aer_pistas.append(self.__obj_pst)

                # salva o arquivo no disco
                l_sPath = os.path.join(self.__dct_config["dir.aer"], self.__obj_pst._sInd + ".pst")
                M_LOG.debug("l_sPath: " + str(l_sPath))

                # salva o arquivo no disco
                self.__obj_pst.save2Disk(l_sPath)

                # se ok, atualiza a lista de pistas
                self.__update_qtw_pst(self.__obj_aer)

        # logger
        M_LOG.info("pstNew:<<")
    '''
    # ---------------------------------------------------------------------------------------------

    def reject(self):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("reject:>>")

        self.__obj_aer = None

        # faz o "reject"
        QtGui.QDialog.reject(self)

        self.close()

        # logger
        M_LOG.info("reject:<<")
    '''
    # ---------------------------------------------------------------------------------------------

    def __remove_pst(self, f_oPst):
        """
        remove a pista selecionada

        @param f_oPst: pointer para a pista a remover
        """
        # logger
        M_LOG.info("__remove_pst:>>")

        # verifica condições de execução
        assert f_oPst is not None

        M_LOG.debug("f_oPst: " + str(f_oPst))

        # remove a linha da widget
        self.qtw_pst.removeRow(self.qtw_pst.currentRow ())

        # remove a pista da lista
        self.__obj_aer.dct_aer_pistas.remove(f_oPst)

        # logger
        M_LOG.info("__remove_pst:<<")
    '''
    # ---------------------------------------------------------------------------------------------

    def restore_settings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # logger
        M_LOG.info("restore_settings:>>")

        # obtém os settings
        l_set = QtCore.QSettings("ICEA", "dbEdit")
        assert l_set

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self.__txt_settings)).toByteArray())

        # logger
        M_LOG.info("restore_settings:<<")

        # return
        return True

    # ---------------------------------------------------------------------------------------------

    def __update_aer_list(self):
        """
        atualiza na tela os dados do aeródromo
        """
        # logger
        M_LOG.info("__update_aer_list:>>")

        # verifica condições de execução
        assert self.qtw_aer is not None
        assert self.__dct_aer is not None

        # atualiza a QTableWidget de aeródromos
        self.__update_qtw_aer()

        # obtém o aeródromo selecionado
        self.__obj_aer = self.__get_selected_obj(self.__dct_aer, self.qtw_aer)

        # atualiza a QTableWidget de pistas
        self.__update_pst_list(self.__obj_aer)

        # logger
        M_LOG.info("__update_aer_list:<<")

    # ---------------------------------------------------------------------------------------------

    def __update_aer_sel(self):
        """
        atualiza na tela os dados do aeródromo selecionado
        """
        # logger
        M_LOG.info("__update_aer_sel:>>")

        # aeródromo selecionado existe ?
        if self.__obj_aer is not None:

            # indicativo do aeródromo
            ls_aer_indc = self.__obj_aer.s_aer_indc

            # identificação
            self.txt_aer_indc.setText(self.__obj_aer.s_aer_indc)
            self.qle_aer_desc.setText(self.__obj_aer.s_aer_desc)

            # geografia

            # declinação magnética
            self.dsb_decl.setValue(self.__obj_aer.f_aer_decl_mag)

            # ARP
            self.qle_lat.setText(cconv.format_ica_lat(self.__obj_aer.f_aer_lat))
            self.qle_lng.setText(cconv.format_ica_lng(self.__obj_aer.f_aer_lng))

            # elevação
            self.sbx_elev.setValue(self.__obj_aer.f_aer_elev)

            # lista de pistas do aeródromo
            self.__update_pst_list(self.__obj_aer)

        # senão, o aeródromo não existe
        else:
            # posiciona cursor no início do formulário
            self.txt_aer_indc.setFocus()

        # logger
        M_LOG.info("__update_aer_sel:<<")

    # ---------------------------------------------------------------------------------------------

    def __update_pst_list(self, f_aer):
        """
        atualiza na tela os dados da lista de pistas
        """
        # logger
        M_LOG.info("__update_pst_list:>>")

        # verifica condições de execução
        assert f_aer is not None
        assert f_aer.dct_aer_pistas is not None
        assert self.qtw_pst is not None

        # atualiza a QTableWidget de pistas
        self.__update_qtw_pst(f_aer)

        # obtém a pista selecionada
        self.__obj_pst = self.__get_selected_obj(f_aer.dct_aer_pistas, self.qtw_pst)

        # logger
        M_LOG.info("__update_pst_list:<<")

    # ---------------------------------------------------------------------------------------------

    def __update_qtw_aer(self):
        """
        atualiza na tela os dados da QTableWidget de aeródromos
        """
        # logger
        M_LOG.info("__update_qtw_aer:>>")

        # verifica condições de execução
        assert self.qtw_aer is not None
        assert self.__dct_aer is not None

        # limpa a QTableWidget
        self.qtw_aer.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtw_aer.setRowCount(len(self.__dct_aer))

        # seta número de colunas e cabeçalho das colunas
        self.qtw_aer.setColumnCount(2)
        self.qtw_aer.setHorizontalHeaderLabels(["Indicativo", u"Descrição"])

        # seta QTableWidget
        self.qtw_aer.setAlternatingRowColors(True)
        self.qtw_aer.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtw_aer.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtw_aer.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtw_aer.setSortingEnabled(False)

        # linha selecionada (objeto aeródromo)
        l_item_sel = None

        # para cada aeródromo no dicionário
        for li_ndx, (ls_aer_indc, l_aer) in enumerate(sorted(self.__dct_aer.iteritems(), key=lambda (k, v): (v, k))):

            # indicativo do aeródromo
            ltwi_aer_indc = QtGui.QTableWidgetItem(ls_aer_indc)
            assert ltwi_aer_indc

            ltwi_aer_indc.setData(QtCore.Qt.UserRole, QtCore.QVariant(ls_aer_indc))

            self.qtw_aer.setItem(li_ndx, 0, ltwi_aer_indc)

            # é o aeródromo selecionado ?
            if (self.__obj_aer is not None) and (self.__obj_aer.s_aer_indc == ls_aer_indc):

                # salva pointer para o item selecionado
                l_item_sel = ltwi_aer_indc

            # descrição
            ltwi_aer_desc = QtGui.QTableWidgetItem(l_aer.s_aer_desc)

            self.qtw_aer.setItem(li_ndx, 1, ltwi_aer_desc)

        # existe um aeródromo selecionado ?
        if self.__obj_aer is not None:

            # seleciona o item
            self.qtw_aer.setCurrentItem(l_item_sel)

            # posiciona no item selecionado
            self.qtw_aer.scrollToItem(l_item_sel)

            # marca que existe seleção
            l_item_sel.setSelected(True)

        # senão, não existe um aeródromo selecionado
        else:
            # seleciona a primeira linha
            self.qtw_aer.selectRow(0)

            # obtém o aeródromo atual
            # self.__obj_aer = self.__get_selected_obj(self.__dct_aer, self.qtw_aer)
            # assert self.__obj_aer

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtw_aer.resizeColumnsToContents()

        # habilita a ordenação
        self.qtw_aer.setSortingEnabled(True)

        # logger
        M_LOG.info("__update_qtw_aer:<<")

    # ---------------------------------------------------------------------------------------------

    def __update_qtw_pst(self, f_aer):
        """
        atualiza na tela os dados da QTableWidget de pistas

        @param f_aer: aeródromo
        """
        # logger
        M_LOG.info("__update_qtw_pst:>>")

        # check input parameters
        assert f_aer

        # check dependencies
        assert f_aer.dct_aer_pistas is not None
        assert self.qtw_pst is not None

        # limpa a QTableWidget
        self.qtw_pst.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtw_pst.setRowCount(len(f_aer.dct_aer_pistas))

        # seta número de colunas
        self.qtw_pst.setColumnCount(4)

        # seta cabeçalho das colunas
        self.qtw_pst.setHorizontalHeaderLabels(["Indicativo", "Rumo", "Latitude", "Longitude"])

        # seta QTableWidget
        self.qtw_pst.setAlternatingRowColors(True)
        self.qtw_pst.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtw_pst.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtw_pst.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtw_pst.setSortingEnabled(False)

        # linha selecionada (QTableWidgetItem)
        l_item_sel = None

        # para cada pista no dicionário...
        for li_ndx, (ls_pst_indc, l_pst) in enumerate(sorted(f_aer.dct_aer_pistas.iteritems(), key=lambda (k, v): (v, k))):

            # indicativo da pista
            ltwi_pst_indc = QtGui.QTableWidgetItem(ls_pst_indc)
            assert ltwi_pst_indc

            ltwi_pst_indc.setData(QtCore.Qt.UserRole, QtCore.QVariant(ls_pst_indc))
                                    
            self.qtw_pst.setItem(li_ndx, 0, ltwi_pst_indc)

            # a pista atual é a selecionada ?
            if (self.__obj_pst is not None) and \
               (self.__obj_pst.ptr_pst_aer == l_pst.ptr_pst_aer) and \
               (self.__obj_pst.s_pst_indc == ls_pst_indc):

                # marca como selecionado
                l_item_sel = ltwi_pst_indc

            # rumo
            ltwi_pst_rumo = QtGui.QTableWidgetItem(str(l_pst.i_pst_rumo))
            assert ltwi_pst_rumo

            self.qtw_pst.setItem(li_ndx, 1, ltwi_pst_rumo)

            # latitude
            ltwi_pst_lat = QtGui.QTableWidgetItem(cconv.format_ica_lat(l_pst.f_pst_lat))
            assert ltwi_pst_lat

            self.qtw_pst.setItem(li_ndx, 2, ltwi_pst_lat)

            # longitude
            ltwi_pst_lng = QtGui.QTableWidgetItem(cconv.format_ica_lng(l_pst.f_pst_lng))
            assert ltwi_pst_lng

            self.qtw_pst.setItem(li_ndx, 3, ltwi_pst_lng)

        # existe uma pista selecionada ?
        if (self.__obj_pst is not None) and (l_item_sel is not None):

            # seleciona o item
            self.qtw_pst.setCurrentItem(l_item_sel)

            # posiciona no item selecionado
            self.qtw_pst.scrollToItem(l_item_sel)

            # marca que existe seleção
            l_item_sel.setSelected(True)

        # senão, não existe uma pista selecionada
        else:
            # seleciona a primeira linha
            self.qtw_pst.selectRow(0)

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtw_pst.resizeColumnsToContents ()

        # habilita a ordenação
        self.qtw_pst.setSortingEnabled(True)

        # logger
        M_LOG.info("__update_qtw_pst:<<")

# < the end >--------------------------------------------------------------------------------------
