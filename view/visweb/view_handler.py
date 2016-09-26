#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_handler

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
import os

import SimpleHTTPServer

# view
from . import generate_anv_json as anvjson
from . import generate_arr_json as arrjson
from . import generate_dep_json as depjson
from . import generate_esp_json as espjson
from . import generate_fix_json as fixjson
from . import generate_prf_json as prfjson
from . import generate_status_json as sttjson
from . import generate_sub_json as subjson
from . import generate_trj_json as trjjson

# < defines >--------------------------------------------------------------------------------------

D_MODES_CONTENT_TYPE_CSS  = "text/css;charset=utf-8"
D_MODES_CONTENT_TYPE_GIF  = "image/gif"
D_MODES_CONTENT_TYPE_HTML = "text/html;charset=utf-8"
D_MODES_CONTENT_TYPE_JPG  = "image/jpg"
D_MODES_CONTENT_TYPE_JS   = "application/javascript;charset=utf-8"
D_MODES_CONTENT_TYPE_JSON = "application/json;charset=utf-8"

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CViewHandler >---------------------------------------------------------------------------

class CViewHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    handles any incoming request from the browser
    """
    # ---------------------------------------------------------------------------------------------

    def do_GET(self):
        """
        handler for the GET requests
        """
        # logger
        # M_LOG.info("do_GET:>>")

        # default path ?
        if "/" == self.path:
            self.path = "/index.html"

        # ditch any trailing query part (AJAX might add one to avoid caching)
        llst_path = self.path.split('?')
        # M_LOG.debug("do_GET:llst_path:[{}]".format(llst_path))

        self.path = llst_path[0]
        # M_LOG.debug("do_GET:path:[{}]".format(self.path))

        # check the file extension required and set the right mime type
        try:
            lv_send_reply = False

            # json file ?
            if self.path.endswith(".json"):

                # aircraft ?
                if "/data/aircraft.json" == self.path:

                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # monta e envia mensagem de aeronave
                    self.wfile.write(anvjson.generate_anv_json(self.server.dct_flight, self.server.coords))

                # pouso ?
                elif "/data/arr.json" == self.path:

                    # create and send headers
                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # recebeu pouso ?
                    if len(llst_path) > 1:

                        # create and send json
                        self.wfile.write(arrjson.generate_arr_json(self.server.lst_arr_dep, llst_path[1]))

                    # senão, envia todo dicionário
                    else:
                        # create and send json
                        self.wfile.write(arrjson.generate_arr_json(self.server.lst_arr_dep))

                # decolagem ?
                elif "/data/dep.json" == self.path:

                    # create and send headers
                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # recebeu decolagem ?
                    if len(llst_path) > 1:

                        # create and send json
                        self.wfile.write(depjson.generate_dep_json(self.server.lst_arr_dep, llst_path[1]))

                    # senão, envia todo dicionário
                    else:
                        # create and send json
                        self.wfile.write(depjson.generate_dep_json(self.server.lst_arr_dep))

                # espera ?
                elif "/data/esp.json" == self.path:

                    # create and send headers
                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # recebeu espera ?
                    if len(llst_path) > 1:

                        # create and send json
                        self.wfile.write(espjson.generate_esp_json(self.server.dct_esp, llst_path[1]))

                    # senão, envia todo dicionário
                    else:
                        # create and send json
                        self.wfile.write(espjson.generate_esp_json(self.server.dct_esp))

                # fixo ?
                elif "/data/fix.json" == self.path:

                    # create and send headers
                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # recebeu fixo ?
                    if len(llst_path) > 1:

                        # create and send json
                        self.wfile.write(fixjson.generate_fix_json(self.server.dct_fix, llst_path[1]))

                    # senão, envia todo dicionário
                    else:
                        # create and send json
                        self.wfile.write(fixjson.generate_fix_json(self.server.dct_fix))

                # performance ?
                elif "/data/prf.json" == self.path:

                    # create and send headers
                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # create and send json file
                    self.wfile.write(prfjson.generate_prf_json(self.server.dct_prf, llst_path[1]))

                # subida ?
                elif "/data/sub.json" == self.path:

                    # create and send headers
                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # recebeu subida ?
                    if len(llst_path) > 1:

                        # create and send json
                        self.wfile.write(subjson.generate_sub_json(self.server.dct_sub, llst_path[1]))

                    # senão, envia todo dicionário
                    else:
                        # create and send json
                        self.wfile.write(subjson.generate_sub_json(self.server.dct_sub))

                # trajetórias ?
                elif "/data/trj.json" == self.path:

                    # create and send headers
                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # recebeu trajetória ?
                    if len(llst_path) > 1:

                        # create and send json
                        self.wfile.write(trjjson.generate_trj_json(self.server.dct_trj, llst_path[1]))

                    # senão, envia todo dicionário
                    else:
                        # create and send json
                        self.wfile.write(trjjson.generate_trj_json(self.server.dct_trj))

                # status ?
                elif "/data/status.json" == self.path:

                    # create and send headers
                    self.send_response(200)
                    self.send_header("Content-type", D_MODES_CONTENT_TYPE_JSON)
                    self.end_headers()

                    # create and send json file
                    self.wfile.write(sttjson.generate_status_json(self.server.dct_flight, llst_path[1]))

            # html file ?
            elif self.path.endswith(".html"):
                # set file type
                mimetype = D_MODES_CONTENT_TYPE_HTML
                lv_send_reply = True

            # css file ?
            elif self.path.endswith(".css"):
                # set file type
                mimetype = D_MODES_CONTENT_TYPE_CSS
                lv_send_reply = True

            # gif file ?
            elif self.path.endswith(".gif"):
                # set file type
                mimetype = D_MODES_CONTENT_TYPE_GIF
                lv_send_reply = True

            # jpeg file ?
            elif self.path.endswith(".jpg"):
                # set file type
                mimetype = D_MODES_CONTENT_TYPE_JPG
                lv_send_reply = True

            # javascript file ?
            elif self.path.endswith(".js"):
                # set file type
                mimetype = D_MODES_CONTENT_TYPE_JS
                lv_send_reply = True

            if lv_send_reply:

                # open the static file requested and send it
                f = open(os.curdir + os.sep + "public_html" + self.path)

                # create and send headers
                self.send_response(200)
                self.send_header("Content-type", mimetype)
                self.end_headers()

                # create and send contents
                self.wfile.write(f.read())

                # close file
                f.close()

        # em caso de erro...
        except IOError:

            # send error
            self.send_error(404, "File Not Found:[{}]".format(self.path))

        # logger
        # M_LOG.info("do_GET:<<")

    # ---------------------------------------------------------------------------------------------
    
    def log_message(self, format, *args): pass
        
# < the end >--------------------------------------------------------------------------------------
