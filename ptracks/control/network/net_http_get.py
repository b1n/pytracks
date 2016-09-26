#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
net_http_get.

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
import logging
import urllib2

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CNetHttpGet >----------------------------------------------------------------------------

class CNetHttpGet(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_event, f_config):
        """
        initializes the network http sender.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # check input parameters
        assert f_event
        assert f_config

        # inicializa a super class
        super(CNetHttpGet, self).__init__()

        # salva o event manager localmente
        # self.__event = f_event
                
        # salva o config manager localmente
        # self.__config = f_config
                
        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def get_data(self, fs_srv, fs_msg):
        """
        @param fs_srv: DOCUMENT ME!
        @param fs_msg: DOCUMENT ME!
        """
        # logger
        # M_LOG.info("get_data:>>")

        # check requirements
        # assert

        try:
            M_LOG.debug("request: http://{}/{}".format(fs_srv, fs_msg))

            # envia o request
            l_resp = urllib2.urlopen("http://{}/{}".format(fs_srv, fs_msg))

        except Exception as ls_err:

            # logger
            l_log = logging.getLogger("CNetHttpGet::get_data")
            l_log.setLevel(logging.NOTSET)
            l_log.warning("<E01: server {} reports {} for request {}".format(fs_srv, ls_err, fs_msg))
                                                
            # return
            return None

        # logger
        # M_LOG.info("get_data:<<")

        # return data
        return l_resp.read()

# < the end >--------------------------------------------------------------------------------------
