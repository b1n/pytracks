# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
event_manager.

coordinates communications between the model, views and controllers through the use of events.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging

# < module data >----------------------------------------------------------------------------------

# logging level
# M_LOG_LVL = logging.DEBUG

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(M_LOG_LVL)

# < class CEventsManager >-------------------------------------------------------------------------


class CEventsManager(object):
    """
    coordinates communications between the model, views and controllers through the use of events.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self):

        # logger
        # M_LOG.info("__init__:>>")

        # weakref
        from weakref import WeakKeyDictionary

        # listeners dictionary
        self.__dct_listeners = WeakKeyDictionary()
        assert self.__dct_listeners is not None

        # event queue
        self.__lst_event_queue = []

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def post(self, f_event):
        """
        difundir um evento a todos os membros da lista de recebedores.

        @param f_event: evento a disseminar.
        """
        # logger
        # M_LOG.info("post:>>")

        # para todos os listeners cadastrados...
        for l_listener in self.__dct_listeners:

            # ...envio a notificação do evento
            l_listener.notify(f_event)

        # logger
        # M_LOG.info("post:<<")

    # ---------------------------------------------------------------------------------------------

    def register_listener(self, f_listener):
        """
        register the object as listener.

        @param f_listener: objeto a registrar.
        """
        # logger
        # M_LOG.info("register_listener:>>")

        # coloca o objeto na lista de recebedores de eventos
        self.__dct_listeners[f_listener] = True

        # logger
        # M_LOG.info("register_listener:<<")

    # ---------------------------------------------------------------------------------------------

    def unregister_listener(self, f_listener):
        """
        unregister the object as listener.

        @param f_listener: objeto a remover.
        """
        # logger
        # M_LOG.info("unregister_listener:>>")

        # o objeto está na lista de recebedores de eventos ?
        if f_listener in self.__dct_listeners:

            # retira o objeto na lista de recebedores de eventos
            del self.__dct_listeners[f_listener]

        # logger
        # M_LOG.info("unregister_listener:<<")

# < the end >--------------------------------------------------------------------------------------
