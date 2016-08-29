#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
radar_scope.

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
import math
import random
import sys

# PyQt library
from PyQt4 import QtCore, QtGui

# model
import model.tMath as tMath
import model.newton.defs_newton as ldefs

import model.coords.pos_lat_lng as pll
import model.coords.pos_xy as pxy
#import model.visil.clsAircraft as clsAircraft

# view
import view.visil.viewport as vwp
import view.visil.paint_engine as peng
#import view.visil.map.displayElement as displayElement
#import view.visil.map.viewMap as viewMap

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CRadarScope >----------------------------------------------------------------------------

class CRadarScope(QtGui.QWidget):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    C_LMODE_APP = 0
    C_LMODE_DCT = 1
    C_LMODE_HDG = 2
    C_LMODE_RTE = 3

    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_control, f_parent=None):

        # logger
        M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_control
        assert f_parent

        # inicia a super classe
        super(CRadarScope, self).__init__(f_parent)

        # salva o control manager localmente
        # self.__control = f_control

        # salva a QMainWindow localmente
        self.__parent = f_parent

        # salva o model manager localmente
        l_model = f_control.model
        assert l_model

        # obtém o event manager
        #self.__event = f_control.event
        #assert self.__event

        # registra a sí próprio como recebedor de eventos
        # self.__event.registerListener(self)

        # obtém o flight model
        #self.__emula_model = l_model.emula_model
        #assert self.__emula_model

        self.__f_radar_vector = 0.
        self.__i_lateral_mode = self.C_LMODE_APP

        self.__s_direct = ""
        self.__s_route = ""
        self.__s_approach = ""

        # lista de aeronaves
        self.__dct_flight = l_model.emula_model.dct_flight
        assert self.__dct_flight is not None
                        
        # save airspace locally
        self.__airspace = l_model.airspace
        assert self.__airspace

        # save landscape locally
        #l_landscape = l_model.landscape
        #assert l_landscape

        # lista de views de mapas
        #self.__lst_view_maps = [viewMap.viewMap(l_map) for l_map in l_landscape.lstMaps]

        # save weather locally
        #self.__weather = l_model.getWeather()
        #assert self.__weather

        # create a viewport
        self.__viewport = vwp.CViewport(self.width() - 1, self.height() - 1)
        assert self.__viewport

        # obtém o centro de referência
        self.__viewport.center = self.__airspace.getPosition("SBSJ") #16
        M_LOG.debug("__init__:center:[{}]/[{}]".format(self.__viewport.center.f_lat, self.__viewport.center.f_lng))

        # create paint engine
        self.__paint_engine = peng.CPaintEngine()
        assert self.__paint_engine

        self.__paint_engine.setColors(False)

        # get color background area
        l_clr = None  # colorMngr.getColor("WND_MAIN_AREA_BKGRND")

        if l_clr is None:

            # create color background
            l_clr = QtGui.QColor(14, 22, 22)
            assert l_clr

        # QBrush
        self.__brush = QtGui.QBrush(l_clr)
        assert self.__brush

        # QPen
        self.__pen = QtGui.QPen()
        assert self.__pen

        # QRect
        self.__rect_invalid = QtCore.QRect()
        assert self.__rect_invalid is not None

        # fast track simulation speed
        self.__f_simulation_speed = 1.

        # radar timer (4s cycle)
        self.__f_radar_interval = 4000. / self.__f_simulation_speed
        self.__i_radar_timer = self.startTimer(round(self.__f_radar_interval, 0))

        # update timer (0.4s cycle)
        self.__f_update_interval = 400. / self.__f_simulation_speed
        self.__i_aircraft_timer = self.startTimer(round(self.__f_update_interval, 0))

        self.__i_active_ac = -1
        self.__v_paused = False

        # setup UI
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setCursor(QtCore.Qt.CrossCursor)

        self.setMouseTracking(True)
        self.setStyleSheet("background-color: rgb(0, 0, 0);")

        # monta a lista de aeronaves ativas
        #self.__build_aircraft_list()

        # logger
        M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    """
    def __build_aircraft_list(self):

        # logger
        M_LOG.info("__build_aircraft_list:>>")

        # testing
        # csc = ""

        # init aircrafts list
        self.__dct_flight = []

        # trava a lista de vôos
        # locData.g_lckFlight.acquire ()

        # try:
        if (1):

            # inicia o contador de strips
            li_ndx = 0

            # obtém o dicionário de vôos ativos
            ldct_flight = self.__emula_model.dct_flight

            # para todos os vôos ativos...
            for l_key, l_atv in ldct_flight.iteritems():

                # cria uma aeronave
                l_anv = clsAircraft.clsAircraft(self.__airspace, self.__weather)
                assert l_anv is not None

                # p = int(random.random () * 19.)
                # n = int(random.random () * 10000.)

                # seta o callsign da aeronave
                l_anv.setCallSign(l_key)
                '''
                self.__s_route = self.__airspace.arrival(li_ndx)

                if self.__s_route is None:
                    l_log.fatal("FlightPlan error: standard route unknown.")
                    sys.exit(1)
                '''
                '''
                pos1 = self.__airspace.getPosition(self.__s_route._aoItem [ 0 ]._sName)

                if pos1 is None:
                    l_log.fatal("FlightPlan error (1): waypoint \"%s\" unknown." % self.__s_route._aoItem [ 0 ]._sName)
                    sys.exit(1)

                pos2 = self.__airspace.getPosition(self.__s_route._aoItem [ 1 ]._sName)

                if pos2 is None:
                    l_log.fatal("FlightPlan error (2): waypoint \"%s\" unknown." % self.__s_route._aoItem [ 0 ]._sName)
                    sys.exit(1)

                tr = tMath.track(pos2, pos1)
                '''
                lf_lat, lf_lng = l_atv.tPosicao

                # cria a posição de referência
                '''
                pos = pll.posLatLngRef(self.__airspace.getPosition(self.__s_route._aoItem [ 0 ]._sName),
                                               self.__airspace.variation (),
                                               tr - 60 + random.random () * 120,
                                               1 + random.random () * 20)
                '''
                l_pos = pll.posLatLng(lf_lat, lf_lng)
                assert l_pos is not None

                # posiciona a aeronave
                l_anv.initPosition(l_pos)

                del l_pos
                '''
                # coloca a aeronave em rota
                l_anv.instructRoute(self.__s_route.getName ())
                '''
                # inclui a aeronave na lista
                self.__dct_flight.append(l_anv)

            # incrementa o contador de strips
            li_ndx += 1

        # finally:

            # libera a lista de vôos
            # locData.g_lckFlight.release ()

        M_LOG.debug("self.__dct_flight(bld): %s" % str(self.__dct_flight))

        # logger
        M_LOG.info("__build_aircraft_list:<<")
    """
    # ---------------------------------------------------------------------------------------------
    """
    def findMap(self, f_sName):

        # logger
        M_LOG.info("findMap:>>")

        # para todos os mapas da lista...
        for l_map in self.__lst_view_maps:

            # achou o mapa procurado ?
            if f_sName == l_map.oTitle["text"]:

                # logger
                M_LOG.info("findMap:<<")

                # retorna o pointer para o mapa
                return l_map

        # logger
        M_LOG.info("findMap:<E01: Map not found.")

        # retorna erro
        return None
    """
    # ---------------------------------------------------------------------------------------------

    def hideLateral(self):

        # logger
        M_LOG.info("hideLateral:>>")

        self.__i_active_ac = -1
        self.setMouseTracking(False)

        # logger
        M_LOG.info("hideLateral:<<")

    # ---------------------------------------------------------------------------------------------

    def makeApproach(self):

        # logger
        M_LOG.info("makeApproach:>>")

        # verifica parâmetros de entrada
        # assert f_control

        l_oXY = pxy.CPosXY(self._iMouseX, self._iMouseY)
        assert l_oXY is not None

        pos = self.__viewport.translate_xy(l_oXY)

        l_fClosest_r = 1000000
        l_sClosest = ""

        i = 0

        while (self.__airspace.arrivalRunway(i)):

            pos1 = self.__airspace.getPosition(self.__airspace.arrivalRunway(i))

            d = tMath.distLL(pos, pos1)
            a = tMath.trackDelta(self.__airspace.runway(self.__airspace.arrivalRunway(i)).track(),
                tMath.track(pos,pos1))

            r = d * tMath.dsin(abs(a))

            if ((r < l_fClosest_r) and (abs(a) < 90)):

                l_sClosest = self.__airspace.arrivalRunway(i)
                l_fClosest_r = r

            i += 1

        self.__s_approach = l_sClosest
        self.__i_lateral_mode = self.C_LMODE_APP

        # logger
        M_LOG.info("makeApproach:<<")

    # ---------------------------------------------------------------------------------------------

    def makeDirect(self):

        # logger
        M_LOG.info("makeDirect:>>")

        # verifica parâmetros de entrada
        # assert f_control

        # get mouse position
        l_oXY = pxy.CPosXY(self._iMouseX, self._iMouseY)
        assert l_oXY is not None

        # converte as coordenadas de tela para mapa
        pos = self.__viewport.translate_xy(l_oXY)

        # inicia variáveis
        l_sClosest = ""
        l_fClosest_r = 1000000

        # primeiro waypoint
        i = 0
        wpt = self.__airspace.waypoint(0)

        # scan all waypoints
        while wpt is not None:

            # calcula a distância do mouse ao waypoint
            r = tMath.distLL(pos, wpt.position())

            # distância menor que a anterior ?
            if r < l_fClosest_r:

                # this is the new closest waypoint
                l_sClosest = wpt._sName()
                l_fClosest_r = r

            # next waypoint
            i += 1
            wpt = self.__airspace.waypoint(i)

        # primeiro vor
        i = 0
        wpt = self.__airspace.vor(0)

        # scan all vor's
        while wpt is not None:

            # calcula a distância do mouse ao vor
            r = tMath.distLL(pos, wpt.position())

            # distância menor que a anterior ?
            if r < l_fClosest_r:

                # this is the new closest element
                l_sClosest = wpt._sName()
                l_fClosest_r = r

            # next vor
            i += 1
            wpt = self.__airspace.vor(i)

        # primeiro ndb
        i = 0
        wpt = self.__airspace.ndb(0)

        # scan all ndb's
        while wpt is not None:

            # calcula a distância do mouse ao ndb
            r = tMath.distLL(pos, wpt.position())

            # distância menor que a anterior ?
            if r < l_fClosest_r:

                # this is the new closest element
                l_sClosest = wpt._sName()
                l_fClosest_r = r

            # next ndb
            i += 1
            wpt = self.__airspace.ndb(i)

        # salva nome do elemento mais próximo do mouse
        self.__s_direct = l_sClosest
        self.__i_lateral_mode = self.C_LMODE_DCT

        # logger
        M_LOG.info("makeDirect:<<")

    # ---------------------------------------------------------------------------------------------

    def makeRoute(self):

        # logger
        M_LOG.info("makeRoute:>>")

        # verifica parâmetros de entrada
        # assert f_control

        # get mouse position
        l_oXY = pxy.CPosXY(self._iMouseX, self._iMouseY)
        assert l_oXY is not None

        # converte as coordenadas de tela para mapa
        pos = self.__viewport.translate_xy(l_oXY)

        # inicia variáveis
        l_sClosest = ""
        l_fClosest_r = 1000000

        # first arrival
        i = 0
        srt = self.__airspace.arrival(0)

        # scan all arrival's
        while srt is not None:

            # init flag
            apply = False

            # first runway
            rw = 0

            # scan all runway's
            while self.__airspace.arrivalRunway(rw):

                # arrival belongs to runway ?
                if srt.belongsToRunway(self.__airspace.arrivalRunway(rw)):

                    # ok, found
                    apply = True

                # next runway
                rw += 1

            # no found any runway ?
            if not apply:

                # next arrival
                i += 1
                srt = self.__airspace.arrival(i)

                # next loop
                continue

            n = 0
            while srt.item(n) is not None:

                pos1 = self.__airspace.getPosition(srt.item(n)._sName)
                r = tMath.distLL(pos, pos1)

                if srt.item(n + 1):
                    pos2 = self.__airspace.getPosition(srt.item(n + 1)._sName)
                    rttrk = tMath.track(pos1, pos2)
                    rtdist = tMath.distLL(pos1, pos2)
                    mstrk = tMath.track(pos1, pos)
                    tdelta = tMath.trackDelta(rttrk, mstrk)
                    prog = tMath.distLL(pos, pos1) * tMath.dcos(tdelta)

                    if ((prog > 0) and (prog < rtdist)):
                        r = tMath.distLL(pos, pos1) * tMath.dsin(abs(tdelta))

                # distância menor que a anterior ?
                if r < l_fClosest_r:

                    # this is the new closest element
                    l_sClosest = srt.getName()
                    l_fClosest_r = r

                n += 1

            # next arrival
            i += 1
            srt = self.__airspace.arrival(i)

        # first transition
        i = 0
        srt = self.__airspace.transition(0)

        # scan all transitions
        while srt is not None:

            # init flag
            apply = False

            # first runway
            rw = 0

            # scan all runway's
            while self.__airspace.arrivalRunway(rw):

                # transition belongs to runway ?
                if srt.belongsToRunway(self.__airspace.arrivalRunway(rw)):

                    # ok, found
                    apply = True

                # next runway
                rw += 1

            # no found any transition ?
            if not apply:

                # next transition
                i += 1
                srt = self.__airspace.transition(i)

                # next loop
                continue

            n = 0
            while srt.item(n):
                pos1 = self.__airspace.getPosition(srt.item(n)._sName)
                r = tMath.distLL(pos, pos1)

                if srt.item(n + 1):
                    pos2 = self.__airspace.getPosition(srt.item(n + 1)._sName)
                    rttrk = tMath.track(pos1, pos2)
                    rtdist = tMath.distLL(pos1, pos2)
                    mstrk = tMath.track(pos1, pos)
                    tdelta = tMath.trackDelta(rttrk, mstrk)
                    prog = tMath.distLL(pos, pos1) * tMath.dcos(tdelta)

                    if ((prog > 0) and (prog < rtdist)):
                        r = tMath.distLL(pos, pos1) * tMath.dsin(abs(tdelta))

                if r < l_fClosest_r:
                    l_sClosest = srt._sName()
                    l_fClosest_r = r

                n += 1

            # next transition
            i += 1
            srt = self.__airspace.transition(i)

        self.__s_route = l_sClosest
        self.__i_lateral_mode = self.C_LMODE_RTE

        # logger
        M_LOG.info("makeRoute:<<")

    # ---------------------------------------------------------------------------------------------

    def makeVector(self, f_iVal):

        # logger
        M_LOG.info("makeVector:>>")

        # verifica parâmetros de entrada
        # assert f_control

        M_LOG.debug("f_iVal....: " + str(f_iVal))
        M_LOG.debug("aoAircraft: " + str(len(self.__dct_flight)))

        # verifica se o índice é válido
        if (f_iVal < 0) or (f_iVal >= len(self.__dct_flight)):

            # logger
            M_LOG.info("makeVector:<E01. índice inválido.")

            # cai fora...
            return

        # get mouse position
        l_XY = pxy.CPosXY(self._iMouseX, self._iMouseY)
        assert l_XY is not None

        # converte as coordenadas de tela para mapa
        l_pos = self.__viewport.translate_xy(l_XY)

        self.__f_radar_vector = tMath.track(self.__dct_flight[f_iVal].radarPosition(), l_pos) + self.__airspace.variation()

        l_iRem = int(self.__f_radar_vector * 10.) % 50

        self.__f_radar_vector = int(self.__f_radar_vector) - (int(self.__f_radar_vector) % 5)

        if l_iRem >= 25:
            self.__f_radar_vector += 5.

        if self.__f_radar_vector > 360.:
            self.__f_radar_vector -= 360.

        if 0. == self.__f_radar_vector:
            self.__f_radar_vector = 360.

        self.__i_lateral_mode = self.C_LMODE_HDG

        # logger
        M_LOG.info("makeVector:<<")

    # ---------------------------------------------------------------------------------------------

    # void(QPainter *)
    def onDraw(self, f_painter):
        """
        called to draw the radar window content. calls the onDraw function for every graphical
        element to be displayed in the view. Those elements are listed in the _lstDisplayElement
        table. The elements are displayed from the lower layer to the upper and within a layer
        from the lowest priority order to the upper, so that elements with the highest priority
        are displayed over any other graphical elements.

        @param f_painter: painting device.
        """
        # logger
        M_LOG.info("onDraw:>>")

        # verifica parâmetros de entrada
        assert f_painter

        # pTrkMngr = CRadarScope.cls_app.GetTrackMngr ()

        # set background mode
        # f_painter.setBackgroundMode(QtCore.Qt.TransparentMode)

        # desenha o fundo de tela
        self.__paint_engine.draw_background(self, f_painter)

        # para todas as prioridades...
        #for l_iPrio in xrange(displayElement.PRIO_MAP_MAX, -1, -1):

            #M_LOG.debug("l_iPrio: " + str(l_iPrio))

            # para todos os mapas da lista...
            #for l_oVMap in self.__lst_view_maps:

                # desenha o elemento
                #l_oVMap.onDraw(self, f_painter, l_iPrio)

        # desenha o ARP
        self.__paint_engine.draw_arp(self)

        # para todos os aeródromos...
        for l_aer in self.__airspace.dct_aer.values():
            # desenha o aeródromo
            self.__paint_engine.draw_aerodromo(self, l_aer)
        '''
        # init index
        l_iI = 0
        l_iJ = 0

        # draw standard routes
        while self.__airspace.arrivalRunway(l_iI):
            while self.__airspace.arrival(l_iJ):
                if self.__airspace.arrival(l_iJ).belongsToRunway(self.__airspace.arrivalRunway(l_iI)):
                    self.__paint_engine.drawArrival(self, self.__airspace.arrival(l_iJ))

                l_iJ += 1
            l_iJ = 0

            while self.__airspace.transition(l_iJ):
                if self.__airspace.transition(l_iJ).belongsToRunway(self.__airspace.arrivalRunway(l_iI)):
                    self.__paint_engine.drawTransition(self, self.__airspace.transition(l_iJ))

                l_iJ += 1
            l_iI += 1
        l_iI = 0

        # draw standard routes
        while self.__airspace.departureRunway(l_iI):

            l_iJ = 0

            while self.__airspace.departure(l_iJ):
                if self.__airspace.departure(l_iJ).belongsToRunway(self.__airspace.departureRunway(l_iI)):
                    self.__paint_engine.drawDeparture(self, self.__airspace.departure(l_iJ))

                l_iJ += 1
            l_iI += 1
        '''
        # draw DMEs navaids
        for l_dme in [fix for fix in self.__airspace.dct_fix.values() if ldefs.E_DME == fix.en_fix_tipo]:
            # desenha o DME
            self.__paint_engine.draw_navaid(self, l_dme)

        # draw NDBs navaids
        for l_ndb in [fix for fix in self.__airspace.dct_fix.values() if ldefs.E_NDB == fix.en_fix_tipo]:
            # desenha o NDB
            self.__paint_engine.draw_navaid(self, l_ndb)

        # draw VORs navaids
        for l_vor in [fix for fix in self.__airspace.dct_fix.values() if ldefs.E_VOR == fix.en_fix_tipo]:
            # desenha o VOR
            self.__paint_engine.draw_navaid(self, l_vor)

        # draw waypoints
        #for l_wpt in [fix for fix in self.__airspace.dct_fix.values() if ldefs.E_BRANCO == fix.en_fix_tipo]:
            #self.__paint_engine.draw_navaid(self, l_wpt)
        '''
        # draw runways
        for l_oRWY in self.__airspace.aoRWY:
            self.__paint_engine.drawRunway(self, l_oRWY)
        '''
        # para todas as subidas...
        #for l_sub in self.__airspace.dct_sub.values():
            # desenha o procedimento de subida
            #self.__paint_engine.draw_subida(self, l_sub)

        # para todas as trajetórias...
        for l_trj in self.__airspace.dct_trj.values():
            # desenha o procedimento de trajetória
            self.__paint_engine.draw_trajetoria(self, l_trj)

        # draw aircraft targets
        for l_anv in self.__dct_flight.values():
            # desenha a aeronave
            self.__paint_engine.draw_blip(self, l_anv)
        '''
        if self.__i_active_ac >= 0:
            if self.C_LMODE_HDG == self.__i_lateral_mode:
                self.__paint_engine.drawVector(self, self.__dct_flight[self.__i_active_ac], self.__f_radar_vector)

            elif self.C_LMODE_DCT == self.__i_lateral_mode:
                if self.__s_direct != "":
                    self.__paint_engine.drawDirect(self, self.__dct_flight[self.__i_active_ac], self.__s_direct)

            elif self.C_LMODE_RTE == self.__i_lateral_mode:
                if self.__s_route != "":
                    self.__paint_engine.drawRoute(self, self.__dct_flight[self.__i_active_ac], self.__s_route)

            elif self.C_LMODE_APP == self.__i_lateral_mode:
                if self.__s_approach != "":
                    self.__paint_engine.drawApproach(self, self.__dct_flight[self.__i_active_ac], self.__s_approach)
        '''
        '''
        # if the currently selected radar service is not available the message
        # "display frozen" is displayed in the top of the underlay layer
        if True: #not pTrkMngr.m_pTrkSrc):

            FrozenTime = QtCore.QTime ().currentTime () # pTrkMngr.GetFrozenTime ()
            rect = self.rect ()

            f_painter.setFont(FontMngr.GetFontByName("FROZEN"))
            f_painter.setPen(ColorMngr.GetColor(ColorMngr.GetColorNb("FROZEN_MSG")))

            txt = "FROZEN AT " + FrozenTime.toString("hh:mm:ss")
            size = f_painter.boundingRect(0, 0, 0, 0, QtCore.Qt.AlignLeft, txt).size ()

            f_painter.drawText(rect.center ().x () - size.width () / 2, rect.center ().y (), txt)
        '''
        '''
        # and with a higher priority the element with implicit focus
        if self.m_pCurElem is not None:
            M_LOG.debug("self.m_pCurElem: ", + str(self.m_pCurElem))
            self.m_pCurElem.onDraw(f_painter, 1)

        if self.m_pModifElem is not None:
            M_LOG.debug("self.m_pModifElem: ", + str(self.m_pModifElem))
            self.m_pModifElem.onDraw(f_painter, 0)
        '''
        # logger
        M_LOG.info("onDraw:<<")

    # ---------------------------------------------------------------------------------------------

    def showLateral(self, f_iVal):

        # logger
        M_LOG.info("showLateral:>>")

        self.__i_active_ac = f_iVal

        self.setMouseTracking(True)

        # logger
        M_LOG.info("showLateral:<<")

    # =============================================================================================
    # Qt Slots
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot(bool)
    def invert(self, f_vInverted):

        # logger
        M_LOG.info("invert:>>")

        # inverte as cores dos elementos
        self.__paint_engine.setColors(f_vInverted)

        # redesenha
        self.repaint()

        # logger
        M_LOG.info("invert:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot(bool)
    def pause(self, f_vVal):

        # logger
        M_LOG.info("pause:>>")

        self.__v_paused = f_vVal

        if self.__v_paused:

            self.killTimer(self.__i_radar_timer)
            self.killTimer(self.__i_aircraft_timer)

        else:

            self.__i_radar_timer = self.startTimer(tMath.round(self.__f_radar_interval, 0))
            self.__i_aircraft_timer = self.startTimer(tMath.round(self.__f_update_interval, 0))

        # logger
        M_LOG.info("pause:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def showRange(self):

        # logger
        M_LOG.info("showRange:>>")

        self.__parent.status_bar.lblRange.setText("R%d" % int(self.__viewport.f_zoom))

        # logger
        M_LOG.info("showRange:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def zoom_in(self):

        # logger
        M_LOG.info("zoom_in:>>")

        # change zoom  
        self.__viewport.f_zoom = round(self.__viewport.f_zoom / math.sqrt(2.), 0)
                
        # update scope
        self.repaint()

        # logger
        M_LOG.info("zoom_in:<<")

    # ---------------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def zoom_out(self):

        # logger
        M_LOG.info("zoom_out:>>")

        # change zoom
        self.__viewport.f_zoom = round(self.__viewport.f_zoom * math.sqrt(2.), 0)
                
        # update scope
        self.repaint()

        # logger
        M_LOG.info("zoom_out:<<")

    # =============================================================================================
    # Qt Events
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    def keyReleaseEvent(self, f_evt):

        # logger
        M_LOG.info("keyReleaseEvent:>>")

        if self.__i_active_ac < 0:

            # logger
            M_LOG.info("keyReleaseEvent:<E01: not active.")

            # return
            return

        if QtCore.Qt.Key_D == f_evt.key():

            self.makeDirect()
            self.repaint()

        elif QtCore.Qt.Key_R == f_evt.key():

            self.makeRoute()
            self.repaint()

        elif QtCore.Qt.Key_H == f_evt.key():

            self.makeVector(self.__i_active_ac)
            self.repaint()

        elif QtCore.Qt.Key_A == f_evt.key():

            self.makeApproach()
            self.repaint()

        elif QtCore.Qt.Key_Escape == f_evt.key():

            if self.__i_active_ac >= 0:
                self.hideLateral()
                self.repaint()

        else:
            f_evt.ignore()

        # logger
        M_LOG.info("keyReleaseEvent:<<")

    # ---------------------------------------------------------------------------------------------

    def mouseMoveEvent(self, f_evt):
        """
        called when the mouse pointer is moved over the radar window.

        @param  f_evt: QMouseEvent*, not used in this function.
        """
        # logger
        M_LOG.info("mouseMoveEvent:>>")

        # verifica condições de execução
        Normal = 0
        Panning = 1
        Zoom = 2

        m_Mode = 0

        '''
        QRect radarwndrect ;
        QPoint globalpnt ;
        QRect statusbarrect ;
        '''

        M_LOG.debug("_iActiveAC...: " + str(self.__i_active_ac))
        M_LOG.debug("_iLateralMode: " + str(self.__i_lateral_mode))

        self._iMouseX = f_evt.x()
        self._iMouseY = f_evt.y()

        if self.__i_active_ac >= 0:

            if self.C_LMODE_HDG == self.__i_lateral_mode:
                self.makeVector(self.__i_active_ac)

            elif self.C_LMODE_DCT == self.__i_lateral_mode:
                self.makeDirect()

            elif self.C_LMODE_RTE == self.__i_lateral_mode:
                self.makeRoute()

            elif self.C_LMODE_APP == self.__i_lateral_mode:
                self.makeApproach()

            self.repaint()

        else:
            # pnt = QtGui.QCursor.pos () ;
            # point = mapFromGlobal(pnt) ;

            # CheckFocus () ;

            # check the radar window mode
            if Normal == m_Mode:
                '''
                # No mode is activated for the radar window having the focus
                # No process is to be performed if the radar window is over
                # another radar window for which the panning mode is activated
                if m_psMainWnd
                    if(m_psMainWnd->m_Mode == Panning)
                        break ;

                if m_psSecWnd1
                    if(m_psSecWnd1->m_Mode == Panning)
                        break ;

                if m_psSecWnd2
                    if(m_psSecWnd2->m_Mode == Panning)
                        break ;
                '''
                # the status bar must show the current lat long of the mouse pointer
                # if it presents the focus and the mouse pointer is over the view
                # QPoint pnt ;

                if (1):  # m_bsForcedMove or (( point != m_LastCursorPos) and(hasMouse ()))):
                    '''
                    killTimer(m_TimerId) ;
                    m_TimerId = startTimer(100) ;

                    pnt = point ;
                    DPtoLP(&pnt) ;

                    radarwndrect = this->geometry () ;
                    statusbarrect = GetStatusBar ()->rect () ;
                    '''
                    # the mouse pointer must not be over the status bar
                    if (1):  # globalpnt.y () <= radarwndrect.y () + radarwndrect.height () - statusbarrect.height ()):

                        # converte a posição do mouse para coordenadas XY
                        l_oXY = pxy.CPosXY(f_evt.x(), f_evt.y())
                        assert l_oXY

                        # converte coordenadas XY para geográfica
                        l_oGeo = self.__viewport.translate_xy(l_oXY)
                        assert l_oGeo

                        # atualiza a statusBar
                        self.__parent.status_bar.updateCoordinates(unicode(l_oGeo) + " (%d, %d)" % (f_evt.x(), f_evt.y()))

                        # libera a área alocada
                        del l_oGeo

                pass
                '''
                m_LastCursorPos = point ;

                # the event is then transmitted to the graphical element that are
                # under modification or that has the implicit focus
                if(hasMouse ())

                    if(m_pModifElem)
                        m_pModifElem->onMouseMove(0, point) ;

                    if(m_pCurElem)

                        curprio = m_pCurElem->GetPriority(point, true) ;

                        if(curprio == 0)

                            m_pCurElem->SelectElement(false) ;
                            m_pCurElem = NULL ;
                else:
                    # if the element being modified is not within the view the event is transmitted
                    # anyway in order to cancel the tool creation mode
                    if(m_pModifElem)
                        m_pModifElem->onMouseMove(0, point) ;
                '''
                pass

            elif (Panning == m_Mode):
                '''
                # panning mode
                if(m_ReducePanning >= 10)
                {
                    m_ReducePanning = 0 ;
                    QRect rect = QWidget::rect () ;
                    QSize size ;
                    QPoint pnt ;
                    size = QSize(rect.center ().x () - point.x (), rect.center ().y () - point.y ()) ;
                    DPtoLP(&size) ;
                    size.setHeight(-size.height ()) ;

                    # Because of the range limitation, the center must remains within predefined limits
                    # if (( size.width ()) ||(size.height ()))
                    {
                        # Following the first move of the mouse pointer this check is not performed and over all the presentation of the view is not updated as the first move is the positionning of the mouse pointer at the center of the view
                        if(!m_FirstPanningMove)
                        {
                            pnt = GetCentre () ;
                            pnt = QPoint(pnt.x () + size.width (), pnt.y () + size.height ()) ;

                            /*if(pnt.x () >5000)
                                pnt.setX(5000) ;

                            if(pnt.x () <-5000)
                                pnt.setX(-5000) ;

                            if(pnt.y () >5000)
                                pnt.setY(5000) ;

                            if(pnt.y () <-5000)
                                pnt.setY(-5000) ;*/

                            SetCentre(pnt) ;
                            onUpdate(NULL, 0, NULL) ;

                        } # end if

                        m_FirstPanningMove = false ;
                        rect = geometry () ;
                        QCursor::setPos(rect.center () .x (), rect.center () .y ()) ;
                        CTOORArrow::UpdateFromView(this) ;

                    } # end if
                }
                else
                    m_ReducePanning ++ ;
                '''
                pass

            elif Zoom == m_Mode:
                '''
                # zoom mode
                radarwndrect = this->geometry () ;
                globalpnt = QCursor::pos () ;
                statusbarrect = GetStatusBar ()->rect () ;

                # the mouse pointer must be over the radar window to perform the change
                if (( globalpnt.x () >= radarwndrect.x () + radarwndrect.width ()) ||
                   (globalpnt.x () <= radarwndrect.x ()) ||
                   (globalpnt.y () <= radarwndrect.y ()) ||
                   (globalpnt.y () >= radarwndrect.y () + radarwndrect.height () - statusbarrect.height ()))
                {
                    m_Mode = Normal ;
                    setCursor(*CAsdApp::GetApp ()->GetCursor(MPNormalSelect)) ;

                } # end if
                '''
                pass

        # logger
        M_LOG.info("mouseMoveEvent:<<")

    # ---------------------------------------------------------------------------------------------

    def mouseReleaseEvent(self, f_evt):

        # logger
        M_LOG.info("mouseReleaseEvent:>>")

        # verifica parâmetros de entrada
        # assert f_control

        if f_evt.button() & QtCore.Qt.LeftButton:

            # none aircraft active ?
            if self.__i_active_ac < 0:

                # update mouse
                self._iMouseX = f_evt.x()
                self._iMouseY = f_evt.y()

                # find closest aircraft
                l_XY = pxy.CPosXY(self._iMouseX, self._iMouseY)
                assert l_XY is not None

                l_pos = self.__viewport.translate_xy(l_XY)

                l_fClosest_r = 1000000
                l_iClosest = -1

                for i in xrange(len(self.__dct_flight)):

                    r = tMath.distLL(l_pos, self.__dct_flight[i].radarPosition())

                    if r < l_fClosest_r:
                        l_iClosest = i
                        l_fClosest_r = r

                # activate Vector
                self.showLateral(l_iClosest)
                self.makeVector(self.__i_active_ac)
                self.repaint()

            else:  # Yes, order HDG

                if self.C_LMODE_HDG == self.__i_lateral_mode:
                    self.__dct_flight[self.__i_active_ac].instructHeading(int(self.__f_radar_vector))

                elif self.C_LMODE_DCT == self.__i_lateral_mode:
                    self.__dct_flight[self.__i_active_ac].instructDirect(self.__s_direct)

                elif self.C_LMODE_RTE == self.__i_lateral_mode:
                    self.__dct_flight[self.__i_active_ac].instructRoute(self.__s_route)

                elif self.C_LMODE_APP == self.__i_lateral_mode:
                    self.__dct_flight[self.__i_active_ac].instructApproach(self.__s_approach)

                self.hideLateral()
                self.repaint()

        elif f_evt.button() & QtCore.Qt.MidButton:

            l_XY = pxy.CPosXY(f_evt.x(), f_evt.y())
            assert l_XY is not None

            l_pos = self.__viewport.translate_xy(l_XY)
            self.__viewport.center = l_pos

            self.repaint()

        elif f_evt.button() & QtCore.Qt.RightButton:

            # cancel vectoring
            if self.__i_active_ac >= 0:
                self.hideLateral()
                self.repaint()

        # logger
        M_LOG.info("mouseReleaseEvent:<<")

    # ---------------------------------------------------------------------------------------------

    def paintEvent(self, f_evt):

        # logger
        M_LOG.info("paintEvent:>>")

        # verifica condições de execução
        assert self.__pen
        assert self.__brush
        assert self.__rect_invalid is not None

        # cria um painter para o pixmap
        l_oPainter = QtGui.QPainter(self)
        assert l_oPainter

        # caneta
        l_oPainter.setPen(self.__pen)

        # pincel
        l_oPainter.setBrush(self.__brush)

        if 1:  # not self.__rect_invalid.isEmpty():

            # save painter
            l_oPainter.save()

            # preenche o fundo
            l_oPainter.fillRect(self.__rect_invalid, self.__brush)

            # desenha os elementos gráficos
            self.onDraw(l_oPainter)

            # sinaliza que a área deve ser redesenhada
            self.__rect_invalid.setRect(0, 0, -1, -1)

            # restore painter
            l_oPainter.restore()

        # logger
        M_LOG.info("paintEvent:<<")

    # ---------------------------------------------------------------------------------------------

    def resizeEvent(self, f_evt):

        # logger
        M_LOG.info("resizeEvent:>>")

        # update size
        # self.__viewport.update_size(QtCore.QRect(0, 0, self.width() - 1, self.height() - 1))
        self.__viewport.update_size(self.width() - 1, self.height() - 1)

        # logger
        M_LOG.info("resizeEvent:<<")

    # ---------------------------------------------------------------------------------------------

    def timerEvent(self, f_evt):

        # logger
        M_LOG.info("timerEvent:>>")

        # timer de radar acionado ?
        if f_evt.timerId() == self.__i_radar_timer:

            M_LOG.debug("RadarTimer...")

            # reconstroi a lista de vôos ativos
            # self.__build_aircraft_list()

            # para todas as aeronaves na lista...
            for l_atv in self.__dct_flight.values():

                # faz a atualização da posição das aeronaves
                l_atv.update_radar_position(self.__f_simulation_speed * self.__f_radar_interval)

                # atualiza a posição da aeronave
                # self.updateAnv(l_atv, l_iI)

            # atualiza a tela
            self.repaint()

        # timer de aeronave acionado ?
        elif f_evt.timerId() == self.__i_aircraft_timer:

            # para todas as aeronaves na lista...
            for l_atv in self.__dct_flight.values():

                # faz a cinemática da aeronave
                l_atv.fly(self.__f_simulation_speed * self.__f_update_interval)

        # logger
        M_LOG.info("timerEvent:<<")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def fRadarInterval(self):
        """
        get radar interval
        """
        return self.__f_radar_interval

    @fRadarInterval.setter
    def fRadarInterval(self, f_val):
        """
        set radar interval
        """
        self.__f_radar_interval = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def fUpdateInterval(self):
        """
        get update interval
        """
        return self.__f_update_interval

    @fUpdateInterval.setter
    def fUpdateInterval(self, f_val):
        """
        set update interval
        """
        self.__f_update_interval = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def viewport(self):
        """
        get viewport
        """
        return self.__viewport

    @viewport.setter
    def viewport(self, f_val):
        """
        set viewport
        """
        self.__viewport = f_val

# < the end >--------------------------------------------------------------------------------------
