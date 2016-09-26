#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
generate_status_json

DOCUMENT ME!

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2016/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import json
import logging
import time

# model
from ...model.newton import defs_newton as ldefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# ------------------------------------------------------------------------------------------------

def generate_status_json(fdct_flight, fs_callsign):
    """
    DOCUMENT ME!

    @param fdct_flight: dicionário de flight engines
    @param fs_callsign: aircraft callsign
    """
    # logger
    # M_LOG.info("generate_status_json:>>")

    # check input parameters
    assert fdct_flight is not None
    assert fs_callsign

    # M_LOG.debug(u"generate_status_json::fs_callsign:[{}]".format(fs_callsign))

    # aeronave existe no dicionário ?
    l_atv = fdct_flight.get(fs_callsign, None)

    if l_atv is None:

        # logger
        l_log = logging.getLogger("generate_status_json")
        l_log.setLevel(logging.ERROR)
        l_log.error(u"<E01: aeronave {} não existe no dicionário.".format(fs_callsign))
                                                
        # return
        return None

    # M_LOG.debug(u"generate_status_json:en_trf_fnc_ope:[{}]".format(ldefs.DCT_FNC_OPE[l_atv.en_trf_fnc_ope]))

    # está em procedimento ?
    if l_atv.ptr_trf_prc is not None:

        # pouso/decolagem ?
        if l_atv.en_trf_fnc_ope in [ldefs.E_DECOLAGEM, ldefs.E_POUSO]:

            # identificação do pouso/decolagem
            ls_prc_id = "{}/{}".format(l_atv.ptr_atv_aer.s_aer_indc, l_atv.ptr_atv_pst.s_pst_indc)

        # direcionamento a fixo ?
        elif l_atv.en_trf_fnc_ope in [ldefs.E_DIRFIXO]:

            # identificação do fixo
            ls_prc_id = "{}/{}".format(l_atv.ptr_atv_fix_prc.i_fix_id, l_atv.ptr_atv_fix_prc.s_fix_indc)

        # senão,...
        else:
            # obtém o número do procedimento
            ls_prc_id = str(l_atv.ptr_trf_prc.i_prc_id)

    # senão,...
    else:
        # sem identificação
        ls_prc_id = ""
        
    # monta um dicionário com o status
    ldct_status = { "fnc_ope": ldefs.DCT_FNC_OPE[l_atv.en_trf_fnc_ope],
                    "prc_id": ls_prc_id,
                  }

    # converte para json
    ls_buf = json.dumps(ldct_status)
    # M_LOG.debug(u"generate_status_json:ls_buf:[{}]".format(ls_buf))

    # logger
    # M_LOG.info("generate_status_json:<<")

    # return
    return ls_buf

# < the end >--------------------------------------------------------------------------------------
