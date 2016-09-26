#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
wnd_main_visil

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

# Python library
import logging
import random
import sys
import time

# PyQt library
from PyQt4 import QtCore, QtGui

# model
from ...model.visil import defs_visil as ldefs
# import model.visil.airspace as airs
# import model.visil.landscape as lands
# import model.visil.weather as wtr
# import model.visil.strip_model as mstp
from ...model.visil import strip_table_model as stm

# view
from . import radar_scope as rdrscp
from . import statusbar_visil as stbar
from . import strip_visil as strp
#import view.visil.wid_runway_config as wrc
#import view.visil.wid_weather_config as wwc
from . import wnd_main_visil_ui as wndmain_ui

# control
from ...control.events import events_basic as events

# resources
import icons_rc
import resources_visil_rc

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CWndMainVisil >--------------------------------------------------------------------------

class CWndMainVisil(QtGui.QMainWindow, wndmain_ui.Ui_wndMainVisil):
    """
    DOCUMENT ME!
    """
    # signals
    # C_SIG_STRIP_CHG = QtCore.pyqtSignal(anv.CAircraftPiloto)
    # C_SIG_STRIP_DEL = QtCore.pyqtSignal(anv.CAircraftPiloto)
    # C_SIG_STRIP_INS = QtCore.pyqtSignal(anv.CAircraftPiloto)
    # C_SIG_STRIP_SEL = QtCore.pyqtSignal(anv.CAircraftPiloto)
                    
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control):
        """
        constructor.
        initializes the viewer.

        @param f_control: control manager.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_control

        # inicia a super classe
        super(CWndMainVisil, self).__init__()

        # salva o control manager localmente
        self.__control = f_control
        assert self.__control

        # salva o model manager localmente
        self.__model = f_control.model
        assert self.__model

        # obtém o event manager
        self.__event = f_control.event
        assert self.__event

        # registra a sí próprio como recebedor de eventos
        # self.__event.register_listener(self)
        '''
        # obtém o config manager
        self.__config = f_control.config
        assert self.__config

        # obtém o dicionário de configuração
        self.__dct_config = self.__config.dct_config
        assert self.__dct_config
        '''
        # create landscape
        #self.__landscape = self.__model.landscape
        #assert self.__landscape

        # get airspace
        #self.__airspace = self.__model.airspace
        #assert self.__airspace

        # weather and runway config widgets
        # self._widPageWeatherConfig = None
        # self._widPageRunwayConfig = None

        # salva o dicionário de aeronaves
        self.__dct_flight = f_control.model.emula_model.dct_flight  
        assert self.__dct_flight is not None
                        
        # current strip
        self.__strip_cur = None
                
        # create main Ui
        self.setupUi(self)

        # the radar screen is the main widget
        self.__radar_scope = rdrscp.CRadarScope(f_control, self)
        assert self.__radar_scope

        # the radar screen goes to central widget
        self.setCentralWidget(self.__radar_scope)

        # window title
        self.setWindowTitle(self.tr(u"ViSIL 0.1 [Visualização]", None,))

        # create windows elements
        self.status_bar = stbar.CStatusBarVisil(self)
        assert self.status_bar

        # config statusBar
        self.setStatusBar(self.status_bar)

        # create windows elements
        self.__config_strips()

        # create windows elements
        self.__create_actions()
        self.__create_toolbars()
        self.__config_toolboxes()

        # make SIGNAL-SLOT connections
        self.__make_connections()

        # get initial values from weather()
        # self.__weather.initSignals()

        # read saved settings
        self.__read_settings()

        # XXX
        self.xxx()

        # clock timer (1s cycle)
        self.__i_timer_clock = self.startTimer(1000)

        # fetch aircrafts data timer (1s cycle)
        self.__i_timer_fetch = self.startTimer(1000)
                
        # config tableview
        self.qtv_stp.setFocus()
        self.qtv_stp.setCurrentIndex(self.__stp_model.index(0, 0))

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def about(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("about:>>")

        # show about box
        QtGui.QMessageBox.about(self, self.tr("About ViSIL"),
                                      self.tr("Lorem ipsum dolor sit amet, no vim quas animal intellegam.\n"
                                              "Click pro ad impetus tractatos deterruisset. Atqui tritani ut.\n"
                                              "Per postea conclusionemque ad, discere scripserit referrentur.\n"
                                              "Eos esse commune atomorum et, ex mei appareat platonem.\n"
                                              "Use the middle mouse button to center your radar screen.\n"
                                              "pre-alpha release! Please report bugs to bugtrack@icea.gov.br"))

        # logger
        # M_LOG.info("about:<<")

    # ---------------------------------------------------------------------------------------------

    # @QtCore.pyqtSlot()
    def closeEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("closeEvent:>>")

        # really quit ?
        if self.__really_quit():

            # salva a configuração atual
            self.__write_settings()

            # accept
            f_evt.accept()

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

        # senão, continua...
        else:
            # ignore
            f_evt.ignore()

        # logger
        # M_LOG.info("closeEvent:<<")

    # ---------------------------------------------------------------------------------------------

    def __config_strips(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__config_strips:>>")

        ###
        # strips

        # strips table model
        self.__stp_model = stm.CStripTableModel()
        assert self.__stp_model

        # make connections
        # self.__stp_model.dataChanged.connect(self.__on_strip_data_changed)

        # config strip tableview
        self.qtv_stp.setModel(self.__stp_model)
        self.qtv_stp.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.qtv_stp.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.qtv_stp.setColumnHidden(ldefs.D_STP_0, True)
        self.qtv_stp.setColumnHidden(ldefs.D_STP_ID, True)
        self.qtv_stp.resizeColumnsToContents()

        # make connections
        self.qtv_stp.selectionModel().currentRowChanged.connect(self.__on_strip_row_changed)

        # initial change
        self.__on_strip_row_changed(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())

        # config ins/del buttons
        # self.btn_stp_ins.clicked.connect(self.__on_strip_add)
        # self.btn_stp_del.clicked.connect(self.__on_strip_remove)

        # logger
        # M_LOG.info("__config_strips:<<")

    # ---------------------------------------------------------------------------------------------

    def __config_toolboxes(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__config_toolboxes:>>")

        ###
        # toolbox

        # config toolbox
        self.tool_box.setEnabled(True)

        ###
        # runways toolbox

        # create page runways widget
        #self._widPageRunwayConfig = wrc.widRunwayConfig(self)
        #assert self._widPageRunwayConfig

        # runways have to be dynamically added
        #for l_oRWY in self.__airspace.lstRWY:
            #self._widPageRunwayConfig.addRunway(l_oRWY.sName)

        # config page runways widget
        #self._widPageRunwayConfig.setGeometry(QtCore.QRect(0, 0, 212, 79))

        # put page runways in toolbox
        #self.tool_box.addItem(self._widPageRunwayConfig, self.tr("Runways"))

        ###
        # weather toolbox

        # create page weather widget
        #self._widPageWeatherConfig = wwc.widWeatherConfig(self)
        #assert self._widPageWeatherConfig

        # config page runways widget
        #self._widPageWeatherConfig.setGeometry(QtCore.QRect(0, 0, 212, 79))

        # put page weather in toolbox
        #self.tool_box.addItem(self._widPageWeatherConfig, self.tr("Weather"))

        ###
        # landscape toolbox

        # create landscape tree view
        #self._qtwPageLand = QtGui.QTreeWidget()
        #assert self._qtwPageLand

        # config landscape tree widget
        #self._qtwPageLand.setGeometry(QtCore.QRect(0, 0, 212, 158))
        #self._qtwPageLand.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        #### self._qtwPageLand.setModel ( model )
        #self._qtwPageLand.setUniformRowHeights(True)
        #self._qtwPageLand.headerItem().setText(0, self.tr("Graphical Items"))
        #self._qtwPageLand.itemChanged.connect(self.__update_checks)

        # carrega dos dados na QTreeView
        #self.__load_tree_view(self._qtwPageLand, self.__landscape.treeMaps.toDict())

        # put page in toolbox
        #self.tool_box.addItem(self._qtwPageLand, self.tr("Landscape"))

        ###
        # airspace toolbox

        # create airspace tree view
        #self._qtwPageAirs = QtGui.QTreeWidget()
        #assert self._qtwPageAirs

        # config airspace tree widget
        #self._qtwPageAirs.setGeometry(QtCore.QRect(0, 0, 212, 158))
        #self._qtwPageAirs.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        ##### self._qtwPageAirs.setModel ( model )
        #self._qtwPageAirs.setUniformRowHeights(True)
        #self._qtwPageAirs.headerItem().setText(0, self.tr("Graphical Items"))
        #self._qtwPageAirs.itemChanged.connect(self.__update_checks)

        # carrega dos dados na QTreeView
        #self.__load_tree_view(self._qtwPageAirs, self.__landscape.treeMaps.toDict())

        # put page in toolbox
        #self.tool_box.addItem(self._qtwPageAirs, self.tr("Airspace"))

        # select toolbox item
        self.tool_box.setCurrentIndex(0)

        # logger
        # M_LOG.info("__config_toolboxes:<<")

    # ---------------------------------------------------------------------------------------------

    def __create_actions(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__create_actions:>>")

        # action new
        self.__act_new = QtGui.QAction(QtGui.QIcon(":/pixmaps/gamenew.xpm"), self.tr("&New"), self)
        assert self.__act_new is not None

        # config action new
        self.__act_new.setShortcut(self.tr("Ctrl+N"))
        self.__act_new.setStatusTip(self.tr("Start a new console"))
        # FIXME
        self.__act_new.setEnabled(False)

        # connect action new
        self.__act_new.triggered.connect(self.newCons)

        # action pause
        self.__act_pause = QtGui.QAction(QtGui.QIcon(":/pixmaps/gamepause.xpm"), self.tr("&Pause"), self)
        assert self.__act_pause is not None

        # config action pause
        self.__act_pause.setCheckable(True)
        self.__act_pause.setChecked(False)
        self.__act_pause.setShortcut(self.tr("Ctrl+P"))
        self.__act_pause.setStatusTip(self.tr("Pause the console"))

        # action quit
        self.__act_quit = QtGui.QAction(QtGui.QIcon(":/pixmaps/gamequit.xpm"), self.tr("&Quit"), self)
        assert self.__act_quit is not None

        # config action quit
        self.__act_quit.setShortcut(self.tr("Ctrl+Q"))
        self.__act_quit.setStatusTip(self.tr("Leave the console"))

        # connect action quit
        self.__act_quit.triggered.connect(QtGui.qApp.closeAllWindows)

        # action zoomIn
        self.__act_zoom_in = QtGui.QAction(QtGui.QIcon(":/pixmaps/zoomin.xpm"), self.tr("Zoom &In"), self)
        assert self.__act_zoom_in is not None

        # config action zoomIn
        self.__act_zoom_in.setShortcut(self.tr("Ctrl++"))
        self.__act_zoom_in.setStatusTip(self.tr("Set coverage of radar screen"))

        self.__act_zoom_in.triggered.connect(self.__radar_scope.zoom_in)
        self.__act_zoom_in.triggered.connect(self.__radar_scope.showRange)

        # action zoomOut
        self.__act_zoom_out = QtGui.QAction(QtGui.QIcon(":/pixmaps/zoomout.xpm"), self.tr("Zoom &Out"), self)
        assert self.__act_zoom_out is not None

        # config action zoomOut
        self.__act_zoom_out.setShortcut(self.tr("Ctrl+-"))
        self.__act_zoom_out.setStatusTip(self.tr("Set coverage of radar screen"))

        self.__act_zoom_out.triggered.connect(self.__radar_scope.zoom_out)
        self.__act_zoom_out.triggered.connect(self.__radar_scope.showRange)

        # action invert
        self.__act_invert = QtGui.QAction(QtGui.QIcon(":/pixmaps/invert.xpm"), self.tr("&Invert Screen"), self)
        assert self.__act_invert is not None

        # config action invert
        self.__act_invert.setCheckable(True)
        self.__act_invert.setChecked(False)
        self.__act_invert.setShortcut(self.tr("Ctrl+I"))
        self.__act_invert.setStatusTip(self.tr("Invert radar screen"))

        # action about
        self.__act_about = QtGui.QAction(self.tr("&About"), self)
        assert self.__act_about is not None

        # config action about
        self.__act_about.setStatusTip(self.tr("About ViSIL"))

        # connect action about
        self.__act_about.triggered.connect(self.about)

        # action aboutQt
        self.__act_about_qt = QtGui.QAction(self.tr("About &Qt"), self)
        assert self.__act_about_qt is not None

        # config action aboutQt
        self.__act_about_qt.setStatusTip(self.tr("About Qt"))

        # connect action aboutQt
        self.__act_about_qt.triggered.connect(QtGui.qApp.aboutQt)

        # logger
        # M_LOG.info("__create_actions:<<")

    # ---------------------------------------------------------------------------------------------

    def __create_toolbars(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__create_toolbars:>>")

        # create toolBar file
        ltbr_file = self.addToolBar(self.tr("File"))
        assert ltbr_file is not None

        ltbr_file.addAction(self.__act_quit)
        ltbr_file.addAction(self.__act_new)
        ltbr_file.addAction(self.__act_pause)

        # create toolBar view
        ltbr_view = self.addToolBar(self.tr("View"))
        assert ltbr_view is not None

        ltbr_view.addAction(self.__act_zoom_out)
        ltbr_view.addAction(self.__act_zoom_in)
        ltbr_view.addAction(self.__act_invert)

        # create toolBar help
        ltbr_help = self.addToolBar(self.tr("Help"))
        assert ltbr_help is not None

        ltbr_help.addAction(self.__act_about)
        ltbr_help.addAction(self.__act_about_qt)

        # logger
        # M_LOG.info("__create_toolbars:<<")

    # ---------------------------------------------------------------------------------------------

    def __get_current_strip(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__get_current_strip:>>")

        # get current index
        l_index = self.qtv_stp.currentIndex()
                
        if not l_index.isValid():
            # return
            return None

        # get current row
        l_row = l_index.row()

        # get strip
        self.__strip_cur = self.__stp_model.lst_strips[l_row]
        assert self.__strip_cur

        # get strip info
        # l_info = self.__stp_model.data(self.__stp_model.index(l_row, ldefs.D_FIX_INFO)).toString()

        # M_LOG.debug("__on_strip_remove:l_strip.info: " + str(l_strip.s_info))
        # M_LOG.debug("__on_strip_remove:l_strip.info: " + str(l_info))

        # logger
        # M_LOG.info("__get_current_strip:<<")

        # return current strip
        return self.__strip_cur
        
    # ---------------------------------------------------------------------------------------------

    def __load_tree_view(self, f_parent, f_dat):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__load_tree_view:>>")

        # recebeu um dicionário ?
        if isinstance(f_dat, dict):

            # para todos os ítens no dicionário...
            for l_key, l_val in f_dat.iteritems():

                # cria uma linha de mapa
                l_item = QtGui.QTreeWidgetItem(f_parent)
                assert l_item

                # configura o item
                l_item.setText(0, l_key)
                l_item.setCheckState(0, QtCore.Qt.Checked)
                l_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

                # seleciona o ícone pelo tipo de mapa
                if l_key.startswith("MAP"):
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/Camera.png")))

                elif l_key.startswith("NDB"):
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/Transform.png")))

                elif l_key.startswith("Navaids"):
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/Light.png")))

                else:
                    l_item.setIcon(0, QtGui.QIcon(QtGui.QPixmap(":/Transform.png")))

                # expande a árvore
                l_item.setExpanded(True)

                # propaga os itens
                self.__load_tree_view(l_item, l_val)

        # senão, é uma lista
        else:
            '''
            # para todos os ítens na lista...
            for l_txt in f_dat:

                # cria uma linha de mapa
                l_item = QtGui.QTreeWidgetItem ( f_parent )
                assert l_item

                # configura o item
                l_item.setText ( 0, l_txt )
                l_item.setCheckState ( 0, QtCore.Qt.Unchecked )
                l_item.setFlags ( QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled )
            '''
            # salva o nome do mapa na widget
            f_parent.setData(0, QtCore.Qt.WhatsThisRole, QtCore.QVariant(f_dat))

        # logger
        # M_LOG.info("__load_tree_view:<<")

    # ---------------------------------------------------------------------------------------------

    def __make_connections(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__make_connections:>>")

        # verifica condições de execução
        #assert self.__weather is not None
        #assert self._widPageWeatherConfig is not None
        assert self.__radar_scope is not None

        assert self.__act_pause is not None
        assert self.__act_zoom_in is not None
        assert self.__act_zoom_out is not None
        assert self.__act_invert is not None

        # self.__weather.qnhChanged.connect(self._widPageWeatherConfig.setQNH)
        # self.__weather.surfaceWindChanged.connect(self._widPageWeatherConfig.setSurfaceWind)
        # self.__weather.aloftWindChanged.connect(self._widPageWeatherConfig.setAloftWind)
        # self.__weather.qnhChanged.connect(self.showQNH)
        # self.__weather.qnhChanged.connect(self.showTL)
        # self.__weather.surfaceWindChanged.connect(self.showWind)

        self.__act_pause.toggled.connect(self.__radar_scope.pause)
        self.__act_invert.toggled.connect(self.__radar_scope.invert)

        # logger
        # M_LOG.info("__make_connections:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def newCons(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("newCons:>>")
        pass

    # -->FIXME
    #    del self.__radar_scope
    #    del self.__weather

    #    self.__weather = clsWeather.clsWeather ( self.__airspace )
    #    assert self.__weather is not None

    #    self.__radar_scope = widRadarScope.widRadarScope ( self )
    #    assert self.__radar_scope is not None

    #    self.setCentralWidget ( self.__radar_scope )

    #    self.__make_connections ()

    #    self.__weather.initSignals ()

        # logger
        # M_LOG.info("newCons:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot(QtCore.QModelIndex,QtCore.QModelIndex)
    def __on_strip_row_changed(self, f_index_new, f_index_old):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("__on_strip_row_changed:>>")

        # is index valid ?
        if f_index_old.isValid():

            # get old strip
            l_strip_old = self.__stp_model.lst_strips[f_index_old.row()]
            assert l_strip_old

            M_LOG.debug("old strip callsign: " + str(l_strip_old.s_callsign))

        # is index valid ?
        if f_index_new.isValid():

            # get new strip
            self.__strip_cur = self.__stp_model.lst_strips[f_index_new.row()]
            assert self.__strip_cur

            # habilita botoeira
            self.gbx_comandos.setEnabled(True)

            # inicia o comando
            self.lbl_comando.setText("{}: ".format(self.__strip_cur.s_callsign))

            # desabilita o envio
            self.btn_send.setEnabled(False)

            # emit signal
            # self.C_SIG_STRIP_SEL.emit(self.__strip_cur)

        M_LOG.debug("strip: " + str(self.__strip_cur))

        # logger
        M_LOG.info("__on_strip_row_changed:<<")

    # ---------------------------------------------------------------------------------------------

    def __read_settings(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__read_settings:>>")

        l_settings = QtCore.QSettings("ICEA", "visil")

        l_pos = l_settings.value("pos", QtCore.QPoint(200, 200)).toPoint()
        l_size = l_settings.value("size", QtCore.QSize(400, 400)).toSize()

        self.resize(l_size)
        self.move(l_pos)

        # logger
        # M_LOG.info("__read_settings:<<")

    # ---------------------------------------------------------------------------------------------

    def __really_quit(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__really_quit:>>")

        l_ret = QtGui.QMessageBox.warning(self,
                    self.tr("ViSIL"),
                    self.tr("Do you want to quit ViSIL ?"),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default, QtGui.QMessageBox.No)

        if l_ret == QtGui.QMessageBox.Yes:

            # logger
            # M_LOG.info("__really_quit:<E01")

            # retorna SIM
            return True

        # logger
        # M_LOG.info("__really_quit:<<")

        # retorna NÃO
        return False

    # ---------------------------------------------------------------------------------------------

    def __recursive_checks(self, f_oParent):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__recursive_checks:>>")

        # obtém o checkState
        l_checkState = f_oParent.checkState(0)

        # o nó é uma folha ? (i.e. sem filhos)
        if 0 == f_oParent.childCount():

            # o nó tem dados associados ?
            if f_oParent.data(0, QtCore.Qt.WhatsThisRole).toPyObject() is not None:

                # obtém o nome do mapa
                l_sName = f_oParent.data(0, QtCore.Qt.WhatsThisRole).toPyObject()[0]

                # nome válido ?
                if l_sName is not None:

                    # obtém o mapa
                    l_map = self.__radar_scope.findMap(l_sName)

                    # achou o mapa ?
                    if l_map is not None:

                        # muda o status de exibição
                        l_map.showMap(QtCore.Qt.Checked == l_checkState)

        # para todos os filhos...
        for l_i in xrange(f_oParent.childCount()):

            # muda o checkState
            f_oParent.child(l_i).setCheckState(0, l_checkState)
            f_oParent.child(l_i).setDisabled(QtCore.Qt.Unchecked == l_checkState)

            # o nó tem dados associados ?
            if f_oParent.data(0, QtCore.Qt.WhatsThisRole).toPyObject() is not None:

                # obtém o nome do mapa
                l_sName = f_oParent.child(l_i).data(0, QtCore.Qt.WhatsThisRole).toPyObject()[0]
                M_LOG.debug("l_sName: " + l_sName)

                # nome válido ?
                if l_sName is not None:

                    # obtém o mapa
                    l_map = self.__radar_scope.findMap(l_sName)

                    # achou o mapa ?
                    if l_map is not None:

                        # muda o status de exibição
                        l_map.showMap(QtCore.Qt.Checked == l_checkState)

            # propaga aos filhos
            self.__recursive_checks(f_oParent.child(l_i))

        # logger
        # M_LOG.info("__recursive_checks:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot(int)
    def showCoords(self, f_coords):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("showCoords:>>")

        self.status_bar.lblCoords.setText(u"99ᵒ 99' 99\" N 999ᵒ 99' 99\" E" % int(f_coords))

        # logger
        # M_LOG.info("showCoords:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot(int)
    def showQNH(self, f_qnh):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("showQNH:>>")

        self.status_bar.lblQNH.setText("Q%d" % int(f_qnh))

        # logger
        # M_LOG.info("showQNH:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot(int)
    def showTL(self, f_qnh):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("showTL:>>")

        # TODO: airport specific
        if f_qnh >= 1013.:
            l_tl = 60.

        else:
            l_tl = 70.

        self.status_bar.lblTL.setText("TL%d" % int(l_tl))

        # logger
        # M_LOG.info("showTL:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot(int, int)
    def showWind(self, f_dir, f_v):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("showWind:>>")

        if f_v == 0.:
            l_windstring = "CALM"

        else:
            l_windstring = "%d%c/%dkt" % (int(f_dir), u'°'.encode("utf-8")[1:], int(f_v))

        self.status_bar.lblWind.setText(l_windstring)

        # logger
        # M_LOG.info("showWind:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot(QtCore.QTimerEvent)
    def timerEvent(self, f_evt):

        # logger
        # M_LOG.info("timerEvent:>>")

        # timer de clock acionado ?
        if f_evt.timerId() == self.__i_timer_clock:

            # display simulation time
            self.lbl_hora.setText(self.__control.sim_time.get_hora_format())

        # timer de fetch de dados de aeronave acionado ?
        elif f_evt.timerId() == self.__i_timer_fetch:

            # for all flights...
            for l_callsign, l_flight in self.__dct_flight.iteritems():

                M_LOG.debug("timerEvent:l_callsign: " + str(l_callsign))

                # new flight ?
                if l_flight not in self.__stp_model.lst_strips:

                    # insert flight on model
                    self.__stp_model.lst_strips.append(l_flight)

                    # reset flag de modificações
                    self.__stp_model.v_dirty = False

                    # emit signal
                    # self.C_SIG_STRIP_INS.emit(l_flight)

                # senão, update data...
                # else:
                    # select strip
                    # self.__on_strip_data_changed(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())
                
                    # reset flag de modificações
                    # self.__stp_model.v_dirty = True

                    # emit signal
                    # self.C_SIG_STRIP_CHG.emit(l_flight)

            # update view
            # self.__stp_model.dataChanged.emit(self.qtv_stp.currentIndex(), self.qtv_stp.currentIndex())
            self.__stp_model.layoutChanged.emit()

            # ajusta as colunas da view
            self.qtv_stp.resizeColumnsToContents()

        # logger
        # M_LOG.info("timerEvent:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot("QTreeWidgetItem", int)
    def __update_checks(self, f_item, f_iColumn):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__update_checks:>>")

        # checkState is stored on column 0
        if 0 != f_iColumn:

            # logger
            # M_LOG.info("__update_checks:<E01: checkState is stored on column 0.")

            # retorna
            return

        # propaga
        self.__recursive_checks(f_item)

        # logger
        # M_LOG.info("__update_checks:<<")

    # ---------------------------------------------------------------------------------------------

    def __write_settings(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__write_settings:>>")

        l_settings = QtCore.QSettings("ICEA", "visil")

        l_settings.setValue("pos", self.pos())
        l_settings.setValue("size", self.size())

        # logger
        # M_LOG.info("__write_settings:<<")

    # ---------------------------------------------------------------------------------------------

    def xxx(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("xxx:>>")

        # build the list widgets
        for i in xrange(10):

            listItem = QtGui.QListWidgetItem(self.qlw_strips)
            listItem.setSizeHint(QtCore.QSize(300, 63))  # Or else the widget items will overlap (irritating bug)
            self.qlw_strips.setItemWidget(listItem, strp.CWidStrip(self.__control, i, self))

        # logger
        # M_LOG.info("xxx:<<")

# < the end >--------------------------------------------------------------------------------------
