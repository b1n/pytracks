#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
generate_anv_json.

DOCUMENT ME!

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
import time

# model
import model.coords.coord_defs as cdefs

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# message count
M_MSG = 0

# ------------------------------------------------------------------------------------------------

def generate_anv_json(fdct_flight, f_coords):
    """
    DOCUMENT ME!

    @param fdct_flight: dicionário de flight engines
    @param f_coords: coordinate system
    """
    # logger
    # M_LOG.info("generate_anv_json:>>")

    # globals
    global M_MSG

    # obtém a hora atual
    l_now = time.time()

    # monta a parte inicial do buffer
    ls_buf = "{{ \"now\" : {:.1f},\n" \
             "  \"messages\" : {:d},\n" \
             "  \"aircraft\" : [".format(l_now, M_MSG)
             # f_setup.stats_current.messages_total + f_setup.stats_alltime.messages_total)

    # flag primeira aeronave
    lv_first = True

    # first aircraft
    l_anv = None # f_setup.aircrafts

    for l_anv in fdct_flight.values():  # while l_anv is not None:

        # if l_anv.modeACflags & MODEAC_MSG_FLAG:
            # skip any fudged ICAO records Mode A/C
            # continue

        # if l_anv.messages < 2:
            # basic filter for bad decodes
            # continue

        # primeira aeronave ?
        if lv_first:

            # reset flag
            lv_first = False

        # senão, não é a primeira aeronave...
        else:
            # continua o buffer 
            ls_buf += ','

        # monta o endereço icao
        ls_buf += "\n    {{\"hex\":\"{}{:6x}\"".format("", l_anv.i_trf_id)  # , (l_anv.addr & MODES_NON_ICAO_ADDRESS) ? "~" : "", l_anv.addr & 0xFFFFFF);

        # if (l_anv.bFlags & MODES_ACFLAGS_SQUAWK_VALID)
        # monta o código transponder
        ls_buf += ",\"squawk\":\"{:04o}\"".format(int(l_anv.i_trf_ssr, 8))  # , l_anv.modeA);

        # if (l_anv.bFlags & MODES_ACFLAGS_CALLSIGN_VALID)
        # monta o callsign
        ls_buf += ",\"flight\":\"{}\"".format(l_anv.s_trf_ind)  # , jsonEscapeString(l_anv.flight));

        # converte para lat/long
        lf_lat, lf_lng, lf_alt = f_coords.xyz2geo(l_anv.f_trf_x, l_anv.f_trf_y, l_anv.f_trf_z)
        # # M_LOG.debug("coords:lat:[{}] / lng:[{}] / alt:[{}]".format(lf_lat, lf_lng, lf_alt))

        # if (l_anv.bFlags & MODES_ACFLAGS_LATLON_VALID) 23°06′03″S 45°42′25″W
        # monta a posição
        ls_buf += ",\"lat\":{},\"lon\":{}".format(lf_lat, lf_lng)

        # if (l_anv.bFlags & MODES_ACFLAGS_LATLON_VALID) 23°06′03″S 45°42′25″W
        ls_buf += ",\"nucp\":%u,\"seen_pos\":%.1f" % (15, 1.)  #, l_anv.pos_nuc, (l_now - l_anv.seenLatLon)/1000.0);

        # if ((l_anv.bFlags & MODES_ACFLAGS_AOG_VALID) && (l_anv.bFlags & MODES_ACFLAGS_AOG))
        # ls_buf += ",\"altitude\":\"ground\""  # );

        # else if (l_anv.bFlags & MODES_ACFLAGS_ALTITUDE_VALID)
        # monta a altitude
        ls_buf += ",\"altitude\":{}".format(int(l_anv.f_trf_alt_atu * cdefs.D_CNV_M2FT))  # , l_anv.altitude);

        # if (l_anv.bFlags & MODES_ACFLAGS_VERTRATE_VALID)
        # monta a razão de subida/descida
        ls_buf += ",\"vert_rate\":{}".format(l_anv.f_atv_raz_sub)  # , l_anv.vert_rate);

        # if (l_anv.bFlags & MODES_ACFLAGS_HEADING_VALID)
        # monta a proa
        ls_buf += ",\"track\":{}".format(int(l_anv.f_trf_pro_atu))  # , l_anv.track);

        # if (l_anv.bFlags & MODES_ACFLAGS_SPEED_VALID)
        # monta a velocidade
        ls_buf += ",\"speed\":{}".format(int(l_anv.f_trf_vel_atu * cdefs.D_CNV_MS2KT))  # , l_anv.speed);

        #if (l_anv.bFlags & MODES_ACFLAGS_CATEGORY_VALID)
        ls_buf += ",\"category\":\"{:2X}\"".format(17)  # , l_anv.category);

        # if l_anv.mlatFlags:

        #    ls_buf += snprintf(l_p, l_end-l_p, ",\"mlat\":[");

        #    if (l_anv.mlatFlags & MODES_ACFLAGS_SQUAWK_VALID)
        #        ls_buf += snprintf(l_p, l_end-l_p, "\"squawk\",");

        #    if (l_anv.mlatFlags & MODES_ACFLAGS_CALLSIGN_VALID)
        #        ls_buf += snprintf(l_p, l_end-l_p, "\"callsign\",");

        #    if (l_anv.mlatFlags & MODES_ACFLAGS_LATLON_VALID)
        #        ls_buf += snprintf(l_p, l_end-l_p, "\"lat\",\"lon\",");

        #    if (l_anv.mlatFlags & MODES_ACFLAGS_ALTITUDE_VALID)
        #        ls_buf += snprintf(l_p, l_end-l_p, "\"altitude\",");

        #    if (l_anv.mlatFlags & MODES_ACFLAGS_HEADING_VALID)
        #        ls_buf += snprintf(l_p, l_end-l_p, "\"track\",");

        #    if (l_anv.mlatFlags & MODES_ACFLAGS_SPEED_VALID)
        #        ls_buf += snprintf(l_p, l_end-l_p, "\"speed\",");

        #    if (l_anv.mlatFlags & MODES_ACFLAGS_VERTRATE_VALID)
        #        ls_buf += snprintf(l_p, l_end-l_p, "\"vert_rate\",");

        #    if (l_anv.mlatFlags & MODES_ACFLAGS_CATEGORY_VALID)
        #        ls_buf += snprintf(l_p, l_end-l_p, "\"category\",");

        #    if (ls_buf[-1] != '[')
        #        --ls_buf;

        #    ls_buf += snprintf(l_p, l_end-l_p, "]");

        ls_buf += ",\"messages\":%ld,\"seen\":%.1f}" % (M_MSG, 1.)  # ,
        #              l_anv.messages, (l_now - l_anv.seen)/1000.0,
        #              10 * log10((l_anv.signalLevel[0] + l_anv.signalLevel[1] + l_anv.signalLevel[2] + l_anv.signalLevel[3] +
        #                          l_anv.signalLevel[4] + l_anv.signalLevel[5] + l_anv.signalLevel[6] + l_anv.signalLevel[7] + 1e-5) / 8));

    ls_buf += "\n  ]\n}\n"
    # M_LOG.debug("ls_buf:[{}]".format(ls_buf))

    # incrementa contador de mensagens
    M_MSG += 1

    # logger
    # M_LOG.info("generate_anv_json:<<")

    # return
    return ls_buf

# < the end >--------------------------------------------------------------------------------------
