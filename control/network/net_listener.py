#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
net_listener.

DOCUMENT ME!

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
desmembramento do netManager.
inclusão do config_manager e event_manager.

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import multiprocessing
import socket
import struct
import time

# model
from ...model import glb_data as gdata
from ...model import glb_defs as gdefs

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = multiprocessing.get_logger()
M_LOG.setLevel(logging.DEBUG)

# < class CNetListener >---------------------------------------------------------------------------

class CNetListener(multiprocessing.Process):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, ft_ifce, fs_addr, fi_port, f_queue):
        """
        initializes network listener

        @param ft_ifce: tupla in/out de interfaces. ('eth0', 'eth0')
        @param fs_addr: endereço multicast. ('225.12.2')
        @param fi_port: porta. (1970)
        @param f_queue: queue de dados
        """
        # logger
        M_LOG.info("__init__:>>")

        # check input parameters
        assert fs_addr
        assert fi_port
        assert f_queue

        # init super class
        super(CNetListener, self).__init__()

        # salva a queue de dados localmente
        self.__q_queue = f_queue
                
        # cria o socket de recebimento
        self.__fd_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        assert self.__fd_recv

        # especificou uma interface ?
        if ft_ifce[0] is not None:
            # seleciona a interface (from socket.h, SO_BINDTODEVICE 25)
            self.__fd_recv.setsockopt(socket.SOL_SOCKET, 25, ft_ifce[0])

        # set some options to make it multicast-friendly
        self.__fd_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            # set some options to make it multicast-friendly
            self.__fd_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # em caso de erro...
        except AttributeError as ls_err:

            # logger
            l_log = multiprocessing.getLogger("CNetListener::__init__")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E01: some systems don't support SO_REUSEPORT:[{}]".format(ls_err))

        # set some options to make it multicast-friendly
        # self.__fd_recv.setsockopt ( socket.SOL_IP, socket.IP_MULTICAST_TTL, 20 )
        self.__fd_recv.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

        # bind udp port. Better use:
        self.__fd_recv.bind((fs_addr, fi_port))

        # instead of: self.__fd_recv.bind(('', fi_port))
        # ... because if you want to listen to multiple mcast groups on the same port, you'll get
        # all messages on all listeners

        # set mcast group
        l_mreq = struct.pack("4sl", socket.inet_aton(fs_addr), socket.INADDR_ANY)
        assert l_mreq

        # set some more multicast options
        self.__fd_recv.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, l_mreq)

        # logger
        M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def run(self):
        """
        drive application.
        """
        # logger
        M_LOG.info("run:>>")

        # check requirements
        assert self.__fd_recv

        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:

            # aguarda 1 seg
            time.sleep(1)

        # application loop
        while gdata.G_KEEP_RUN:

            M_LOG.debug("net_listener.run: wait recvfrom.")
            
            # aguarda receber uma mensagem (de até 512 bytes)
            l_data, l_addr = self.__fd_recv.recvfrom(512)
            M_LOG.debug("Msg [{}] recebida de [{}]: ".format(l_data, l_addr))

            # divide a mensagem em seus componentes
            llst_data = l_data.split(gdefs.D_MSG_SEP)
            M_LOG.debug("Msg [{}] em partes [{}]: ".format(l_data, llst_data))

            # versão da mensagem não reconhecida ?
            if gdefs.D_MSG_VRS != int(llst_data[0]):

                # próxima mensagem
                continue

            # mensagem válida ?
            if int(llst_data[1]) in gdefs.SET_MSG_VALIDAS:

                # coloca a mensagem na queue
                self.__q_queue.put(llst_data[1:])

            # senão, mensagem não reconhecida ou inválida
            else:
                # logger
                l_log = multiprocessing.getLogger("CNetListener::run")
                l_log.setLevel(logging.WARNING)
                l_log.warning("<E01: Unknow:[{}]".format(llst_data[2:]))

        # logger
        M_LOG.info("run:<<")

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    def get_data(self):
        """
        DOCUMENT ME!
        """
        # logger
        M_LOG.info("get_data:>>")

        # return list
        llst_data = []

        # fila tem dados ?
        if self.__q_queue:

            # obtém o primeiro item da fila
            llst_data = self.__q_queue.pop(0)
            M_LOG.debug("llst_data: " + str(llst_data))

        # logger
        M_LOG.info("get_data:<<")

        # retorna o dado recebido
        return llst_data

    # ---------------------------------------------------------------------------------------------

    @property
    def queue(self):
        """
        get queue
        """
        return self.__q_queue

# < the end >--------------------------------------------------------------------------------------
