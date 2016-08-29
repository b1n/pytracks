#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_newton

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
import threading
import time

import SocketServer

# model
import model.glb_data as gdata

# view
import view.visweb.view_handler as vhnd

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CViewNewton >----------------------------------------------------------------------------

class CViewNewton(threading.Thread):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_control):
        """
        init newton view manager

        @param f_model: model manager
        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_model
        assert f_control
                
        # init super class
        super(CViewNewton, self).__init__()

        # save model manager
        self.__model = f_model

        # save control manager
        self.__control = f_control

        # obtém o MPI rank
        self.__mpi_rank = f_control.mpi_rank
        assert self.__mpi_rank > -1
                                                
        # obtém o dicionário de configuração
        ldct_config = f_control.config.dct_config
        assert ldct_config is not None

        # configura a porta do servidor
        self.__i_port = int(ldct_config["srv.port"]) + self.__mpi_rank

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def run(self):
        """
        thread that runs the web server
        """
        # logger
        # M_LOG.info("run:>>")

        # wait loop
        while not gdata.G_KEEP_RUN:

            # wait...
            time.sleep(1)

        try:
            # allow address reuse (avoid '[Errno 98] Address already in use')
            SocketServer.TCPServer.allow_reuse_address = True
            
            # create a web server and define the handler to manage the incoming request
            l_server = CViewServer(self.__model, self.__control, ('', self.__i_port), vhnd.CViewHandler)
            assert l_server

            # logger
            l_log = logging.getLogger("CViewNewton::run")
            l_log.setLevel(logging.INFO)
            l_log.info(u"E01: started http server on port {}.".format(self.__i_port))

            # wait forever for incoming http requests
            l_server.serve_forever()

        # em caso de erro...
        except KeyboardInterrupt:

            # logger
            l_log = logging.getLogger("CViewNewton::run")
            l_log.setLevel(logging.WARNING)
            l_log.warning(u"E02: ^C received, shutting down the web server.")

            # close socket
            l_server.socket.close()

        # server loop
        while gdata.G_KEEP_RUN:

            # give a break...
            time.sleep(.5)

        # logger
        # M_LOG.info("run:<<")

# < class CViewServer >----------------------------------------------------------------------------

class CViewServer(SocketServer.TCPServer):
    
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_control, f_server_address, f_handler_class=vhnd.CViewHandler):
        """
        init newton web server

        @param f_control: control manager.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_model
        assert f_control
                
        # init super class
        SocketServer.TCPServer.__init__(self, f_server_address, f_handler_class)

        # save control manager
        self.__control = f_control

        # save model manager
        self.__model = f_model

        # lista de pousos/decolagens
        self.__lst_arr_dep = f_model.lst_arr_dep
        assert self.__lst_arr_dep is not None                

        # dicionário de esperas
        self.__dct_esp = f_model.dct_esp
        assert self.__dct_esp is not None                

        # dicionário de fixos
        self.__dct_fix = f_model.dct_fix
        assert self.__dct_fix is not None                

        # dicionário de performances
        self.__dct_prf = f_model.dct_prf
        assert self.__dct_prf is not None                

        # dicionário de subidas
        self.__dct_sub = f_model.dct_sub
        assert self.__dct_sub is not None                

        # dicionário de trajetórias
        self.__dct_trj = f_model.dct_trj
        assert self.__dct_trj is not None                

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    
    @property
    def control(self):
        """
        get control manager
        """
        return self.__control 
                                            
    # ---------------------------------------------------------------------------------------------
    
    @property
    def coords(self):
        """
        get coord system
        """
        return self.__model.coords
                                            
    # ---------------------------------------------------------------------------------------------
    
    @property
    def model(self):
        """
        get model manager
        """
        return self.__model 
                                            
    # ---------------------------------------------------------------------------------------------
    
    @property
    def lst_arr_dep(self):
        """
        get lista de pousos/decolagens
        """
        return self.__lst_arr_dep 
                                            
    # ---------------------------------------------------------------------------------------------
    
    @property
    def dct_esp(self):
        """
        get dicionário de esperas
        """
        return self.__dct_esp 
                                            
    # ---------------------------------------------------------------------------------------------
    
    @property
    def dct_fix(self):
        """
        get dicionário de fixos
        """
        return self.__dct_fix 
                                            
    # ---------------------------------------------------------------------------------------------
    
    @property
    def dct_flight(self):
        """
        get dicionário de flight engines
        """
        return self.__model.emula_model.dct_flight 
                                            
    # ---------------------------------------------------------------------------------------------
    
    @property
    def dct_prf(self):
        """
        get dicionário de performances
        """
        return self.__dct_prf 
                                            
    # ---------------------------------------------------------------------------------------------
    
    @property
    def dct_sub(self):
        """
        get dicionário de subidas
        """
        return self.__dct_sub 
                                            
    # ---------------------------------------------------------------------------------------------
    
    @property
    def dct_trj(self):
        """
        get dicionário de trajetórias
        """
        return self.__dct_trj 
                                            
# < the end >--------------------------------------------------------------------------------------
