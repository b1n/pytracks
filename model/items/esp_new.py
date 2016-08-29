#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------------------------
esp_new

mantém as informações sobre um espera

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
-------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import sys

# model
import model.items.prc_model as model
import model.newton.defs_newton as ldefs

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CEspNEW >------------------------------------------------------------------------------

class CEspNEW(model.CPrcModel):
    """
    mantém as informações específicas sobre um procedimento de espera

    <espera nEsp="1">
        <fixo>83</fixo>
        <sentido>D</sentido>
        <rumo>274</rumo>
    </espera>
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, f_model, f_data=None, fs_ver="0001"):
        """
        @param f_model: model manager
        @param f_data: dados da espera
        @param fs_ver: versão do formato
        """
        # logger
        # M_LOG.info("__init__:>>")
                
        # init super class
        super(CEspNEW, self).__init__()

        # salva o model manager localmente
        self.__model = f_model
        assert self.__model

        # salva o event manager localmente
        self.__event = f_model.event
        assert self.__event

        # herados de CPrcModel
        # self.v_prc_ok    # (bool)
        # self.i_prc_id    # identificação do procedimento de espera

        # fixo da espera
        self.__ptr_esp_fix = None

        # sentido da espera
        self.__en_esp_sentido_curva = ldefs.E_MENOR

        # rumo da espera
        self.__f_esp_rumo = 0.

        # recebeu dados ?
        if f_data is not None:

            # recebeu uma lista ?
            if isinstance(f_data, dict):

                # cria uma espera com os dados da lista
                self.__load_esp(f_data, fs_ver)

            # recebeu uma espera ?
            elif isinstance(f_data, CEspNEW):

                # copia a espera
                self.copy_esp(f_data)

        # logger
        # M_LOG.info("__init__:<<")
                
    # ---------------------------------------------------------------------------------------------

    def copy_esp(self, f_esp):
        """
        copy constructor
        cria uma nova espera a partir de uma outra espera

        @param f_esp: espera a ser copiada
        """
        # logger
        # M_LOG.info("copy_esp:>>")
                
        # verifica parâmetros de entrada
        assert f_esp

        # copy super class attributes
        super(CEspNEW, self).copy_esp(f_esp)
                
        # fixo
        self.__ptr_esp_fix = f_esp.ptr_esp_fix

        # rumo
        self.__f_esp_rumo = f_esp.f_esp_rumo

        # sentido
        self.__en_esp_sentido_curva = f_esp.en_esp_sentido_curva

        # logger
        # M_LOG.info("copy_esp:<<")
                
    # ---------------------------------------------------------------------------------------------

    def __load_esp(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados de espera a partir de um dicionário

        @param fdct_data: dicionário com os dados do espera
        @param fs_ver: versão do formato dos dados
        """
        # logger
        # M_LOG.info("__load_esp:>>")
                
        # formato versão 0.01 ?
        if "0001" == fs_ver:

            # cria a espera
            self.__make_esp(fdct_data)

        # senão, formato desconhecido
        else:

            # logger
            l_log = logging.getLogger("CEspNEW::__load_esp")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: formato desconhecido.")

            # cria um evento de quit
            l_evt = events.Quit()
            assert l_evt

            # dissemina o evento
            self.__event.post(l_evt)

            # cai fora...
            sys.exit(1)

        # logger
        # M_LOG.info("__load_esp:<<")
                
    # ---------------------------------------------------------------------------------------------

    def __make_esp(self, fdct_data):
        """
        carrega os dados de espera a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do espera
        """
        # logger
        # M_LOG.info("__make_esp:>>")
                
        # identificação da espera
        if "nEsp" in fdct_data:

            self.i_prc_id = int(fdct_data["nEsp"])
            self.s_prc_desc = "Espera {:02d}".format(fdct_data["nEsp"])
            # M_LOG.debug("self.i_prc_id: " + str(self.i_prc_id))

        # fixo da espera
        if "fixo" in fdct_data:

            # obtém o dicionário de fixos
            ldct_fix = self.__model.coords.dct_fix
            assert ldct_fix is not None

            # obtém o número do fixo
            li_fix = int(fdct_data["fixo"])
            # M_LOG.debug("li_fix: " + str(li_fix))

            # obtém o fixo da espera
            self.__ptr_esp_fix = ldct_fix.get(li_fix, None)

            # fixo não existe ?
            if self.__ptr_esp_fix is None:

                # logger
                l_log = logging.getLogger("CEspNEW::__make_esp")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E01: espera:[{}]. Fixo [{}] não existe no dicionário".format(self.i_prc_id, li_fix))

        # rumo
        if "rumo" in fdct_data:

            self.__f_esp_rumo = abs(int(fdct_data["rumo"])) % 360
            # M_LOG.debug("self.__f_esp_rumo: " + str(self.__f_esp_rumo))

        # sentido
        if "sentido" in fdct_data:

            # sentido de curva
            lc_sentido = fdct_data["sentido"].strip().upper()
            # M_LOG.debug("lc_sentido: " + str(lc_sentido))

            # valida o sentido de curva
            self.__en_esp_sentido_curva = ldefs.DCT_SENTIDOS_CURVA_INV.get(lc_sentido, ldefs.E_MENOR)

        # (bool)
        self.v_prc_ok = True

        # logger
        # M_LOG.info("__make_esp:<<")
                
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------

    @property
    def ptr_esp_fix(self):
        """
        get fixo da espera
        """
        return self.__ptr_esp_fix

    @ptr_esp_fix.setter
    def ptr_esp_fix(self, f_val):
        """
        set fixo da espera
        """
        self.__ptr_esp_fix = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def f_esp_rumo(self):
        """
        get rumo
        """
        return self.__f_esp_rumo

    @f_esp_rumo.setter
    def f_esp_rumo(self, f_val):
        """
        set rumo
        """
        # verifica parâmetros de entrada
        # assert 0. <= f_val <= 360.

        # rumo
        self.__f_esp_rumo = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def en_esp_sentido_curva(self):
        """
        get sentido de curva
        """
        return self.__en_esp_sentido_curva

    @en_esp_sentido_curva.setter
    def en_esp_sentido_curva(self, f_val):
        """
        set sentido de curva
        """
        # verifica parâmetros de entrada
        assert f_val in ldefs.SET_SENTIDOS_CURVA

        # sentido de curva
        self.__en_esp_sentido_curva = f_val

# < the end >--------------------------------------------------------------------------------------
