#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
airspace_visil.

DOCUMENT ME!

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os
import sys

# PyQt4 library
from PyQt4 import QtCore, QtXml

# model
from ..coords import pos_lat_lng as pll

from ..stock import airspace_basic as airs
from ..stock import fix as cfix
from ..stock import flight_plan_item as cfpi
from ..stock import holding as cesp
from ..stock import runway as crun
from ..stock import standard_route as stdrt

from ..items import esp_data as espdata
from ..items import sub_data as subdata
from ..items import trj_data as trjdata

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CAirspaceVisil >------------------------------------------------------------------------------

class CAirspaceVisil(airs.CAirspaceBasic):
    """
    represent an airspace
    """
    # ---------------------------------------------------------------------------------------------

    C_ARRIVAL = 0
    C_DEPARTURE = 1

    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, fs_location):
        """
        read datafile for specified location (airport)
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_model
        assert fs_location

        # init super class
        super(CAirspaceVisil, self).__init__(f_model)

        # herdados de CAirspaceBase
        # self.config         # config manager
        # self.dct_config     # dicionário de configuração
        # self.event          # event manager
        # self.model          # model manager
        # self.dct_aer        # dicionário de aeródromos
        # self.dct_fix        # dicionário de fixos
        # self.dct_fix_indc   # dicionário de indicativos

        # dicionários locais
        self.__dct_dme = {}
        self.__dct_ndb = {}
        self.__dct_vor = {}
        self.__dct_wpt = {}

        self.__dct_dep = {}
        self.__dct_esp = {}
        self.__dct_pso = {}
        self.__dct_sub = {}
        self.__dct_trj = {}

        self.__dct_rwy = {}
        self.__dct_arr_runways = {}
        self.__dct_dep_runways = {}

        self.__dct_transitions = {}

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def activateRunway(self, fs_indc, fi_mode):
        """
        add a runway for arrivals or departures
        """
        # logger
        # M_LOG.info("activateRunway:>>")

        # verifica parâmetros de entrada
        # assert f_model

        if self.C_DEPARTURE == fi_mode:
            if fs_indc in self.__dct_dep_runways:

                # logger
                # M_LOG.info("<E01")

                return

            self.__dct_dep_runways.append(fs_indc)
            # M_LOG.info("added runway ", fs_indc, " for departures.")

        elif self.C_ARRIVAL == fi_mode:
            if fs_indc in self.__dct_arr_runways:

                # logger
                # M_LOG.info("<E02")

                return

            self.__dct_arr_runways.append(fs_indc)
            # M_LOG.info("added runway " + fs_indc + " for arrivals.")

        # logger
        # M_LOG.info("activateRunway:<<")

    # ---------------------------------------------------------------------------------------------

    def arrival(self, fi_ndx):
        """
        return a pointer to the arrival route with specified index
        """
        # logger
        # M_LOG.info("arrival:><")

        # verifica parâmetros de entrada
        # assert f_model

        if fi_ndx >= len(self.__dct_pso):
            return None

        # return
        return self.__dct_pso[fi_ndx]

    # ---------------------------------------------------------------------------------------------

    def arrivalRunway(self, fi_ndx):
        """
        return a pointer to a string naming the arrival runway of specified index
        """
        # logger
        # M_LOG.info("arrivalRunway:><")

        # verifica parâmetros de entrada
        # assert f_model

        if fi_ndx >= len(self.__dct_arr_runways):
            return None

        # return
        return self.__dct_arr_runways[fi_ndx]

    # ---------------------------------------------------------------------------------------------

    def deactivateRunway(self, fs_indc, fi_mode):
        """
        remove a runway from available departure or arrival runways
        """
        # logger
        # M_LOG.info("deactivateRunway:>>")

        # verifica parâmetros de entrada
        # assert f_model

        if self.C_DEPARTURE == fi_mode:
            if fs_indc in self.__dct_dep_runways:
                self.__dct_dep_runways.remove(fs_indc)
                # M_LOG.info("removed runway ", fs_indc, " for departures.")

        elif self.C_ARRIVAL == fi_mode:
            if fs_indc in self.__dct_arr_runways:
                self.__dct_arr_runways.remove(fs_indc)
                # M_LOG.info("removed runway ", fs_indc, " for arrivals.")

        # logger
        # M_LOG.info("deactivateRunway:<<")

    # ---------------------------------------------------------------------------------------------

    def departure(self, fi_ndx):
        """
        return a pointer to the departure route with specified index
        """
        # logger
        # M_LOG.info("departure:><")

        # verifica parâmetros de entrada
        # assert f_model

        if fi_ndx >= len(self.___dep):
            return None

        # return
        return self.___dep[fi_ndx]

    # ---------------------------------------------------------------------------------------------

    def departureRunway(self, fi_ndx):
        """
        return a pointer to a string naming the departure runway of specified index
        """
        # logger
        # M_LOG.info("departureRunway:><")

        # verifica parâmetros de entrada
        # assert f_model

        if fi_ndx >= len(self.__dct_dep_runways):
            return None

        # return
        return self.__dct_dep_runways[fi_ndx]

    # ---------------------------------------------------------------------------------------------

    def dme(self, fi_ndx):
        """
        return a pointer to the DME with specified index
        """
        # logger
        # M_LOG.info("dme:><")

        # verifica parâmetros de entrada
        # assert f_model

        if fi_ndx >= len(self.__dct_dme):
            return None

        # return
        return self.__dct_dme[fi_ndx]

    # ---------------------------------------------------------------------------------------------

    def getPosition(self, fs_indc):
        """
        get position of a waypoint/vor/ndb/... named as specified
        """
        # logger
        # M_LOG.info("getPosition:>>")

        # verifica parâmetros de entrada
        # assert f_model

        # pesquisa aeródromos
        l_aer = self.dct_aer.get(fs_indc, None)
        M_LOG.debug("getPosition:aer:[{}]".format(l_aer))

        if l_aer is not None:

            M_LOG.debug("getPosition:aer:[{}]/[{}]".format(l_aer.f_aer_lat, l_aer.f_aer_lng))

            # logger
            # M_LOG.info("getPosition:<E01")

            # return
            return pll.CPosLatLng(l_aer.f_aer_lat, l_aer.f_aer_lng)

        # pesquisa fixos
        l_key = self.dct_fix_indc.get(fs_indc, None)

        if l_key is not None:

            # acessa o fixo pela key
            l_fix = self.dct_fix[l_key]
            assert l_fix

            # logger
            # M_LOG.info("getPosition:<E02")

            # return
            return pll.CPosLatLng(l_fix.f_fix_lat, l_fix.f_fix_lng)

        # pesquisa runway's
        for l_item in self.__dct_rwy:
            if l_item.s_indc == fs_indc:

                # logger
                # M_LOG.info("getPosition:<E03")

                # return
                return l_item.position

        # logger
        # M_LOG.info("getPosition:<<")

        # return
        return None

    # ---------------------------------------------------------------------------------------------

    def holding(self, f_val):
        """
        return a pointer to the holding with specified index
        """
        # logger
        # M_LOG.info("holding:><")

        # verifica parâmetros de entrada
        # assert f_model

        if isinstance(f_val, int):
            return self.dct_esp.get(f_val, None)

        elif isinstance(f_val, str):
            return self.dct_esp_indc.get(f_val, None)

        # return
        return None

    # ---------------------------------------------------------------------------------------------

    def load_dicts(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("load_dicts:>>")

        # monta o nome da tabela de procedimentos de espera
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.esp"])

        # carrega a tabela de procedimentos de espera em um dicionário
        self.__dct_esp = espdata.CEspData(self.model, ls_path)
        assert self.__dct_esp is not None

        # monta o nome da tabela de procedimentos de subida
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.sub"])

        # carrega a tabela de procedimentos de subida em um dicionário
        self.__dct_sub = subdata.CSubData(self.model, ls_path)
        assert self.__dct_sub is not None

        # monta o nome da tabela de procedimentos de trajetória
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.trj"])

        # carrega a tabela de procedimentos de trajetória em um dicionário
        self.__dct_trj = trjdata.CTrjData(self.model, ls_path)
        assert self.__dct_trj is not None

        # resolve os procedimentos dos break-points
        # self.resolv_procs()

        # logger
        # M_LOG.info("load_dicts:<<")

    # ---------------------------------------------------------------------------------------------

    def load_xml(self, fs_filename):
        """
        load xml airspace file
        """
        # logger
        # M_LOG.info("load_xml:>>")

        # verifica parâmetros de entrada
        # assert f_model

        # read coordinates
        ls_filename = ":/data/" + fs_filename + ".xml"
        M_LOG.debug("ls_filename: " + str(ls_filename))

        l_data_file = QtCore.QFile(ls_filename)
        assert l_data_file is not None

        l_data_file.open(QtCore.QIODevice.ReadOnly)

        if not l_data_file.isOpen():
            # logger
            l_log = logging.getLogger("airspace::load_xml")
            l_log.setLevel(logging.NOTSET)
            l_log.fatal("E01: Failed to open %s" % ls_filename)

            # abend
            sys.exit(1)

        l_xml_doc = QtXml.QDomDocument("airspace")
        assert l_xml_doc is not None

        if not l_xml_doc.setContent(l_data_file):

            l_data_file.close()

            # logger
            l_log = logging.getLogger("airspace::load_xml")
            l_log.setLevel(logging.NOTSET)
            l_log.fatal("E02: Failed to parse %s" % ls_filename)

            # abend
            sys.exit(1)

        l_data_file.close()

        l_doc_elem = l_xml_doc.documentElement()
        assert l_doc_elem is not None

        self.__f_variation, lv_ok = l_doc_elem.attribute(QtCore.QString("variation"), QtCore.QString("0")).toDouble()
        self.__f_elevation, lv_ok = l_doc_elem.attribute(QtCore.QString("elevation"), QtCore.QString("0")).toDouble()

        l_node = l_doc_elem.firstChild()
        assert l_node is not None

        while not l_node.isNull():

            l_element = l_node.toElement()
            assert l_element is not None

            if not l_element.isNull():
                self.__parse_dom_element(l_element)

            l_node = l_node.nextSibling()
            assert l_node is not None

        # logger
        # M_LOG.info("load_xml:<<")

    # ---------------------------------------------------------------------------------------------

    def ndb(self, fi_ndx):
        """
        return a pointer to the NDB with specified index
        """
        # logger
        # M_LOG.info("ndb:><")

        # verifica parâmetros de entrada
        # assert f_model

        if fi_ndx >= len(self.__dct_ndb):
            return None

        # return
        return self.__dct_ndb[fi_ndx]

    # ---------------------------------------------------------------------------------------------

    def __parse_dom_element(self, f_element):
        """
        helper function to the constructor, parses xml entries
        """
        # logger
        # M_LOG.info("__parse_dom_element:>>")

        # verifica parâmetros de entrada
        # assert f_model

        lv_ok = False

        lf_lat = 0
        lf_lng = 0

        ls_indc = f_element.text().toLocal8Bit().data()  # constData ()
        # M_LOG.info("ls_indc: %s" % ls_indc)

        # read coordinates if available
        if f_element.hasAttribute(QtCore.QString("longitude")) and \
           f_element.hasAttribute(QtCore.QString("latitude")):

            lf_lat, lv_ok = f_element.attribute(QtCore.QString("latitude"), QtCore.QString("0")).toDouble()
            lf_lng, lv_ok = f_element.attribute(QtCore.QString("longitude"), QtCore.QString("0")).toDouble()

        # handle case of ARP
        if f_element.tagName() == QtCore.QString("ARP"):

            self.__arp = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert self.__arp

        # handle case of VOR
        elif f_element.tagName() == QtCore.QString("VOR"):

            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self.__dct_vor.append(l_fix)

        # handle case of DME
        elif f_element.tagName() == QtCore.QString("DME"):

            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self.__dct_dme.append(l_fix)

        # handle case of NDB
        elif f_element.tagName() == QtCore.QString("NDB"):

            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self.__dct_ndb.append(l_fix)

        # handle case of WPT
        elif f_element.tagName() == QtCore.QString("WPT"):

            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self.__dct_wpt.append(l_fix)

        # handle case of RWY
        elif f_element.tagName() == QtCore.QString("RWY"):

            l_track, lv_ok = f_element.attribute(QtCore.QString("track"), QtCore.QString("0")).toDouble()
            l_gp, lv_ok = f_element.attribute(QtCore.QString("glidepath"), QtCore.QString("0")).toDouble()

            l_rwy = crun.CRunway(ls_indc, lf_lat, lf_lng, l_track, l_gp)
            assert l_rwy is not None

            self.__dct_rwy.append(l_rwy)

        # handle case of holding
        elif f_element.tagName() == QtCore.QString("holding"):

            l_inb, lv_ok = f_element.attribute(QtCore.QString("inbound"), QtCore.QString("0")).toDouble()
            # M_LOG.info("l_inb: %f" % l_inb)

            l_dir = 'l' if f_element.attribute(QtCore.QString("direction"),
                           QtCore.QString("0")).startsWith(QtCore.QString("l")) else 'r'
            # M_LOG.info("l_dir: %c" % l_dir)

            l_hold = cesp.CHolding(f_element.attribute(QtCore.QString("waypoint"),
                                                       QtCore.QString("")).toLocal8Bit().data(), l_inb, l_dir)
            assert l_hold is not None

            self.__dct_esp.append(l_hold)

        # handle case of standard route
        elif (f_element.tagName() == QtCore.QString("departure")) or \
             (f_element.tagName() == QtCore.QString("arrival")) or \
             (f_element.tagName() == QtCore.QString("transition")):

            ls_rt = stdrt.CStandardRoute()
            assert ls_rt is not None

            ls_rt.s_indc = f_element.attribute(QtCore.QString("name"), QtCore.QString("")).toLocal8Bit().data()

            l_nodeList = f_element.elementsByTagName(QtCore.QString("runway"))
            # M_LOG.info("l_nodeList.len (RWY): %d" % l_nodeList.length())

            for l_iI in xrange(l_nodeList.length()):
                l_e = l_nodeList.at(l_iI).toElement()

                if l_e.isNull():
                    continue

                ls_rt.addRunway(l_e.text().toLocal8Bit().data())

            l_nodeList = f_element.elementsByTagName(QtCore.QString("waypoint"))
            # M_LOG.info("l_nodeList.len (WPT): %d" % l_nodeList.length())

            for l_iI in xrange(l_nodeList.length()):
                l_e = l_nodeList.at(l_iI).toElement()

                if l_e.isNull():
                    continue

                l_fpItem = cfpi.CFlightPlanItem()
                assert l_fpItem is not None

                l_fpItem.s_indc = l_e.text().toLocal8Bit().data()
                # M_LOG.info("l_fpItem.s_indc: %s" % l_fpItem.s_indc)

                l_fpItem._iSpeedConstraint, lv_ok = l_e.attribute(
                    QtCore.QString("speed"), QtCore.QString("0")).toInt()

                # parse the altitude constraint
                altc = l_e.attribute(QtCore.QString("altitude"), QtCore.QString("0"))

                if altc.endsWith(QtCore.QChar('B')):
                    altc = altc.mid(0, altc.length() - 1)

                    l_fpItem._iAltConstraint, lv_ok = altc.toInt()
                    l_fpItem._iAltConstraintType = cfpi.CFlightPlanItem._OR_BELOW

                elif altc.endsWith(QtCore.QChar('A')):
                    altc = altc.mid(0, altc.length() - 1)

                    l_fpItem._iAltConstraint, lv_ok = altc.toInt()
                    l_fpItem._iAltConstraintType = cfpi.CFlightPlanItem._OR_ABOVE

                else:
                    l_fpItem._iAltConstraint, lv_ok = altc.toInt()
                    l_fpItem._iAltConstraintType = cfpi.CFlightPlanItem._EXACTLY

                l_fpItem._vFlyOver = l_e.hasAttribute("flyover")

                ls_rt.addItem(l_fpItem)

            if f_element.tagName() == QtCore.QString("departure"):
                self.___dep.append(ls_rt)

            if f_element.tagName() == QtCore.QString("arrival"):
                self.__dct_pso.append(ls_rt)

            if f_element.tagName() == QtCore.QString("transition"):
                self.__dct_transitions.append(ls_rt)

        # logger
        # M_LOG.info("__parse_dom_element:<<")

    # ---------------------------------------------------------------------------------------------

    def route(self, fs_indc):
        """
        return a pointer to the standard route with specified name
        """
        # logger
        # M_LOG.info("route:>>")

        # verifica parâmetros de entrada
        # assert f_model

        for l_iI in xrange(len(self.__dct_pso)):
            if self.arrival(l_iI).s_indc == fs_indc:

                # logger
                # M_LOG.info("<E01")

                return self.arrival(l_iI)

        for l_iI in xrange(len(self.___dep)):
            if self.departure(l_iI).s_indc == fs_indc:

                # logger
                # M_LOG.info("<E02")

                return self.departure(l_iI)

        for l_iI in xrange(len(self.__dct_transitions)):
            if self.transition(l_iI).s_indc == fs_indc:

                # logger
                # M_LOG.info("<E03")

                return self.transition(l_iI)

        # logger
        # M_LOG.info("route:<<")

        # return
        return None

    # ---------------------------------------------------------------------------------------------

    def runway(self, f_val):
        """
        return a pointer to the runway with specified index
        """
        # logger
        # M_LOG.info("runway:><")

        # verifica parâmetros de entrada
        # assert f_model

        if isinstance(f_val, int):
            return self.__runway_by_no(f_val)

        elif isinstance(f_val, str):
            return self.__runway_by_indc(f_val)

        # return
        return None

    # ---------------------------------------------------------------------------------------------

    def __runway_by_no(self, fi_ndx):
        """
        return a pointer to the runway with specified index
        """
        # logger
        # M_LOG.info("__runway_by_no:><")

        # verifica parâmetros de entrada
        # assert f_model

        if fi_ndx >= len(self.__dct_rwy):
            return None

        # return
        return self.__dct_rwy[fi_ndx]

    # ---------------------------------------------------------------------------------------------

    def __runway_by_indc(self, fs_indc):
        """
        return a pointer to the runway with specified indc
        """
        # logger
        # M_LOG.info("__runway_by_indc:>>")

        # verifica parâmetros de entrada
        # assert f_model

        li_ndx = 0

        while self.__runway_by_no(li_ndx):
            if self.__runway_by_no(li_ndx).s_indc == fs_indc:

                # logger
                # M_LOG.info("<E01")

                return self.__runway_by_no(li_ndx)

            li_ndx += 1

        # logger
        # M_LOG.info("__runway_by_indc:<<")

        # return
        return None

    # ---------------------------------------------------------------------------------------------

    def transition(self, fi_ndx):
        """
        return a pointer to the transition with specified index
        """
        # logger
        # M_LOG.info("transition:><")

        # verifica parâmetros de entrada
        # assert f_model

        if fi_ndx >= len(self.__dct_transitions):
            return None

        # return
        return self.__dct_transitions[fi_ndx]

    # ---------------------------------------------------------------------------------------------

    def vor(self, fi_ndx):
        """
        return a pointer to the VOR with specified index
        """
        # logger
        # M_LOG.info("vor:><")

        # verifica parâmetros de entrada
        # assert f_model

        if fi_ndx >= len(self.__dct_vor):
            return None

        # return
        return self.__dct_vor[fi_ndx]

    # ---------------------------------------------------------------------------------------------

    def waypoint(self, fi_ndx):
        """
        return a pointer to the waypoint with specified index
        """
        # logger
        # M_LOG.info("waypoint:><")

        # verifica parâmetros de entrada
        # assert f_model

        if fi_ndx >= len(self.__dct_wpt):
            return None

        # return
        return self.__dct_wpt[fi_ndx]

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def airport(self):
        """
        pointer to the aerodrome reference point
        """
        return self.__arp

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_elevation(self):
        """
        get aerodrome elevation
        """
        return self.__f_elevation
                                            
    # @f_elevation.setter
    # def f_elevation(self, f_val):
        # """
        # set aerodrome elevation
        # """
        # self.__f_elevation = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_sub(self):
        """
        get subidas
        """
        return self.__dct_sub

    @dct_sub.setter
    def dct_sub(self, f_val):
        """
        set subidas
        """
        self.__dct_sub = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def dct_trj(self):
        """
        get trajetórias
        """
        return self.__dct_trj

    @dct_trj.setter
    def dct_trj(self, f_val):
        """
        set trajetórias
        """
        self.__dct_trj = f_val

    # ---------------------------------------------------------------------------------------------
    
    @property
    def f_variation(self):
        """
        get magnetic variation
        """
        return self.__f_variation
                                            
    # @f_variation.setter
    # def f_variation(self, f_val):
        # """
        # set magnetic variation
        # """
        # self.__f_variation = f_val

# < the end >--------------------------------------------------------------------------------------
