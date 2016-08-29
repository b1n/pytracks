#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
strip_table_model.

provide all the interface to store the strip

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2015/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# this is only needed for Python v2 but is harmless for Python v3.
# import sip
# sip.setapi("QString", 2)
# sip.setapi("QVariant", 1)

# PyQt library
#from PyQt4 import QtGui
from PyQt4 import QtCore

# model
import model.coords.coord_conv as cconv
import model.coords.coord_defs as cdefs

#import model.glb_data as gdata
import model.piloto.defs_piloto as ldefs
import model.piloto.aircraft_piloto as anvmdl

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CStripTableModel >-----------------------------------------------------------------------

class CStripTableModel(QtCore.QAbstractTableModel):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__init__:>>")

        # init super class
        super(CStripTableModel, self).__init__()

        # local attributes
        self.__v_dirty = False
        self.__lst_strips = []

        # make signal connections
        # self.dataChanged.connect(self.__data_changed)
        # self.rowsRemoved.connect(self.__rows_removed)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # int columnCount (self, QModelIndex parent = QModelIndex())

    def columnCount(self, f_parent=QtCore.QModelIndex()):
        """
        @return the number of columns for the children of the given parent.
        """
        # logger
        # M_LOG.info("columnCount:><")

        # return
        return 12

    # ---------------------------------------------------------------------------------------------
    # QVariant data (self, QModelIndex index, int role = Qt.DisplayRole)

    def data(self, f_index, f_role=QtCore.Qt.DisplayRole):
        """
        @return the data stored under the given role for the strip referred to by the index.
        """
        # logger
        # M_LOG.info("data:>>")

        # index or row invalid ?
        if not f_index.isValid() or not (0 <= f_index.row() < len(self.__lst_strips)):
            return QtCore.QVariant()

        # get strip
        l_anv = self.__lst_strips[f_index.row()]

        # get attribute (column)
        l_column = f_index.column()

        # display role ?
        if f_role == QtCore.Qt.DisplayRole:

            # icao id ?
            if l_column == ldefs.D_STP_ID:
                return QtCore.QVariant(l_anv.s_icao_addr)

            # indicativo ?
            elif l_column == ldefs.D_STP_IND:
                return QtCore.QVariant(l_anv.s_callsign)

            # código transponder ?
            elif l_column == ldefs.D_STP_SSR:
                return QtCore.QVariant(l_anv.i_ssr)

            # performance ?
            elif l_column == ldefs.D_STP_PRF:
                return QtCore.QVariant(l_anv.s_prf)

            # latitude ?
            elif l_column == ldefs.D_STP_LAT:
                return QtCore.QVariant(cconv.format_ica_lat(l_anv.f_lat))

            # longitude ?
            elif l_column == ldefs.D_STP_LNG:
                return QtCore.QVariant(cconv.format_ica_lng(l_anv.f_lng))

            # altitude ?
            elif l_column == ldefs.D_STP_ALT:
                return QtCore.QVariant(int(l_anv.f_alt))

            # proa ?
            elif l_column == ldefs.D_STP_PROA:
                return QtCore.QVariant(int(l_anv.f_proa))

            # velocidade ?
            elif l_column == ldefs.D_STP_VEL:
                return QtCore.QVariant(int(l_anv.f_vel))

            # razão descida/subida ?
            elif l_column == ldefs.D_STP_RAZ:
                return QtCore.QVariant(round(l_anv.f_raz, 1))

            # hora ?
            elif l_column == ldefs.D_STP_HORA:
                return QtCore.QVariant(round(l_anv.i_hora))

        # text alignment role ?
        elif f_role == QtCore.Qt.TextAlignmentRole:

            # indicativo ?
            if l_column == ldefs.D_STP_IND:
                return QtCore.QVariant(int(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter))

            # performance ?
            elif l_column == ldefs.D_STP_PRF:
                return QtCore.QVariant(int(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter))

            return QtCore.QVariant(int(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter))
        ''' 
        # text color role e código transponder ?
        #elif (f_role == QtCore.Qt.TextColorRole) and (l_column == ldefs.D_STP_SSR):

            #if l_anv.i_ssr < 8:
                #return QtCore.QVariant(QtGui.QColor(QtCore.Qt.black))

            #elif l_anv.i_ssr < 16:
                #return QtCore.QVariant(QtGui.QColor(QtCore.Qt.darkBlue))

            #elif l_anv.i_ssr < 24:
                #return QtCore.QVariant(QtGui.QColor(QtCore.Qt.yellow))

            #else:
                #return QtCore.QVariant(QtGui.QColor(QtCore.Qt.red))

        # background color role ?
        # elif f_role == QtCore.Qt.BackgroundColorRole:

            # retorna a cor da linha
            # return QtCore.QVariant(l_anv.color)

        # tooltip role ?
        elif f_role == QtCore.Qt.ToolTipRole:

            l_msg = "<br>(minimum of 3 characters)"

            # icao id ?
            if l_column == ldefs.D_STP_ID:
                return QtCore.QVariant(l_anv.s_icao_addr + l_msg)

            # indicativo ?
            elif l_column == ldefs.D_STP_IND:
                return QtCore.QVariant(l_anv.s_callsign + l_msg)

            # código transponder ?
            elif l_column == ldefs.D_STP_SSR:
                return QtCore.QVariant(str(l_anv.i_ssr) +l_msg)

            # performance ?
            elif l_column == ldefs.D_STP_PRF:
                return QtCore.QVariant(str(l_anv.s_prf) + l_msg)

            # latitude ?
            elif l_column == ldefs.D_STP_LAT:
                return QtCore.QVariant(l_anv.f_lat + l_msg)

            # longitude ?
            elif l_column == ldefs.D_STP_LNG:
                return QtCore.QVariant(str(l_anv.f_lng) + l_msg)
        '''
        # logger
        # M_LOG.info("data:<<")

        # return
        return QtCore.QVariant()

    # ---------------------------------------------------------------------------------------------
    '''
    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    def __data_changed(self, f_index_tl, f_index_br):
        """
        signal emitted whenever the data in an existing item changes.  If the items are of the
        same parent, the affected ones are those between topLeft and bottomRight inclusive. If
        the items do not have the same parent, the behavior is undefined.

        @param f_index_tl: topLeft index
        @param f_index_br: bottomRight index
        """
        # logger
        M_LOG.info("__data_changed:>>")

        M_LOG.debug("__data_changed:f_index_tl: " + str(f_index_tl))
        M_LOG.debug("__data_changed:f_index_br: " + str(f_index_br))

        # logger
        M_LOG.info("__data_changed:<<")
    '''
    # ---------------------------------------------------------------------------------------------
    # Qt.ItemFlags flags (self, QModelIndex index)
    '''
    def flags(self, f_index):
        """
        @return the strip flags for the given index.
        """
        # logger
        # M_LOG.info("flags:>>")

        if not f_index.isValid():
            return QtCore.Qt.ItemIsEnabled

        # logger
        # M_LOG.info("flags:<<")

        # return
        return QtCore.Qt.ItemFlags(QtCore.QAbstractTableModel.flags(self, f_index)|QtCore.Qt.ItemIsEditable)
    '''
    # ---------------------------------------------------------------------------------------------
    # QVariant headerData (self, int section, Qt.Orientation orientation, int role = Qt.DisplayRole)

    def headerData(self, f_section, f_orientation, f_role=QtCore.Qt.DisplayRole):
        """
        for horizontal headers, the section number corresponds to the column number. Similarly,
        for vertical headers, the section number corresponds to the row number.

        @return the data for the given role and section in the header with the specified orientation.
        """
        # logger
        # M_LOG.info("headerData:>>")

        # text alignment role ?
        if f_role == QtCore.Qt.TextAlignmentRole:
            # horizontal ?
            if f_orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant(int(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter))

            return QtCore.QVariant(int(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter))

        # not display role ?
        if f_role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        # horizontal ?
        if f_orientation == QtCore.Qt.Horizontal:

            # icao id ?
            if f_section == ldefs.D_STP_ID:
                return QtCore.QVariant(u"ICAO ID")

            # indicativo ?
            elif f_section == ldefs.D_STP_IND:
                return QtCore.QVariant("Callsign")

            # código transponder ?
            elif f_section == ldefs.D_STP_SSR:
                return QtCore.QVariant("SSR")

            # performance ?
            elif f_section == ldefs.D_STP_PRF:
                return QtCore.QVariant("Prf")

            # latitude ?
            elif f_section == ldefs.D_STP_LAT:
                return QtCore.QVariant("Latitude")

            # longitude ?
            elif f_section == ldefs.D_STP_LNG:
                return QtCore.QVariant("Longitude")

            # altitude ?
            elif f_section == ldefs.D_STP_ALT:
                return QtCore.QVariant("Altitude")

            # proa ?
            elif f_section == ldefs.D_STP_PROA:
                return QtCore.QVariant("Proa")

            # velocidade ?
            elif f_section == ldefs.D_STP_VEL:
                return QtCore.QVariant("Veloc.")

            # razão descida/subida ?
            elif f_section == ldefs.D_STP_RAZ:
                return QtCore.QVariant(u"Razão")

            # hora ?
            elif f_section == ldefs.D_STP_HORA:
                return QtCore.QVariant("Age")

        # logger
        # M_LOG.info("headerData:<<")

        # return
        return QtCore.QVariant(int(f_section + 1))

    # ---------------------------------------------------------------------------------------------
    # bool insertRows (self, int row, int count, QModelIndex parent = QModelIndex())
    '''
    def insertRows(self, f_row, f_count=1, f_parent=QtCore.QModelIndex()):
        """
        inserts count rows into the model before the given row.  Items in the new row will be
        children of the strip represented by the parent model index.

        if row is 0, the rows are prepended to any existing rows in the parent.
        if row is rowCount(), the rows are appended to any existing rows in the parent.
        if parent has no children, a single column with count rows is inserted.

        @return true if the rows were successfully inserted; otherwise returns false.
        """
        # logger
        # M_LOG.info("insertRows:>>")

        # begins a row insertion operation
        self.beginInsertRows(QtCore.QModelIndex(), f_row, f_row + f_count - 1)

        # for count rows...
        for l_row in xrange(f_count):

            # rows are prepended to any existing rows
            self.__lst_strips.insert(f_row + l_row, anvmdl.CAircraftPiloto({}))

            # posiciona o strip !!!REVER!!!
            self.__lst_strips[f_row + l_row].point = QtCore.QPointF(gdata.G_CTR_LAT, gdata.G_CTR_LNG)

        # ends a row insertion operation
        self.endInsertRows()

        # avisa que existem modificações
        self.__v_dirty = True

        # logger
        # M_LOG.info("insertRows:<<")

        # return
        return True
    '''
    # ---------------------------------------------------------------------------------------------
    # bool removeRows (self, int row, int count, QModelIndex parent = QModelIndex())
    '''
    def removeRows(self, f_row, f_count=1, f_parent=QtCore.QModelIndex()):
        """
        removes count rows starting with the given row under parent parent from the model.

        @return true if the rows were successfully removed; otherwise returns false.
        """
        # logger
        # M_LOG.info("removeRows:>>")

        # begins a row removal operation
        self.beginRemoveRows(QtCore.QModelIndex(), f_row, f_row + f_count - 1)

        # rebuild strips list
        self.__lst_strips = (self.__lst_strips[:f_row] + self.__lst_strips[f_row + f_count:])

        # ends a row removal operation
        self.endRemoveRows()

        # marca que existem modificações
        self.__v_dirty = True

        # logger
        # M_LOG.info("removeRows:<<")

        # return
        return True
    '''
    # ---------------------------------------------------------------------------------------------
    # int rowCount (self, QModelIndex parent = QModelIndex())

    def rowCount(self, f_parent=QtCore.QModelIndex()):
        """
        returns the number of rows under the given parent.
        """
        # logger
        # M_LOG.info("rowCount:><")

        # return
        return len(self.__lst_strips)

    # ---------------------------------------------------------------------------------------------
    '''
    @QtCore.pyqtSlot(QtCore.QModelIndex, int, int)
    def __rows_removed(self, f_parent, fi_start=0, fi_end=0):
        """
        signal emitted after rows have been removed from the model.  The removed items are those
        between start and end inclusive, under the given parent item.

        @param f_parent: DOC!
        @param f_start: DOC!
        @param f_end: DOC!
        """
        # logger
        # M_LOG.info("__rows_removed:>>")

        # M_LOG.debug("__rows_removed:f_parent: " + str(f_parent))
        # M_LOG.debug("__rows_removed:fi_start: " + str(fi_start))
        # M_LOG.debug("__rows_removed:fi_end..: " + str(fi_end))

        if not f_parent.isValid():
            return

        # logger
        # M_LOG.info("__rows_removed:<<")
    '''
    # ---------------------------------------------------------------------------------------------
    # bool setData (self, QModelIndex index, QVariant value, int role = Qt.EditRole)
    '''
    def setData(self, f_index, f_value, f_role=QtCore.Qt.EditRole):
        """
        sets the role data for the strip at index to value.

        @return true if successful; otherwise returns false.
        """
        # logger
        # M_LOG.info("setData:>>")
        # M_LOG.debug("f_value:" + str(f_value))

        if f_index.isValid() and (0 <= f_index.row() < len(self.__lst_strips)):

            # get anv/strip
            l_anv = self.__lst_strips[f_index.row()]

            # get attribute (column)
            l_column = f_index.column()

            # icao id ?
            if l_column == ldefs.D_STP_ID:
                l_anv.s_icao_addr = f_value.toString()

            # indicativo ?
            elif l_column == ldefs.D_STP_IND:
                l_anv.s_callsign = f_value.toString()

            # código transponder ?
            elif l_column == ldefs.D_STP_SSR:
                f_value, lv_ok = f_value.toInt()

                if lv_ok:
                    l_anv.i_ssr = f_value

            # performance ?
            elif l_column == ldefs.D_STP_PRF:
                l_anv.s_prf = f_value.toString()

            # latitude ?
            elif l_column == ldefs.D_STP_LAT:
                f_value, lv_ok = f_value.toFloat()

                if lv_ok:
                    l_anv.f_lat = f_value

            # longitude ?
            elif l_column == ldefs.D_STP_LNG:
                f_value, lv_ok = f_value.toFloat()

                if lv_ok:
                    l_anv.f_lng = f_value

            # altitude ?
            elif l_column == ldefs.D_STP_ALT:
                f_value, lv_ok = f_value.toFloat()

                if lv_ok:
                    l_anv.f_alt = f_value

            # proa ?
            elif l_column == ldefs.D_STP_PROA:
                f_value, lv_ok = f_value.toFloat()

                if lv_ok:
                    l_anv.f_proa = f_value

            # velocidade ?
            elif l_column == ldefs.D_STP_VEL:
                f_value, lv_ok = f_value.toFloat()

                if lv_ok:
                    l_anv.f_vel = f_value

            # razão descida/subida ?
            elif l_column == ldefs.D_STP_RAZ:
                f_value, lv_ok = f_value.toFloat()

                if lv_ok:
                    l_anv.f_raz = f_value

            # hora ?
            elif l_column == ldefs.D_STP_HORA:
                f_value, lv_ok = f_value.toInt()
                
                if lv_ok:
                    l_anv.i_hora = f_value

            # marca que existem modificações
            self.__v_dirty = True

            # emit data changed signal
            # self.emit(QtCore.SIGNAL("dataChanged(QModelIndex,QModelIndex)"), f_index, f_index)
            self.dataChanged.emit(f_index, f_index)

            # return
            return True

        # logger
        # M_LOG.info("setData:<<")

        # return
        return False
    '''
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def v_dirty(self):
        """
        get dirty
        """
        return self.__v_dirty

    @v_dirty.setter
    def v_dirty(self, f_val):
        """
        set dirty
        """
        self.__v_dirty = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def lst_strips(self):
        """
        get strips
        """
        return self.__lst_strips

    @lst_strips.setter
    def lst_strips(self, f_val):
        """
        set strips
        """
        self.__lst_strips = f_val

# < the end >--------------------------------------------------------------------------------------
