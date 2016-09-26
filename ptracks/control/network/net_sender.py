#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
net_sender.

DOCUMENT ME!

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
desmembramento do NetManager.
inclusão do config_manager e event_manager.

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging
import multiprocessing
import socket

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CNetSender >-----------------------------------------------------------------------------

class CNetSender(multiprocessing.Process):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, ft_ifce, fs_addr, fi_port, f_queue):
        """
        initializes network sender

        @param ft_ifce: tupla in/out de interfaces. ('eth0', 'eth0')
        @param fs_addr: endereço. ('255.12.2')
        @param fi_port: porta (1970)
        @param f_queue: queue de mensagens
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input parameters
        assert fs_addr
        assert fi_port
        assert f_queue

        # inicializa a super class
        super(CNetSender, self).__init__()

        # salva o event manager localmente
        self.__queue = f_queue
                
        # salva tupla endereço e porta
        self.__t_addr = (fs_addr, fi_port)

        # cria o socket de envio
        self.__fd_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        assert self.__fd_send

        # especificou uma interface ?
        if ft_ifce[1] is not None:
            # seleciona a interface (from socket.h, SO_BINDTODEVICE 25)
            self.__fd_send.setsockopt(socket.SOL_SOCKET, 25, ft_ifce[1])

        # config sender socket
        self.__fd_send.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def send_data(self, fs_msg):
        """
        @param fs_msg: DOCUMENT ME!
        """
        # logger
        # M_LOG.info("send_data:>>")

        # check requirements
        assert self.__fd_send

        # envia a mensagem
        self.__fd_send.sendto(fs_msg, self.__t_addr)
        # M_LOG.debug("dados [{}] enviados para [{}]".format(fs_msg, self.__t_addr))

        # logger
        # M_LOG.info("send_data:<<")

# < the end >--------------------------------------------------------------------------------------
