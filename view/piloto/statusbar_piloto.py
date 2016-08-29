#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
statusbar_piloto.

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
# import logging

# pyQt library
from PyQt4 import Qt, QtCore, QtGui

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CStatusBarPiloto >-----------------------------------------------------------------------

class CStatusBarPiloto(QtGui.QStatusBar):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_parent=None):
        """
        constructor.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_parent

        # init super class
        super(CStatusBarPiloto, self).__init__(f_parent)

        # salva a QMainWindow localmente
        self._parent = f_parent

        # local variables
        self.__lbl_exe = None
        self.__lbl_hora = None
        self.__lbl_msg = None

        # config status bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # create permanent widgets
        self.__create_statusbar_labels()

        # add widgets in status bar
        self.addWidget(self.__lbl_msg)

        # add permanent widgets in status bar
        self.addPermanentWidget(self.__lbl_exe)
        self.addPermanentWidget(self.__lbl_hora)

        # exibe a status bar
        self.show()

        # show temporary message (5s)
        self.showMessage(self.tr("Ready..."), 5000)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __create_statusbar_labels(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("__create_statusbar_labels:>>")

        # mensagem
        self.__lbl_msg = QtGui.QLabel()
        assert self.__lbl_msg

        self.__lbl_msg.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.__lbl_msg.setMinimumSize(self.__lbl_msg.sizeHint())

        # exercício
        self.__lbl_exe = QtGui.QLabel("XXXX9999")
        assert self.__lbl_exe

        self.__lbl_exe.setAlignment(QtCore.Qt.AlignHCenter)
        self.__lbl_exe.setMinimumSize(self.__lbl_exe.sizeHint())
        self.__lbl_exe.setAutoFillBackground(True)

        l_pal = self.__lbl_exe.palette()
        l_pal.setColor(QtGui.QPalette.Window, QtGui.QColor(150, 255, 255))

        self.__lbl_exe.setPalette(l_pal)

        # horário
        self.__lbl_hora = QtGui.QLabel("00:00:00")
        assert self.__lbl_hora

        self.__lbl_hora.setAlignment(QtCore.Qt.AlignHCenter)
        self.__lbl_hora.setMinimumSize(self.__lbl_hora.sizeHint())
        self.__lbl_hora.setAutoFillBackground(True)

        l_pal = self.__lbl_hora.palette()
        l_pal.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 150))

        self.__lbl_hora.setPalette(l_pal)

        # logger
        # M_LOG.info("__create_statusbar_labels:<<")

    # ---------------------------------------------------------------------------------------------

    def update_exe(self, fs_exe, fv_update=True):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("update_exe:>>")

        # flag update ?
        if fv_update:

            # independant mode ?
            self.__lbl_exe.setText(fs_exe)

            # update status bar
            self.update()

        # logger
        # M_LOG.info("update_exe:<<")

    # ---------------------------------------------------------------------------------------------

    def update_hora(self, fs_hora, fv_update=True):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("update_hora:>>")

        # set hora label
        self.__lbl_hora.setText(fs_hora)

        # flag update ?
        if fv_update:

            # update status bar
            self.update()

        # logger
        # M_LOG.info("update_hora:<<")

    # ---------------------------------------------------------------------------------------------

    def update_msg(self, fs_msg, fv_update=True):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("update_msg:>>")

        # flag update ?
        if fv_update:

            # set message label
            self.__lbl_msg.setText(fs_msg)

            # update status bar
            self.update()

        # logger
        # M_LOG.info("update_msg:<<")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def lbl_exe(self):
        """
        get exercício
        """
        return self.__lbl_exe

    @lbl_exe.setter
    def lbl_exe(self, f_val):
        """
        set exercício
        """
        self.__lbl_exe = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def lbl_hora(self):
        """
        get hora
        """
        return self.__lbl_hora

    @lbl_hora.setter
    def lbl_hora(self, f_val):
        """
        set hora
        """
        self.__lbl_hora = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def lbl_msg(self):
        """
        get message
        """
        return self.__lbl_msg

    @lbl_msg.setter
    def lbl_msg(self, f_val):
        """
        set message
        """
        self.__lbl_msg = f_val

# < the end >--------------------------------------------------------------------------------------
